#!/usr/bin/env python3
"""Run the axis separation test and score it against the calibration manifest.

Forty calls: the four document axes on the five calibration documents, and the
five item axes on the four entries of the base document. Every expectation is
in `calibration/{audience}/manifest.json` and in the rubric; nothing from
`labels/{audience}/` is ever sent.

    python3 judge/run_separation.py --dry-run      # counts tokens, spends nothing
    python3 judge/run_separation.py                # runs it
    python3 judge/run_separation.py --audience technical

`--dry-run` uses the token counting endpoint, which is free, and prints what the
run would cost before any of it is spent.
"""

from __future__ import annotations

import argparse
import csv
import functools
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import anthropic

REPO = Path(__file__).resolve().parent.parent
PROMPT = REPO / "judge" / "axis-prompt.md"

# Everything below the prompt is per audience. The prompt is not: one axis, one
# subject, one verdict is the same call whoever the rendering is for.
DEFAULT_AUDIENCE = "customer"


def rubric_rel(audience: str = DEFAULT_AUDIENCE) -> str:
    """The rubric as git wants it named: repo-relative, forward slashes."""
    return f"rubric/{audience}.md"


def rubric_path(audience: str = DEFAULT_AUDIENCE) -> Path:
    return REPO / "rubric" / f"{audience}.md"


def labels_dir(audience: str = DEFAULT_AUDIENCE) -> Path:
    return REPO / "labels" / audience


def calibration_dir(audience: str = DEFAULT_AUDIENCE) -> Path:
    return REPO / "calibration" / audience


def results_dir(audience: str = DEFAULT_AUDIENCE) -> Path:
    return REPO / "judge" / "results" / audience


DOCUMENT_AXES = ["A1", "B1", "B2", "B3"]
ITEM_AXES = ["C1", "C2", "C3", "C4", "C5"]

# Only C4 defines n/a as a verdict of its own. C2 calls the not-applicable case a
# pass in as many words, so offering n/a there would invent a third answer the
# rubric does not have.
NA_AXES = {"C4"}

# $ per million tokens: input, output, cache write, cache read.
PRICES = {
    "claude-opus-5": (5.00, 25.00, 6.25, 0.50),
    "claude-sonnet-5": (2.00, 10.00, 2.50, 0.20),
    "claude-haiku-4-5": (1.00, 5.00, 1.25, 0.10),
}


def _git(*args: str) -> str:
    import subprocess

    try:
        return subprocess.run(
            ["git", *args], cwd=REPO, capture_output=True, text=True, check=True
        ).stdout.strip()
    except Exception:
        return ""


def _is_ancestor(older: str, newer: str) -> bool:
    import subprocess

    return (
        subprocess.run(
            ["git", "merge-base", "--is-ancestor", older, newer],
            cwd=REPO,
            capture_output=True,
        ).returncode
        == 0
    )


def _oldest(commits: set[str]) -> str:
    found = ""
    for commit in sorted(commits):
        if not found or _is_ancestor(commit, found):
            found = commit
    return found


def _newest(commits: set[str]) -> str:
    found = ""
    for commit in sorted(commits):
        if not found or _is_ancestor(found, commit):
            found = commit
    return found


@functools.lru_cache(maxsize=None)
def rubric_history(audience: str = DEFAULT_AUDIENCE) -> tuple[tuple[str, str], ...]:
    """(commit, the name the rubric had in it), newest first.

    The file has been renamed - `rubric-customer.md` became `rubric/customer.md` -
    and `git show commit:path` wants the name of the day, not the name it has
    now. `--follow` walks across the rename and `--name-only` says, per commit,
    which name that was, so neither is written down here."""
    out = _git("log", "--follow", "--format=%h", "--name-only", "--", rubric_rel(audience))
    history: list[list[str]] = []
    for line in out.splitlines():
        line = line.strip()
        if not line:
            continue
        # The pathspec admits one file per commit, and it is a markdown file;
        # the bare hash that opens each block is not.
        if line.endswith(".md"):
            if history and history[-1][1] is None:
                history[-1][1] = line
        else:
            history.append([line, None])
    return tuple((commit, path) for commit, path in history if path)


def rubric_names(audience: str = DEFAULT_AUDIENCE) -> list[str]:
    """Every name this rubric has gone by, newest first."""
    names = [rubric_rel(audience)]
    for _, path in rubric_history(audience):
        if path not in names:
            names.append(path)
    return names


