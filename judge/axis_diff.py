#!/usr/bin/env python3
"""Show one axis: what it says now, and what changed since the column was
passed against it.

    python3 judge/axis_diff.py C1          # diff since the column was passed
    python3 judge/axis_diff.py C1 --full   # the whole current section as well
    python3 judge/axis_diff.py C1 --audience technical

Read the diff first. Only what changed there can move a verdict, and the
direction of the change says which side of the column to re-read: a section
that became more permissive can only turn a fail into a pass.
"""

from __future__ import annotations

import argparse
import difflib
import sys
import importlib.util
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
_s = importlib.util.spec_from_file_location("sep", Path(__file__).with_name("run_separation.py"))
sep = importlib.util.module_from_spec(_s)
_s.loader.exec_module(sep)


GONE, NEW, OFF = "\033[31m", "\033[32m", "\033[0m"


def _print_prose_diff(before: str, now: str, color: str) -> None:
    """A diff meant to be read, not applied. Each change is shown as what is
    gone and what stands there now, in blocks rather than as +/- lines around
    hunk headers - these sections are prose and read that way."""
    tint = color == "always" or (color == "auto" and sys.stdout.isatty())
    gone, new, off = (GONE, NEW, OFF) if tint else ("", "", "")
    a, b = before.splitlines(), now.splitlines()

    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b).get_opcodes():
        if tag == "equal":
            continue
        if tag in ("replace", "delete"):
            print(f"{gone}- gone{off}")
            for line in a[i1:i2]:
                print(f"{gone}  {line}{off}")
            print()
        if tag in ("replace", "insert"):
            print(f"{new}+ now{off}")
            for line in b[j1:j2]:
                print(f"{new}  {line}{off}")
            print()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("axis")
    parser.add_argument("--audience", default=sep.DEFAULT_AUDIENCE)
    parser.add_argument(
        "--since",
        help="commit to diff from (default: the rubric_commit the column carries)",
    )
    parser.add_argument("--full", action="store_true", help="also print the current section")
    parser.add_argument(
        "--color",
        choices=["auto", "always", "never"],
        default="auto",
        help="colour the removed and added text (default: only on a terminal)",
    )
    args = parser.parse_args()

    axis, audience = args.axis, args.audience
    since = args.since or sep.column_passed_against(axis, audience)
    heading = axis if axis == "Units" else f"{axis} -"
    now = sep.rubric_section(axis, audience)

    if not since:
        print(f"no rubric_commit on any {axis} row; showing the current section only\n")
        print(now)
        return

    before = sep._section_at(since, heading, audience)
    if before == now:
        print(f"{axis}: unchanged since {since}. The column does not need re-reading.")
    else:
        print(f"{axis}: changed since {since}, the version the column was read against.\n")
        _print_prose_diff(before, now, args.color)

    if args.full:
        print("\n" + "=" * 70 + f"\nthe section as it stands, which is what to read against:\n")
        print(now)


if __name__ == "__main__":
    main()
