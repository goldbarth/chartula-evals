#!/usr/bin/env python3
"""Assemble the calibration documents from the minimal pairs in the rubric.

The texts live in `rubric/{audience}.md`, section "Minimal pairs", and are read
from there: the base document from its fenced block, the inserted and replaced
entries from the block quotes that follow. Only the transformations - where a
group is inserted, which two entries are swapped - are encoded here, because
they are instructions in prose that no parser can be trusted with.

Nothing is written by hand twice. Edit the rubric; run this again.

    python3 tools/build_calibration_set.py [--audience customer] [--out calibration]

One set per audience, written to `{out}/{audience}/`, which is where
`judge/run_separation.py --audience` reads it from.

Writes one document per case plus `manifest.json`, which carries the axis each
case is expected to fail. That manifest is the ground truth of the separation
test: hand each document to the judge, one axis per call, and compare.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DEFAULT_AUDIENCE = "customer"

SECTION_START = "### Minimal pairs"
SECTION_END = "### Realistic case"

# The A1 case is a fact base, not a document, and no fact base is written out in
# the rubric - it names the missing change in prose instead. The fixture is
# therefore literal here, and the one entry that has no counterpart in the base
# document is marked so the omission stays visible to a reader.
A1_FACTS = """\
Changes in release 0.1.0, as the fact base holds them:

1. Release notes are written to the GitHub release instead of a separate file.
   Breaking. User-visible.
2. Technical, customer and product notes are rendered from one set of facts.
   User-visible.
3. A release can be previewed before anything is written or published.
   User-visible.
4. Generated text is no longer cut off when a release is long. User-visible.
5. A release whose commits have no pull requests attached no longer fails; the
   commit subjects are used instead. User-visible.
6. The categoriser moved into its own component, with identical output.
   Not user-visible.
"""


def section(text: str) -> str:
    start = text.index(SECTION_START)
    end = text.index(SECTION_END, start)
    return text[start:end]


def base_document(sec: str) -> str:
    match = re.search(r"```markdown\n(.*?)```", sec, re.DOTALL)
    if not match:
        sys.exit("no fenced base document in the minimal pairs section")
    return match.group(1).rstrip("\n")


def quoted_blocks(sec: str) -> list[str]:
    """Every block quote in the section, unquoted and stripped of its marker."""
    blocks, current = [], []
    for line in sec.splitlines():
        if line.startswith(">"):
            current.append(re.sub(r"^> ?", "", line))
        elif current:
            blocks.append("\n".join(current).rstrip())
            current = []
    if current:
        blocks.append("\n".join(current).rstrip())
    return blocks


def split_groups(doc: str) -> list[tuple[str, str]]:
    """The document as (heading, body) pairs, the preamble under an empty heading."""
    parts = re.split(r"^(### .*)$", doc, flags=re.MULTILINE)
    groups = [("", parts[0])]
    for heading, body in zip(parts[1::2], parts[2::2]):
        groups.append((heading, body))
    return groups


def join_groups(groups: list[tuple[str, str]]) -> str:
    out = []
    for heading, body in groups:
        if heading:
            out.append(heading)
        out.append(body.rstrip("\n"))
        out.append("")
    joined = "\n".join(out).rstrip("\n") + "\n"
    # A variant must differ from the base in the one intended way and in nothing
    # else. Stray blank lines from splitting and rejoining are a difference a
    # judge can see, so they are collapsed away.
    return re.sub(r"\n{3,}", "\n\n", joined)


def entries(body: str) -> list[str]:
    """The bullets of one group, each including its continuation lines."""
    found, current = [], []
    for line in body.splitlines():
        if line.startswith("- "):
            if current:
                found.append("\n".join(current))
            current = [line]
        elif current and line.strip():
            current.append(line)
        elif current:
            found.append("\n".join(current))
            current = []
    if current:
        found.append("\n".join(current))
    return found


def group_index(groups: list[tuple[str, str]], name: str) -> int:
    for i, (heading, _) in enumerate(groups):
        if heading.strip() == f"### {name}":
            return i
    sys.exit(f"group {name!r} not found in the base document")


def case_b1(base: str, insert: str) -> str:
    """An action-carrying entry below the informational groups, groups still in order."""
    groups = split_groups(base)
    at = group_index(groups, "What's New") + 1
    groups.insert(at, ("### What's Changed", "\n" + insert + "\n"))
    return join_groups(groups)


def case_b2(base: str) -> str:
    """What's New and Bug Fixes swapped, so the fixes are printed first."""
    groups = split_groups(base)
    i = group_index(groups, "What's New")
    j = group_index(groups, "Bug Fixes")
    groups[i], groups[j] = groups[j], groups[i]
    return join_groups(groups)


def case_b3(base: str, replacement: str) -> str:
    """The fix entry padded past its outcome and given a superlative."""
    groups = split_groups(base)
    i = group_index(groups, "Bug Fixes")
    heading, _ = groups[i]
    groups[i] = (heading, "\n" + replacement + "\n")
    return join_groups(groups)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--audience", default=DEFAULT_AUDIENCE)
    parser.add_argument("--out", default="calibration")
    args = parser.parse_args()

    rubric = REPO / "rubric" / f"{args.audience}.md"
    if not rubric.exists():
        sys.exit(f"no rubric at rubric/{args.audience}.md")

    sec = section(rubric.read_text(encoding="utf-8"))
    base = base_document(sec)
    blocks = quoted_blocks(sec)
    if len(blocks) < 2:
        sys.exit(f"expected two block quotes in the section, found {len(blocks)}")
    b1_insert, b3_replacement = blocks[0], blocks[1]

    out = REPO / args.out / args.audience
    out.mkdir(parents=True, exist_ok=True)

    cases = {
        "base.md": (base + "\n", None),
        "b1.md": (case_b1(base, b1_insert), "B1"),
        "b2.md": (case_b2(base), "B2"),
        "b3.md": (case_b3(base, b3_replacement), "B3"),
        "a1.md": (base + "\n", "A1"),
    }

    manifest = []
    for name, (content, fails) in cases.items():
        (out / name).write_text(content, encoding="utf-8")
        entry = {"document": name, "fails": fails}
        if name == "a1.md":
            (out / "a1-facts.md").write_text(A1_FACTS, encoding="utf-8")
            entry["facts"] = "a1-facts.md"
            entry["note"] = (
                "the document is the base; fact 5 is the user-visible change it "
                "has no entry for. The fixture carries no marker - the judge has "
                "to find the omission, and a hint in the text would answer it."
            )
        manifest.append(entry)

    (out / "manifest.json").write_text(
        json.dumps(
            {
                "source": f"rubric/{args.audience}.md, section Minimal pairs",
                "generated": "by tools/build_calibration_set.py - do not edit by hand",
                "cases": manifest,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"{len(cases)} documents written to {out.relative_to(REPO)}/")


if __name__ == "__main__":
    main()
