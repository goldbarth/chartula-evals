#!/usr/bin/env python3
"""Judge the labelled runs and compare the verdicts with the human labels.

The separation run showed the axes can be told apart on constructed cases.
This asks the harder question: does the judge agree with a person on real
renderings - 53 entries across three runs, plus the document axes.

    python3 judge/run_labelled.py --dry-run
    python3 judge/run_labelled.py --model claude-sonnet-5
    python3 judge/run_labelled.py --axis C3 --run sonnet-5-out   # one column
    python3 judge/run_labelled.py --audience technical

Agreement alone is not the measure. C2 and C5 pass on almost every entry, so a
judge that always answers pass scores above ninety percent there and has
understood nothing. The report gives, per axis, how often the judge finds the
verdict a person gave *and* what it does with the minority of that column.

The prompt, the rubric sections and the calling code are the ones from
run_separation.py. The labels are read from `labels/{audience}/items.csv` and
`runs.csv`; nothing here shows the judge a human verdict or a note.
"""

from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RUNS = REPO / "test-runs"

_spec = importlib.util.spec_from_file_location("sep", Path(__file__).with_name("run_separation.py"))
sep = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sep)

ITEM_AXES = ["A1", "C1", "C2", "C3", "C4", "C5"]
# A1 is here as well as above: an entry that should not be there is judged
# against the entry, a change carried by no entry at all against the whole
# rendering and the fact base. `runs.csv` holds that second verdict and nothing
# was asking for it.
DOCUMENT_AXES = ["A1", "B1", "B2", "B3"]


def _rows(path: Path) -> list[dict]:
    if not path.exists():
        sys.exit(f"no labels at {path.relative_to(REPO)}")
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def human_labels(audience: str = sep.DEFAULT_AUDIENCE) -> tuple[dict, dict]:
    """(item verdicts keyed by (run, item), document verdicts keyed by run).

    One row per (run, item, axis) in `items.csv`, per (run, axis) in `runs.csv`.
    A row whose axis is `*` carries a note about the item or the run as a whole
    and holds no verdict, so it contributes the entry and nothing else.

    Whether an item ships is not read from the table: it follows from the C
    verdicts, and `tools/labels.py` is where that rule is applied."""
    labels = sep.labels_dir(audience)
    items, documents = {}, {}

    for row in _rows(labels / "items.csv"):
        entry = items.setdefault(
            (row["run"], row["item"]),
            {"kind": row["kind"], "verdicts": {}},
        )
        if row["axis"] in ITEM_AXES:
            entry["verdicts"][row["axis"]] = row["verdict"].strip().lower()

    for row in _rows(labels / "runs.csv"):
        if row["axis"] in DOCUMENT_AXES:
            documents.setdefault(row["run"], {})[row["axis"]] = row["verdict"].strip().lower()
    return items, documents


def audience_section(run: str, audience: str = sep.DEFAULT_AUDIENCE) -> str:
    """One rendering out of a run file. The sections are marked `--- Customer ---`,
    `--- Technical ---`, `--- Product ---`, so the audience names its own."""
    marker = f"--- {audience.capitalize()} ---"
    text = (RUNS / f"{run}.md").read_text(encoding="utf-8").splitlines()
    out, inside = [], False
    for line in text:
        if line.startswith(marker):
            inside = True
            continue
        if inside and line.startswith("--- ") and line.endswith(" ---"):
            break
        if inside:
            out.append(line)
    found = "\n".join(out).strip()
    if not found:
        sys.exit(f"{run}.md has no {marker} section")
    return found


def build_calls(
    items: dict,
    documents: dict,
    want_run: str | None,
    want_axis: str | None,
    audience: str = sep.DEFAULT_AUDIENCE,
) -> list[dict]:
    units = sep.rubric_section("Units", audience)
    system, user_template = sep.prompt_parts()
    calls = []

    by_run = defaultdict(list)
    for (run, item) in items:
        by_run[run].append(item)

    for run, ids in by_run.items():
        if want_run and run != want_run:
            continue
        document = audience_section(run, audience)
        found = sep.entries(document)
        ids = sorted(ids)
        if len(found) != len(ids):
            sys.exit(
                f"{run}: {len(found)} entries in the rendering but {len(ids)} labelled rows. "
                "The tables and the run have drifted apart; fix that before judging."
            )
        for item, entry in zip(ids, found):
            for axis in ITEM_AXES:
                if want_axis and axis != want_axis:
                    continue
                calls.append(
                    {
                        "id": f"{run}::{item}::{axis}",
                        "audience": audience,
                        "run": run,
                        "item": item,
                        "axis": axis,
                        # "?" is the rubric's value for an axis not judged yet;
                        # report() drops those rather than scoring them.
                        "human": items[(run, item)]["verdicts"].get(axis, "?"),
                        "subject_label": "The entry",
                        "subject": entry,
                        # The item half asks about the entry in hand; the facts
                        # belong to the document call below.
                        "facts": "",
                        "system": system,
                        "user_template": user_template,
                        "units": units,
                    }
                )
        for axis in DOCUMENT_AXES:
            if want_axis and axis != want_axis:
                continue
            if run not in documents:
                continue
            calls.append(
                {
                    "id": f"{run}::document::{axis}",
                    "audience": audience,
                    "run": run,
                    "item": "document",
                    "axis": axis,
                    "human": documents[run].get(axis, "?"),
                    "subject_label": "The document",
                    "subject": document,
                    "facts": sep.fact_base(audience) if axis in sep.AXIS_NEEDS_FACTS else "",
                    "system": system,
                    "user_template": user_template,
                    "units": units,
                }
            )
    return calls


