#!/usr/bin/env python3
"""Where the evaluation stands, computed from the files rather than remembered.

    python3 judge/status.py
    python3 judge/status.py --audience technical
    python3 judge/status.py --verify            # every result file
    python3 judge/status.py --verify <file>     # one of them

Prints what is labelled, which axes can be compared with the judge right now,
which need a hand re-pass first, and what has been spent. One audience at a
time: an axis is stale or not against its own rubric.
"""

from __future__ import annotations

import argparse
import glob
import subprocess
import importlib.util
import json
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

_s = importlib.util.spec_from_file_location("sep", Path(__file__).with_name("run_separation.py"))
sep = importlib.util.module_from_spec(_s)
_s.loader.exec_module(sep)
_l = importlib.util.spec_from_file_location("lab", Path(__file__).with_name("run_labelled.py"))
lab = importlib.util.module_from_spec(_l)
_l.loader.exec_module(lab)



def verify(paths: list[Path], audience: str) -> int:
    """Say which result files were produced against the criterion in the tree.

    A figure is only comparable with a figure of today if both were made
    against the same criterion, and the durable name for that is the content
    digest, not a commit. Result files written before the digest existed carry
    none; they are reported as unknown rather than as matching, because a
    commit that has since been amended away cannot answer the question either
    way."""
    here = sep.criterion_digest(audience)
    print(f"CRITERION {sep.criterion_version()}  {here}\n")
    unknown = mismatched = 0
    for path in sorted(paths):
        theirs = sep.read_log(path)["digest"]
        if not theirs:
            verdict, unknown = "unknown  - written before the digest existed", unknown + 1
        elif theirs == here:
            verdict = "comparable"
        else:
            verdict, mismatched = f"DIFFERENT criterion  {theirs}", mismatched + 1
        print(f"  {path.name:<58} {verdict}")
    print(f"\n  {len(paths)} file(s): {len(paths) - unknown - mismatched} comparable, "
          f"{mismatched} against a different criterion, {unknown} unknown")
    return 1 if mismatched else 0



# --- What the documents decide, read from them rather than restated here. ---
#
# Three facts decided the work wrongly on 2026-09-08, and all three were written
# down: that C3 gates nothing, that a movement of one is not a result, and that a
# spot check was overdue. A document nobody re-reads mid-decision is a document
# that does not hold. These read the owning file and quote it, so there is no
# second copy to drift.

DOCS = sep.REPO / "docs"


def _section(path: Path, heading: str) -> list[str]:
    """The lines under a `## heading`, up to the next one. Empty if absent."""
    if not path.exists():
        return []
    out, inside = [], False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            if inside:
                break
            inside = line[3:].strip().lower().startswith(heading.lower())
            continue
        if inside:
            out.append(line)
    return out


def gate_status(audience: str = sep.DEFAULT_AUDIENCE) -> dict[str, str]:
    """Which axes are in the stage 4 gate, from the table in targets.md.

    An axis that is out gates nothing - `targets.md` says so in as many words -
    and the point of printing it beside the counts is that a count from an axis
    that gates nothing is a direction and not a figure."""
    status: dict[str, str] = {}
    for line in _section(DOCS / "targets.md", "The stage 4 threshold"):
        cells = [c.strip() for c in line.split("|")[1:-1]]
        if len(cells) == 4 and cells[0] in sep.axes(audience):
            status[cells[0]] = "in" if cells[3].startswith("in") else "out"
    return status


def noise_floor() -> str:
    """The first line of the noise floor figure, quoted from targets.md."""
    for line in _section(DOCS / "targets.md", "The noise floor"):
        if line.startswith(">"):
            # The first sentence only, and without the markdown: this is a
            # reminder in a terminal, not a quotation of the document.
            text = line.lstrip("> ").replace("**", "").strip()
            return text.split(". ")[0].rstrip(".") + "."
    return "not measured"


def turns_since_spot_check() -> tuple[int, str]:
    """Sections of measurements.md since the last spot check, and that one's date.

    Stage 6 of `pipeline.md` counts turns this way, and the first spot check was
    missed by three because the count lived in nobody's head."""
    path = DOCS / "measurements.md"
    if not path.exists():
        return (0, "never")
    headings = [l[3:].strip() for l in path.read_text(encoding="utf-8").splitlines()
                if l.startswith("## ")]
    last = max((i for i, h in enumerate(headings) if "spot check" in h.lower()), default=None)
    if last is None:
        return (len(headings), "never")
    return (len(headings) - last - 1, headings[last].split(" - ")[0])


