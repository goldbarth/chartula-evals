# Labels

One folder per audience - [`customer/`](customer), plus `technical/` and
`product/` once those rubrics exist. Each holds `items.csv`, `runs.csv`,
`run-summary.csv`, `missing.md`, `friction-log.md` and a `what-is-labelled.md`
with the worked example for that audience. This file is what all of them share:
the rules a verdict is written under, and the pass they are written in.

Labelling is one person applying one axis of a rubric to one run, by hand. The
tables are the record of that. `tools/labels.py` keeps the tables consistent so
that the reading is the only thing left to do; it never decides a verdict.

## Before the first pass

Read, in this order:

1. `rubric/{audience}.md` - the axes themselves. Nothing below replaces reading
   the axis you are about to apply.
2. `docs/output-format.md` - the shape a rendering is built to. Several axes
   judge conformance to it rather than restating it.
3. `labels/{audience}/what-is-labelled.md` - the worked example, one entry
   scored on every axis with the reason spelled out.

`python3` and a git checkout are all `tools/labels.py` needs. No API key, and
no virtualenv - those are for the judge in `judge/`, whose runners want
`.venv/bin/python3`, not for labelling.

## A pass, start to finish

A pass is one axis, down one run or down all of them. That unit is not a
suggestion; see *Order of work* below.

**1. Find out where the work stands.**

    python3 judge/status.py             # what is labelled, which axes are stale
    python3 tools/labels.py check       # what is missing or contradictory
    python3 tools/labels.py show --run sonnet-5-out   # the run and its verdicts

`check` reports two kinds of thing. **Problems** mean the tables contradict
themselves or the runs - a missing axis row, a verdict that is not a verdict,
an id at the wrong position. **Worth a look** means unfinished rather than
wrong: an axis not judged yet, a `fail` with no reason, a column that was read
against an older rubric than the one in the tree.

**2. Cut the column out.**

    python3 tools/labels.py column --axis C3                     # every labelled run
    python3 tools/labels.py column --axis C3 --run sonnet-5-out  # one of them

This writes `labels/{audience}/pass-C3.md`: the axis as it currently stands in
the rubric, then one block per entry, in document order, each carrying the
entry itself and the verdict the table holds today. The worksheet is scratch
and is not committed.

**3. Fill it in.** One block at a time, top to bottom. Only `verdict:` and
`note:` are read back; everything else in the file is ignored, so the quoted
axis and the quoted entries can be annotated freely. A note may run over
several lines - it is folded into one when it is written back.

**4. Write it back.**

    python3 tools/labels.py column --axis C3 --write

It refuses unless every block carries a verdict the axis allows, and prints
which verdicts moved. It also stamps `rubric_commit` onto the rows it touched,
which is the record that *this* column was read against *this* version of the
axis - so run it only when you have actually read the column.

**5. Rewrite what follows from the verdicts, then check.**

    python3 tools/labels.py sync
    python3 tools/labels.py check

**6. Write down the friction.** Anything the axis did not decide on its own
goes into `friction-log.md` by hand, along with what moved and why, in the
re-pass table. A pass that moved nothing is a result too, and belongs there
just as much.

**7. Commit** the label tables, the friction log and the derived files
together. `pass-*.md` is ignored by git and does not go with them.

## A run nobody has labelled yet

    python3 tools/labels.py init --run haiku-4-5-out --prefix h45

Lays out one row per (item, axis) with every verdict `?`, taking the number of
items and their order from the rendering itself, so the table cannot start out
disagreeing with the run. Set `kind` per item by hand, then work axis by axis
as above. Entries are read as `- ` bullets; a run that writes its items as
headings and paragraphs has none by that reading, which is a finding at level B
and means the ids have to be laid out by hand.

`haiku-4-5-out`, `opus-4-8-out` and `opus-5-no-thinking-out` are **not** to be
labelled by hand. They are the held-out set: once a judge is trusted it labels
them, and a sample of that is checked against a person. Labelling them earlier
spends the only unseen data there is, and it cannot be got back.

## Values

`pass`, `fail`, `?` (not judged yet), `n/a` (the axis does not apply to this
entry). Only C4 defines `n/a`; C2 calls its not-applicable case a pass in as
many words, so `n/a` there would invent a third answer the rubric does not have.

**Item IDs.** Run prefix plus the position of the entry in the rendering, in
document order, counted from one: `s5-01`, `s5-02`.

## Aggregation

An item is `shippable` only if no C axis is `fail`. No weighting, no overall
impression. A single failed axis is enough.
A run is `shippable` only if no B axis is `fail` and no item is `not shippable`.

Neither is written down by hand. `run-summary.csv` and the table of runs in
`what-is-labelled.md` are computed from the verdicts by `labels.py sync`, and
`check` fails if they have drifted. The verdicts are the only place a
judgement is recorded.

## Order of work

1. One axis at a time, down the whole run, not one item at a time across all
   axes. Judging C1 for twenty-six items in a row compares the same question
   against itself; judging one item across five axes lets the first verdict
   colour the rest. `labels.py column` cuts the work into exactly this unit.
2. Items before the run. The document axes are only judgeable once the items
   are known, not the other way round.
3. The rubric is not edited during a pass. Friction goes into that audience's
   `friction-log.md` and is applied afterwards, in one go.

## Reasons

The note quotes the passage the verdict points at, not an adjective
describing it. `"the deeper (thorough) check"` is a reason. "too technical"
is not.

One reason per axis, written into the `note` column of that axis's own row in
`items.csv` / `runs.csv` - not one shared paragraph covering several axes.
Text that belongs to no single axis (an observation about the whole item, or
about the run as a whole) goes into a row with `axis` set to `*`.

A reason argues from the entry, and points at the axis rather than repeating
it. Neither a note nor the worked example in `what-is-labelled.md` restates a
rule or an example out of the rubric: the copy is what nobody re-reads when the
rubric changes. C4's n/a example was carried into the worked example word for
word, so one reading exists in three places and was checked in none: the rubric
was rewritten around it and both copies go on stating the rule the axis no
longer has. Recorded in `../docs/parked.md`, because repairing it edits an axis.

## What the tool does not do

It does not decide a verdict, and it does not read the rubric for you. It does
not write `missing.md` - what is absent from a rendering cannot be found in the
rendering, only against the fact base. It does not write the friction log. And
a `rubric_commit` stamp says a person read that column; nothing checks that
claim, so `--write` on a column you have not read is a lie the tables will
carry.

## The files

| file | written by | what it holds |
|------|------------|---------------|
| `items.csv` | hand, via `column` | one row per (run, item, axis) - level C, plus A1 for entries wrongly included |
| `runs.csv` | hand, via `column --level run` | one row per (run, axis) - the document axes |
| `missing.md` | hand | level A1's other half: changes with no entry at all |
| `friction-log.md` | hand | where the rubric did not decide a case on its own, and every re-pass |
| `run-summary.csv` | `labels.py sync` | shippable per run |
| `what-is-labelled.md` | hand, one table by `sync` | the worked example for that audience |
