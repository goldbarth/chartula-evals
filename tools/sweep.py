#!/usr/bin/env python3
"""Render one release many times over a plan of model settings, and keep every run.

    python3 tools/sweep.py sweeps/servicedesklite-v1.9.0.json --dry-run
    python3 tools/sweep.py sweeps/servicedesklite-v1.9.0.json
    python3 tools/sweep.py sweeps/servicedesklite-v1.9.0.json --only sol-disabled

A plan names a clone, the `chartula generate` arguments, how many repetitions, and
the cells: each cell is a set of `Chartula__...` environment variables. Chartula
reads those after `chartula.yaml`, so a cell overrides whatever the clone's file
says. Every `Chartula__` variable inherited from the shell is dropped first, so a
setting left in the terminal cannot leak into a cell unseen. The keys
(`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GITHUB_TOKEN`) are inherited as they are.

**Every run is kept.** Chartula writes `changelog.json`, `CHANGELOG.md`,
`release-<tag>.md` and a run record into the directory it runs in, and the next
run overwrites the first three. After each run they are moved to
`sweeps/<plan>/<cell>/run-<n>/`, together with the terminal output and a
`sweep-run.json` saying what was asked for. A tracked `CHANGELOG.md` is copied and
then restored with git, because Chartula prepends to it and the next run would
otherwise read a changelog that grew.

**Repetitions go round the cells**, not cell after cell: repetition 1 of every
cell, then repetition 2. A sweep stopped halfway still has every cell at the same
depth, rather than three runs of the first cells and none of the last.

**A finished run is skipped**, so a sweep that stopped is resumed by running it
again. A run is finished when its `sweep-run.json` exists and does not say
`failed`; a failed run is tried again, and its folder is kept as
`run-<n>.failed-<time>`.

**The record is checked against the cell.** The run record's provenance says
which model, thinking, check model and depth the run actually used. A cell whose
record says otherwise is marked `mismatch`, because a figure read from it would
belong to another cell.

The thorough check shares the rendering's provider and endpoint; only its model
and thinking are its own (`ThoroughCheckModel` in Chartula). A cell that renders
on a local endpoint therefore checks on it too.

This makes no model call itself, so it runs on a plain `python3`.
"""

from __future__ import annotations

import argparse
import itertools
import json
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SWEEPS = REPO / "sweeps"

PREFIX = "Chartula__"

# Which provenance field of the run record answers which setting.
# Provider is compared as written; thinking and depth are Chartula's canonical names.
PROVENANCE = {
    "Chartula__Llm__Provider": "provider",
    "Chartula__Llm__Model": "model",
    "Chartula__Llm__Thinking": "thinking",
    "Chartula__Faithfulness__Model": "checkModel",
    "Chartula__Faithfulness__Thinking": "checkThinking",
    "Chartula__Faithfulness__Thorough": "thoroughCheck",
    "Chartula__FactBase__Depth": "factBaseDepth",
}

# What one run leaves in the clone, besides its run record.
OUTPUTS = ["changelog.json", "CHANGELOG.md"]


def cells(plan: dict) -> list[dict]:
    """The plan's cells in order: listed ones as written, a grid as its product.
    A name that comes up twice is kept once, so two grids that overlap run it once."""
    out: dict[str, dict] = {}
    for entry in plan["cells"]:
        if "grid" in entry:
            keys = list(entry["grid"])
            for values in itertools.product(*(entry["grid"][k] for k in keys)):
                env = {**entry.get("env", {}), **dict(zip(keys, values))}
                # Chartula__Faithfulness__Model is {faithfulness_model} in a name template,
                # so a render model and a check model in one grid stay apart.
                name = entry["name"].format(**{placeholder(k): v for k, v in zip(keys, values)})
                out.setdefault(name, {"name": name, "env": env, "note": entry.get("note")})
        else:
            out.setdefault(entry["name"], {"name": entry["name"], "env": entry["env"], "note": entry.get("note")})
    for cell in out.values():
        bad = [k for k in cell["env"] if not k.startswith(PREFIX)]
        if bad:
            sys.exit(f"cell {cell['name']}: {', '.join(bad)} is not a {PREFIX} setting")
    return list(out.values())


