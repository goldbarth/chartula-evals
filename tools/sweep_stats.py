#!/usr/bin/env python3
"""Read what a sweep cost and what it found from its run records.

    python3 tools/sweep_stats.py costs  sweeps/servicedesklite-v1.9.0 sweeps/prices-2026-09-25.json --budget 4.60
    python3 tools/sweep_stats.py report sweeps/servicedesklite-v1.9.0 sweeps/prices-2026-09-25.json

Every figure comes from the run records `tools/sweep.py` moved into
`sweeps/<plan>/<cell>/run-<n>/`; nothing is read from the terminal output.

`costs` keeps the spend in view while a sweep runs. `report` writes the statistics
next to the sweep, into `sweeps/<plan>-stats/`: the raw data as CSV (one row per
run, one per flag, one per cell, and a pull request by cell matrix), `report.md`
with the same figures as tables, and two charts for the axes.

**Two costs per run.** *Billed* prices cached input at the cached rate, which is
what the account pays at list price. *Uncached* prices every input token at the
full rate. The provider's cache depends on what ran just before, so billed cost
depends on run order; uncached cost does not, and cells are compared on it.

**Failed runs count.** A run kept as `run-<n>.failed-<time>` may have spent tokens
before it failed, so `costs` prices its record when there is one and lists it as
unknown when there is none, never as zero. `report` counts it as an attempt; its
figures stay out of the medians, which are over the runs that finished.

**A model missing from the price table stops the script**, rather than pricing it
at nothing: a figure that quietly left out a model would read as a real one.

**Who checked is named with every flag count.** A local cell's thorough check runs
on the rendering's endpoint, so its flags come from another checker than the
reference's and are not comparable with them as one column.

This makes no model call and needs nothing beyond the standard library.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import statistics
import sys
from pathlib import Path

PER = 1_000_000
THINKING = ["disabled", "low", "medium", "high"]


def load_prices(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def price(prices: dict, model: str, usage: dict) -> tuple[float, float]:
    """Billed and uncached cost of one phase's calls, in USD."""
    if model not in prices:
        sys.exit(f"{model} is not in the price table")
    p = prices[model]
    total, cached, out = usage["inputTokens"], usage.get("cachedInputTokens", 0), usage["outputTokens"]
    billed = ((total - cached) * p["input"] + cached * p["cachedInput"] + out * p["output"]) / PER
    uncached = (total * p["input"] + out * p["output"]) / PER
    return billed, uncached


def runs(sweep: Path):
    """Every run folder, kept failures included, with its sweep result and run record."""
    for cell in sorted(p for p in sweep.iterdir() if p.is_dir()):
        for run in sorted(p for p in cell.iterdir() if p.is_dir() and p.name.startswith("run-")):
            marker = run / "sweep-run.json"
            result = json.loads(marker.read_text(encoding="utf-8")) if marker.exists() else {}
            records = sorted(run.glob("run-record-*.json"))
            record = json.loads(records[-1].read_text(encoding="utf-8")) if records else None
            yield cell.name, run.name, result, record


def run_cost(prices: dict, record: dict) -> tuple[float, float]:
    m, prov = record["metrics"], record["provenance"]
    billed, uncached = price(prices, prov["model"], m["rephrase"])
    if prov.get("thoroughCheck"):
        b, u = price(prices, prov["checkModel"], m["faithfulnessCheck"])
        billed, uncached = billed + b, uncached + u
    return billed, uncached


