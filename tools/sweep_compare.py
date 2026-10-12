#!/usr/bin/env python3
"""Read a comparison that spans several sweep plans: what it has cost, and what it found.

    python3 tools/sweep_compare.py spend  sweeps/prices-2026-10-09.json sweeps/cmp-*.json \\
        --budget openai=5.50 --budget anthropic=5.50
    python3 tools/sweep_compare.py report sweeps/prices-2026-10-09.json sweeps/cmp-*.json \\
        --out sweeps/cmp-2026-10-stats --withhold cmp-difficult-ingestor-v3.2.0

`tools/sweep.py` runs one release per plan, and `tools/sweep_stats.py` reads one
plan's runs. A comparison over several releases is several plans with the same
cells, and this reads them together. The arguments are the plans, not the result
folders: a plan says which case it is, which provider a cell spends on, and how
many runs are still owed.

**`spend` is for the budget.** It adds up what the records say was billed, one
total per provider, and projects what the runs still owed would cost from the
median of the runs each cell already has. A cell without a run has no figure and
is listed as such rather than counted as nothing.

**A cost that is not known is never zero.** A run without a record is counted as
unknown. A run whose record says a call came back without usage is a lower bound,
and every total it enters is marked as one.

**Two costs, kept apart.** *Billed* applies the provider's cache as it fell and is
what the budget pays. *Uncached* prices every input token in full, does not depend
on what ran just before, and is what cells are compared on. Both are given for the
rendering and for the check separately.

**An incomplete run is a finished one.** `sweep.py` marks a run `incomplete` when
every model call was answered and Chartula still refused an audience's text. It
is a draw like any other and is not repeated, so a cell has as many draws as the
plan asks for and the report says in how many each audience did not render. Cost
and duration are summarised over the complete runs, because a run that lost an
audience skipped that audience's check; what belongs to one audience (its flags,
its length) is summarised over every draw in which that audience rendered.

**A plan on a private repository is withheld, not left out.** `--withhold <plan>`
keeps the plan's figures in every table and file and leaves out what quotes the
repository: the text of its flags and the plan's description of its pull requests.
Its run folders are not in this repository either, so a report made from a fresh
clone has only the plans that are.

**`report` makes no judgement.** It writes what was measured: cost, tokens and
duration by phase, retries, failed renderings, checks that could not be read, the
flags and how often the same one came back across a cell's repetitions, and the
length of each text. A flag is what a checker reported, not a confirmed error, and
fewer flags do not mean a better text. Nothing here ranks a configuration.

This makes no model call and needs nothing beyond the standard library.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import statistics
import sys
from pathlib import Path

from sweep_stats import checked_by, fmt, load_prices, price, row, runs, spread

REPO = Path(__file__).resolve().parent.parent
SWEEPS = REPO / "sweeps"

AUDIENCES = ["technical", "customer"]
# A draw: a run that is finished and is not repeated, complete or not.
DRAWS = ("ok", "incomplete")
# What a cell's complete runs are summarised on, as median and range.
RUN_MEASURES = ["uncachedUsd", "billedUsd", "renderUncachedUsd", "checkUncachedUsd", "inputTokens", "outputTokens",
                "durationSeconds", "renderSeconds", "checkSeconds", "flags"]
# What belongs to one audience, summarised over every draw in which that audience rendered.
AUDIENCE_MEASURES = ["flagsTechnical", "flagsCustomer", "technicalCharacters", "technicalEntries",
                     "customerCharacters", "customerEntries"]


def load(plan_path: Path) -> dict:
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    plan["_stem"] = plan_path.stem
    plan["_sweep"] = SWEEPS / plan_path.stem
    plan["_cells"] = {c["name"]: c for c in plan["cells"]}
    for cell in plan["cells"]:
        if "provider" not in cell:
            sys.exit(f"{plan_path}: cell {cell['name']} names no provider; a comparison keeps one budget per provider")
    return plan


def all_runs(plans: list[dict]):
    """Every run folder of every plan: plan, cell name, run name, folder, sweep result, run record."""
    for plan in plans:
        if not plan["_sweep"].is_dir():
            continue
        for cell, run, result, record in runs(plan["_sweep"]):
            if cell in plan["_cells"]:
                yield plan, cell, run, plan["_sweep"] / cell / run, result, record


def status_of(run: str, result: dict) -> str:
    # A folder without sweep-run.json is the run in progress, or one cut off mid-run.
    return result.get("status", "failed" if ".failed-" in run else "running")


def phase_costs(prices: dict, record: dict) -> dict:
    """Billed and uncached cost of the rendering and of the check, each on its own model."""
    m, prov = record["metrics"], record["provenance"]
    render = price(prices, prov["model"], m["rephrase"])
    check = price(prices, prov["checkModel"], m["faithfulnessCheck"]) if prov.get("thoroughCheck") else (0.0, 0.0)
    return {"renderBilledUsd": render[0], "renderUncachedUsd": render[1],
            "checkBilledUsd": check[0], "checkUncachedUsd": check[1]}


def lower_bound(record: dict) -> bool:
    m = record["metrics"]
    return bool(m["rephrase"].get("callsWithoutUsage", 0) or m["faithfulnessCheck"].get("callsWithoutUsage", 0))


# ----------------------------------------------------------------------------- spend

def spend(args: argparse.Namespace) -> None:
    prices = load_prices(args.prices)["models"]
    plans = [load(p) for p in args.plans]
    budgets = dict(b.split("=", 1) for b in args.budget or [])
    providers: dict[str, dict] = {}
    done: dict[tuple, list[float]] = {}

    def of(provider: str) -> dict:
        return providers.setdefault(provider, {"billed": 0.0, "priced": 0, "unknown": [], "lower": 0})

    print(f"{'provider':<10} {'case':<10} {'cell':<52} {'run':<8} {'status':<8} "
          f"{'render $':>9} {'check $':>9} {'billed $':>9} {'uncached $':>10} {'s':>5}")
    for plan, cell, run, folder, result, record in all_runs(plans):
        provider, case = plan["_cells"][cell]["provider"], plan["case"]["size"]
        status = status_of(run, result)
        if record is None:
            of(provider)["unknown"].append(f"{plan['_stem']}/{cell}/{run}")
            print(f"{provider:<10} {case:<10} {cell:<52} {run:<8} {status:<8} {'no run record, cost unknown':>46}")
            continue
        c = phase_costs(prices, record)
        billed, uncached = c["renderBilledUsd"] + c["checkBilledUsd"], c["renderUncachedUsd"] + c["checkUncachedUsd"]
        total = of(provider)
        total["billed"] += billed
        total["priced"] += 1
        total["lower"] += lower_bound(record)
        if status in DRAWS:
            done.setdefault((plan["_stem"], cell), []).append(billed)
        mark = " (lower bound)" if lower_bound(record) else ""
        print(f"{provider:<10} {case:<10} {cell:<52} {run[:8]:<8} {status:<8} {c['renderBilledUsd']:>9.4f} "
              f"{c['checkBilledUsd']:>9.4f} {billed:>9.4f} {uncached:>10.4f} {record['metrics']['durationSeconds']:>5.0f}{mark}")

    # What the plans still owe: an optional cell counts once it has been started.
    owed: dict[str, dict] = {}
    for plan in plans:
        for name, cell in plan["_cells"].items():
            have = done.get((plan["_stem"], name), [])
            if cell.get("optional") and not have:
                continue
            pending = plan["repetitions"] - len(have)
            if pending <= 0:
                continue
            o = owed.setdefault(cell["provider"], {"runs": 0, "usd": 0.0, "blind": 0})
            o["runs"] += pending
            if have:
                o["usd"] += pending * statistics.median(have)
            else:
                o["blind"] += pending

    print()
    for provider in sorted(set(providers) | set(owed) | set(budgets)):
        t = providers.get(provider, {"billed": 0.0, "priced": 0, "unknown": [], "lower": 0})
        floor = " or more" if t["lower"] or t["unknown"] else ""
        print(f"{provider}: spent ${t['billed']:.4f}{floor} (billed, {t['priced']} priced runs)")
        if t["lower"]:
            print(f"  {t['lower']} of them had a call without usage: their cost is a lower bound")
        for name in t["unknown"]:
            print(f"  cost unknown, no run record: {name}")
        o = owed.get(provider)
        if o:
            blind = f", and {o['blind']} runs in cells without a figure yet" if o["blind"] else ""
            print(f"  still owed: {o['runs']} runs; ${o['usd']:.4f} for the {o['runs'] - o['blind']} whose cell has a run{blind}")
        if provider in budgets:
            budget = float(budgets[provider])
            after = f", ${budget - t['billed'] - o['usd']:.4f} after the owed runs with a figure" if o else ""
            print(f"  budget ${budget:.2f}: ${budget - t['billed']:.4f} left by the records{after}")


# ---------------------------------------------------------------------------- report

def text_measures(folder: Path) -> dict:
    """Length and entries of each audience's text, from the run's changelog.json.
    An entry is a top-level list item; an audience that did not render has no text."""
    path = folder / "changelog.json"
    renderings = json.loads(path.read_text(encoding="utf-8")).get("renderings", {}) if path.exists() else {}
    out = {}
    for audience in AUDIENCES:
        text = renderings.get(audience)
        out[f"{audience}Characters"] = len(text) if text is not None else None
        out[f"{audience}Words"] = len(text.split()) if text is not None else None
        out[f"{audience}Entries"] = sum(1 for line in text.splitlines() if line.startswith("- ")) if text is not None else None
    return out


def facts_hash(record: dict) -> str | None:
    facts = record.get("facts")
    if facts is None:
        return None
    return hashlib.sha256(json.dumps(facts, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()


def run_row(plan: dict, cell: str, run: str, folder: Path, result: dict, record: dict, prices: dict) -> dict:
    meta, m, prov = plan["_cells"][cell], record["metrics"], record["provenance"]
    base = row(cell, run, result, record, prices)
    # Which key a run spent on belongs to the run folder, not to an export that travels.
    base.pop("openaiKey", None)
    costs = {k: round(v, 6) for k, v in phase_costs(prices, record).items()}
    return {
        "case": plan["case"]["size"],
        "plan": plan["_stem"],
        "repository": plan["case"]["repository"],
        "provider": meta["provider"],
        "configuration": meta["configuration"],
        **base,
        **costs,
        "notRendered": ";".join(a["audience"] for a in record["audiences"] if not a["rendered"]),
        "costIsLowerBound": lower_bound(record),
        "renderCalls": m["rephrase"]["calls"],
        "checkCalls": m["faithfulnessCheck"]["calls"],
        "renderFailedCalls": m["rephrase"].get("failedCalls"),
        "checkFailedCalls": m["faithfulnessCheck"].get("failedCalls"),
        "checkReasoning": m["faithfulnessCheck"].get("reasoningTokens"),
        "promptHash": prov.get("promptHash"),
        "rangeFromCommit": (record.get("range") or {}).get("fromCommit"),
        "rangeToCommit": (record.get("range") or {}).get("toCommit"),
        "factsSha256": facts_hash(record),
        **text_measures(folder),
    }


def overlap(flags: list[dict], rendered: dict[tuple, int]) -> list[dict]:
    """For each audience and pull request a cell flagged: in how many of the draws that rendered that audience."""
    seen: dict[tuple, set] = {}
    for f in flags:
        seen.setdefault((f["case"], f["cell"], f["audience"], f["pullRequest"] or "none"), set()).add(f["run"])
    return [{"case": case, "cell": cell, "audience": audience, "pullRequest": pr,
             "flaggedInRuns": len(found), "runs": rendered[(case, cell, audience)]}
            for (case, cell, audience, pr), found in sorted(seen.items(), key=lambda kv: tuple(map(str, kv[0])))]


def write_csv(path: Path, rows: list[dict], fields: list[str] | None = None) -> None:
    """`fields` names the columns of a file that may have no row, so it still gets its header."""
    fields = fields or list(dict.fromkeys(k for r in rows for k in r if not k.startswith("_")))
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def report(args: argparse.Namespace) -> None:
    table = load_prices(args.prices)
    prices = table["models"]
    plans = [load(p) for p in args.plans]
    withheld = set(args.withhold or [])
    unknown = withheld - {p["_stem"] for p in plans}
    if unknown:
        sys.exit(f"--withhold names no plan of this comparison: {', '.join(sorted(unknown))}")

    rows, attempts, without_record, flags = [], {}, [], []
    for plan, cell, run, folder, result, record in all_runs(plans):
        key = (plan["case"]["size"], cell)
        attempts[key] = attempts.get(key, 0) + 1
        if record is None:
            without_record.append(f"{plan['_stem']}/{cell}/{run} ({status_of(run, result)})")
            continue
        rows.append(run_row(plan, cell, run, folder, result, record, prices))
        if rows[-1]["status"] in DRAWS:
            flags += [{"case": plan["case"]["size"], "cell": cell, "run": run, "checkedBy": checked_by(record["provenance"]),
                       "audience": a["audience"], "pullRequest": f.get("pullRequest"),
                       "text": "" if plan["_stem"] in withheld else f["text"]}
                      for a in record["audiences"] for f in a.get("flags", [])]
    if not rows:
        sys.exit("no run with a record yet")

    ok = [r for r in rows if r["status"] == "ok"]
    draws = [r for r in rows if r["status"] in DRAWS]
    rendered: dict[tuple, int] = {}
    for r in draws:
        for audience in AUDIENCES:
            if audience not in r["notRendered"].split(";"):
                rendered[(r["case"], r["cell"], audience)] = rendered.get((r["case"], r["cell"], audience), 0) + 1
    shared = overlap(flags, rendered)

    cells = []
    for plan in plans:
        for name, meta in plan["_cells"].items():
            case = plan["case"]["size"]
            mine = [r for r in ok if r["case"] == case and r["cell"] == name]
            drawn = [r for r in draws if r["case"] == case and r["cell"] == name]
            every = [r for r in rows if r["case"] == case and r["cell"] == name]
            if not every:
                continue
            keys = [o for o in shared if o["case"] == case and o["cell"] == name]
            cells.append({
                "case": case, "cell": name, "provider": meta["provider"], "configuration": meta["configuration"],
                # Joined over every run, so a cell whose setting was changed between runs shows both.
                **{k: " / ".join(sorted({str(r[k]) for r in every})) for k in ("model", "thinking", "checkModel", "checkThinking")},
                "draws": len(drawn), "runs": len(mine), "incomplete": len(drawn) - len(mine),
                "attempts": attempts[(case, name)],
                **{f"{a}NotRendered": sum(1 for r in drawn if a in r["notRendered"].split(";")) for a in AUDIENCES},
                "mismatches": sum(1 for r in every if r["status"] == "mismatch"),
                "failed": sum(1 for r in every if r["status"] == "failed"),
                **{f"{k}{s}": v for k in RUN_MEASURES for s, v in zip(("Median", "Min", "Max"), spread([r[k] for r in mine]))},
                **{f"{k}{s}": v for k in AUDIENCE_MEASURES for s, v in zip(("Median", "Min", "Max"), spread([r[k] for r in drawn]))},
                "lowerBoundRuns": sum(1 for r in mine if r["costIsLowerBound"]),
                "retries": sum(r["retries"] for r in drawn),
                "notEvaluated": sum(r["notEvaluated"] for r in drawn),
                "flagKeys": len(keys),
                "flagKeysInEveryRun": sum(1 for o in keys if o["flaggedInRuns"] == o["runs"]),
                "flagKeysInOneRun": sum(1 for o in keys if o["flaggedInRuns"] == 1),
                "_rows": mine, "_draws": drawn,
            })

    out = args.out or SWEEPS / f"{plans[0].get('comparison', plans[0]['_stem'])}-stats"
    out.mkdir(exist_ok=True)
    write_csv(out / "runs.csv", rows)
    write_csv(out / "cells.csv", cells)
    write_csv(out / "flags.csv", flags, ["case", "cell", "run", "checkedBy", "audience", "pullRequest", "text"])
    write_csv(out / "flag-overlap.csv", shared, ["case", "cell", "audience", "pullRequest", "flaggedInRuns", "runs"])

    def one(values: list) -> str:
        found = sorted({str(v) for v in values})
        return found[0] if len(found) == 1 else f"**{len(found)} different**: " + ", ".join(found)

    md = [f"# Comparison statistics: {plans[0].get('comparison', plans[0]['_stem'])}", "",
          "Generated by `tools/sweep_compare.py report` from the run records and each run's `changelog.json`; do not edit by hand.",
          f"Runs: {len(draws)} draws, {len(ok)} of them complete; {len(rows)} with a record, {sum(attempts.values())} attempts.",
          f"Prices: `{args.prices.name}`, as of {table['date']}, USD per 1M tokens, list price.",
          f"Price table confirmed: {table.get('confirmed', 'not stated')}.", "",
          "## How to read this", "",
          "A flag is what a checker reported about a text, not a confirmed error.",
          "Fewer flags do not mean a better text: a checker that reports less, or a text that says less, gives the same count.",
          "Every cell renders anew, so two cells that share a rendering model do not share a text.",
          "A cell is one whole configuration, and its flags say nothing about the checking model alone.",
          "The models do not run at one thinking setting: each runs at the lowest it accepts, named with every cell below.",
          "Cost compares cells on *uncached* (every input token at the full rate); *billed* applies the cache as it fell.",
          "An incomplete run is a draw in which every model call was answered and Chartula still refused an audience's text, "
          "for example because it left out a fact. It is not repeated, and counts as what the configuration did.",
          "Cost and duration are the median of a cell's complete runs, with min-max in brackets when they differ: "
          "a run that lost an audience skipped that audience's check.",
          "Flags and lengths of one audience are over every draw in which that audience rendered.",
          "Nothing here says which text is better; that is judged separately, from the texts kept with every run.", "",
          "## Were the runs made under the same conditions", "",
          f"- Chartula: {one([r['toolVersion'] for r in rows])}",
          f"- Prompt: {one([r['promptHash'] for r in rows])}",
          f"- Fact base depth: {one([r['factBaseDepth'] for r in rows])}; thorough check: {one([r['thoroughCheck'] for r in rows])}"]
    for plan in plans:
        mine = [r for r in rows if r["plan"] == plan["_stem"]]
        if not mine:
            continue
        base_path = plan["_sweep"] / "_baseline" / "baseline.json"
        base = json.loads(base_path.read_text(encoding="utf-8")) if base_path.exists() else None
        counted = "no baseline"
        if base:
            same = all(r["facts"] == base["release"]["facts"] for r in mine)
            counted = f"baseline of {base['recordedAt']}, {base['release']['facts']} facts, " + \
                      ("every run counts the same" if same else "**runs count another number of facts**")
        md.append(f"- {plan['case']['size']} (`{plan['_stem']}`): facts {one([r['factsSha256'][:12] for r in mine])}; "
                  f"range to {one([str(r['rangeToCommit'])[:9] for r in mine])}; {counted}")
    if without_record:
        md += ["", f"Attempts without a run record, cost unknown: {', '.join(without_record)}."]

    for plan in plans:
        case = plan["case"]
        mine = [c for c in cells if c["case"] == case["size"]]
        if not mine:
            continue
        why = case["why"]
        if plan["_stem"] in withheld:
            why = (f"{case['repository']} is private. {case['pullRequests']} pull requests; its run folders are not in this "
                   "repository, and the text of its flags is left out of `flags.csv`. The figures are complete.")
        md += ["", f"## {case['size'].capitalize()}: {case['repository']} {case['range']}", "", why, "",
               "| configuration | render (thinking) | check (thinking) | draws: complete + incomplete / attempts "
               "| not rendered: technical, customer | cost uncached $ | rendering $ | check $ "
               "| cost billed $ | duration s | rendering s | check s | flags / complete run | technical | customer "
               "| flagged in every draw / at all | not evaluated | retries "
               "| technical: characters, entries | customer: characters, entries |",
               "|" + "---|" * 20]
        for c in mine:
            rs, ds = c["_rows"], c["_draws"]
            g = lambda k, d=0: fmt([r[k] for r in rs], d)  # noqa: E731
            a = lambda k: fmt([r[k] for r in ds])  # noqa: E731
            bound = f" (lower bound in {c['lowerBoundRuns']})" if c["lowerBoundRuns"] else ""
            odd = "".join(f", {c[k]} {k}" for k in ("mismatches", "failed") if c[k])
            md.append(f"| {c['provider']} {c['configuration']} | {c['model']} ({c['thinking']}) | {c['checkModel']} ({c['checkThinking']}) | "
                      f"{c['runs']} + {c['incomplete']} / {c['attempts']}{odd} | "
                      f"{c['technicalNotRendered']} of {c['draws']}, {c['customerNotRendered']} of {c['draws']} | "
                      f"{g('uncachedUsd', 4)}{bound} | {g('renderUncachedUsd', 4)} | "
                      f"{g('checkUncachedUsd', 4)} | {g('billedUsd', 4)} | {g('durationSeconds')} | {g('renderSeconds')} | "
                      f"{g('checkSeconds')} | {g('flags')} | {a('flagsTechnical')} | {a('flagsCustomer')} | "
                      f"{c['flagKeysInEveryRun']} / {c['flagKeys']} | {c['notEvaluated']} | {c['retries']} | "
                      f"{a('technicalCharacters')}, {a('technicalEntries')} | "
                      f"{a('customerCharacters')}, {a('customerEntries')} |")
    md += ["", "## Files", "",
           "- `runs.csv`: one row per run with a record, every figure the tables use, cost and duration by phase.",
           "- `cells.csv`: the per-cell medians and ranges.",
           "- `flags.csv`: one row per flag, with its audience, pull request, checker and text.",
           "- `flag-overlap.csv`: for each audience and pull request a cell flagged, in how many of the draws that rendered that audience.",
           "- The texts, facts, logs and run records stay in `sweeps/<plan>/<cell>/run-<n>/`.", ""]
    (out / "report.md").write_text("\n".join(md), encoding="utf-8")
    print(f"wrote {out}/: report.md, runs.csv, cells.csv, flags.csv, flag-overlap.csv")
    print(f"{len(draws)} draws ({len(ok)} complete) in {len(cells)} cells, {sum(attempts.values())} attempts, {len(flags)} flags")


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    s = sub.add_parser("spend", help="what the runs so far were billed, per provider, and what is still owed")
    s.add_argument("prices", type=Path, help="a price table, e.g. sweeps/prices-2026-10-09.json")
    s.add_argument("plans", type=Path, nargs="+", help="the comparison's plans, e.g. sweeps/cmp-*.json")
    s.add_argument("--budget", action="append", metavar="PROVIDER=USD", help="what may be spent on a provider; may be given per provider")
    s.set_defaults(run=spend)
    r = sub.add_parser("report", help="statistics and raw CSV over every plan of the comparison")
    r.add_argument("prices", type=Path, help="a price table, e.g. sweeps/prices-2026-10-09.json")
    r.add_argument("plans", type=Path, nargs="+", help="the comparison's plans, e.g. sweeps/cmp-*.json")
    r.add_argument("--out", type=Path, help="where to write; default: sweeps/<comparison>-stats")
    r.add_argument("--withhold", action="append", metavar="PLAN",
                   help="a plan on a private repository, by file name without .json: its flag texts and description are left out")
    r.set_defaults(run=report)
    args = parser.parse_args()
    args.run(args)


if __name__ == "__main__":
    main()
