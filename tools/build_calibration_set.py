#!/usr/bin/env python3
"""Assemble the calibration documents from the minimal pairs in the rubric.

The texts live in `rubric/{audience}.md`, section "Minimal pairs", and are read
from there: the base document from its fenced block, the inserted and replaced
entries from the block quotes that follow. Only the transformations - where a
group is inserted, which two entries are swapped - are encoded here, because
they are instructions in prose that no parser can be trusted with.

One set of transformations per audience, below: which group is inserted where,
which two are swapped, which entry is replaced. The texts stay in the rubric.

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
CUSTOMER_A1_FACTS = """\
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


def case_a1_included(base: str, insert: str) -> str:
    """An entry no reader can come into contact with, in a group of its own."""
    groups = split_groups(base)
    at = group_index(groups, "What's New") + 1
    groups.insert(at, ("### What's Changed", "\n" + insert + "\n"))
    return join_groups(groups)


def case_b3(base: str, replacement: str) -> str:
    """The fix entry padded past its outcome and given a superlative."""
    groups = split_groups(base)
    i = group_index(groups, "Bug Fixes")
    heading, _ = groups[i]
    groups[i] = (heading, "\n" + replacement + "\n")
    return join_groups(groups)


# The technical pairs need two fact bases, and neither can carry the other's
# defect. The A1 fixture holds one change the base document has no entry for;
# the C3 fixture holds every change the document does carry, with the titles the
# pull requests gave them, so a copied description is visible as a copy. Both
# are written as sentences rather than as titles where they are not the point:
# a fixture that reads like a list of titles would fail C3 everywhere.
TECHNICAL_A1_FACTS = """\
Changes in release 0.1.0, as the fact base holds them:

1. Release notes are written to the GitHub release rather than to a separate
   file. Breaking. Pull request #61.
2. Configuration is read from chartula.yaml, layered before environment
   variables. Pull request #64.
3. Every run reports what it did and what it cost. Pull request #66.
4. A ceiling is sent on every model call, so long output is no longer cut off.
   Pull request #70.
5. Breaking changes are detected from the Conventional Commits footer rather
   than from prose. Pull request #70.
6. A release whose commits have no pull requests attached no longer fails; the
   commit subjects are used instead. Pull request #72.
"""

TECHNICAL_C3_FACTS = """\
Changes in release 0.1.0, with the title of the pull request that carried each:

1. "Write release notes to the GitHub release" - breaking. Pull request #61.
2. "Read chartula.yaml with sensible defaults" - pull request #64.
3. "Report what a run does and what it costs" - pull request #66.
4. "Send MaxOutputTokens on every model call" - pull request #70.
5. "Match the Conventional Commits footer when detecting a breaking change" -
   pull request #70.
"""


def replace_entry(base: str, group: str, index: int, replacement: str) -> str:
    """One entry of one group swapped for another, everything else untouched."""
    groups = split_groups(base)
    i = group_index(groups, group)
    heading, body = groups[i]
    found = entries(body)
    if index >= len(found):
        sys.exit(f"group {group!r} has no entry {index + 1}")
    found[index] = replacement
    groups[i] = (heading, "\n" + "\n".join(found) + "\n")
    return join_groups(groups)


def append_entry(base: str, group: str, entry: str) -> str:
    groups = split_groups(base)
    i = group_index(groups, group)
    heading, body = groups[i]
    groups[i] = (heading, "\n" + "\n".join(entries(body) + [entry]) + "\n")
    return join_groups(groups)


def insert_paragraph(base: str, group: str, paragraph: str) -> str:
    """A block of prose under the entries of a group: not an entry, which is
    the whole point of the pair it builds."""
    groups = split_groups(base)
    i = group_index(groups, group)
    heading, body = groups[i]
    groups[i] = (heading, "\n" + "\n".join(entries(body)) + "\n\n" + paragraph + "\n")
    return join_groups(groups)


def swap_groups(base: str, first: str, second: str) -> str:
    groups = split_groups(base)
    i, j = group_index(groups, first), group_index(groups, second)
    groups[i], groups[j] = groups[j], groups[i]
    return join_groups(groups)


# A case is its document, the axis it is built to fail, and - where the axis
# cannot be answered from the document - the fact base handed alongside it,
# as (filename, text). `note` explains a fixture that carries no marker.
def entries_of(document: str) -> list[str]:
    """Every bullet of a document, in the order a reader meets them."""
    found = []
    for _, body in split_groups(document):
        found += entries(body)
    return found


def first_difference(before: list[str], after: list[str]) -> int | None:
    """The 1-based position of the first entry that is not the one it replaced."""
    for i, entry in enumerate(after, start=1):
        if i > len(before) or entry != before[i - 1]:
            return i
    return None