def placeholder(key: str) -> str:
    return key[len(PREFIX):].replace("__", "_").lower()


def done(target: Path) -> bool:
    """A run is done once it has a result that is not a failure. A failed run is
    tried again on the next start, and its folder is kept beside the new one."""
    marker = target / "sweep-run.json"
    return marker.exists() and json.loads(marker.read_text(encoding="utf-8"))["status"] != "failed"


def environment(plan: dict, cell: dict) -> dict:
    env = {k: v for k, v in os.environ.items() if not k.startswith(PREFIX)}
    env.update({k: str(v) for k, v in plan.get("env", {}).items()})
    env.update({k: str(v) for k, v in cell["env"].items()})
    return env


def tracked(clone: Path, name: str) -> bool:
    return subprocess.run(
        ["git", "-C", str(clone), "ls-files", "--error-unmatch", name],
        capture_output=True,
    ).returncode == 0


def leftovers(clone: Path, tag: str) -> list[str]:
    """Outputs of an earlier run still in the clone. A run would overwrite them, and
    one that fails would leave them looking like its own."""
    found = [n for n in ["changelog.json", f"release-{tag}.md"] if (clone / n).exists()]
    if (clone / "CHANGELOG.md").exists() and tracked(clone, "CHANGELOG.md"):
        dirty = subprocess.run(
            ["git", "-C", str(clone), "status", "--porcelain", "--", "CHANGELOG.md"],
            capture_output=True, text=True,
        ).stdout.strip()
        if dirty:
            found.append("CHANGELOG.md (modified)")
    elif (clone / "CHANGELOG.md").exists():
        found.append("CHANGELOG.md (untracked)")
    return found


def collect(clone: Path, tag: str, target: Path, started: float) -> Path | None:
    """Move this run's outputs into its folder. Returns the run record, if one was written."""
    for name in OUTPUTS + [f"release-{tag}.md"]:
        source = clone / name
        if not source.exists():
            continue
        if name == "CHANGELOG.md" and tracked(clone, name):
            shutil.copy2(source, target / name)
            subprocess.run(["git", "-C", str(clone), "checkout", "--", name], check=True)
        else:
            shutil.move(str(source), target / name)

    records = sorted(
        p for p in (clone / "chartula-runs").glob("*.json") if p.stat().st_mtime >= started - 1
    )
    if len(records) > 1:
        print(f"    {len(records)} run records newer than this run; keeping all of them", file=sys.stderr)
    record = None
    for p in records:
        record = target / f"run-record-{p.name}"
        shutil.move(str(p), record)
    return record


def mismatches(record: Path | None, cell_env: dict, plan_env: dict) -> list[str]:
    if record is None:
        return ["no run record was written"]
    provenance = json.loads(record.read_text(encoding="utf-8")).get("provenance", {})
    asked = {**plan_env, **cell_env}
    out = []
    for key, field in PROVENANCE.items():
        if key not in asked:
            continue
        want, got = str(asked[key]).lower(), str(provenance.get(field)).lower()
        if want != got:
            out.append(f"{field}: asked {asked[key]}, recorded {provenance.get(field)}")
    return out


