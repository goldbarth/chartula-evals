#!/usr/bin/env python3
"""Turn a Chartula run's `changelog.json` into the files this harness reads.

    python3 tools/from_chartula_run.py <changelog.json> --run sonnet-5-format-out
    python3 tools/from_chartula_run.py <changelog.json> --run <name> --facts

A run of `chartula generate --no-publish` writes one file holding both halves of
a case: the fact base under `changes`, and the rendered text per audience under
`renderings`. Neither is in the shape the judge reads, so this writes them out.

**The rendering** goes to `test-runs/{run}.md`, split into the `--- Customer ---`
sections `run_labelled.py` looks for.

**The customer page**, when `--page` names one, is the customer section rather
than the `renderings.customer` field. The two are not the same document: the
field is the model's text alone, while `release-<tag>.md` is what a person would
publish, front matter and all. B2 judges the opening the format requires, so
handing it the field fails a document for missing something Chartula wrote to a
different file.

**The fact base** goes to `test-runs/{tag}-facts.md`, and only when `--facts` is
passed, because it is usually already there. A fact base belongs to a release
rather than to a run: every rendering of v0.1.0 is judged against the same one,
and rewriting it would move A1's figures for reasons that have nothing to do
with the rendering being measured.

`userVisible` is dropped on the way. Chartula decides it per change and writes it
into the file, but it is the question A1 asks - whether a reader could come into
contact with the change - and a fact base that answers it hands over the verdict
instead of setting it. The category and the breaking marker are dropped for a
duller reason: the fact base already in the repository does not carry them, and
a figure is only comparable with the one before it if both were read from the
same shape.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RUNS = REPO / "test-runs"

AUDIENCES = ["technical", "customer", "product"]


def rendering(data: dict, run: str, page: Path | None = None) -> str:
    """The three audience texts, under the markers the judge splits on."""
    texts = dict(data.get("renderings") or {})
    if page is not None:
        # The page is the customer rendering as it is published, so it replaces
        # the field rather than being appended beside it.
        texts["customer"] = page.read_text(encoding="utf-8")
    present = [a for a in AUDIENCES if (texts.get(a) or "").strip()]
    if not present:
        sys.exit("this run carries no rendered text: `renderings` is empty")

    out = [f"{run}, rendered by Chartula from {data.get('tag', 'an unnamed tag')}", ""]
    for audience in present:
        out.append(f"--- {audience.capitalize()} ---")
        out.append("")
        out.append(texts[audience].strip())
        out.append("")
    missing = [a for a in AUDIENCES if a not in present]
    if missing:
        print(f"  no text for: {', '.join(missing)}", file=sys.stderr)
    return "\n".join(out).rstrip() + "\n"


def facts(data: dict) -> str:
    """The fact base, in the shape the one already in the repository has.

    One section per change, `## #<number> <title>`, then the description it was
    merged with. Nothing here says whether a change is user-visible."""
    tag = data.get("tag", "an unnamed tag")
    changes = data.get("changes") or []
    out = [
        f"# Fact base: Chartula {tag}",
        "",
        f"The {len(changes)} changes the release was cut from, each with the title and the",
        "description it was merged with.",
        "",
        f"Written by `tools/from_chartula_run.py` from a run's `changelog.json`, which is",
        "Chartula's own record of what it was given. Not read from the repository by hand.",
        "",
        "Nothing here marks a change as user-visible or internal. Chartula decides that",
        "per change and records it, and it is dropped on the way in: that is the question",
        "A1 asks, and a fact base that answered it would be handing over the verdict.",
        "",
        "---",
        "",
    ]
    for change in changes:
        number = change.get("number")
        heading = f"#{number} {change['title']}" if number else change["title"]
        out.append(f"## {heading}")
        out.append("")
        description = (change.get("description") or "").strip()
        out.append(description if description else "_No description._")
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def write(path: Path, text: str, force: bool) -> None:
    if path.exists() and not force:
        sys.exit(
            f"{path.relative_to(REPO)} exists. A rendering and a fact base are evidence "
            "a figure was read from;\noverwriting one silently changes what an older "
            "result meant. Pass --force if that is what you want."
        )
    path.write_text(text, encoding="utf-8")
    print(f"  wrote {path.relative_to(REPO)}  ({len(text.splitlines())} lines)")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("changelog", type=Path, help="a run's changelog.json")
    parser.add_argument("--run", required=True, help="the name this run gets in test-runs/")
    parser.add_argument(
        "--facts",
        action="store_true",
        help="also write the fact base; only for a release that has none yet",
    )
    parser.add_argument(
        "--page",
        type=Path,
        help="the run's release-<tag>.md, used as the customer section instead of "
             "the changelog.json field, so the judge sees the opening as published",
    )
    parser.add_argument("--force", action="store_true", help="overwrite a file that exists")
    args = parser.parse_args()

    if not args.changelog.exists():
        raise SystemExit(f"no such file: {args.changelog}")
    data = json.loads(args.changelog.read_text(encoding="utf-8"))

    version = data.get("schemaVersion")
    if version != 1:
        print(
            f"  schemaVersion is {version}, not 1. The fields this reads may have moved;\n"
            "  check docs/changelog-json.md in Chartula before trusting the output.",
            file=sys.stderr,
        )

    if args.page is not None and not args.page.exists():
        raise SystemExit(f"no such file: {args.page}")

    write(RUNS / f"{args.run}.md", rendering(data, args.run, args.page), args.force)

    if args.facts:
        write(RUNS / f"{data.get('tag', 'untagged')}-facts.md", facts(data), args.force)
    else:
        existing = RUNS / f"{data.get('tag', 'untagged')}-facts.md"
        where = existing.relative_to(REPO) if existing.exists() else "none in the repository"
        print(f"  fact base left alone: {where}")


if __name__ == "__main__":
    main()