def report(results: list[dict]) -> dict:
    """Per axis: agreement, and what the judge does with the minority class."""
    per_axis = defaultdict(lambda: {"n": 0, "agree": 0, "human_fail": 0, "caught": 0, "false_fail": 0})
    for r in results:
        human, judge = r["human"], r["verdict"]
        if human not in {"pass", "fail", "n/a"} or judge is None:
            continue
        a = per_axis[r["axis"]]
        a["n"] += 1
        # n/a and pass are both "not a fail": the axes that use n/a mean by it
        # that there was nothing to fail on.
        human_fails, judge_fails = human == "fail", judge == "fail"
        a["agree"] += human_fails == judge_fails
        if human_fails:
            a["human_fail"] += 1
            a["caught"] += judge_fails
        elif judge_fails:
            a["false_fail"] += 1
    return dict(per_axis)


SHIP_AXES = ["C1", "C2", "C3", "C4", "C5"]
VERDICTS = {"pass", "fail", "n/a"}


def ship_decision(results: list[dict]) -> dict:
    """The product figure: how often the judge would send an entry out, and how
    often that disagrees with the person.

    An item ships when no C axis fails - the same rule `tools/labels.py sync`
    applies to the labels, applied here to the judge's verdicts so the figure
    lives in the file rather than in a script someone writes twice.

    `let_through` is the number that decides whether a person still has to read
    the output: entries the judge ships that the person would have sent back.
    `blocked` is the opposite error and costs a turn rather than a release, so
    the two are reported apart and never averaged. Computed over whichever C
    axes this run judged, which `axes` names; `complete` says whether that was
    all of them."""
    judged = [a for a in SHIP_AXES if any(r["axis"] == a for r in results)]
    if not judged:
        return {"axes": [], "complete": False, "note": "no item axis in this run"}

    by_item: dict[tuple[str, str], dict] = defaultdict(dict)
    for r in results:
        if r["axis"] in judged and r.get("item"):
            by_item[(r["run"], r["item"])][r["axis"]] = (r["human"], r["verdict"])

    ships = lambda pairs, side: not any(v[side] == "fail" for v in pairs.values())
    # An item nobody has labelled has no human side. Counting "?" as "not a
    # fail" would report human_ships as every item and let_through as zero,
    # which reads as "nothing slips through" on a run where nothing was
    # compared - the most misleading answer this figure could give.
    labelled = {k: v for k, v in by_item.items() if any(h in VERDICTS for h, _ in v.values())}
    judge_ships = sum(ships(pairs, 1) for pairs in by_item.values())
    out = {
        "axes": judged,
        "complete": judged == SHIP_AXES,
        "items": len(by_item),
        "judge_ships": judge_ships,
        "compared_against_labels": len(labelled),
    }
    if not labelled:
        return {**out, "human_ships": None, "let_through": None, "blocked": None,
                "note": "no human verdict in this run; the judge side stands alone"}
    human_ships = let_through = blocked = 0
    for pairs in labelled.values():
        h, j = ships(pairs, 0), ships(pairs, 1)
        human_ships += h
        let_through += (not h) and j
        blocked += h and not j
    return {**out, "human_ships": human_ships, "let_through": let_through, "blocked": blocked}


def print_report(summary: dict) -> None:
    print(f"\n{'axis':<6}{'n':>5}{'agree':>8}{'fails':>7}{'caught':>8}{'false':>7}")
    for axis in sorted(summary):
        a = summary[axis]
        pct = 100 * a["agree"] / a["n"] if a["n"] else 0
        print(
            f"{axis:<6}{a['n']:>5}{pct:>7.0f}%{a['human_fail']:>7}"
            f"{a['caught']:>8}{a['false_fail']:>7}"
        )
    print("\nfails  = entries a person failed on that axis")
    print("caught = how many of those the judge also failed")
    print("false  = entries a person passed and the judge failed")
    print("An axis with a high agreement and a low caught count is answering the")
    print("majority class, not the axis.")