def key_suffix() -> str | None:
    """The last four characters of OPENAI_API_KEY, the part the provider's key list shows.
    Which key a run spent on is otherwise known only from memory, and the usage
    dashboard splits by key; four characters name the key without disclosing it."""
    key = os.environ.get("OPENAI_API_KEY")
    return f"...{key[-4:]}" if key else None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("plan", type=Path, help="a sweep plan, see sweeps/")
    parser.add_argument("--dry-run", action="store_true", help="list the runs, run nothing")
    parser.add_argument("--only", action="append", help="only this cell; may be given more than once")
    args = parser.parse_args()

    plan = json.loads(args.plan.read_text(encoding="utf-8"))
    clone = Path(os.path.expanduser(plan["clone"])).resolve()
    tag = plan["tag"]
    command = [plan.get("chartula", "chartula"), *plan["args"]]
    out_dir = SWEEPS / args.plan.stem
    todo = [c for c in cells(plan) if not args.only or c["name"] in args.only]
    if args.only and len(todo) != len(set(args.only)):
        known = {c["name"] for c in cells(plan)}
        sys.exit(f"no such cell: {', '.join(sorted(set(args.only) - known))}")

    binary = shutil.which(command[0])
    key = key_suffix()
    runs = [(n, c) for n in range(1, plan["repetitions"] + 1) for c in todo]
    pending = [(n, c) for n, c in runs if not done(out_dir / c["name"] / f"run-{n}")]

    print(f"plan      {args.plan}")
    print(f"clone     {clone}")
    print(f"chartula  {binary or 'NOT FOUND: ' + command[0]}")
    print(f"command   {' '.join(command)}")
    print(f"openai    {key or 'OPENAI_API_KEY not set'}")
    print(f"cells     {len(todo)}, repetitions {plan['repetitions']}: {len(runs)} runs, {len(pending)} not done")
    for cell in todo:
        note = f"   ({cell['note']})" if cell.get("note") else ""
        print(f"  {cell['name']}{note}")

    if args.dry_run:
        return
    if binary is None:
        sys.exit(f"{command[0]} is not on PATH")
    if not (clone / ".git").exists():
        sys.exit(f"{clone} is not a git checkout")
    left = leftovers(clone, tag)
    if left:
        sys.exit(f"{clone} still holds the outputs of an earlier run: {', '.join(left)}.\n"
                 "Move them away first; a run here would overwrite them.")

    versions: set[str] = set()
    for i, (n, cell) in enumerate(pending, start=1):
        target = out_dir / cell["name"] / f"run-{n}"
        if target.exists():
            target.rename(target.with_name(f"run-{n}.failed-{datetime.now():%Y%m%dT%H%M%S}"))
        target.mkdir(parents=True)
        print(f"[{i}/{len(pending)}] {cell['name']} run-{n}", flush=True)

        started = time.time()
        with open(target / "chartula.log", "w", encoding="utf-8") as log:
            code = subprocess.run(
                command, cwd=clone, env=environment(plan, cell), stdout=log, stderr=subprocess.STDOUT,
            ).returncode
        finished = time.time()

        record = collect(clone, tag, target, started)
        problems = mismatches(record, cell["env"], plan.get("env", {}))
        version = None
        if record is not None:
            version = json.loads(record.read_text(encoding="utf-8")).get("provenance", {}).get("toolVersion")
            versions.add(version)

        status = "failed" if code != 0 else "mismatch" if problems else "ok"
        (target / "sweep-run.json").write_text(json.dumps({
            "cell": cell["name"],
            "repetition": n,
            "status": status,
            "exitCode": code,
            "mismatches": problems,
            "settings": {**plan.get("env", {}), **cell["env"]},
            "command": command,
            "chartula": binary,
            "toolVersion": version,
            "openaiKey": key,
            "startedAt": datetime.fromtimestamp(started, timezone.utc).isoformat(timespec="seconds"),
            "seconds": round(finished - started, 1),
        }, indent=2) + "\n", encoding="utf-8")

        print(f"    {status}, exit {code}, {finished - started:.0f} s", flush=True)
        for problem in problems:
            print(f"    {problem}", flush=True)

    if len(versions) > 1:
        print(f"\nWARNING: the runs report {len(versions)} tool versions: {', '.join(sorted(map(str, versions)))}")


if __name__ == "__main__":
    main()