def costs(args: argparse.Namespace) -> None:
    prices = load_prices(args.prices)["models"]
    per_cell: dict[str, list[float]] = {}
    spent, unknown = 0.0, 0

    print(f"{'cell':<44} {'run':<22} {'status':<8} {'render in/cached/out':>22} "
          f"{'check in/cached/out':>22} {'billed $':>9} {'uncached $':>10} {'s':>6}")
    for cell, run, result, record in runs(args.sweep):
        # A folder without sweep-run.json is the run in progress, or one cut off mid-run.
        status = result.get("status", "failed" if ".failed-" in run else "running")
        if record is None:
            unknown += 1
            print(f"{cell:<44} {run:<22} {status:<8} {'no run record, cost unknown':>46}")
            continue

        m = record["metrics"]
        billed, uncached = run_cost(prices, record)
        lower_bound = m["rephrase"].get("callsWithoutUsage", 0) or m["faithfulnessCheck"].get("callsWithoutUsage", 0)
        spent += billed
        if status == "ok":
            per_cell.setdefault(cell, []).append(uncached)

        def phase(u: dict) -> str:
            return f"{u['inputTokens']}/{u.get('cachedInputTokens', 0)}/{u['outputTokens']}"

        mark = " (lower bound)" if lower_bound else ""
        print(f"{cell:<44} {run:<22} {status:<8} {phase(m['rephrase']):>22} {phase(m['faithfulnessCheck']):>22} "
              f"{billed:>9.4f} {uncached:>10.4f} {m['durationSeconds']:>6.0f}{mark}")

    print()
    print("uncached cost per ok run, by cell (median, min-max, n):")
    for cell, values in per_cell.items():
        print(f"  {cell:<44} {statistics.median(values):.4f}  {min(values):.4f}-{max(values):.4f}  n={len(values)}")

    print()
    print(f"spent (billed, all priced runs): ${spent:.4f}")
    if unknown:
        print(f"runs without a record, cost unknown: {unknown}")
    if args.budget is not None:
        print(f"budget ${args.budget:.2f}, left by the records: ${args.budget - spent:.4f}")


# ---------------------------------------------------------------------------- report

def short(model: str | None) -> str:
    """A model's name as the tables print it: the provider's prefix and Ollama's
    context variant are the same model to a reader."""
    if not model:
        return "-"
    name = model.replace("-ctx24k", "")
    return {"granite4.1-guardian:8b": "granite", "qwen3:14b": "qwen3"}.get(name, name)


def checked_by(prov: dict) -> str:
    return f"checked by {short(prov.get('checkModel'))}" if prov.get("thoroughCheck") else "no thorough check"


def row(cell: str, run: str, result: dict, record: dict, prices: dict) -> dict:
    """One run, flattened. Every column is read from the record or the sweep result."""
    prov, m = record["provenance"], record["metrics"]
    re, fc = m["rephrase"], m["faithfulnessCheck"]
    billed, uncached = run_cost(prices, record)
    flags = {a["audience"]: len(a["flags"]) for a in record["audiences"] if "flags" in a}
    return {
        "cell": cell,
        "run": run,
        "status": result.get("status", "failed" if ".failed-" in run else "running"),
        "startedAt": result.get("startedAt"),
        "toolVersion": prov.get("toolVersion"),
        "openaiKey": result.get("openaiKey"),
        "model": prov.get("model"),
        "thinking": prov.get("thinking"),
        "thoroughCheck": prov.get("thoroughCheck"),
        "checkModel": prov.get("checkModel") if prov.get("thoroughCheck") else None,
        "checkThinking": prov.get("checkThinking") if prov.get("thoroughCheck") else None,
        "checkedBy": checked_by(prov),
        "factBaseDepth": prov.get("factBaseDepth"),
        "facts": m["release"]["facts"],
        "renderInput": re["inputTokens"],
        "renderCached": re.get("cachedInputTokens", 0),
        "renderOutput": re["outputTokens"],
        "renderReasoning": re.get("reasoningTokens"),
        "checkInput": fc["inputTokens"],
        "checkCached": fc.get("cachedInputTokens", 0),
        "checkOutput": fc["outputTokens"],
        "inputTokens": re["inputTokens"] + fc["inputTokens"],
        "outputTokens": re["outputTokens"] + fc["outputTokens"],
        "callsWithoutUsage": re["callsWithoutUsage"] + fc["callsWithoutUsage"],
        "retries": (re.get("retries") or 0) + (fc.get("retries") or 0),
        "billedUsd": round(billed, 6),
        "uncachedUsd": round(uncached, 6),
        "durationSeconds": m["durationSeconds"],
        "renderSeconds": re["durationSeconds"],
        "checkSeconds": fc["durationSeconds"],
        "flags": sum(flags.values()),
        "flagsTechnical": flags.get("technical"),
        "flagsCustomer": flags.get("customer"),
        "ruleBasedFlags": m["ruleBasedCheck"]["flags"],
        "thoroughFlags": m["thoroughCheck"]["flags"],
        "notEvaluated": m["thoroughCheck"]["notEvaluated"],
        "failedAudiences": ";".join(a["audience"] for a in record["audiences"] if not a["rendered"]),
    }


