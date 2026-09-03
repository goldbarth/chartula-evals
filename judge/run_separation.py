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
import hashlib
import json
import os
import uuid
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

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


def prompt_last_changed(axis: str, audience: str = DEFAULT_AUDIENCE) -> str:
    """The newest commit that changed anything this axis is judged against.

    An axis is not the whole of what the judge reads: `Units` goes into every
    prompt beside it, and a column read before Units changed was read against a
    different question, however untouched its own section is. Comparing against
    the axis alone left that hole - one edit to Units and no column anywhere
    would have been reported stale."""
    return _newest({axis_last_changed(axis, audience), axis_last_changed("Units", audience)} - {""})


def rubric_uncommitted(audience: str = DEFAULT_AUDIENCE) -> bool:
    """True when the rubric in the working tree differs from the last commit.

    The prompt is built from the working tree and staleness is computed from
    git history, so an uncommitted edit is judged and reported as though it
    were the committed text."""
    return bool(_git("status", "--porcelain", "--", rubric_rel(audience)))


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
    """True when what the axis is judged against changed after the column was
    last read by hand. The date of a label file cannot answer this - a note
    about one axis would mark every other column as freshly checked."""
    axis_commit = prompt_last_changed(axis, audience)
    column_commit = column_passed_against(axis, audience)
    if not axis_commit or not column_commit:
        return True
    return _is_ancestor(column_commit, axis_commit) and axis_commit != column_commit


CRITERION_AXES = ["Units", "A1", "B1", "B2", "B3", "C1", "C2", "C3", "C4", "C5"]


def criterion_digest(audience: str = DEFAULT_AUDIENCE) -> str:
    """A hash of the exact text the judge is shown, read from the working tree.

    A commit is not a durable name for that text. Two of this repository's own
    rubric commits were replaced by `git commit --amend` and survive only as
    unreachable objects; the `rubric_commit` stamps naming them still resolve
    today and will not once git prunes them. A content hash answers the one
    question provenance exists for - were these two figures produced against
    the same criterion - and it answers it without git.

    Covers every axis section, `Units`, the format sections that are inlined
    beside an axis, and both halves of the prompt. Anything the judge reads is
    in here; anything it does not read is not, so a note written elsewhere in
    the rubric leaves the digest alone."""
    parts = [rubric_section(h if h == "Units" else f"{h} -", audience) for h in CRITERION_AXES]
    for axis in sorted(AXIS_NEEDS_FORMAT):
        parts.append(format_sections(AXIS_NEEDS_FORMAT[axis]))
    parts.extend(prompt_parts())
    joined = "\x00".join(part.strip() for part in parts)
    return "sha256:" + hashlib.sha256(joined.encode("utf-8")).hexdigest()[:16]


def criterion_version() -> str:
    """The frozen version this tree is at, from the nearest tag.

    `v1.0.0` alone means the tree is exactly the tagged criterion. A suffix
    such as `v1.0.0-3-gea0788c` means three commits have landed since, and
    whether they touched the criterion is what the digest above settles."""
    return _git("describe", "--tags", "--always", "--dirty") or "untagged"


SCHEMA = "chartula-evals/eval-log/1"


def eval_id() -> str:
    """A name for this run that does not depend on the file it is written to.

    The filename carried the identity before, which meant a rename lost it and
    a result quoted in prose could not be traced back."""
    return "evl_" + uuid.uuid4().hex[:12]


def environment() -> str:
    """Where the run happened. A figure from a laptop mid-edit and a figure
    from a pipeline are not the same evidence."""
    return "ci" if os.environ.get("CI") else "local"


def parameters(args) -> dict:
    """What was sent to the model, beside the prompt.

    `sampling` is a sentence rather than a number on purpose. The rubric prompt
    said "run at temperature 0" from the beginning and no runner ever sent a
    temperature: on this model family the sampling parameters are rejected
    outright, so the claim was not merely unimplemented but unimplementable,
    and no run was ever deterministic. What is pinned is the effort level and
    the one-axis-one-subject shape of the call, not the sampling."""
    return {
        "max_tokens": args.max_tokens,
        "effort": args.effort,
        "thinking": "adaptive",
        "sampling": "not settable: temperature, top_p and top_k are rejected by this model family",
    }