@functools.lru_cache(maxsize=None)
def _section_at(commit: str, heading: str, audience: str = DEFAULT_AUDIENCE, path: str = "") -> str:
    import re as _re

    text = ""
    for candidate in [path] if path else rubric_names(audience):
        text = _git("show", f"{commit}:{candidate}")
        if text:
            break
    pattern = rf"^(#{{2,3}} {_re.escape(heading)}[^\n]*\n.*?)(?=^#{{2,3}} |\Z)"
    found = _re.search(pattern, text, _re.DOTALL | _re.MULTILINE)
    return found.group(1) if found else ""


def axis_last_changed(axis: str, audience: str = DEFAULT_AUDIENCE) -> str:
    """The commit that last changed this axis' own section, not the file."""
    heading = axis if axis == "Units" else f"{axis} -"
    history = rubric_history(audience)
    for (newer, newer_path), (older, older_path) in zip(history, history[1:]):
        if _section_at(newer, heading, audience, newer_path) != _section_at(
            older, heading, audience, older_path
        ):
            return newer
    return history[-1][0] if history else ""


def _rubric_commits(audience: str, axis: str | None = None) -> set[str]:
    """The `rubric_commit` values in this audience's label rows, for one axis or
    for all of them. The column lives per row: a note written about one axis
    says nothing about when any other column was last read."""
    found = set()
    for name in ("items.csv", "runs.csv"):
        path = labels_dir(audience) / name
        if not path.exists():
            continue
        with path.open(encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                commit = (row.get("rubric_commit") or "").strip()
                if commit and (axis is None or row.get("axis") == axis):
                    found.add(commit)
    return found


def column_passed_against(axis: str, audience: str = DEFAULT_AUDIENCE) -> str:
    """The rubric commit a column was last read against, from the `rubric_commit`
    of its own rows. Kept by hand on purpose: only the person who re-read the
    column knows that they did.

    A column read in two sittings carries two commits. It is then only as fresh
    as its oldest row, so that is the one returned."""
    return _oldest(_rubric_commits(audience, axis))


def labels_passed_against(audience: str = DEFAULT_AUDIENCE) -> str:
    """The newest rubric commit any column of this audience was read against -
    how far the labels as a whole have been brought. Not a substitute for the
    per-axis answer above, which is the one a verdict is compared against."""
    return _newest(_rubric_commits(audience))


def labels_are_older_than(axis: str, audience: str = DEFAULT_AUDIENCE) -> bool:
    """True when the axis changed after the column was last read by hand. The
    date of a label file cannot answer this - a note about one axis would mark
    every other column as freshly checked."""
    axis_commit = axis_last_changed(axis, audience)
    column_commit = column_passed_against(axis, audience)
    if not axis_commit or not column_commit:
        return True
    return _is_ancestor(column_commit, axis_commit) and axis_commit != column_commit


def provenance(audience: str = DEFAULT_AUDIENCE) -> dict:
    return {
        "commit": _git("rev-parse", "--short", "HEAD"),
        "dirty": bool(_git("status", "--porcelain")),
        "audience": audience,
        "rubric_last_changed": _git(
            "log", "-1", "--follow", "--format=%h %ad", "--date=short", "--", rubric_rel(audience)
        ),
        "prompt_last_changed": _git("log", "-1", "--format=%h %ad", "--date=short", "--", "judge/axis-prompt.md"),
        "labels_passed_against": labels_passed_against(audience),
    }


def rubric_section(heading: str, audience: str = DEFAULT_AUDIENCE) -> str:
    """One `### AXIS - ...` or `## Units` section of the rubric, verbatim."""
    text = rubric_path(audience).read_text(encoding="utf-8")
    pattern = rf"^(#{{2,3}} {re.escape(heading)}[^\n]*\n.*?)(?=^#{{2,3}} |\Z)"
    match = re.search(pattern, text, re.DOTALL | re.MULTILINE)
    if not match:
        sys.exit(f"section {heading!r} not found in {rubric_rel(audience)}")
    return match.group(1).rstrip()


def prompt_parts() -> tuple[str, str]:
    """The system and user templates, read from judge/axis-prompt.md."""
    text = PROMPT.read_text(encoding="utf-8")
    system = text[text.index("## System") : text.index("## User")]
    user = text[text.index("## User") : text.index("## Expected result")]
    system = system[system.index("\n") :].strip().rstrip("-").rstrip()
    user = user[user.index("\n") :].strip().rstrip("-").rstrip()
    return system, user


def entries(document: str) -> list[str]:
    """The bullets of a document, each with its continuation lines."""
    found, current = [], []
    for line in document.splitlines():
        if line.startswith("- "):
            if current:
                found.append("\n".join(current))
            current = [line]
        elif current and line.strip() and line.startswith(" "):
            current.append(line)
        elif current:
            found.append("\n".join(current))
            current = []
    if current:
        found.append("\n".join(current))
    return found


def build_calls(audience: str = DEFAULT_AUDIENCE) -> list[dict]:
    calibration = calibration_dir(audience)
    manifest = json.loads((calibration / "manifest.json").read_text(encoding="utf-8"))
    units = rubric_section("Units", audience)
    system, user_template = prompt_parts()
    calls = []

    for case in manifest["cases"]:
        document = (calibration / case["document"]).read_text(encoding="utf-8")
        facts = ""
        if case.get("facts"):
            fact_text = (calibration / case["facts"]).read_text(encoding="utf-8")
            facts = "The fact base for the release:\n\n```text\n" + fact_text.rstrip() + "\n```"
        for axis in DOCUMENT_AXES:
            calls.append(
                {
                    "id": f"{case['document']}::{axis}",
                    "audience": audience,
                    "axis": axis,
                    "subject_label": "The document",
                    "subject": document.rstrip(),
                    "facts": facts if axis == "A1" else "",
                    "expected": "fail" if case["fails"] == axis else "pass",
                    "system": system,
                    "user_template": user_template,
                    "units": units,
                }
            )

    base = (calibration / "base.md").read_text(encoding="utf-8")
    for i, entry in enumerate(entries(base), start=1):
        for axis in ITEM_AXES:
            calls.append(
                {
                    "id": f"base.md#entry{i}::{axis}",
                    "audience": audience,
                    "axis": axis,
                    "subject_label": "The entry",
                    "subject": entry,
                    "facts": "",
                    # The base is written to pass every item axis. C4 may answer
                    # n/a where an entry has nothing to set, so both count as
                    # "not a fail" when scoring.
                    "expected": "pass",
                    "system": system,
                    "user_template": user_template,
                    "units": units,
                }
            )
    return calls


# An axis that refers to the output format has to be given that part of the
# format, or the model is asked about a rule it cannot read. Written down as a
# rule in rubric/how-a-rubric-is-built.md, and enforced here.
AXIS_NEEDS_FORMAT = {"B2": ["Two serialisations", "Groups"]}


def format_sections(names: list[str]) -> str:
    text = (REPO / "docs" / "output-format.md").read_text(encoding="utf-8")
    out = []
    for name in names:
        start = text.index(f"### {name}")
        end = text.index("\n### ", start + 1)
        out.append(text[start:end].rstrip())
    return "\n\n".join(out)


def render(call: dict) -> tuple[str, list[dict]]:
    verdicts = "`pass`, `fail`" + (", `n/a`" if call["axis"] in NA_AXES else "")
    body = (
        call["user_template"]
        .replace("{{AXIS_ID}}", call["axis"])
        .replace("{{ALLOWED_VERDICTS}}", verdicts)
        .replace(
            "{{AXIS_SECTION}}",
            rubric_section(call["axis"], call["audience"])
            + (
                "\n\nThe part of the output format this axis refers to:\n\n"
                + format_sections(AXIS_NEEDS_FORMAT[call["axis"]])
                if call["axis"] in AXIS_NEEDS_FORMAT
                else ""
            ),
        )
        .replace("{{FACTS_BLOCK}}", call["facts"])
        .replace("{{SUBJECT_LABEL}}", call["subject_label"])
        .replace("{{SUBJECT}}", call["subject"])
    )
    # The system prompt and the units section are identical in all forty calls,
    # so they are the cached prefix. The axis and the subject vary and come after.
    system = [
        {
            "type": "text",
            "text": call["system"].replace("{{UNITS_SECTION}}", call["units"]),
            "cache_control": {"type": "ephemeral"},
        }
    ]
    return body, system


def _collapse(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def parse_answer(text: str) -> dict:
    stripped = re.sub(r"^```(?:json)?\n|\n```$", "", text.strip())
    try:
        answer = json.loads(stripped)
    except json.JSONDecodeError:
        return {"verdict": None, "quote": None, "reason": None, "raw": text}
    return {
        "verdict": str(answer.get("verdict", "")).strip().lower() or None,
        "quote": answer.get("quote"),
        "reason": answer.get("reason"),
    }


def cost(usage, model: str) -> float:
    inp, out, write, read = PRICES.get(model, PRICES["claude-opus-5"])
    return (
        getattr(usage, "input_tokens", 0) * inp
        + getattr(usage, "output_tokens", 0) * out
        + (getattr(usage, "cache_creation_input_tokens", 0) or 0) * write
        + (getattr(usage, "cache_read_input_tokens", 0) or 0) * read
    ) / 1_000_000


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--audience", default=DEFAULT_AUDIENCE)
    parser.add_argument("--model", default="claude-opus-5")
    parser.add_argument("--effort", default="low", choices=["low", "medium", "high"])
    parser.add_argument("--max-tokens", type=int, default=2000)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--limit", type=int, help="run only the first N calls")
    args = parser.parse_args()

    if not rubric_path(args.audience).exists():
        sys.exit(f"no rubric at {rubric_rel(args.audience)}")
    if not (calibration_dir(args.audience) / "manifest.json").exists():
        sys.exit(
            f"no calibration set for {args.audience} - run "
            f"tools/build_calibration_set.py --audience {args.audience} first"
        )

    calls = build_calls(args.audience)
    if args.limit:
        calls = calls[: args.limit]
    client = anthropic.Anthropic()

    if args.dry_run:
        total_in = 0
        for call in calls:
            body, system = render(call)
            counted = client.messages.count_tokens(
                model=args.model,
                system=system,
                messages=[{"role": "user", "content": body}],
            )
            total_in += counted.input_tokens
        inp, out, _, _ = PRICES.get(args.model, PRICES["claude-opus-5"])
        # Output is mostly thinking. 400 tokens a call is what low effort costs
        # on a task this small; 1200 is the pessimistic end.
        low = total_in * inp / 1e6 + len(calls) * 400 * out / 1e6
        high = total_in * inp / 1e6 + len(calls) * 1200 * out / 1e6
        print(f"{len(calls)} calls, {total_in:,} input tokens, uncached")
        print(f"estimate {args.model}: ${low:.2f} to ${high:.2f}")
        print("caching the shared prefix takes the input side down by roughly 80 percent")
        return

    results, spent = [], 0.0
    for i, call in enumerate(calls, start=1):
        body, system = render(call)
        response = client.messages.create(
            model=args.model,
            max_tokens=args.max_tokens,
            system=system,
            output_config={"effort": args.effort},
            thinking={"type": "adaptive"},
            messages=[{"role": "user", "content": body}],
        )
        text = "".join(b.text for b in response.content if b.type == "text")
        answer = parse_answer(text)
        spent += cost(response.usage, args.model)

        quote = answer.get("quote") or ""
        # The documents are hard-wrapped, so a quote read as flowing text will
        # not match character for character even when it is verbatim. Compare
        # with whitespace collapsed; anything still missing is invented.
        record = {
            "id": call["id"],
            "axis": call["axis"],
            "expected": call["expected"],
            **answer,
            "quote_found": bool(quote)
            and _collapse(quote) in _collapse(call["subject"]),
            "usage": {
                "input": response.usage.input_tokens,
                "output": response.usage.output_tokens,
                "cache_read": getattr(response.usage, "cache_read_input_tokens", 0) or 0,
            },
        }
        # n/a counts as "not a fail": on the base every item axis should decline
        # to fail, and C4 declines by answering n/a.
        got_fail = record["verdict"] == "fail"
        record["match"] = got_fail == (call["expected"] == "fail")
        results.append(record)
        mark = "ok " if record["match"] else "MISS"
        print(f"[{i:>2}/{len(calls)}] {mark} {call['id']:<28} {record['verdict']}  ${spent:.3f}")

    matched = sum(r["match"] for r in results)
    quoted = sum(r["quote_found"] for r in results)
    out_dir = results_dir(args.audience)
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%S")
    out = out_dir / f"separation-{args.model}-{stamp}.json"
    out.write_text(
        json.dumps(
            {
                "model": args.model,
                "audience": args.audience,
                "effort": args.effort,
                "run_at": stamp,
                "provenance": provenance(args.audience),
                "calls": len(results),
                "matched": matched,
                "quotes_found_in_subject": quoted,
                "cost_usd": round(spent, 4),
                "results": results,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"\n{matched}/{len(results)} verdicts as expected, {quoted} quotes found verbatim")
    print(f"${spent:.3f} spent, written to {out.relative_to(REPO)}")


if __name__ == "__main__":
    main()