def axis(first: dict) -> str:
    """Which question a cell answers, from what its runs were made with, not its name."""
    local = first["model"].startswith(("qwen3", "granite"))
    if local:
        return "local"
    if not first["thoroughCheck"] or first["factBaseDepth"] != "title-and-description":
        return "side"
    reference = first["checkModel"] == "gpt-6-sol" and first["checkThinking"] == "disabled"
    if reference and first["thinking"] == "disabled":
        return "A+B"
    return "A" if reference else "B"


def spread(values: list) -> tuple:
    values = [v for v in values if v is not None]
    if not values:
        return None, None, None
    return statistics.median(values), min(values), max(values)


def fmt(values: list, digits: int = 0, prefix: str = "") -> str:
    med, lo, hi = spread(values)
    if med is None:
        return "-"
    f = f"{{:,.{digits}f}}"
    if lo == hi:
        return prefix + f.format(med)
    return f"{prefix}{f.format(med)} ({f.format(lo)}-{f.format(hi)})"


def summarise(rows: list[dict]) -> list[dict]:
    cells: dict[str, list[dict]] = {}
    for r in rows:
        cells.setdefault(r["cell"], []).append(r)
    out = []
    for cell, all_runs in cells.items():
        ok = [r for r in all_runs if r["status"] == "ok"]
        if not ok:
            continue
        first = ok[0]
        col = lambda k: [r[k] for r in ok]  # noqa: E731
        med = lambda k: spread(col(k))  # noqa: E731
        out.append({
            "axis": axis(first),
            "cell": cell,
            "model": first["model"],
            "thinking": first["thinking"],
            "checkedBy": first["checkedBy"],
            "checkThinking": first["checkThinking"],
            "factBaseDepth": first["factBaseDepth"],
            "runs": len(ok),
            "attempts": len(all_runs),
            **{f"{k}{s}": v for k in ("uncachedUsd", "billedUsd", "inputTokens", "outputTokens", "renderReasoning",
                                      "durationSeconds", "flags", "flagsTechnical", "flagsCustomer")
               for s, v in zip(("Median", "Min", "Max"), med(k))},
            "notEvaluated": sum(col("notEvaluated")),
            "retries": sum(col("retries")),
            "_rows": ok,
        })
    order = {"A+B": 0, "A": 1, "B": 2, "side": 3, "local": 4}
    return sorted(out, key=lambda c: (order[c["axis"]], c["model"],
                                      THINKING.index(c["thinking"]) if c["thinking"] in THINKING else 9, c["cell"]))


def flag_rows(sweep: Path, rows: list[dict]) -> list[dict]:
    ok = {(r["cell"], r["run"]) for r in rows if r["status"] == "ok"}
    out = []
    for cell, run, result, record in runs(sweep):
        if (cell, run) not in ok:
            continue
        for a in record["audiences"]:
            for f in a.get("flags", []):
                out.append({"cell": cell, "run": run, "checkedBy": checked_by(record["provenance"]),
                            "audience": a["audience"], "pullRequest": f.get("pullRequest"), "text": f["text"]})
    return out


def write_csv(path: Path, rows: list[dict]) -> None:
    rows = [{k: v for k, v in r.items() if not k.startswith("_")} for r in rows]
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def pr_matrix(cells: list[dict], flags: list[dict]) -> tuple[list[int | str], dict]:
    """For each pull request and cell: in how many of the cell's finished runs it was flagged."""
    seen: dict[tuple, set] = {}
    for f in flags:
        seen.setdefault((f["pullRequest"] or "none", f["cell"]), set()).add(f["run"])
    prs = sorted({k[0] for k in seen}, key=lambda p: (p == "none", p if p != "none" else 0))
    return prs, {k: len(v) for k, v in seen.items()}


# ---- charts: static SVG, light and dark from the same tokens, native tooltips via <title>.
# Plain colours in class rules, not CSS variables, so renderers without var() (rsvg) draw them too.

