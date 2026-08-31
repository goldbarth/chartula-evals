#!/usr/bin/env python3
"""Judge the labelled runs and compare the verdicts with the human labels.

The separation run showed the axes can be told apart on constructed cases.
This asks the harder question: does the judge agree with a person on real
renderings - 53 entries across three runs, plus the document axes.

    python3 judge/run_labelled.py --dry-run
    python3 judge/run_labelled.py --model claude-sonnet-5
    python3 judge/run_labelled.py --axis C3 --run sonnet-5-out   # one column

Agreement alone is not the measure. C2 and C5 pass on almost every entry, so a
judge that always answers pass scores above ninety percent there and has
understood nothing. The report gives, per axis, how often the judge finds the
verdict a person gave *and* what it does with the minority of that column.

The prompt, the rubric sections and the calling code are the ones from
run_separation.py. Nothing here shows the judge a human verdict or a note.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import anthropic

REPO = Path(__file__).resolve().parent.parent
LABELS = REPO / "labels" / "customer.md"
RUNS = REPO / "test-runs"
RESULTS = REPO / "judge" / "results"

_spec = importlib.util.spec_from_file_location("sep", Path(__file__).with_name("run_separation.py"))
sep = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sep)

ITEM_AXES = ["A1", "C1", "C2", "C3", "C4", "C5"]
DOCUMENT_AXES = ["B1", "B2", "B3"]


def table_rows(text: str) -> list[list[str]]:
    rows = []
    for line in text.splitlines():
        if line.startswith("|") and not re.match(r"^\|[\s|:-]+\|$", line):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            rows.append(cells)
    return rows


def human_labels() -> tuple[dict, dict]:
    """(item verdicts keyed by (run, item), document verdicts keyed by run)."""
    text = LABELS.read_text(encoding="utf-8")
    items, documents = {}, {}

    item_block = text[text.index("## Item table") : text.index("## Friction log")]
    for row in table_rows(item_block):
        if len(row) < 11 or row[1].startswith(("item", "---")):
            continue
        run, item = row[0], row[1]
        items[(run, item)] = {
            "kind": row[2],
            "verdicts": dict(zip(ITEM_AXES, [c.lower() for c in row[3:9]])),
            "shippable": row[9].lower(),
        }

    run_block = text[text.index("## Run table") : text.index("## Item table")]
    for row in table_rows(run_block):
        if len(row) < 5 or row[0].startswith(("run", "---")):
            continue
        documents[row[0]] = dict(zip(DOCUMENT_AXES, [c.lower() for c in row[1:4]]))
    return items, documents


def customer_section(run: str) -> str:
    text = (RUNS / f"{run}.md").read_text(encoding="utf-8").splitlines()
    out, inside = [], False
    for line in text:
        if line.startswith("--- Customer ---"):
            inside = True
            continue
        if inside and line.startswith("--- ") and line.endswith(" ---"):
            break
        if inside:
            out.append(line)
    return "\n".join(out).strip()


def build_calls(items: dict, documents: dict, want_run: str | None, want_axis: str | None) -> list[dict]:
    units = sep.rubric_section("Units")
    system, user_template = sep.prompt_parts()
    calls = []

    by_run = defaultdict(list)
    for (run, item) in items:
        by_run[run].append(item)

    for run, ids in by_run.items():
        if want_run and run != want_run:
            continue
        document = customer_section(run)
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
                        "run": run,
                        "item": item,
                        "axis": axis,
                        "human": items[(run, item)]["verdicts"][axis],
                        "subject_label": "The entry",
                        "subject": entry,
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
                    "run": run,
                    "item": "document",
                    "axis": axis,
                    "human": documents[run][axis],
                    "subject_label": "The document",
                    "subject": document,
                    "facts": "",
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
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="claude-opus-5")
    parser.add_argument("--effort", default="low", choices=["low", "medium", "high"])
    parser.add_argument("--max-tokens", type=int, default=2000)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--run", help="only this run")
    parser.add_argument("--axis", help="only this axis")
    args = parser.parse_args()

    items, documents = human_labels()
    calls = build_calls(items, documents, args.run, args.axis)
    if args.limit:
        calls = calls[: args.limit]
    if not calls:
        sys.exit("nothing to judge with those filters")
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
                "human": call["human"],
                **answer,
                "agree": agree,
                "quote_found": bool(quote) and sep._collapse(quote) in sep._collapse(call["subject"]),
            }
        )
        mark = "ok " if agree else "DIFF"
        print(f"[{i:>3}/{len(calls)}] {mark} {call['id']:<34} human={call['human']:<5} judge={answer['verdict']}  ${spent:.3f}")

    summary = report(results)
    print_report(summary)

    RESULTS.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M")
    out = RESULTS / f"labelled-{args.model}-{stamp}.json"
    out.write_text(
        json.dumps(
            {
                "model": args.model,
                "effort": args.effort,
                "run_at": stamp,
                "calls": len(results),
                "agreed": sum(r["agree"] for r in results),
                "quotes_found_in_subject": sum(r["quote_found"] for r in results),
                "cost_usd": round(spent, 4),
                "per_axis": summary,
                "results": results,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"\n{sum(r['agree'] for r in results)}/{len(results)} agree, ${spent:.3f}, written to {out.relative_to(REPO)}")


if __name__ == "__main__":
    main()