def cases_customer(base: str, blocks: list[str]) -> dict:
    if len(blocks) < 3:
        sys.exit(f"expected three block quotes in the section, found {len(blocks)}")
    b1_insert, b3_replacement, a1_insert = blocks[0], blocks[1], blocks[2]
    return {
        "base.md": {"document": base + "\n", "fails": None},
        "b1.md": {"document": case_b1(base, b1_insert), "fails": "B1"},
        "b2.md": {"document": case_b2(base), "fails": "B2"},
        "b3.md": {"document": case_b3(base, b3_replacement), "fails": "B3"},
        "a1-absent.md": {
            "document": base + "\n",
            "fails": "A1",
            "facts": ("a1-facts.md", CUSTOMER_A1_FACTS),
            "note": "the missing half: the document is the base, and fact 5 is "
                    "the user-visible change it has no entry for. The fixture "
                    "carries no marker - the judge has to find the omission, and "
                    "a hint in the text would answer it.",
        },
        "a1-included.md": {"document": case_a1_included(base, a1_insert), "fails": "A1"},
        # a1-absent carries the facts and no marker; a1-included carries an
        # entry nothing brings the reader into contact with. One axis, two
        # halves, and a judge has to answer both from the same rules.
    }


def cases_technical(base: str, blocks: list[str]) -> dict:
    if len(blocks) < 7:
        sys.exit(f"expected seven block quotes in the section, found {len(blocks)}")
    b2_para, c1_entry, c2_entry, c3_entry, c4_entry, c5_entry, a1_entry = blocks[:7]
    return {
        "base.md": {"document": base + "\n", "fails": None},
        "b1.md": {"document": swap_groups(base, "Changed", "Added"), "fails": "B1"},
        "b2.md": {"document": insert_paragraph(base, "Added", b2_para), "fails": "B2"},
        "c1.md": {"document": replace_entry(base, "Added", 0, c1_entry), "fails": "C1"},
        "c2.md": {"document": replace_entry(base, "Added", 0, c2_entry), "fails": "C2"},
        # C3 is the only entry axis here that cannot be decided from the
        # document: the copy is visible only beside the title it was taken from.
        "c3.md": {
            "document": replace_entry(base, "Changed", 1, c3_entry),
            "fails": "C3",
            "facts": ("c3-facts.md", TECHNICAL_C3_FACTS),
            "note": "the second Changed entry is the title of pull request #64 "
                    "as the facts give it. Every other entry is written rather "
                    "than copied, and nothing is missing, so A1 passes on this "
                    "document with the same facts in front of it.",
        },
        "c4.md": {"document": replace_entry(base, "Fixed", 1, c4_entry), "fails": "C4"},
        "c5.md": {"document": replace_entry(base, "Fixed", 0, c5_entry), "fails": "C5"},
        "a1-absent.md": {
            "document": base + "\n",
            "fails": "A1",
            "facts": ("a1-facts.md", TECHNICAL_A1_FACTS),
            "note": "the missing half: the document is the base, and fact 6 is "
                    "the change it has no entry for. The fixture carries no "
                    "marker - the judge has to find the omission, and a hint in "
                    "the text would answer it.",
        },
        "a1-included.md": {"document": append_entry(base, "Added", a1_entry), "fails": "A1"},
    }


BUILDERS = {"customer": cases_customer, "technical": cases_technical}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--audience", default=DEFAULT_AUDIENCE)
    parser.add_argument("--out", default="calibration")
    args = parser.parse_args()

    rubric = REPO / "rubric" / f"{args.audience}.md"
    if not rubric.exists():
        sys.exit(f"no rubric at rubric/{args.audience}.md")

    build = BUILDERS.get(args.audience)
    if not build:
        sys.exit(f"no case set written for audience {args.audience!r}")

    sec = section(rubric.read_text(encoding="utf-8"))
    base = base_document(sec)
    cases = build(base, quoted_blocks(sec))

    out = REPO / args.out / args.audience
    out.mkdir(parents=True, exist_ok=True)

    base_entries = entries_of(base)

    manifest = []
    for name, case in cases.items():
        (out / name).write_text(case["document"], encoding="utf-8")
        entry = {"document": name, "fails": case["fails"]}
        # An item axis is answered on one entry, not on the document, so the
        # case has to say which entry it broke. It is the first one that differs
        # from the base, and finding it by comparison keeps the builder from
        # carrying a position that a later edit to the rubric would move.
        if (case["fails"] or " ")[0] == "C":
            changed = first_difference(base_entries, entries_of(case["document"]))
            if changed is None:
                sys.exit(f"{name}: fails {case['fails']} but no entry differs from the base")
            entry["entry_fails"] = changed
        if case.get("facts"):
            facts_name, facts_text = case["facts"]
            (out / facts_name).write_text(facts_text, encoding="utf-8")
            entry["facts"] = facts_name
        if case.get("note"):
            entry["note"] = case["note"]
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