def main() -> None:
    try:
        import anthropic
    except ModuleNotFoundError:
        sys.exit(
            "the anthropic SDK is not on this interpreter, and run_labelled.py needs it to make "
            "a call.\n"
            "    .venv/bin/python3 judge/run_labelled.py ...\n"
            "or install it here: python3 -m pip install -r judge/requirements.txt\n"
            "Everything that only reads the files - status.py, tools/labels.py - runs "
            "without it."
        )

    parser = argparse.ArgumentParser()
    parser.add_argument("--audience", default=sep.DEFAULT_AUDIENCE)
    parser.add_argument("--model", default="claude-opus-5")
    parser.add_argument("--effort", default="low", choices=["low", "medium", "high"])
    parser.add_argument("--max-tokens", type=int, default=2000)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--run", help="only this run")
    parser.add_argument("--axis", help="only this axis")
    parser.add_argument(
        "--allow-stale",
        action="store_true",
        help="judge an axis that changed after the labels were written, or a rubric "
        "that is not committed. The result is then a comparison of two rubrics, not "
        "of two judgements.",
    )
    args = parser.parse_args()

    if not sep.rubric_path(args.audience).exists():
        sys.exit(f"no rubric at {sep.rubric_rel(args.audience)}")

    items, documents = human_labels(args.audience)
    calls = build_calls(items, documents, args.run, args.axis, args.audience)
    if args.limit:
        calls = calls[: args.limit]
    if not calls:
        sys.exit("nothing to judge with those filters")
    if sep.rubric_uncommitted(args.audience) and not args.allow_stale:
        sys.exit(
            f"{sep.rubric_rel(args.audience)} has uncommitted changes.\n"
            "The prompt is built from the working tree and staleness is computed from git, so a\n"
            "run now would be judged against text no commit records and would report itself as\n"
            "current. Commit the rubric first, or pass --allow-stale and say so in the friction\n"
            "log."
        )

    axes = sorted({c["axis"] for c in calls})
    stale = [a for a in axes if sep.labels_are_older_than(a, args.audience)]
    print("axis   last changed   labels older than the axis")
    for axis in axes:
        print(f"{axis:<7}{sep.prompt_last_changed(axis, args.audience):<15}{'YES' if axis in stale else 'no'}")
    if stale and not args.allow_stale:
        sys.exit(
            f"\n{', '.join(stale)} changed after the rubric_commit those columns carry in\n"
            f"labels/{args.audience}/.\n"
            "Judging across that line measures the difference between two rubrics and\n"
            "reports it as disagreement between a person and a model. Re-pass those\n"
            "columns by hand first, or pass --allow-stale if you have checked that the\n"
            "change cannot move a verdict - and say so in the friction log."
        )

    client = anthropic.Anthropic()

    if args.dry_run:
        total = 0
        for call in calls:
            body, system = sep.render(call)
            total += client.messages.count_tokens(
                model=args.model, system=system, messages=[{"role": "user", "content": body}]
            ).input_tokens
        inp, out, _, _ = sep.PRICES.get(args.model, sep.PRICES["claude-opus-5"])
        low = total * inp / 1e6 + len(calls) * 400 * out / 1e6
        high = total * inp / 1e6 + len(calls) * 1200 * out / 1e6
        print(f"{len(calls)} calls, {total:,} input tokens")
        print(f"estimate {args.model}: ${low:.2f} to ${high:.2f}")
        return

    results, spent = [], 0.0
    for i, call in enumerate(calls, start=1):
        body, system = sep.render(call)
        response = client.messages.create(
            model=args.model,
            max_tokens=args.max_tokens,
            system=system,
            output_config={"effort": args.effort},
            thinking={"type": "adaptive"},
            messages=[{"role": "user", "content": body}],
        )
        text = "".join(b.text for b in response.content if b.type == "text")
        answer = sep.parse_answer(text)
        spent += sep.cost(response.usage, args.model)
        quote = answer.get("quote") or ""
        agree = (answer["verdict"] == "fail") == (call["human"] == "fail")
        results.append(
            {
                "id": call["id"],
                "run": call["run"],
                "item": call["item"],
                "axis": call["axis"],
                "test_payload": {
                    "subject_label": call["subject_label"],
                    "subject": call["subject"],
                },
                "human": call["human"],
                **answer,
                "agree": agree,
                "quote_found": bool(quote) and sep._collapse(quote) in sep._collapse(call["subject"]),
                "usage": sep.usage_of(response),
            }
        )
        mark = "ok " if agree else "DIFF"
        print(f"[{i:>3}/{len(calls)}] {mark} {call['id']:<34} human={call['human']:<5} judge={answer['verdict']}  ${spent:.3f}")

    summary = report(results)
    print_report(summary)

    out_dir = sep.results_dir(args.audience)
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%S")
    # The axis and the seconds are both in the name: two runs in the same
    # minute used to overwrite each other silently, and the run that vanished
    # had already been paid for.
    which = args.axis or "all"
    out = out_dir / f"labelled-{which}-{args.model}-{stamp}.json"
    out.write_text(
        json.dumps(
            sep.eval_log(
                "labelled",
                args,
                criterion={
                    "axes": {a: sep.prompt_last_changed(a, args.audience) for a in axes},
                    "judged_stale": stale if args.allow_stale else [],
                },
                execution={
                    "calls": len(results),
                    "agreed": sum(r["agree"] for r in results),
                    "quotes_found_in_subject": sum(r["quote_found"] for r in results),
                    "cost_usd": round(spent, 4),
                    "per_axis": summary,
                    "passed": ship_decision(results),
                    "results": results,
                },
            ),
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"\n{sum(r['agree'] for r in results)}/{len(results)} agree, ${spent:.3f}, written to {out.relative_to(REPO)}")


if __name__ == "__main__":
    main()
