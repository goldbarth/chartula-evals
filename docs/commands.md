# Every command

What each script is for, when you would run it, and what it needs. Nothing here
is a rule - the rules are in [`pipeline.md`](pipeline.md) and
[`../judge/how-the-loop-works.md`](../judge/how-the-loop-works.md). This is the
list you reach for when you know what you want and not what it is called.

**Two interpreters.** Anything that calls the API wants the one the SDK is
installed on: `.venv/bin/python3`, or the virtualenv activated. Everything that
only reads files runs on a plain `python3`. The table says which.

**Every script takes `--audience`**, defaulting to `customer` - the only
audience with a rubric. It is left out of the examples below.

---

## Where do I stand

| | |
|---|---|
| `python3 judge/status.py` | what is labelled, which axes are comparable right now, which need a re-pass first, and what has been spent |
| `python3 judge/status.py --verify` | which result files were produced against the criterion in the tree. Add a filename to check one |
| `python3 tools/labels.py check` | what is missing or contradictory in the label tables. The closest thing here to a test suite |

## Labelling

One axis down a whole run, never one item across all axes. `column` cuts the
work into exactly that unit.

| | |
|---|---|
| `python3 tools/labels.py column --axis C3` | writes `labels/customer/pass-C3.md`: the axis, then one block per entry with the verdict the table holds today |
| `python3 tools/labels.py column --axis C3 --run sonnet-5-out` | the same for one run only |
| `python3 tools/labels.py column --axis B1 --level run` | the document axes, which have one row per run rather than per entry |
| `python3 tools/labels.py column --axis C3 --write` | reads the worksheet back. Only `verdict:` and `note:` are read; everything else is ignored |
| `python3 tools/labels.py sync` | rewrites everything derived from the verdicts: `run-summary.csv` and one table in `what-is-labelled.md` |
| `python3 tools/labels.py show --run sonnet-5-out` | a run, its entries and its verdicts. `--full` prints the entry text too |
| `python3 tools/labels.py init --run haiku-4-5-out --prefix h45` | empty rows for a run nobody has labelled, one per (item, axis), every verdict `?`, taken from the rendering itself |

`--write` stamps `rubric_commit` onto the rows it touches, which is the claim
that a person read that column. Nothing verifies it. Do not run it on a column
you have not read.

The worksheets `labels/*/pass-*.md` are scratch and are not committed.

## The spot check - stage 6

Every five turns of stage 5, one person reads ten entries against the judge's
verdicts on them. Neither half needs an API key.

| | |
|---|---|
| `python3 tools/spot_check.py --run sonnet-5-rules-out` | cuts `labels/customer/spot-check-<date>.md`: ten entries, the judge's verdict on each axis, and an empty line for yours |
| `python3 tools/spot_check.py --run <run> --passed 7 --failed 3` | a different mix. Seven let through and three failed by default, weighted that way because a judge that passes a bad entry costs the release |
| `python3 tools/spot_check.py --read labels/customer/spot-check-<date>.md` | reads it back: agreements, and the entries the judge let through that you failed. That figure is the instrument target |

The worksheet is scratch and is not committed. Nothing it holds goes into
`items.csv` and no `rubric_commit` is stamped: labelling asks what the verdict
is, this asks whether the judge still reaches it. The outcome goes into
`docs/measurements.md` as a spot-check section, which is also the mark stage 6
counts turns from.

## What changed in an axis

| | |
|---|---|
| `python3 judge/axis_diff.py C1` | what changed in that axis since the column was passed against it |
| `python3 judge/axis_diff.py C1 --full` | and the section as it now stands |
| `python3 judge/axis_diff.py C1 --since 57f2900` | from a commit you name instead |

## Judging - these cost money

`--dry-run` uses the free token-counting endpoint and writes nothing. Run it
first. Both runners refuse to start on an uncommitted rubric.

| | |
|---|---|
| `.venv/bin/python3 judge/run_separation.py --dry-run` | the estimate for the separation run |
| `.venv/bin/python3 judge/run_separation.py --model claude-sonnet-5` | five constructed documents, one axis broken in each, 40 calls. Can a model tell the axes apart at all. Roughly $0.12 |
| `.venv/bin/python3 judge/run_labelled.py --dry-run` | the estimate for a full agreement run |
| `.venv/bin/python3 judge/run_labelled.py --axis C4` | one axis over the labelled entries. Roughly $0.16 |
| `.venv/bin/python3 judge/run_labelled.py --axis C4 --run sonnet-5-out` | one axis, one run |
| `.venv/bin/python3 judge/run_labelled.py --axis C4 --limit 5` | the first few calls, to see the shape before paying for all of them |

Shared options on both runners: `--model` (default `claude-sonnet-5`),
`--effort` (`low`, `medium`, `high`; default `low`), `--max-tokens` (2000),
`--limit`, `--dry-run`.

**Judge only the axes the question is about.** All nine over 20 entries is
$0.43; the one axis that is open is $0.07, and a document axis is under a cent.
`docs/pipeline.md` has the full table under *What things cost*.

Run one of these on a plain `python3` and it does not fail obscurely - it says
the SDK is not on this interpreter and prints the line to use instead.

`--allow-stale` judges an axis whose labels are older than the axis, and records
that it did. It exists so the refusal can be overridden deliberately, not
routinely: the figure it produces compares a person reading one rubric with a
model reading another.

## Reading a run nobody labelled - stage 5

| | |
|---|---|
| `python3 judge/count.py <result.json>` | per axis, how many calls were judged and how many failed, plus how many entries the judge would send out |
| `python3 judge/count.py <before.json> <after.json>` | what moved between two turns |
| `python3 judge/count.py --run sonnet-5-out` | the newest result file that judged that run |

It refuses to compare runs judged against different criteria, and refuses just
as firmly when either file records no criterion digest at all.

## The calibration set

| | |
|---|---|
| `python3 tools/build_calibration_set.py` | rebuilds `calibration/customer/` from the *Minimal pairs* section of the rubric |

Run it after editing that section. `calibration/` is generated, gitignored, and
never edited by hand.

---

## The two loops, end to end

**Instrument** - only while it is open, and it is frozen after the gate:

    python3 judge/status.py                          # what is stale
    python3 tools/labels.py column --axis C3         # cut the column
    # read it, fill in verdict: and note:
    python3 tools/labels.py column --axis C3 --write
    python3 tools/labels.py sync && python3 tools/labels.py check
    .venv/bin/python3 judge/run_separation.py        # before any tag
    .venv/bin/python3 judge/run_labelled.py --axis C3

**Product** - the loop the instrument was built for:

    # change Chartula's prompt, re-render into test-runs/
    python3 tools/labels.py init --run <name> --prefix <p>
    .venv/bin/python3 judge/run_labelled.py --run <name>
    python3 judge/count.py <before.json> <after.json>

## Setup

    source .venv/bin/activate && pip install -r judge/requirements.txt

The judge needs `ANTHROPIC_API_KEY` in the environment;
`anthropic.Anthropic()` picks it up. Nothing else here needs it.
