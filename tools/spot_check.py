#!/usr/bin/env python3
"""Stage 6: cut a spot check out of a judged run, and read it back.

    python3 tools/spot_check.py --run sonnet-5-rules-out
    python3 tools/spot_check.py --read labels/customer/spot-check-2026-09-04.md

Every five turns of stage 5, one person reads ten entries against the judge's
verdicts on them - see stage 6 of `docs/pipeline.md`. It was the one step of the
pipeline with no tool, so the first one was cut by hand and could not have been
cut the same way twice.

**This is not labelling.** Nothing it produces goes into `items.csv`, no
`rubric_commit` is stamped, and the run's rows stay `?`. Labelling asks what the
verdict is; this asks whether the judge still reaches it.

**Which entries.** Weighted towards the ones the judge let through, because that
is the expensive error: `docs/targets.md` says a judge that blocks a good entry
costs a turn and one that passes a bad entry costs the release. Seven passed and
three failed, by default, spread through the document rather than taken from the
front, and chosen from the verdicts alone - the text is not read to pick them.

**Reading it back is not optional.** `--read` counts the agreements and, more to
the point, the entries the judge let through that the person failed. That figure
is the instrument target in `docs/targets.md`, at most 2 in 100, and the
convention here is that no aggregation is written by hand.
"""

from __future__ import annotations

import argparse
import datetime as dt
import importlib.util
import json
import re
import sys
import textwrap
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

_spec = importlib.util.spec_from_file_location("rl", REPO / "judge" / "run_labelled.py")
rl = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(rl)

ITEM_AXES = ["C1", "C2", "C3", "C4", "C5"]

WIDTH = 78


def wrap(text: str, indent: str = "") -> list[str]:
    """A rendering's entry is one long line. A person reading it needs it broken.

    Bullets keep their marker on the first line and hang under it, so the shape
    of the entry survives the wrapping instead of becoming a paragraph."""
    lines: list[str] = []
    for raw in text.strip().splitlines():
        stripped = raw.strip()
        if not stripped:
            lines.append("")
            continue
        hang = "  " if stripped.startswith(("- ", "* ")) else ""
        lines += textwrap.wrap(
            stripped,
            width=WIDTH,
            initial_indent=indent,
            subsequent_indent=indent + hang,
            break_long_words=False,
            break_on_hyphens=False,
        ) or [indent + stripped]
    return lines

ASKS = {
    "C1": "does the entry open on what the reader observes, not on the work done",
    "C2": "is the scope named where it is not everyone",
    "C3": "does the entry say what the reader can now rely on or do",
    "C4": "is what the entry asks of the reader reachably named",
    "C5": "is every expression one the reader could have met",
}


def results_dir(audience: str) -> Path:
    return REPO / "judge" / "results" / audience


