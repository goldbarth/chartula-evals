#!/usr/bin/env python3
"""What the judge failed in a rendering nobody has labelled.

    python3 judge/count.py <result.json>
    python3 judge/count.py <before.json> <after.json>
    python3 judge/count.py --run sonnet-5-out

This is the reporting half of stage 5 of `docs/pipeline.md`: change Chartula's
prompt, re-render, judge, count. `run_labelled.py` already judges a rendering
with no labels - `tools/labels.py init` lays the rows out with every verdict
`?`, and the runner builds a call for each of them regardless - but its report
compares against human verdicts and prints nothing when there are none. This
counts the judge's side instead.

No API key and no virtualenv: it reads result files that already exist.

Two things it refuses to do. It will not compare two runs judged against
different criteria - that is what the digest is for, and a figure from either
side of a criterion change is not a figure about the product. And it does not
decide which axes to believe: stage 4 put six of the nine out of the gate, and
`docs/targets.md` says which and why. Out of the gate does not mean out of the
trend, but it does mean reading a large movement and ignoring a small one.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
from collections import defaultdict
from pathlib import Path

_s = importlib.util.spec_from_file_location("sep", Path(__file__).with_name("run_separation.py"))
sep = importlib.util.module_from_spec(_s)
_s.loader.exec_module(sep)


def records(path: Path) -> list[dict]:
    """The per-call records, from either shape of result file."""
    data = json.loads(path.read_text(encoding="utf-8"))
    return (data.get("execution_results") or data).get("results") or []


def counts(rows: list[dict]) -> dict[str, dict]:
    """Per axis: how many calls returned a verdict, and how many were fails.

    `unparsed` is counted rather than dropped. One call of the C5 round
    returned nothing parsable, and a denominator that quietly shrinks is how a
    run comes to look better than it was."""
    per_axis: dict[str, dict] = defaultdict(lambda: {"judged": 0, "failed": 0, "unparsed": 0})
    for row in rows:
        a = per_axis[row["axis"]]
        if row.get("verdict") is None:
            a["unparsed"] += 1
            continue
        a["judged"] += 1
        a["failed"] += row["verdict"] == "fail"
    return dict(per_axis)


SHIP_AXES = {"C1", "C2", "C3", "C4", "C5"}


def ships(rows: list[dict]) -> tuple[int, int]:
    """Items the judge would send out, and items it saw at all.

    The rule is the one the labels use: an item ships when no C axis fails.
    Only the axes present in the run are applied, so a single-axis run reports
    what that axis alone would block.

    Rows outside that are not silently treated as passes. A run that judged no
    C axis returns nothing here rather than "every item ships" - that reads as
    a clean bill of health for a question nobody asked. The document rows are
    excluded for the same reason: they carry the id `document` and are not
    items, so counting them would inflate the denominator by one per run."""
    by_item: dict[tuple[str, str], list[str]] = defaultdict(list)
    for row in rows:
        item = row.get("item")
        if item and item != "document" and row["axis"] in SHIP_AXES:
            by_item[(row.get("run", ""), row["item"])].append(row.get("verdict"))
    if not by_item:
        return 0, 0
    return sum("fail" not in v for v in by_item.values()), len(by_item)


def criterion_of(path: Path) -> tuple[str, str]:
    log = sep.read_log(path)
    return log["version"] or "untagged", log["digest"] or "none recorded"


def show(path: Path) -> dict:
    rows = records(path)
    per_axis = counts(rows)
    shipped, items = ships(rows)
    version, digest = criterion_of(path)

    print(f"{path.name}")
    print(f"  criterion {version}  {digest}")
    labelled = sum(1 for r in rows if r.get("human") in {"pass", "fail", "n/a"})
    if labelled:
        print(f"  {labelled} of {len(rows)} calls also carry a human verdict; "
              f"for agreement use judge/status.py and the run's own per_axis")
    print()
    print(f"  {'axis':<6}{'judged':>8}{'failed':>8}{'unparsed':>10}")
    for axis in sorted(per_axis):
        a = per_axis[axis]
        mark = "" if not a["unparsed"] else "  <- calls with no parsable verdict"
        print(f"  {axis:<6}{a['judged']:>8}{a['failed']:>8}{a['unparsed']:>10}{mark}")
    if items:
        print(f"\n  items the judge would ship: {shipped} of {items}")
    return {"per_axis": per_axis, "shipped": shipped, "items": items, "digest": digest}


def compare(before: dict, after: dict) -> int:
    if any(s["digest"] == "none recorded" for s in (before, after)):
        print("\nNOT COMPARED - at least one run does not record which criterion it "
              "was judged against.")
        print("  Files written before the eval-log schema name a commit and nothing "
              "else, and two of\n  this repository's rubric commits have since been "
              "amended away. Two such files look\n  alike here whether or not the "
              "rubric moved between them, which is the one mistake this\n  tool must "
              "not make. Read them one at a time instead.")
        return 1

    if before["digest"] != after["digest"]:
        print("\nNOT COMPARED - the two runs were judged against different criteria:")
        print(f"  before {before['digest']}")
        print(f"  after  {after['digest']}")
        print("\nA change in the criterion moves the figures on its own, so the "
              "difference between these two says nothing about the rendering. "
              "See docs/criterion-versions.md.")
        return 1

    print(f"\n{'axis':<6}{'before':>8}{'after':>8}{'change':>9}")
    for axis in sorted(set(before["per_axis"]) | set(after["per_axis"])):
        b = before["per_axis"].get(axis, {}).get("failed", 0)
        a = after["per_axis"].get(axis, {}).get("failed", 0)
        change = "-" if a == b else f"{a - b:+d}"
        arrow = "" if a == b else ("  better" if a < b else "  worse")
        print(f"  {axis:<6}{b:>8}{a:>8}{change:>9}{arrow}")

    if before["items"] and after["items"]:
        b, a = before["shipped"], after["shipped"]
        print(f"\n  items the judge would ship: {b} of {before['items']} "
              f"-> {a} of {after['items']}  ({a - b:+d})")
    print("\n  Read a large movement and ignore a small one: six of the nine axes "
          "are out of the gate\n  and carry a bias this comparison cannot remove. "
          "docs/targets.md says which.")
    return 0


def latest_for(run: str, audience: str) -> Path:
    """The newest result file that judged this run."""
    best: tuple[str, Path] | None = None
    for path in sep.results_dir(audience).glob("*.json"):
        rows = records(path)
        if any(r.get("run") == run for r in rows):
            data = json.loads(path.read_text(encoding="utf-8"))
            # The timestamp moved into `metadata` with the eval-log schema; old
            # files keep it at the top level, and the name sorts either way.
            stamp = (data.get("metadata") or {}).get("timestamp") or data.get("run_at") or path.name
            if best is None or stamp > best[0]:
                best = (stamp, path)
    if best is None:
        raise SystemExit(f"no result file judged a run called {run!r}")
    return best[1]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="*", type=Path, help="one result file, or before and after")
    parser.add_argument("--audience", default=sep.DEFAULT_AUDIENCE)
    parser.add_argument("--run", help="use the newest result file that judged this run")
    args = parser.parse_args()

    paths = list(args.files)
    if args.run:
        paths.append(latest_for(args.run, args.audience))
    if not paths:
        raise SystemExit("name a result file, or pass --run")
    if len(paths) > 2:
        raise SystemExit("one file, or two to compare")
    for path in paths:
        if not path.exists():
            raise SystemExit(f"no such result file: {path}")

    summaries = []
    for i, path in enumerate(paths):
        if i:
            print()
        summaries.append(show(path))
    raise SystemExit(compare(*summaries) if len(summaries) == 2 else 0)


if __name__ == "__main__":
    main()
