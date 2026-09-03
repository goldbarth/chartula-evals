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

AXES = ["A1", "B1", "B2", "B3", "C1", "C2", "C3", "C4", "C5"]


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

    print(f"AUDIENCE: {audience}")
    print(f"  rubric {sep.rubric_rel(audience)}, labels labels/{audience}/")

    print("\nLABELLED BY HAND")
    for run in sorted(runs):
        print(f"  {run:<26} {runs[run]:>3} entries")
    print(f"  {'documents':<26} {len(documents):>3} run rows")
    print(f"  {'total entries':<26} {sum(runs.values()):>3}")

    print("\nAXES")
    print(f"  {'axis':<6}{'axis or units changed':<23}{'column passed against':<24}{'comparable now'}")
    ready = []
    for axis in AXES:
        stale = sep.labels_are_older_than(axis, audience)
        if not stale:
            ready.append(axis)
        print(
            f"  {axis:<6}{sep.prompt_last_changed(axis, audience):<23}"
            f"{sep.column_passed_against(axis, audience) or '-':<24}"
            f"{'no - re-pass first' if stale else 'yes'}"
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