STYLE = """<style>
  .viz { font-family: system-ui, -apple-system, "Segoe UI", sans-serif; }
  .bg { fill: #fcfcfb; } .t { fill: #0b0b0b; } .t2 { fill: #52514e; } .m { fill: #898781; }
  .grid { stroke: #e1e0d9; stroke-width: 1; } .base { stroke: #c3c2b7; stroke-width: 1; } .ring { stroke: #fcfcfb; }
  .s1 { stroke: #2a78d6; fill: #2a78d6; } .s2 { stroke: #eb6834; fill: #eb6834; }
  .l1 { stroke: #2a78d6; fill: none; } .l2 { stroke: #eb6834; fill: none; }
  @media (prefers-color-scheme: dark) {
    .bg { fill: #1a1a19; } .t { fill: #ffffff; } .t2 { fill: #c3c2b7; } .grid { stroke: #2c2c2a; }
    .base { stroke: #383835; } .ring { stroke: #1a1a19; }
    .s1 { stroke: #3987e5; fill: #3987e5; } .s2 { stroke: #d95926; fill: #d95926; }
    .l1 { stroke: #3987e5; } .l2 { stroke: #d95926; }
  }
</style>"""


def esc(s: str) -> str:
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def nice_ticks(hi: float) -> list[float]:
    """Four or five round ticks from zero past the largest value."""
    raw = hi / 4 if hi > 0 else 1
    exp = math.floor(math.log10(raw))
    for m in (1, 2, 2.5, 5, 10):
        step = m * 10 ** exp
        if step >= raw:
            break
    count = math.ceil(hi / step) if hi > 0 else 1
    return [round(i * step, 10) for i in range(count + 1)]


def chart_axis_a(cells: list[dict], path: Path) -> None:
    """Three small multiples over the thinking level, one measure each: never two
    scales on one axis. Dot = median of three runs, line = min to max."""
    a = [c for c in cells if c["axis"] in ("A", "A+B")]
    models = sorted({c["model"] for c in a}, key=lambda m: ("sol" in m, m))
    panels = [("uncachedUsd", "Cost per run, USD, list price, uncached", lambda v: f"{v:.2f}"),
              ("flags", "Flags per run (checked by gpt-6-sol)", lambda v: f"{v:g}"),
              ("durationSeconds", "Duration per run, seconds", lambda v: f"{v:g}")]
    W, H, pw, top, left, gap = 780, 340, 220, 96, 44, 40
    ph = 190
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" class="viz" role="img" '
             f'aria-labelledby="ta">{STYLE}<title id="ta">Axis A: render model and thinking level against cost, flags and duration</title>'
             f'<rect class="bg" width="{W}" height="{H}"/>',
             f'<text class="t" x="{left}" y="24" font-size="15" font-weight="600">Axis A - render model and thinking level</text>']
    # legend, identity never by colour alone: the marker shape differs too
    lx = left
    for i, m in enumerate(models):
        cls = f"s{i + 1}"
        mark = (f'<circle class="{cls}" cx="{lx + 5}" cy="46" r="5"/>' if i == 0
                else f'<rect class="{cls}" x="{lx}" y="41" width="10" height="10" rx="2"/>')
        parts.append(mark + f'<text class="t2" x="{lx + 16}" y="50" font-size="12">{esc(m)}</text>')
        lx += 130
    for p, (key, title, label) in enumerate(panels):
        x0 = left + p * (pw + gap)
        hi = max(c[f"{key}Max"] for c in a)
        tv = nice_ticks(hi)
        top_v = tv[-1]
        y = lambda v: top + ph - (v / top_v) * ph  # noqa: E731
        parts.append(f'<text class="t" x="{x0}" y="{top - 14}" font-size="12" font-weight="600">{esc(title)}</text>')
        for t in tv:
            parts.append(f'<line class="grid" x1="{x0}" x2="{x0 + pw}" y1="{y(t):.1f}" y2="{y(t):.1f}"/>'
                         f'<text class="m" x="{x0 - 6}" y="{y(t) + 4:.1f}" font-size="10" text-anchor="end">{label(t)}</text>')
        parts.append(f'<line class="base" x1="{x0}" x2="{x0 + pw}" y1="{y(0):.1f}" y2="{y(0):.1f}"/>')
        step = pw / len(THINKING)
        for j, th in enumerate(THINKING):
            parts.append(f'<text class="m" x="{x0 + step * (j + .5):.1f}" y="{top + ph + 16}" font-size="10" '
                         f'text-anchor="middle">{th}</text>')
        for i, m in enumerate(models):
            cls, off = f"s{i + 1}", (i - (len(models) - 1) / 2) * 12
            pts = []
            for j, th in enumerate(THINKING):
                c = next((c for c in a if c["model"] == m and c["thinking"] == th), None)
                if c is None:
                    continue
                cx = x0 + step * (j + .5) + off
                med, lo, hi_v = c[f"{key}Median"], c[f"{key}Min"], c[f"{key}Max"]
                pts.append((cx, y(med)))
                tip = f"{m}, thinking {th}: median {label(med)}, range {label(lo)}-{label(hi_v)}, n={c['runs']}"
                shape = (f'<circle class="{cls}" cx="{cx:.1f}" cy="{y(med):.1f}" r="4.5"/><circle class="ring" cx="{cx:.1f}" cy="{y(med):.1f}" r="5.5" fill="none" stroke-width="2"/>'
                         if i == 0 else
                         f'<rect class="{cls}" x="{cx - 4.5:.1f}" y="{y(med) - 4.5:.1f}" width="9" height="9" rx="2"/>'
                         f'<rect class="ring" x="{cx - 5.5:.1f}" y="{y(med) - 5.5:.1f}" width="11" height="11" rx="2.5" '
                         f'fill="none" stroke-width="2"/>')
                parts.append(f'<g><title>{esc(tip)}</title>'
                             f'<rect x="{cx - 9:.1f}" y="{y(hi_v) - 9:.1f}" width="18" height="{y(lo) - y(hi_v) + 18:.1f}" fill="transparent"/>'
                             f'<line class="{cls}" x1="{cx:.1f}" x2="{cx:.1f}" y1="{y(lo):.1f}" y2="{y(hi_v):.1f}" stroke-width="2" '
                             f'stroke-linecap="round"/>{shape}</g>')
            if len(pts) > 1:
                d = " ".join(f"{'M' if k == 0 else 'L'}{px:.1f},{py:.1f}" for k, (px, py) in enumerate(pts))
                parts.insert(len(parts) - len(pts), f'<path class="l{i + 1}" d="{d}" stroke-width="1.5" opacity=".55"/>')
    parts.append(f'<text class="m" x="{left}" y="{H - 10}" font-size="10">Dot or square: median of 3 runs. '
                 f'Vertical line: min to max. ServiceDeskLite v1.9.0 since v1.7.0, 18 facts, Chartula 0.1.0-preview.3.</text>')
    parts.append("</svg>")
    path.write_text("\n".join(parts) + "\n", encoding="utf-8")