def newest_result(run: str, audience: str) -> Path:
    """The most recent result file that judged this run."""
    hits = []
    for path in sorted(results_dir(audience).glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        rows = (data.get("execution_results") or {}).get("results") or []
        if any(row.get("run") == run for row in rows):
            hits.append(path)
    if not hits:
        sys.exit(f"no result file in {results_dir(audience).relative_to(REPO)} judged {run!r}")
    return hits[-1]


def verdicts(result: Path, run: str) -> dict[str, dict[str, tuple[str, str, str]]]:
    """Per item, per axis: the judge's verdict, its reason and the passage it quoted."""
    data = json.loads(result.read_text(encoding="utf-8"))
    out: dict[str, dict[str, tuple[str, str, str]]] = {}
    for row in (data.get("execution_results") or {}).get("results") or []:
        # A1 is judged per item as well as per run, and it carries a row the C axes
        # have no counterpart for. This reads the item level only.
        if row.get("run") != run or not row.get("item") or row.get("axis") not in ITEM_AXES:
            continue
        out.setdefault(row["item"], {})[row["axis"]] = (
            row.get("verdict", "-"),
            (row.get("reason") or "").strip(),
            (row.get("quote") or "").strip(),
        )
    return out


def ships(axes: dict[str, tuple[str, str, str]]) -> bool:
    """An entry ships when no C axis fails - the same rule `count.py` applies."""
    return all(axes.get(a, ("-",))[0] != "fail" for a in ITEM_AXES)


def spread(items: list[str], want: int) -> list[str]:
    """`want` of them, evenly spaced, so a sample is not taken from the front."""
    if want >= len(items):
        return items
    step = len(items) / want
    return [items[int(i * step)] for i in range(want)]


def choose(judged: dict, passed: int, failed: int) -> list[str]:
    order = sorted(judged)
    shipped = [i for i in order if ships(judged[i])]
    blocked = [i for i in order if not ships(judged[i])]
    return spread(shipped, passed) + spread(blocked, failed)


def worksheet(run: str, result: Path, picked: list[str], judged: dict,
              text: dict[str, str], passed: int, failed: int) -> str:
    data = json.loads(result.read_text(encoding="utf-8"))
    criterion = (data.get("evaluation_config") or {}).get("criterion") or {}
    model = (data.get("evaluation_config") or {}).get("llm_judge", "unknown")
    today = dt.date.today().isoformat()

    out = [
        f"# Spot check, {today}",
        "",
        "Stage 6 of `../../docs/pipeline.md`: one person reads these entries against",
        "the judge's verdicts on them. This is not labelling - nothing here goes into",
        "`items.csv` and no `rubric_commit` is stamped. It asks one question: has the",
        "judge drifted.",
        "",
        f"**Run** `{run}`, {len(judged)} entries judged.  ",
        f"**Judged by** `{result.relative_to(REPO)}`, `{model}`,  ",
        f"criterion `{criterion.get('version', 'unknown')}`, digest `{criterion.get('digest', 'unknown')}`.",
        "",
        f"**The sample:** {passed} the judge let through and {failed} it failed, spread",
        "through the document and chosen from the verdicts alone. Weighted towards what",
        "the judge passed because that is the expensive error - `targets.md`: a judge",
        "that blocks a good entry costs a turn, one that passes a bad one costs the",
        "release.",
        "",
        "**The axes**, in full in `../../rubric/customer.md`:",
        "",
    ]
    out += [f"- **{a}** - {ASKS[a]}" for a in ITEM_AXES]
    out += [
        "",
        "**How to fill this in.** Read the entry, apply the axis, write your verdict on",
        "the `you:` line - `pass`, `fail`, or `n/a` where C4 defines it. An axis you did",
        "not get to stays empty; empty is not a pass. Where you disagree, say in `why:`",
        "which reading the rubric carries, arguing from the entry and not against the",
        "judge's reason.",
        "",
        "Then: `python3 tools/spot_check.py --read <this file>`.",
        "",
        "---",
        "",
    ]

    for item in picked:
        out += [f"## {item}", "", "```"] + wrap(text[item]) + ["```", ""]
        for axis in ITEM_AXES:
            verdict, reason, quote = judged[item].get(axis, ("-", "", ""))
            out += [f"### {axis} - {ASKS[axis]}", f"judge: {verdict}"]
            if verdict == "fail":
                if quote:
                    out += wrap(f"on: {quote}", indent="  ")
                out += wrap(f"because: {reason}", indent="  ")
            out += ["you: ", "why: ", ""]
        out += ["---", ""]

    out += [
        "## The verdict on the judge",
        "",
        "Filled in by `--read`, not by hand.",
        "",
        "stands / has drifted: ",
        "",
        "A judge that has drifted is the only thing that reopens the instrument loop.",
    ]
    return "\n".join(out) + "\n"


def cut(args: argparse.Namespace) -> None:
    result = Path(args.result) if args.result else newest_result(args.run, args.audience)
    judged = verdicts(result, args.run)
    if not judged:
        sys.exit(f"{result.name} holds no item verdicts for {args.run!r}")

    document = rl.audience_section(args.run, args.audience)
    entries = rl.sep.entries(document)
    ids = sorted(judged)
    if len(entries) != len(ids):
        sys.exit(
            f"{args.run}: {len(entries)} entries in the rendering but {len(ids)} judged. "
            "The result and the run have drifted apart."
        )
    text = dict(zip(ids, entries))

    picked = choose(judged, args.passed, args.failed)
    path = REPO / "labels" / args.audience / f"spot-check-{dt.date.today().isoformat()}.md"
    if path.exists() and not args.force:
        sys.exit(f"{path.relative_to(REPO)} exists. Pass --force to cut it again.")
    path.write_text(
        worksheet(args.run, result, picked, judged, text, args.passed, args.failed),
        encoding="utf-8",
    )
    print(f"  wrote {path.relative_to(REPO)}  ({len(picked)} entries, {len(picked) * len(ITEM_AXES)} cells)")
    print(f"  judged by {result.name}")
    print("  fill in the `you:` lines, then --read it back")


BLOCK = re.compile(r"^## (?P<item>\S+)\s*$")
AXIS = re.compile(r"^### (?P<axis>[A-C]\d) ")
JUDGE = re.compile(r"^judge: (?P<verdict>\S+)\s*$")
YOU = re.compile(r"^you:\s*(?P<verdict>\S+)?\s*$")
WHY = re.compile(r"^why:\s*(?P<text>.*?)\s*$")


def read(args: argparse.Namespace) -> None:
    path = Path(args.read)
    if not path.exists():
        sys.exit(f"no such file: {path}")

    item = axis = None
    cells: list[dict] = []
    current: dict | None = None
    for line in path.read_text(encoding="utf-8").splitlines():
        if m := BLOCK.match(line):
            item = m.group("item")
            continue
        if m := AXIS.match(line):
            axis = m.group("axis")
            current = {"item": item, "axis": axis, "judge": None, "you": None, "why": ""}
            cells.append(current)
            continue
        if current is None:
            continue
        if m := JUDGE.match(line):
            current["judge"] = m.group("verdict")
        elif m := YOU.match(line):
            current["you"] = (m.group("verdict") or "").lower() or None
        elif m := WHY.match(line):
            current["why"] = m.group("text")

    filled = [c for c in cells if c["you"]]
    if not filled:
        sys.exit("nothing filled in: every `you:` line is empty")

    agreed = [c for c in filled if c["you"] == c["judge"]]
    disagreed = [c for c in filled if c["you"] != c["judge"]]
    # The costly direction: the judge passed what the person failed.
    let_through = [c for c in disagreed if c["judge"] != "fail" and c["you"] == "fail"]
    too_strict = [c for c in disagreed if c["judge"] == "fail" and c["you"] != "fail"]

    print(f"{path.name}")
    print(f"  cells filled in : {len(filled)} of {len(cells)}")
    print(f"  agreed          : {len(agreed)}")
    print(f"  disagreed       : {len(disagreed)}")
    print()
    print(f"  let through     : {len(let_through)}   judge passed, person failed")
    if filled:
        print(f"                    {100 * len(let_through) / len(filled):.1f} per 100 cells read"
              "   (target: at most 2)")
    print(f"  too strict      : {len(too_strict)}   judge failed, person passed")
    print("                    not counted against the target; it costs a turn, not a release")

    for label, group in (("LET THROUGH", let_through), ("TOO STRICT", too_strict)):
        if not group:
            continue
        print()
        print(f"  {label}")
        for c in group:
            print(f"    {c['item']} {c['axis']}: judge {c['judge']}, you {c['you']}")
            if c["why"]:
                print(f"      {c['why'][:160]}")

    print()
    print("  Write the outcome into docs/measurements.md as a spot-check section: it is")
    print("  the record, and it is the mark stage 6 counts turns from.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--audience", default=rl.sep.DEFAULT_AUDIENCE)
    parser.add_argument("--run", help="the run to cut a spot check out of")
    parser.add_argument("--result", help="a result file, instead of the newest for that run")
    parser.add_argument("--passed", type=int, default=7, help="entries the judge let through (7)")
    parser.add_argument("--failed", type=int, default=3, help="entries the judge failed (3)")
    parser.add_argument("--force", action="store_true", help="cut again over today's file")
    parser.add_argument("--read", help="read a filled-in worksheet back and report")
    args = parser.parse_args()

    if args.read:
        read(args)
    elif args.run:
        cut(args)
    else:
        parser.error("give --run to cut a spot check, or --read to read one back")


if __name__ == "__main__":
    main()
