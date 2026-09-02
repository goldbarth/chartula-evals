#!/usr/bin/env python3
"""Where the evaluation stands, computed from the files rather than remembered.

    python3 judge/status.py
    python3 judge/status.py --audience technical

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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--audience", default=sep.DEFAULT_AUDIENCE)
    args = parser.parse_args()
    audience = args.audience

    if not sep.rubric_path(audience).exists():
        raise SystemExit(f"no rubric at {sep.rubric_rel(audience)}")

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
        data = json.load(open(path, encoding="utf-8"))
        spent += data["cost_usd"]
        kind = "separation" if "separation" in path else "labelled"
        score = data.get("matched", data.get("agreed"))
        prov = data.get("provenance", {}).get("commit", "-")
        print(f"  {Path(path).name:<52} {kind:<11} {score}/{data['calls']:<4} ${data['cost_usd']:<7.4f} at {prov}")
    print(f"  spent in total: ${spent:.2f}")


if __name__ == "__main__":
    main()
