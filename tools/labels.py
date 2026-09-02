#!/usr/bin/env python3
"""The label tables: check them, derive what is derivable, work a column.

Labelling is one person reading one axis down a whole run and writing a verdict
per entry. The tables that hold the result are wider than that: six rows per
item, three files that have to agree, and a rendering that has to be kept open
beside them. Everything here exists so that the hand only writes the verdict
and the reason, and nothing else has to be remembered.

    python3 tools/labels.py check                    # is anything missing or contradictory
    python3 tools/labels.py sync                     # rewrite what is derived from the verdicts
    python3 tools/labels.py show --run sonnet-5-out  # the run, its entries and its verdicts
    python3 tools/labels.py column --axis C3         # one axis out as a worksheet
    python3 tools/labels.py column --axis C3 --write # and back in

One audience at a time, `--audience customer` by default: a verdict belongs to
the rubric it was read against, and each audience has its own.
"""

from __future__ import annotations

import argparse
import csv
import importlib.util
import re
import shutil
import sys
import textwrap
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

_s = importlib.util.spec_from_file_location("sep", REPO / "judge" / "run_separation.py")
sep = importlib.util.module_from_spec(_s)
_s.loader.exec_module(sep)
_l = importlib.util.spec_from_file_location("lab", REPO / "judge" / "run_labelled.py")
lab = importlib.util.module_from_spec(_l)
_l.loader.exec_module(lab)

# Which table an axis is scored in. A1 is in both: an entry that should not be
# there is an item verdict, and a change carried by no entry at all is a
# document one, recorded in missing.md and summed up in the run row.
ITEM_AXES = ["A1", "C1", "C2", "C3", "C4", "C5"]
RUN_AXES = ["A1", "B1", "B2", "B3"]
# The axes an item's shippability is decided by - level C only, per how-to-label.md.
C_AXES = ["C1", "C2", "C3", "C4", "C5"]

VERDICTS = {"pass", "fail", "?", "n/a"}
ITEM_FIELDS = ["run", "item", "kind", "axis", "verdict", "rubric_commit", "note"]
RUN_FIELDS = ["run", "axis", "verdict", "rubric_commit", "note"]

# The row that carries a remark about the item or the run as a whole rather than
# about one axis. It holds no verdict and is scored by nothing.
WHOLE = "*"


# --------------------------------------------------------------------------- io


def read_rows(path: Path) -> list[dict]:
    """The rows of a label table, each with the physical line it starts on, so a
    complaint about one can be printed as `file:line` and clicked."""
    if not path.exists():
        return []
    out = []
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle)
        header = next(reader, None)
        if header is None:
            return []
        for values in reader:
            if not any(v.strip() for v in values):
                continue
            row = dict(zip(header, values))
            row["_line"] = reader.line_num
            out.append(row)
    return out