def usage_of(response) -> dict:
    return {
        "input": response.usage.input_tokens,
        "output": response.usage.output_tokens,
        "cache_read": getattr(response.usage, "cache_read_input_tokens", 0) or 0,
    }


def eval_log(kind: str, args, criterion: dict, execution: dict) -> dict:
    """The four blocks every result file is written in.

    metadata says which run this was and where; evaluation_config says what it
    was judged against and with; execution_results holds the figures and, per
    result, the subject it was given. The subject is in the file rather than
    referenced, because the renderings are rewritten every turn of the
    production loop and a reference into `test-runs/` stops meaning anything
    the moment one is."""
    prov = provenance(args.audience)
    return {
        "schema": SCHEMA,
        "metadata": {
            "eval_id": eval_id(),
            "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "environment": environment(),
            "commit": prov["commit"],
            "dirty": prov["dirty"],
        },
        "evaluation_config": {
            "kind": kind,
            "audience": args.audience,
            "criterion": {
                "name": args.audience,
                "version": prov["criterion_version"],
                "digest": prov["criterion_digest"],
                "rubric_last_changed": prov["rubric_last_changed"],
                "prompt_last_changed": prov["prompt_last_changed"],
                "labels_passed_against": prov["labels_passed_against"],
                **criterion,
            },
            "llm_judge": args.model,
            "parameters": parameters(args),
        },
        "execution_results": execution,
    }


def provenance(audience: str = DEFAULT_AUDIENCE) -> dict:
    return {
        "commit": _git("rev-parse", "--short", "HEAD"),
        "dirty": bool(_git("status", "--porcelain")),
        "audience": audience,
        "criterion_version": criterion_version(),
        "criterion_digest": criterion_digest(audience),
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


# A1's missing half asks what has no entry, which is not in the document at any
# depth: the axis is answerable only against the changes the release was cut
# from. Every other axis reads the subject alone, and sending facts there would
# invite a verdict on grounding, which the rubric leaves to the faithfulness
# check.
AXIS_NEEDS_FACTS = {"A1"}


def fact_base(audience: str = DEFAULT_AUDIENCE) -> str:
    """The release's changes as the prompt takes them, or "" when none is
    written down. One release for now, so the path is fixed; a second one turns
    this into a lookup and nothing else."""
    path = REPO / "test-runs" / "v0.1.0-facts.md"
    if not path.exists():
        return ""
    return "The changes the release was cut from:\n\n```text\n" + path.read_text(encoding="utf-8").rstrip() + "\n```"


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
    try:
        import anthropic
    except ModuleNotFoundError:
        sys.exit(
            "the anthropic SDK is not on this interpreter, and run_separation.py needs it to make "
            "a call.\n"
            "    .venv/bin/python3 judge/run_separation.py ...\n"
            "or install it here: python3 -m pip install -r judge/requirements.txt\n"
            "Everything that only reads the files - status.py, tools/labels.py - runs "
            "without it."
        )

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
            "test_payload": {
                "subject_label": call["subject_label"],
                "subject": call["subject"],
            },
            **answer,
            "quote_found": bool(quote)
            and _collapse(quote) in _collapse(call["subject"]),
            "usage": usage_of(response),
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
            eval_log(
                "separation",
                args,
                criterion={},
                execution={
                    "calls": len(results),
                    "matched": matched,
                    "quotes_found_in_subject": quoted,
                    "cost_usd": round(spent, 4),
                    "results": results,
                },
            ),
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"\n{matched}/{len(results)} verdicts as expected, {quoted} quotes found verbatim")
    print(f"${spent:.3f} spent, written to {out.relative_to(REPO)}")


if __name__ == "__main__":
    main()