def documented_version() -> tuple[str, bool]:
    """The newest version in criterion-versions.md, and whether a tag carries it."""
    path = DOCS / "criterion-versions.md"
    if not path.exists():
        return ("unknown", False)
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## customer-criterion-v"):
            name = line[3:].strip()
            tags = subprocess.run(["git", "tag", "-l", name], cwd=sep.REPO,
                                  capture_output=True, text=True).stdout.split()
            return (name, name in tags)
    return ("unknown", False)


def before_you_decide(audience: str = sep.DEFAULT_AUDIENCE) -> None:
    """The four facts that have to be true before a count means anything."""
    version, tagged = documented_version()
    since, last = turns_since_spot_check()
    gates = gate_status(audience)
    out = [a for a in sep.axes(audience) if gates.get(a) == "out"]

    print("BEFORE YOU DECIDE")
    print(f"  criterion    {version}  {'tagged' if tagged else 'NOT TAGGED'}"
          f"   docs/criterion-versions.md")
    print(f"  noise floor  {noise_floor()}   docs/targets.md")
    print(f"  spot check   {since} turn(s) since {last}, due at 5"
          f"   docs/pipeline.md stage 6"
          f"{'   OVERDUE' if since >= 5 else ''}")
    print(f"  gates nothing: {', '.join(out) if out else 'none'}"
          f"   docs/targets.md - a count from these is a direction, not a figure")
    print()

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--audience", default=sep.DEFAULT_AUDIENCE)
    parser.add_argument(
        "--verify",
        nargs="?",
        const="",
        metavar="FILE",
        help="check result files against the criterion in the working tree, "
             "all of them or the one named",
    )
    args = parser.parse_args()
    audience = args.audience

    if not sep.rubric_path(audience).exists():
        raise SystemExit(f"no rubric at {sep.rubric_rel(audience)}")

    if args.verify is not None:
        if args.verify:
            chosen = [Path(args.verify)]
            if not chosen[0].exists():
                raise SystemExit(f"no such result file: {args.verify}")
        else:
            chosen = sorted(sep.results_dir(audience).glob("*.json"))
            if not chosen:
                raise SystemExit(f"no result files in {sep.results_dir(audience)}")
        raise SystemExit(verify(chosen, audience))

    items, documents = lab.human_labels(audience)
    runs = Counter(run for run, _ in items)

    before_you_decide(audience)

    print(f"AUDIENCE: {audience}")
    print(f"  rubric {sep.rubric_rel(audience)}, labels labels/{audience}/")

    print("\nLABELLED BY HAND")
    for run in sorted(runs):
        print(f"  {run:<26} {runs[run]:>3} entries")
    print(f"  {'documents':<26} {len(documents):>3} run rows")
    print(f"  {'total entries':<26} {sum(runs.values()):>3}")

    print("\nAXES")
    print(f"  {'axis':<6}{'axis or units changed':<23}{'column passed against':<24}"
          f"{'comparable now':<20}{'gate'}")
    gates = gate_status(audience)
    ready = []
    for axis in sep.axes(audience):
        stale = sep.labels_are_older_than(axis, audience)
        if not stale:
            ready.append(axis)
        gate = gates.get(axis, "?")
        print(
            f"  {axis:<6}{sep.prompt_last_changed(axis, audience):<23}"
            f"{sep.column_passed_against(axis, audience) or '-':<24}"
            f"{'no - re-pass first' if stale else 'yes':<20}"
            f"{'in' if gate == 'in' else 'out - gates nothing' if gate == 'out' else '?'}"
        )
    print(f"\n  ready to judge: {', '.join(ready) if ready else 'none'}")

    print("\nJUDGE RUNS")
    spent = 0.0
    for path in sorted(glob.glob(str(sep.results_dir(audience) / "*.json"))):
        log = sep.read_log(Path(path))
        spent += log["cost"]
        kind = "separation" if "separation" in path else "labelled"
        through = "" if log["let_through"] is None else f"  {log['let_through']} let through"
        print(
            f"  {Path(path).name:<52} {kind:<11} {log['score']}/{log['calls']:<4} "
            f"${log['cost']:<7.4f} at {log['commit']}{through}"
        )
    print(f"  spent in total: ${spent:.2f}")


if __name__ == "__main__":
    main()