def chart_axis_b(cells: list[dict], path: Path) -> None:
    """Render x check as a two-by-two grid of labelled cells. The value is written in
    every cell, so the fill only supports the reading and is never the sole carrier."""
    b = [c for c in cells if c["axis"] in ("B", "A+B")]
    renders = sorted({c["model"] for c in b}, key=lambda m: ("sol" in m, m))
    checks = sorted({c["checkedBy"].replace("checked by ", "") for c in b}, key=lambda m: ("sol" in m, m))
    ramp = ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95"]
    hi = max(c["flagsMedian"] for c in b) or 1
    W, cw, ch, left, top = 560, 190, 96, 150, 92
    H = top + ch * len(renders) + 62
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" class="viz" role="img" '
             f'aria-labelledby="tb">{STYLE}<title id="tb">Axis B: flags per run by render model and check model</title>'
             f'<rect class="bg" width="{W}" height="{H}"/>',
             f'<text class="t" x="20" y="24" font-size="15" font-weight="600">Axis B - does it depend on who checks?</text>',
             f'<text class="t2" x="20" y="44" font-size="12">Flags per run, median (min-max) of 3 runs; thinking disabled for both.</text>',
             f'<text class="t2" x="{left + cw * len(checks) / 2:.0f}" y="{top - 30}" font-size="12" text-anchor="middle">checked by</text>']
    for j, chk in enumerate(checks):
        parts.append(f'<text class="t" x="{left + cw * (j + .5):.0f}" y="{top - 10}" font-size="12" font-weight="600" '
                     f'text-anchor="middle">{esc(chk)}</text>')
    for i, rnd in enumerate(renders):
        parts.append(f'<text class="t2" x="{left - 12}" y="{top + ch * (i + .5) - 4:.0f}" font-size="11" text-anchor="end">rendered by</text>'
                     f'<text class="t" x="{left - 12}" y="{top + ch * (i + .5) + 12:.0f}" font-size="12" font-weight="600" '
                     f'text-anchor="end">{esc(rnd)}</text>')
        for j, chk in enumerate(checks):
            c = next((c for c in b if c["model"] == rnd and c["checkedBy"] == f"checked by {chk}"), None)
            x, yy = left + cw * j, top + ch * i
            if c is None:
                parts.append(f'<rect x="{x + 1}" y="{yy + 1}" width="{cw - 2}" height="{ch - 2}" rx="4" fill="none" '
                             f'class="base"/><text class="m" x="{x + cw / 2}" y="{yy + ch / 2}" font-size="11" '
                             f'text-anchor="middle">not run</text>')
                continue
            k = min(len(ramp) - 1, round(c["flagsMedian"] / hi * (len(ramp) - 1)))
            ink = "#ffffff" if k >= 4 else "#0b0b0b"
            self_check = chk == rnd
            tip = (f"{rnd} checked by {chk}: flags {fmt([r['flags'] for r in c['_rows']])}, technical "
                   f"{fmt([r['flagsTechnical'] for r in c['_rows']])}, customer {fmt([r['flagsCustomer'] for r in c['_rows']])}")
            parts.append(f'<g><title>{esc(tip)}</title><rect x="{x + 1}" y="{yy + 1}" width="{cw - 2}" height="{ch - 2}" rx="4" '
                         f'fill="{ramp[k]}"/>'
                         f'<text x="{x + cw / 2}" y="{yy + ch / 2 - 6}" font-size="20" font-weight="600" fill="{ink}" '
                         f'text-anchor="middle">{esc(fmt([r["flags"] for r in c["_rows"]]))}</text>'
                         f'<text x="{x + cw / 2}" y="{yy + ch / 2 + 14}" font-size="11" fill="{ink}" text-anchor="middle">'
                         f'technical {esc(fmt([r["flagsTechnical"] for r in c["_rows"]]))} · customer '
                         f'{esc(fmt([r["flagsCustomer"] for r in c["_rows"]]))}</text>'
                         + (f'<text x="{x + cw / 2}" y="{yy + ch - 10}" font-size="10" fill="{ink}" text-anchor="middle">'
                            f'checks itself</text>' if self_check else "") + "</g>")
    parts.append(f'<text class="m" x="20" y="{H - 14}" font-size="10">ServiceDeskLite v1.9.0 since v1.7.0, 18 facts, '
                 f'Chartula 0.1.0-preview.3.</text><text class="m" x="20" y="{H - 2}" font-size="10">'
                 f'The fill darkens with the median; the number is the value.</text></svg>')
    path.write_text("\n".join(parts) + "\n", encoding="utf-8")