def write_rows(path: Path, fields: list[str], rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def header_of(path: Path) -> list[str]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8", newline="") as handle:
        return next(csv.reader(handle), [])


def rendering(run: str, audience: str) -> list[str]:
    """The entries of one run's rendering, in document order."""
    return sep.entries(lab.audience_section(run, audience))


def item_number(item: str) -> int:
    """The position an item id claims - `s5-07` is 7. Ids are prefix plus
    position in document order, counted from one."""
    match = re.search(r"(\d+)$", item)
    return int(match.group(1)) if match else 0


# ------------------------------------------------------------------- the tables


class Labels:
    """Both tables of one audience, read once and asked questions of."""

    def __init__(self, audience: str):
        self.audience = audience
        self.dir = sep.labels_dir(audience)
        self.item_rows = read_rows(self.dir / "items.csv")
        self.run_rows = read_rows(self.dir / "runs.csv")

    @property
    def runs(self) -> list[str]:
        """Every run that has item rows, in the order they first appear."""
        found = []
        for row in self.item_rows:
            if row["run"] not in found:
                found.append(row["run"])
        return found

    def items(self, run: str) -> list[str]:
        """The item ids of one run, in the order they appear in the table."""
        found = []
        for row in self.item_rows:
            if row["run"] == run and row["item"] not in found:
                found.append(row["item"])
        return found

    def kind(self, run: str, item: str) -> str:
        for row in self.item_rows:
            if row["run"] == run and row["item"] == item and row.get("kind"):
                return row["kind"]
        return ""

    def verdict(self, run: str, item: str, axis: str) -> str:
        for row in self.item_rows:
            if row["run"] == run and row["item"] == item and row["axis"] == axis:
                return row["verdict"].strip().lower()
        return ""

    def run_verdict(self, run: str, axis: str) -> str:
        for row in self.run_rows:
            if row["run"] == run and row["axis"] == axis:
                return row["verdict"].strip().lower()
        return ""

    def whole_note(self, run: str, item: str | None = None) -> str:
        """The note on the `*` row - a remark about the item, or about the run
        when no item is named. An axis whose reason lives there is explained,
        even though its own note column is empty."""
        rows = self.item_rows if item else self.run_rows
        for row in rows:
            if row["run"] == run and row["axis"] == WHOLE and (not item or row["item"] == item):
                return row["note"].strip()
        return ""

    def commits(self, axis: str, level: str) -> set[str]:
        """The rubric commits one axis carries in one of the two tables."""
        rows = self.item_rows if level == "item" else self.run_rows
        return {row["rubric_commit"].strip() for row in rows if row["axis"] == axis and row["rubric_commit"].strip()}

    def item_shippable(self, run: str, item: str) -> str:
        """`no` as soon as one C axis fails, `?` while one is unjudged, else
        `yes`. The rule is how-to-label.md's, and this is the only place it is
        applied - it used to be a column repeated on all six rows of an item."""
        verdicts = [self.verdict(run, item, axis) for axis in C_AXES]
        if "fail" in verdicts:
            return "no"
        if any(v in ("", "?") for v in verdicts):
            return "?"
        return "yes"

    def run_shippable(self, run: str) -> str:
        """A run ships only if no B axis fails and no item is unshippable."""
        document = [self.run_verdict(run, axis) for axis in RUN_AXES]
        items = [self.item_shippable(run, item) for item in self.items(run)]
        if "fail" in document or "no" in items:
            return "not shippable"
        if any(v in ("", "?") for v in document) or "?" in items:
            return "?"
        return "shippable"


# ------------------------------------------------------------------- the check


class Report:
    """Problems found, printed as `file:line  what` so the place can be opened."""

    def __init__(self) -> None:
        self.problems: list[tuple[str, str]] = []
        self.warnings: list[tuple[str, str]] = []

    def problem(self, where: str, text: str) -> None:
        self.problems.append((where, text))

    def warn(self, where: str, text: str) -> None:
        self.warnings.append((where, text))

    def at(self, path: Path, line: int | None = None) -> str:
        rel = path.relative_to(REPO)
        return f"{rel}:{line}" if line else str(rel)

    def print(self) -> int:
        width = max((len(w) for w, _ in self.problems + self.warnings), default=0)
        if self.problems:
            print("\nPROBLEMS - the tables contradict themselves or the runs")
            for where, text in self.problems:
                print(f"  {where:<{width}}  {text}")
        if self.warnings:
            print("\nWORTH A LOOK - not wrong, but unfinished or unexplained")
            for where, text in self.warnings:
                print(f"  {where:<{width}}  {text}")
        if not self.problems and not self.warnings:
            print("\nnothing to report - the tables agree with the runs and with each other")
        else:
            print(f"\n{len(self.problems)} problem(s), {len(self.warnings)} to look at")
        return 1 if self.problems else 0


def known_commit(commit: str) -> bool:
    return bool(sep._git("cat-file", "-t", commit)) if commit else False


def check(labels: Labels, report: Report) -> None:
    items_csv = labels.dir / "items.csv"
    runs_csv = labels.dir / "runs.csv"

    for path, expected in ((items_csv, ITEM_FIELDS), (runs_csv, RUN_FIELDS)):
        header = header_of(path)
        if not header:
            report.problem(report.at(path), "no table here")
            continue
        for extra in [f for f in header if f not in expected]:
            hint = " - derived from the verdicts now, run `labels.py sync --migrate`" if extra == "shippable" else ""
            report.problem(report.at(path, 1), f"column `{extra}` is not part of the table{hint}")
        for missing in [f for f in expected if f not in header]:
            report.problem(report.at(path, 1), f"column `{missing}` is missing")

    seen: set[tuple[str, str, str]] = set()
    for row in labels.item_rows:
        where = report.at(items_csv, row["_line"])
        run, item, axis = row["run"], row["item"], row["axis"]
        verdict = row["verdict"].strip().lower()

        if axis != WHOLE and axis not in ITEM_AXES:
            report.problem(where, f"{item}: `{axis}` is not an item axis")
            continue
        key = (run, item, axis)
        if key in seen:
            report.problem(where, f"{item} {axis}: a second row for an axis already scored")
        seen.add(key)

        if axis == WHOLE:
            if verdict:
                report.problem(where, f"{item}: a `*` row carries a verdict, and nothing scores it")
            continue
        if verdict not in VERDICTS:
            report.problem(where, f"{item} {axis}: `{row['verdict']}` is not a verdict")
        if verdict == "n/a" and axis not in sep.NA_AXES:
            report.problem(where, f"{item} {axis}: n/a, but only {', '.join(sorted(sep.NA_AXES))} defines one")
        if verdict in ("pass", "fail", "n/a") and not row["rubric_commit"].strip():
            report.problem(where, f"{item} {axis}: scored against no rubric_commit")
        elif row["rubric_commit"].strip() and not known_commit(row["rubric_commit"].strip()):
            report.problem(where, f"{item} {axis}: rubric_commit {row['rubric_commit']} is not a commit")
        if verdict == "fail" and not row["note"].strip() and not labels.whole_note(run, item):
            report.warn(where, f"{item} {axis}: fails, with no reason written")
        if verdict == "?":
            report.warn(where, f"{item} {axis}: not judged yet")

    for row in labels.run_rows:
        where = report.at(runs_csv, row["_line"])
        axis, verdict = row["axis"], row["verdict"].strip().lower()
        if axis != WHOLE and axis not in RUN_AXES:
            report.problem(where, f"{row['run']}: `{axis}` is not a document axis")
            continue
        if axis == WHOLE:
            continue
        if verdict not in VERDICTS:
            report.problem(where, f"{row['run']} {axis}: `{row['verdict']}` is not a verdict")
        if verdict in ("pass", "fail") and not row["rubric_commit"].strip():
            report.problem(where, f"{row['run']} {axis}: scored against no rubric_commit")
        if verdict == "fail" and not row["note"].strip() and not labels.whole_note(row["run"]):
            report.warn(where, f"{row['run']} {axis}: fails, with no reason written")

    for run in labels.runs:
        items = labels.items(run)
        try:
            found = rendering(run, labels.audience)
        except SystemExit as stop:
            report.problem(report.at(items_csv), str(stop))
            continue

        if len(found) != len(items):
            report.problem(
                report.at(items_csv),
                f"{run}: {len(found)} entries in the rendering, {len(items)} in the table",
            )
        prefixes = {item.rsplit("-", 1)[0] for item in items}
        if len(prefixes) > 1:
            report.problem(report.at(items_csv), f"{run}: two id prefixes in one run, {sorted(prefixes)}")
        for position, item in enumerate(items, start=1):
            if item_number(item) != position:
                report.problem(
                    report.at(items_csv),
                    f"{run}: {item} sits at position {position} - ids count document order from one",
                )
                break
        for item in items:
            kinds = {row["kind"].strip() for row in labels.item_rows if row["run"] == run and row["item"] == item}
            if len(kinds) > 1:
                report.problem(report.at(items_csv), f"{run}: {item} is {' and '.join(sorted(kinds))} on different rows")
            elif kinds == {""}:
                report.warn(report.at(items_csv), f"{run}: {item} has no kind set")
            missing = [axis for axis in ITEM_AXES if not labels.verdict(run, item, axis)]
            if missing:
                report.problem(report.at(items_csv), f"{run}: {item} has no row for {', '.join(missing)}")

        missing = [axis for axis in RUN_AXES if not labels.run_verdict(run, axis)]
        if missing:
            report.problem(report.at(runs_csv), f"{run}: no document row for {', '.join(missing)}")

    missing_md = labels.dir / "missing.md"
    if missing_md.exists():
        text = missing_md.read_text(encoding="utf-8")
        for run in labels.runs:
            if run not in text:
                report.warn(report.at(missing_md), f"{run}: labelled, but absent from the missing table")

    # A1 is scored in both tables, and a column is only as fresh as its oldest
    # row - so half of it re-read leaves the axis stale, and saying which half
    # is the difference between a hint and a puzzle.
    for axis in sorted(set(ITEM_AXES) | set(RUN_AXES)):
        if not sep.labels_are_older_than(axis, labels.audience):
            continue
        changed = sep.prompt_last_changed(axis, labels.audience)
        halves = [("item", "items.csv"), ("run", "runs.csv")]
        behind = []
        for level, name in halves:
            if axis not in (ITEM_AXES if level == "item" else RUN_AXES):
                continue
            oldest = sep._oldest(labels.commits(axis, level))
            if oldest != changed:
                flag = "" if level == "item" or axis not in ITEM_AXES else " --level run"
                behind.append(f"{name} reads against {oldest or 'nothing'} (`column --axis {axis}{flag}`)")
        current = [name for level, name in halves
                   if axis in (ITEM_AXES if level == "item" else RUN_AXES)
                   and sep._oldest(labels.commits(axis, level)) == changed]
        report.warn(
            report.at(labels.dir),
            f"{axis}: changed in {changed} - " + "; ".join(behind)
            + (f"; {', '.join(current)} is current" if current else ""),
        )

    for path, current, wanted in derived(labels):
        if current != wanted:
            report.problem(report.at(path), "derived from the verdicts and out of date - run `labels.py sync`")


# ----------------------------------------------------------------- the derived

# The generated table in what-is-labelled.md sits between these. Anything
# outside them is written by hand and is never touched.
MARK_START = "<!-- labels.py sync: runs labelled -->"
MARK_END = "<!-- labels.py sync: end -->"


def markdown_table(header: list[str], rows: list[list[str]]) -> str:
    widths = [max(len(str(cell)) for cell in column) for column in zip(header, *rows)] if rows else [len(h) for h in header]
    out = ["| " + " | ".join(h.ljust(w) for h, w in zip(header, widths)) + " |"]
    out.append("|" + "|".join("-" * (w + 2) for w in widths) + "|")
    for row in rows:
        out.append("| " + " | ".join(str(c).ljust(w) for c, w in zip(row, widths)) + " |")
    return "\n".join(out)


def run_summary_text(labels: Labels) -> str:
    lines = ["run,shippable"]
    lines += [f"{run},{labels.run_shippable(run)}" for run in labels.runs]
    return "\n".join(lines) + "\n"


def runs_labelled_text(labels: Labels) -> str:
    rows = [[run, str(len(labels.items(run))), labels.run_shippable(run)] for run in labels.runs]
    return markdown_table(["run", "items", "shippable"], rows)


def derived(labels: Labels) -> list[tuple[Path, str, str]]:
    """(file, what it says now, what the verdicts say it should say). Nothing in
    here is a judgement: every one of them is a function of the two tables."""
    out = []

    summary = labels.dir / "run-summary.csv"
    out.append((summary, summary.read_text(encoding="utf-8") if summary.exists() else "", run_summary_text(labels)))

    described = labels.dir / "what-is-labelled.md"
    if described.exists():
        text = described.read_text(encoding="utf-8")
        if MARK_START in text and MARK_END in text:
            start = text.index(MARK_START) + len(MARK_START)
            end = text.index(MARK_END)
            out.append((described, text[start:end], "\n\n" + runs_labelled_text(labels) + "\n\n"))
    return out


def sync(labels: Labels, migrate: bool) -> None:
    if migrate:
        header = header_of(labels.dir / "items.csv")
        if "shippable" in header:
            write_rows(labels.dir / "items.csv", ITEM_FIELDS, labels.item_rows)
            print(f"  {labels.dir.relative_to(REPO)}/items.csv  dropped `shippable` - derived now")
            labels.item_rows = read_rows(labels.dir / "items.csv")

    for path, current, wanted in derived(labels):
        if current == wanted:
            print(f"  {path.relative_to(REPO)}  already agrees")
            continue
        if path.suffix == ".csv":
            path.write_text(wanted, encoding="utf-8")
        else:
            text = path.read_text(encoding="utf-8")
            start = text.index(MARK_START) + len(MARK_START)
            end = text.index(MARK_END)
            path.write_text(text[:start] + wanted + text[end:], encoding="utf-8")
        print(f"  {path.relative_to(REPO)}  rewritten from the verdicts")


# ------------------------------------------------------------------- the views

MARKS = {"pass": ".", "fail": "F", "n/a": "-", "?": "?", "": "?"}


def entry_title(entry: str) -> str:
    """The one line an entry can be recognised by, without its markup."""
    first = " ".join(entry.split())
    first = re.sub(r"^-\s*", "", first)
    return first.replace("**", "")


def show(labels: Labels, want_run: str | None, full: bool, width: int) -> None:
    for run in labels.runs:
        if want_run and run != want_run:
            continue
        found = rendering(run, labels.audience)
        items = labels.items(run)
        document = "  ".join(f"{axis} {labels.run_verdict(run, axis) or '?'}" for axis in RUN_AXES)
        print(f"\n{run} - {len(found)} entries, {labels.run_shippable(run)}")
        print(f"  document: {document}")
        for row in labels.run_rows:
            if row["run"] == run and row["axis"] == WHOLE and row["note"].strip():
                print(textwrap.fill(row["note"].strip(), width, initial_indent="  note: ", subsequent_indent="        "))

        if full:
            for position, item in enumerate(items, start=1):
                entry = found[position - 1] if position <= len(found) else "(no entry at this position)"
                print(f"\n  {item}  {labels.kind(run, item)}  {labels.item_shippable(run, item)}")
                print(textwrap.fill(entry_title(entry), width - 4, initial_indent="    ", subsequent_indent="    "))
                for row in labels.item_rows:
                    if row["run"] != run or row["item"] != item:
                        continue
                    verdict = row["verdict"].strip() or " "
                    note = row["note"].strip()
                    head = f"    {row['axis']:<3} {verdict:<5}"
                    print(textwrap.fill(note, width, initial_indent=head, subsequent_indent=" " * len(head)) if note else head.rstrip())
            continue

        axes = " ".join(f"{axis:>2}" for axis in ITEM_AXES)
        print(f"\n  {'id':<8}{'kind':<9}{axes}  {'ship':<5} entry")
        for position, item in enumerate(items, start=1):
            marks = " ".join(f"{MARKS.get(labels.verdict(run, item, axis), '?'):>2}" for axis in ITEM_AXES)
            ship = labels.item_shippable(run, item)
            entry = found[position - 1] if position <= len(found) else "(no entry at this position)"
            used = 8 + 9 + len(marks) + 2 + 5 + 3
            title = entry_title(entry)
            room = max(20, width - used)
            print(f"  {item:<8}{labels.kind(run, item):<9}{marks}  {ship:<5} "
                  f"{title if len(title) <= room else title[: room - 3] + '...'}")
        print(f"\n  . pass   F fail   - n/a   ? not judged")


# --------------------------------------------------------------- one column out

WORKSHEET_HELP = """\
One axis, one verdict per block, in the order the entries appear in the run.
Fill in `verdict:` and `note:`; everything else in this file is ignored when it
is read back. Allowed verdicts: {verdicts}.

The reason quotes the passage the verdict points at, not an adjective
describing it - see labels/how-to-label.md.

Write it back with:

    python3 tools/labels.py column --axis {axis}{run_flag} --write

which is also what stamps rubric_commit {commit} onto the rows it touches.
"""


def worksheet_path(audience: str, axis: str, run: str | None, level: str) -> Path:
    stem = f"pass-{axis}" + (f"-{run}" if run else "") + ("-document" if level == "run" else "")
    return sep.labels_dir(audience) / f"{stem}.md"


def worksheet_blocks(labels: Labels, axis: str, want_run: str | None, level: str) -> list[tuple[str, str, str]]:
    """(id, what is being judged, which run it belongs to), in document order.

    At item level the id is the item and the subject is its entry. At document
    level there is one block per run and the subject is the whole rendering."""
    blocks = []
    for run in labels.runs:
        if want_run and run != want_run:
            continue
        if level == "run":
            blocks.append((run, lab.audience_section(run, labels.audience), run))
            continue
        found = rendering(run, labels.audience)
        for position, item in enumerate(labels.items(run), start=1):
            blocks.append((item, found[position - 1] if position <= len(found) else "", run))
    return blocks


def write_worksheet(labels: Labels, axis: str, want_run: str | None, level: str, path: Path) -> None:
    commit = sep.prompt_last_changed(axis, labels.audience)
    verdicts = ", ".join(sorted(VERDICTS if axis in sep.NA_AXES else VERDICTS - {"n/a"}))
    rows = labels.run_rows if level == "run" else labels.item_rows

    out = [f"# {axis} - {labels.audience}" + (f", {want_run}" if want_run else "") + "\n"]
    out.append(
        WORKSHEET_HELP.format(
            verdicts=verdicts,
            axis=axis,
            run_flag=f" --run {want_run}" if want_run else "",
            commit=commit or "(unknown)",
        )
    )
    out.append(f"The axis as it stands in {sep.rubric_rel(labels.audience)}:\n")
    out.append("\n".join("> " + line if line else ">" for line in sep.rubric_section(axis, labels.audience).splitlines()))

    seen_run = None
    for ident, subject, run in worksheet_blocks(labels, axis, want_run, level):
        if run != seen_run:
            out.append(f"\n# ---- {run} ----")
            seen_run = run
        kind = labels.kind(run, ident) if level == "item" else "document"
        verdict, note = "", ""
        for row in rows:
            same = row["run"] == run and row["axis"] == axis and (level == "run" or row["item"] == ident)
            if same:
                verdict, note = row["verdict"].strip(), row["note"].strip()
        out.append(f"\n## {ident}  ({kind})\n")
        out.append("\n".join("> " + line if line else ">" for line in subject.splitlines()) + "\n")
        out.append(f"verdict: {verdict}".rstrip())
        out.append(f"note: {note}".rstrip())

    path.write_text("\n".join(out).rstrip() + "\n", encoding="utf-8")
    print(f"{len(worksheet_blocks(labels, axis, want_run, level))} blocks written to {path.relative_to(REPO)}")
    print(f"axis last changed in {commit or '(unknown)'}; the column currently reads against "
          f"{sep.column_passed_against(axis, labels.audience) or 'nothing'}")


def read_worksheet(path: Path, expected: list[str]) -> dict[str, tuple[str, str]]:
    """The verdicts out of a worksheet, keyed by id.

    Only headings that name an id this pass asked about are read as blocks, so
    the quoted rubric and the quoted entries above them cannot be mistaken for
    one however they are marked up."""
    if not path.exists():
        sys.exit(f"no worksheet at {path.relative_to(REPO)} - write one first without --write")
    wanted = set(expected)
    found: dict[str, tuple[str, str]] = {}
    current, verdict, note = None, "", []
    for line in path.read_text(encoding="utf-8").splitlines():
        heading = re.match(r"^##\s+(\S+)", line)
        if heading and heading.group(1) in wanted:
            if current:
                found[current] = (verdict, " ".join(" ".join(note).split()))
            current, verdict, note = heading.group(1), "", []
            continue
        if current is None:
            continue
        if line.startswith("verdict:"):
            verdict = line[len("verdict:"):].strip().lower()
        elif line.startswith("note:"):
            note = [line[len("note:"):].strip()]
        elif note and not line.startswith(">") and not line.startswith("#"):
            note.append(line.strip())
    if current:
        found[current] = (verdict, " ".join(" ".join(note).split()))
    return found


def apply_worksheet(labels: Labels, axis: str, want_run: str | None, level: str, path: Path) -> int:
    blocks = worksheet_blocks(labels, axis, want_run, level)
    filled = read_worksheet(path, [ident for ident, _, _ in blocks])

    absent = [ident for ident, _, _ in blocks if ident not in filled]
    if absent:
        sys.exit(
            f"{len(absent)} of {len(blocks)} blocks are missing from the worksheet: "
            f"{', '.join(absent[:6])}{' ...' if len(absent) > 6 else ''}\n"
            "Nothing was written. A column is passed whole or not at all."
        )
    allowed = VERDICTS if axis in sep.NA_AXES else VERDICTS - {"n/a"}
    wrong = {ident: v for ident, (v, _) in filled.items() if v not in allowed}
    if wrong:
        sys.exit(
            "not a verdict this axis has: "
            + ", ".join(f"{ident} `{v}`" for ident, v in list(wrong.items())[:6])
            + f"\nAllowed: {', '.join(sorted(allowed))}. Nothing was written."
        )

    commit = sep.prompt_last_changed(axis, labels.audience)
    if not commit:
        sys.exit("cannot tell which commit last changed this axis - is this a git checkout?")

    rows = labels.run_rows if level == "run" else labels.item_rows
    by_run = {ident: run for ident, _, run in blocks}
    moved, changed = [], 0
    for row in rows:
        if row["axis"] != axis:
            continue
        ident = row["run"] if level == "run" else row["item"]
        if ident not in filled or by_run.get(ident) != row["run"]:
            continue
        verdict, note = filled[ident]
        was = row["verdict"].strip().lower()
        if was != verdict:
            moved.append((ident, was or "?", verdict))
        if (row["verdict"], row["note"], row["rubric_commit"]) != (verdict, note, commit):
            changed += 1
        row["verdict"], row["note"], row["rubric_commit"] = verdict, note, commit

    name = "runs.csv" if level == "run" else "items.csv"
    fields = RUN_FIELDS if level == "run" else ITEM_FIELDS
    write_rows(labels.dir / name, fields, rows)

    print(f"{changed} row(s) written to {(labels.dir / name).relative_to(REPO)}, rubric_commit {commit}")
    if moved:
        print(f"\n{len(moved)} verdict(s) moved:")
        for ident, was, now in moved:
            print(f"  {ident:<10} {was:<5} -> {now}")
    else:
        print("no verdict moved - the column now records that it was read against this rubric")
    return changed


# ------------------------------------------------------------------ a new run

def init(labels: Labels, run: str, prefix: str) -> None:
    """Empty rows for a run that has never been labelled - one per (item, axis)
    plus the document rows, every verdict `?`. The ids and their count come from
    the rendering, so the table cannot start out disagreeing with the run."""
    if run in labels.runs:
        sys.exit(f"{run} already has rows in items.csv")
    found = rendering(run, labels.audience)
    if not found:
        sys.exit(
            f"no entries found in the {labels.audience} rendering of {run}. Entries are read as "
            "`- ` bullets; a run that writes its items as headings and paragraphs instead has "
            "none by that reading, which is itself a finding at level B - lay the ids out by hand."
        )

    rows = list(labels.item_rows)
    for position in range(1, len(found) + 1):
        for axis in ITEM_AXES:
            rows.append({"run": run, "item": f"{prefix}-{position:02d}", "kind": "", "axis": axis, "verdict": "?"})
    write_rows(labels.dir / "items.csv", ITEM_FIELDS, rows)

    run_rows = list(labels.run_rows) + [{"run": run, "axis": axis, "verdict": "?"} for axis in RUN_AXES]
    write_rows(labels.dir / "runs.csv", RUN_FIELDS, run_rows)
    print(f"{len(found)} items ({prefix}-01 to {prefix}-{len(found):02d}) and {len(RUN_AXES)} document rows added")
    print("Set `kind` per item, then work one axis at a time with `labels.py column`.")


# ------------------------------------------------------------------------ main


def resolve_level(axis: str, level: str) -> str:
    if level != "auto":
        return level
    if axis in ITEM_AXES:
        return "item"
    if axis in RUN_AXES:
        return "run"
    sys.exit(f"{axis} is not an axis of either table")


def main() -> None:
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--audience", default=sep.DEFAULT_AUDIENCE)

    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("check", parents=[common], help="what is missing or contradictory")

    sync_parser = sub.add_parser("sync", parents=[common], help="rewrite what is derived from the verdicts")
    sync_parser.add_argument("--migrate", action="store_true", help="also drop columns that became derived")

    show_parser = sub.add_parser("show", parents=[common], help="a run, its entries and its verdicts")
    show_parser.add_argument("--run")
    show_parser.add_argument("--full", action="store_true", help="whole entries and every reason")

    column_parser = sub.add_parser("column", parents=[common], help="one axis out as a worksheet, and back")
    column_parser.add_argument("--axis", required=True)
    column_parser.add_argument("--run", help="one run; every labelled run by default")
    column_parser.add_argument("--level", default="auto", choices=["auto", "item", "run"])
    column_parser.add_argument("--write", action="store_true", help="read the worksheet back into the table")
    column_parser.add_argument("--out", help="where the worksheet lives")

    init_parser = sub.add_parser("init", parents=[common], help="empty rows for a run never labelled")
    init_parser.add_argument("--run", required=True)
    init_parser.add_argument("--prefix", required=True, help="the item id prefix, e.g. h45")

    args = parser.parse_args()
    if not sep.rubric_path(args.audience).exists():
        sys.exit(f"no rubric at {sep.rubric_rel(args.audience)}")
    labels = Labels(args.audience)
    width = min(shutil.get_terminal_size((100, 24)).columns, 110)

    if args.command == "check":
        print(f"CHECK {args.audience} - {len(labels.runs)} run(s), {sum(len(labels.items(r)) for r in labels.runs)} items")
        report = Report()
        check(labels, report)
        raise SystemExit(report.print())

    if args.command == "sync":
        print(f"SYNC {args.audience}")
        sync(labels, args.migrate)
        return

    if args.command == "show":
        if args.run and args.run not in labels.runs:
            sys.exit(f"{args.run} has no labels - {', '.join(labels.runs)}")
        show(labels, args.run, args.full, width)
        return

    if args.command == "init":
        init(labels, args.run, args.prefix)
        return

    axis = args.axis.upper()
    level = resolve_level(axis, args.level)
    if args.run and args.run not in labels.runs:
        sys.exit(f"{args.run} has no labels yet - run `labels.py init --run {args.run} --prefix ...` first")
    path = Path(args.out) if args.out else worksheet_path(args.audience, axis, args.run, level)

    if args.write:
        apply_worksheet(labels, axis, args.run, level, path)
        print("\nNow: python3 tools/labels.py sync && python3 tools/labels.py check")
        return
    write_worksheet(labels, axis, args.run, level, path)
    if axis == "A1" and level == "item":
        print("A1 has a second half at document level - `--level run`, read against missing.md.")


if __name__ == "__main__":
    main()
