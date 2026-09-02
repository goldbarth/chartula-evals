# How the loop works

What this measures, what may be changed when, and where each kind of writing
goes. Written so the state of the work can be checked rather than remembered.

## What is being measured

Whether a model applying `rubric/{audience}.md` reaches the verdicts a person
reached applying the same rubric. Not whether the changelog is good - that is
what the rubric is for. Not whether the facts are right - that is the
faithfulness check inside Chartula.

One audience at a time. `customer` is the one that is written and labelled;
every path below takes the audience as a segment, and every script takes it as
`--audience`, defaulting to `customer`.

Two sides, and both are judgements:

- **Labels** in `labels/{audience}/` - a person's verdict per axis per entry,
  with the passage it points at. `items.csv` holds one row per
  (run, item, axis), `runs.csv` one per (run, axis).
- **Judge runs** in `judge/results/{audience}/` - a model's verdict on the same
  entries, one axis per call, produced by `run_labelled.py`.

## The one invariant

A label and a judge verdict are comparable only if both were made against the
**same version of that axis**. Otherwise the difference between two rubrics is
being reported as disagreement between a person and a model.

The rubric is read from `rubric/{audience}.md` in the working tree - the
section for the axis, verbatim, plus the `Units` section. No copies, nothing
frozen. Which is why changing an axis changes what every future run is judged
against.

Which version a column was read against is the `rubric_commit` on that column's
own rows. It is per row on purpose: one file date would mark every other column
as freshly checked the moment a note was written about one of them.

    python3 judge/status.py

The runners in this folder call the API and want the interpreter the SDK is
installed on - `.venv/bin/python3 judge/run_labelled.py ...`, or the virtualenv
activated. Everything that only reads the files, `status.py` and
`tools/labels.py`, runs on a plain `python3`.

That prints, per axis, when its section last changed and whether the labels are
older than it. `run_labelled.py` refuses to judge an axis whose labels are
older, unless `--allow-stale` is passed and the reason is recorded.

## The four moves

Everything done here is one of these, and each has a defined effect on the
invariant.

| Move | Costs | Effect |
|------|-------|--------|
| **Judge an axis** - `run_labelled.py --axis X` | money | Produces a number. Requires the axis to be non-stale. |
| **Change an axis** - edit its section in the rubric | nothing | Makes that axis stale. Its column has to be re-passed before it can be judged again. |
| **Re-pass a column** - re-read the entries against the current axis text | time | Clears staleness for that axis. Only that column is touched. |
| **Record a decision** - a line in the friction log or the Open list | nothing | Changes no verdict and makes nothing stale. |

Two rules that follow from the table and are worth stating on their own:

*A change that makes an axis more permissive can only turn a fail into a pass.*
So the re-pass after such a change goes through the fails of that column, not
through all of it. A stricter change is the other way round.

*A dispute is not a reason to change an axis.* Record it first, decide it
deliberately, and change the axis only when the decision is made - because the
change costs a re-pass of that column.

## Where each thing is written

| What | Where |
|------|-------|
| What an axis may be at all | `rubric/how-a-rubric-is-built.md` |
| A rule | `rubric/{audience}.md`, in the axis it belongs to |
| A form rule - headings, groups, entry shape | `docs/output-format.md`; the rubric points at it |
| A verdict by a person on an entry | a row in `labels/{audience}/items.csv` |
| A verdict by a person on a run | a row in `labels/{audience}/runs.csv` |
| A change with no entry at all | `labels/{audience}/missing.md` - the other half of A1 |
| Which axis version a column was read against | the `rubric_commit` of that column's rows |
| Why a verdict was hard, or an axis unclear | `labels/{audience}/friction-log.md` |
| What is shared by every audience | `labels/how-to-label.md` |
| A decision not yet taken | the Open list at the end of the rubric |
| A judge's verdicts | `judge/results/{audience}/*.json`, written by the runner, never edited |
| A disagreement between judge and label | `labels/{audience}/friction-log.md`, naming the result file it came from |

The friction log is the right home for a judge disagreement: it is the same
species of finding as a person hesitating - the rubric did not decide the case
on its own. It gets the axis, the entries, and how it was resolved.

## Worked example: the dispute over `o5-17` on C4

The judge passed an entry that says a setting lives "via configuration" and in
"an environment variable"; the label failed it, because C4 asks for the setting
by its plain name, the command, or the place, and a kind of place is not a
place.

The move order is:

1. **Record it.** A friction log row: axis C4, entry `o5-17`, what was unclear,
   naming `results/customer/labelled-claude-sonnet-5-2026-08-31T1552.json`.
   Nothing is stale yet and nothing has to be re-run.
2. **Decide it**, in your own time. Either the label stands - then C4 gains a
   sentence saying a category is not a place - or the judge is right and the
   label changes.
3. If the decision **changes the axis**, C4 becomes stale. Re-pass the C4
   column: the change is stricter, so it is the passes that need review, and
   `status.py` will show C4 as comparable again once the `rubric_commit` on the
   C4 rows names the commit that changed it.
4. If the decision **changes only labels**, edit those rows and note it. The
   axis is untouched, nothing becomes stale.
5. **Judge C4 again** and compare with the previous result file. Both carry the
   commit they ran at.

The same order applies to the two entries the judge answered `n/a` on, `s5-06`
and `s5-14`, and it has since run half its course. The labels moved to `n/a`
too, in the re-pass against `57f2900`, so the disagreement is closed and the
question that produced it is not: C4 rule 1 asks whether the *change* requires
anything of the reader, and both entries describe a change that needs a
credential the entry never names. The re-pass argued from the entry instead,
which announces no requirement. Both C4 rows of the friction log say so - the
one in the re-pass table and the one under *From judge runs* - and until it is
decided, the verdicts rest on a rule nobody has written. That is the correct
price of an undecided rule, not a defect, and it is the Open list that the
decision belongs in once it is taken.

## The order of the work from here

1. Judge the axes that are already comparable, one at a time, cheapest first.
2. For each result: record the disagreements in the friction log, decide what
   they mean, change the axis or the labels, re-pass what that made stale,
   judge again.
3. Repeat until an axis is stable - the disagreements that remain are decisions
   taken deliberately, not rules nobody wrote down.
4. When every axis has a number that holds, run the same set against a cheaper
   model. That answers the question the repository exists for: whether the
   cheap end can be trusted with this rendering.
5. The three unlabelled runs in `test-runs/` stay unlabelled by hand. They are
   the held-out set: once a judge is trusted, it labels them, and a sample is
   checked against a person.

## What "done" looks like

- Every axis non-stale, with an agreement figure and a caught figure from a run
  whose provenance is recorded.
- Every remaining disagreement traceable to a decision written in the friction
  log or the Open list.
- One cheap-model run against the same set, comparable with the calibration
  model's.
- The held-out runs judged by the model, spot-checked by hand.