def report(args: argparse.Namespace) -> None:
    table = load_prices(args.prices)
    prices = table["models"]
    all_runs = [(c, r, res, rec) for c, r, res, rec in runs(args.sweep)]
    rows = [row(c, r, res, rec, prices) for c, r, res, rec in all_runs if rec is not None]
    missing = [f"{c}/{r}" for c, r, res, rec in all_runs if rec is None]
    for c, r, res, rec in all_runs:
        if rec is None:
            rows.append({"cell": c, "run": r, "status": res.get("status", "failed")})
    cells = summarise(rows)
    # Attempts include failed folders that left no record.
    for cell in cells:
        cell["attempts"] = sum(1 for r in rows if r["cell"] == cell["cell"])
    flags = flag_rows(args.sweep, rows)
    prs, matrix = pr_matrix(cells, flags)

    out = args.out or args.sweep.with_name(args.sweep.name + "-stats")
    out.mkdir(exist_ok=True)
    write_csv(out / "runs.csv", [r for r in rows if "model" in r])
    write_csv(out / "flags.csv", flags)
    write_csv(out / "cells.csv", cells)
    write_csv(out / "flags-by-pr.csv", [{"pullRequest": p, **{c["cell"]: matrix.get((p, c["cell"]), 0) for c in cells}}
                                         for p in prs])
    chart_axis_a(cells, out / "axis-a.svg")
    chart_axis_b(cells, out / "axis-b.svg")

    versions = sorted({r["toolVersion"] for r in rows if "model" in r})
    ok_runs = sum(1 for r in rows if r.get("status") == "ok")
    md = [f"# Sweep statistics: {args.sweep.name}", "",
          "Generated by `tools/sweep_stats.py report` from the run records alone; do not edit by hand.",
          f"Chartula: {', '.join(versions)}.",
          f"Runs: {ok_runs} finished in {len(cells)} cells, {len(rows)} attempts.",
          f"Prices: `{args.prices.name}`, {table['source']}, as of {table['date']}, USD per 1M tokens, list price.",
          "Cost compares cells on *uncached* (every input token at the full rate); *billed* applies the cache as it fell.",
          "Every figure is the median of a cell's finished runs, with min-max in brackets when they differ.", ""]
    if missing:
        md += [f"Attempts without a run record: {', '.join(missing)}.", ""]
    md += ["## Cells", "",
           "| axis | cell | render | thinking | check | runs / attempts | cost uncached $ | cost billed $ | input tokens "
           "| output tokens | reasoning (render) | duration s | flags / run | technical | customer | not evaluated |",
           "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for c in cells:
        rs = c["_rows"]
        g = lambda k, d=0: fmt([r[k] for r in rs], d)  # noqa: E731
        check = c["checkedBy"] + (f", {c['checkThinking']}" if c["checkThinking"] else "")
        md.append(f"| {c['axis']} | `{c['cell']}` | {short(c['model'])} | {c['thinking']} | {check} | "
                  f"{c['runs']} / {c['attempts']} | {g('uncachedUsd', 4)} | {g('billedUsd', 4)} | {g('inputTokens')} | "
                  f"{g('outputTokens')} | {g('renderReasoning')} | {g('durationSeconds')} | {g('flags')} | "
                  f"{g('flagsTechnical')} | {g('flagsCustomer')} | {c['notEvaluated']} |")
    md += ["", "Side cells differ from `gpt-6-sol-disabled` in one setting each: thorough check off, or `factBase.depth: title-only`.",
           "Local cells check on their own endpoint (`ThoroughCheckModel` in Chartula), so their flags come from another checker.",
           "", "## Flags by pull request", "",
           "In how many of a cell's finished runs each pull request was flagged at least once.", ""]
    heads = [c["cell"] for c in cells]
    md.append("| PR | " + " | ".join(f"`{h}`" for h in heads) + " |")
    md.append("|---|" + "---|" * len(heads))
    for p in prs:
        md.append(f"| {('#' + str(p)) if p != 'none' else 'no PR'} | "
                  + " | ".join(str(matrix.get((p, h), 0) or "") for h in heads) + " |")
    md += ["", "## Files", "",
           "- `runs.csv`: one row per finished run, every figure the tables use.",
           "- `flags.csv`: one row per flag, with its audience, pull request, checker and text.",
           "- `cells.csv`: the per-cell medians and ranges.",
           "- `flags-by-pr.csv`: the table above.",
           "- `axis-a.svg`, `axis-b.svg`: the charts; hover a mark for its figures.", "",
           "![Axis A](axis-a.svg)", "", "![Axis B](axis-b.svg)", ""]
    (out / "report.md").write_text("\n".join(md), encoding="utf-8")
    print(f"wrote {out}/: report.md, runs.csv, flags.csv, cells.csv, flags-by-pr.csv, axis-a.svg, axis-b.svg")
    print(f"{ok_runs} finished runs in {len(cells)} cells, {len(rows)} attempts, {len(flags)} flags")


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    c = sub.add_parser("costs", help="per-run cost and the running spend")
    c.add_argument("sweep", type=Path, help="a sweep's result folder, e.g. sweeps/servicedesklite-v1.9.0")
    c.add_argument("prices", type=Path, help="a price table, e.g. sweeps/prices-2026-09-25.json")
    c.add_argument("--budget", type=float, help="the credit left before the sweep, in USD")
    c.set_defaults(run=costs)
    r = sub.add_parser("report", help="statistics, raw CSV and charts next to the sweep")
    r.add_argument("sweep", type=Path, help="a sweep's result folder, e.g. sweeps/servicedesklite-v1.9.0")
    r.add_argument("prices", type=Path, help="a price table, e.g. sweeps/prices-2026-09-25.json")
    r.add_argument("--out", type=Path, help="where to write; default: <sweep>-stats next to it")
    r.set_defaults(run=report)
    args = parser.parse_args()
    if not args.sweep.is_dir():
        sys.exit(f"{args.sweep} does not exist yet")
    args.run(args)


if __name__ == "__main__":
    main()
