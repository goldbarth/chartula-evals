# Using the pipeline

How to run one evaluation from start to finish, and what to do when a step does not go the way it should.
Written for someone who has never opened this repository.
The rules themselves live in [`pipeline.md`](pipeline.md); this file only says which command to run next, and what to do with what it prints.

Read this once, then keep [`commands.md`](commands.md) open for the flags.

---

## What this is, in one minute

[Chartula](https://github.com/goldbarth/chartula) turns the pull requests behind a release into changelogs for three audiences: technical, customer, product.
A language model writes the prose, so every change to Chartula's prompt moves the output in ways no unit test can see.

This repository measures whether such a change was an improvement.
It does that with three parts:

- **A criterion.** One rubric per audience (`rubric/*.md`), split into axes.
  Each axis asks one question of an entry, for example "does the closing clause state an outcome the reader can use", and has a pass and a fail condition.
- **A judge.** A model that applies one axis to one entry per call (`judge/run_labelled.py`).
  It is trusted only because it was checked against a person's verdicts on the same entries.
- **Cases.** Renderings of the same release, in `test-runs/`, one per change to Chartula.

The whole thing runs as two loops, and only one of them is ever open:

| | Loop A, the instrument | Loop B, the product |
|---|---|---|
| What changes | the rubric, the format document, the human labels | Chartula's prompt and fact base |
| Who does the work | a person, by hand | the machine |
| Cost per round | hours | minutes and cents |
| State today | **frozen** at criterion v2.0.0 | **open**, this is where the work is |

Almost everything you will do is loop B: change Chartula, render, judge, count, record.
Loop A reopens only when a spot check shows the judge has drifted.

---

## Setup

You need two checkouts side by side, Python 3, and .NET 10.

```bash
git clone https://github.com/goldbarth/chartula-evals
git clone https://github.com/goldbarth/chartula
cd chartula-evals
python3 -m venv .venv
.venv/bin/pip install -r judge/requirements.txt
```

Two interpreters are in play, and the tools tell you which one they want:

| Interpreter | Used for |
|---|---|
| `python3` | everything that only reads files: `status.py`, `count.py`, `tools/labels.py`, `tools/spot_check.py` |
| `.venv/bin/python3` | everything that calls the model: `judge/run_labelled.py`, `judge/run_separation.py` |

Credentials come from the environment and nowhere else:

| Variable | Needed by |
|---|---|
| `ANTHROPIC_API_KEY` | the judge here, and Chartula's rendering |
| `GITHUB_TOKEN` | Chartula, to read pull requests |

Build Chartula once so the binary exists:

```bash
cd ../chartula
dotnet build Chartula.slnx -c Release
```

The binary is at `src/Chartula.Cli/bin/Release/net10.0/chartula`.

---

## The map

Where each thing is, so nothing has to be searched for.

| You want | Look in |
|---|---|
| the rules of the process, and when a stage ends | `docs/pipeline.md` |
| the numbers a stage is measured against | `docs/targets.md` |
| what every past turn measured | `docs/measurements.md` |
| every script and its flags | `docs/commands.md` |
| the criterion for an audience | `rubric/customer.md`, `rubric/technical.md`, `rubric/product.md` |
| the shape a rendering must have | `docs/output-format.md` |
| what each frozen criterion version changed | `docs/criterion-versions.md` |
| findings that belong in Chartula | `docs/for-chartula.md` |
| the renderings and the fact base | `test-runs/` |
| human verdicts | `labels/<audience>/items.csv` and `runs.csv` |
| judge verdicts | `judge/results/<audience>/*.json`, never edited |
| why a verdict was hard | `labels/<audience>/friction-log.md` |

Naming in `test-runs/`: a run is `<model>-<what changed>-out`, with `<run>.md` holding the text the judge reads and `<run>.changelog.json` holding Chartula's own output.
The fact base is per release, `v0.1.0-facts.md`, and is shared by every rendering of that release.

---

## Before every session

Run this first, every time, before deciding anything:

```bash
python3 judge/status.py
```

The first block is four lines, and each one can change what you do next.

| Line | If it says | Then |
|---|---|---|
| `criterion` | `NOT TAGGED` | the criterion has moved since the last tag. Figures are still comparable to each other by digest, but the freeze gate is not closed. See *Closing the freeze gate* below before starting a new phase. |
| `noise floor` | a movement of one is not a result | remember it when reading counts. It is printed so it cannot be forgotten. |
| `spot check` | `OVERDUE`, or the count is at 5 | the next thing you do is a spot check, not a turn. See *The spot check*. |
| `gates nothing` | a list of axes | a count on those axes is a direction, not a figure. Do not credit a turn on them for a small movement. |

Then the `AXES` table.
Every axis should read `yes` under `comparable now`.
An axis that reads `no` is stale: its text changed after its labels were read.
Do not judge it; see *When the tools refuse*.

Then run the free consistency check:

```bash
python3 tools/labels.py check
```

It should report no problems.
If it does, fix those before anything else, because the judge refuses a run whose tables and rendering have drifted apart.

---

## The production turn, step by step

A turn is: one change to Chartula, one or more renderings of the release, every axis judged, the movement counted and recorded.
It costs about $0.70 for one rendering judged on every axis, and about $3.15 for the three renderings [`pipeline.md`](pipeline.md) asks for.

### Step 0: count, and decide the change

Read the `spot check` line from `status.py`.
Five sections of `measurements.md` since the last spot check means the spot check comes first.

Then decide the one change this turn tests.
One change per turn, always.
Two changes that land on the same axis cannot be told apart afterwards.
Before writing it, read all the bullets of Chartula's customer prompt, not only the one being changed, and ask whether another bullet already says something about this or forbids it.

Write down, before rendering, which axis the change is aimed at and what count would show it worked.
For C3 that is known: nine to eleven fails out of about twenty-four is where the prompt sits unchanged, so seven or below is the first count that means anything.

### Step 1: render in Chartula

Make the change in the Chartula checkout, on a branch, and commit it.
The commit hash is part of the record, so do not render from an uncommitted tree.

Then render the release with nothing published:

```bash
cd ../chartula
dotnet build Chartula.slnx -c Release
export GITHUB_TOKEN=$(gh auth token)
src/Chartula.Cli/bin/Release/net10.0/chartula generate --tag <tag> --repo goldbarth/chartula --no-publish --audience customer
```

Three things to check before moving on:

- **Which commit the tag points at.** The release being measured has been `v0.1.0`, and that tag has pointed at different commits over the life of the project (`8061f46` with 28 changes, later `0d4f6f4` with 44).
  Today the checkout carries only `v0.1.0-preview.1`.
  A rendering of a different set of changes is a different case, not a turn.
  Write down the tag and the commit it resolves to, `git rev-parse <tag>`.
- **The run metrics at the end of the output.** They carry the token counts.
  Keep them; they are the only cost record of the render.
- **That every requested audience came back.** An audience can be lost silently.
  If the summary lists an audience as failed or the text is missing from `changelog.json`, the render is not usable.

`chartula.yaml` pins `claude-sonnet-5`.
Do not change the model in the same turn as the prompt; the two cannot be separated afterwards.

The outputs land in the Chartula checkout as `changelog.json` and `release-<tag>.md`.
Copy them out before the next render overwrites them.

### Step 2: bring the rendering in

Choose the run name: `<model>-<what changed>-out`, for example `sonnet-5-fix-outcome-out`.
Then:

```bash
cd ../chartula-evals
cp ../chartula/changelog.json test-runs/<run>.changelog.json
python3 tools/from_chartula_run.py test-runs/<run>.changelog.json --run <run> --page ../chartula/release-<tag>.md
```

This writes `test-runs/<run>.md`, split into the audience sections the judge reads.
`--page` matters: the customer page as published carries front matter that one axis judges, and the field inside `changelog.json` does not.

It refuses to overwrite an existing run.
That is right; pick a new name.

Do **not** pass `--facts` for a release that already has a fact base in `test-runs/`.
The fact base belongs to the release, not to the run, and rewriting it moves figures for reasons that have nothing to do with the rendering.
Pass it only for a release nobody has rendered before.

### Step 3: lay out the rows

```bash
python3 tools/labels.py init --run <run> --prefix <p>
```

The prefix is short and unique per run, for example `s5fo`.
The ones in use are listed by `cut -d, -f2 labels/customer/items.csv | cut -d- -f1 | sort -u`.
A prefix already in use makes two runs' items look alike in every file that names them; check before choosing.

This writes one row per entry per axis with the verdict `?`, plus the document rows.
Nobody fills them in.
The judge builds a call for each anyway; that is what makes stage 5 cost no labelling time.

If `init` says it found no entries, the rendering does not write its items as `- ` bullets.
That is a finding about the rendering at level B, not a tooling problem.
Record it in `measurements.md` and stop this turn.

### Step 4: judge

First the estimate, which is free:

```bash
.venv/bin/python3 judge/run_labelled.py --run <run> --dry-run
```

Then the run, every axis:

```bash
.venv/bin/python3 judge/run_labelled.py --run <run>
```

Every axis, not only the one the turn is aimed at.
A movement on an axis nobody was looking at is the finding of the turn as often as not.

It prints one line per call and writes `judge/results/customer/labelled-all-claude-sonnet-5-<timestamp>.json`.
The agreement table it prints at the end is empty of meaning here, because nothing carries a human verdict; ignore it and go to step 5.

Do not pass `--model` or `--effort`.
Every figure in this repository was produced with the defaults, and a run judged by another model is not comparable with any of them.

### Step 5: count

```bash
python3 judge/count.py --run <baseline-run>
python3 judge/count.py <before.json> <after.json>
```

The baseline is the newest rendering of the same release from the same case, before this turn's change.
`measurements.md` names it in the previous turn's section, and `--run <name>` finds the newest result file that judged it.

`count.py` prints per axis how many entries were judged and how many failed, how many entries the judge would ship, and the change from the baseline.

### Step 6: read the result

Work down this table in order.
The first row that matches decides what the turn showed.

| What you see | What it means | What to do |
|---|---|---|
| `NOT COMPARED`: different criterion digests | the criterion changed between the two runs | the comparison is void. Re-judge the baseline under the current criterion, then compare again. |
| `NOT COMPARED`: no digest recorded | the baseline predates the result schema | read both files one at a time. Do not compare them as a pair. |
| `unparsed` is not zero on an axis | some calls returned no readable verdict | note the count. The denominator on that axis is smaller than it looks. If it is more than one or two, judge that axis again before reading it. |
| the entry count differs from the baseline by more than about five | the rendering is a different length, and a short rendering fails fewer entries on every axis at once | read shares, not counts, and say so in the record. One rendering cannot carry the result on its own; a second draw of the same commit is the next step, not a new change. |
| the target axis moved by one, or by less than the spread in `targets.md` | inside the noise floor | the turn showed nothing. Record it as such. Do not adjust the change and try again in the same turn. |
| the target axis moved past the floor, in the intended direction | the change may have worked | one rendering is one draw. Confirm with a second rendering of the same commit before crediting it. |
| an axis that was not the target moved past the floor, either direction | a collision between the change and another rule | this is the finding, ahead of whatever was planned next. Record it under the turn and understand it before the next change. |
| a document axis (A1, B1, B2, B3) failed where it passed before | the rendering lost coverage or shape | the rendering does not ship regardless of the target axis. Look at which entry or heading caused it. |
| nothing moved anywhere | the change did not reach the model, or was already covered | check the diff in Chartula reached the prompt text, not only the builder. |

Whatever the row, the turn is over after this step.
Three turns is the budget for the current phase, and a fourth is the figure being waited on rather than tested.

### Step 7: record

Add one section to `docs/measurements.md`, headed `## YYYY-MM-DD - <what the turn was>`.
It has to say, in this order:

1. what was changed in Chartula, with the commit and the issue number,
2. which tag and commit were rendered, with which model, and what the render cost from the run metrics,
3. the count per axis against the baseline, naming both result files,
4. what the movement turned out to be worth, read against the noise floor and the length of the rendering,
5. anything that moved that nobody aimed at.

Every section counts as a turn for the spot-check interval, including one that produced nothing.
A section headed with the words `spot check` resets that interval, so do not use those words in the heading of anything else.

A finding about Chartula goes to an issue in that repository and is listed in `for-chartula.md`.
A finding about the criterion goes under its version in `criterion-versions.md`.
Neither goes on a list.

### Step 8: commit

Three commits, in the order the files were produced, so that each can be read alone:

```
test-runs: <what this rendering carries>        # test-runs/<run>.*, labels/customer/items.csv, runs.csv
judge: ...                                       # only if a script changed
docs: <what the turn showed>                     # docs/measurements.md, and the judge/results/*.json it names
```

The result file goes with the docs commit that reads it, so that the figure and its evidence land together.

---

## When the tools refuse

Every refusal is deliberate and names its reason.
None of them is worked around with a flag on a routine turn.

| Tool says | Why | Do |
|---|---|---|
| `run_labelled.py`: the rubric has uncommitted changes | the prompt is built from the working tree, and staleness from git | commit or stash the rubric edit. Never `--allow-stale` on a turn of loop B. |
| `run_labelled.py`: axis X changed after the rubric_commit its labels carry | X is stale; the human column was read against older text | if loop A is closed, this should not happen; find out who edited the rubric. If loop A is open, re-pass the column, see below. |
| `run_labelled.py`: N entries in the rendering but M labelled rows | `init` and the `.md` disagree, usually because the `.md` was regenerated | delete the run's rows and `init` again, or restore the `.md`. |
| `run_labelled.py`: no `--- Customer ---` section | the run was imported with a missing audience | check `changelog.json` for the audience text. If it is not there, the render lost it; render again. |
| `run_labelled.py`: the SDK is not on this interpreter | plain `python3` was used | use `.venv/bin/python3`. |
| `count.py`: `NOT COMPARED` | different criteria, or no digest | see step 6. |
| `from_chartula_run.py`: file exists | a rendering is evidence a figure was read from | choose a new run name. `--force` only if you are sure no result file names this run. |
| `from_chartula_run.py`: schemaVersion is not 1 | Chartula's output format moved | check `docs/changelog-json.md` in Chartula before trusting the import. |
| `labels.py init`: already has rows | the run was initialised before | nothing to do; go to step 4. |
| `labels.py init`: no entries found | the rendering has no `- ` bullets | a level B finding. Record it, do not lay out ids by hand on a loop B turn. |
| `status.py`: `NOT TAGGED` | the freeze gate is not closed | see *Closing the freeze gate*. |
| `status.py`: `OVERDUE` | five turns since the last spot check | do the spot check now. |

---

## The spot check

Every five turns, and once more when a turn budget is spent, one person reads ten entries against the judge's verdicts on them.
It costs no API call and about half an hour.

```bash
python3 tools/spot_check.py --run <newest run>
# open labels/customer/spot-check-<date>.md, fill in every `you:` line
python3 tools/spot_check.py --read labels/customer/spot-check-<date>.md
```

The worksheet picks seven entries the judge passed and three it failed.
For each entry and axis, write `pass`, `fail` or `n/a` on the `you:` line, reading the axis text in `rubric/customer.md` and nothing else.
Do not look at the judge's reason first.

`--read` reports agreements, and two kinds of disagreement that are not the same thing:

| Figure | Meaning | Target |
|---|---|---|
| let through | the judge passed, you failed | at most 2 per 100 cells. This is the one that costs a release. |
| too strict | the judge failed, you passed | not counted against the target. It costs a turn, not a release. |

Then one of two outcomes:

- **The judge stands.** Let through is at or under the target, or over it on one or two cells that you can explain.
  Write a section into `measurements.md` headed `## <date> - spot check: <one line>`, with the counts and the entries that disagreed.
  Loop B continues.
- **The judge has drifted.** Let through is clearly over the target and the disagreements share a pattern.
  Write the same section, and then open loop A for that axis only.
  This is the only thing that reopens loop A.

The worksheet is scratch and is not committed.

---

## Closing the freeze gate

The criterion is `customer-criterion-v2.0.0` and it is not tagged.
Until it is, a new phase should not start.
The gate asks for three things, and one of them costs money:

1. **A separation run since the last rubric edit.**
   Five constructed documents, one axis broken in each, about $0.14.
   ```bash
   .venv/bin/python3 judge/run_separation.py --dry-run
   .venv/bin/python3 judge/run_separation.py
   ```
   It passes when every axis is found in its own document and not in the others, `40/40` in the summary.
   If it does not pass, the axis it misses is written wrong, and that is loop A work.
2. **A clean working tree.**
3. **An entry in `criterion-versions.md`.** It exists for v2.0.0 already.

Then tag and push:

```bash
git tag customer-criterion-v2.0.0
git push origin customer-criterion-v2.0.0
```

`status.py` reads the tag and stops saying `NOT TAGGED`.

---

## Publishing a dataset release

Only after the freeze gate is closed, and only from a clean tree.
A release is what one frozen criterion measured: a person's verdicts, the judge's verdicts at that criterion's digest, and the renderings both were read against.

```bash
python3 tools/export_dataset.py --draft     # anytime; the card lists what is still open
python3 tools/export_dataset.py             # refuses until nothing is
```

Every refusal names its fix, and they are the gates of this file:

| Export says | Do |
|---|---|
| not tagged | *Closing the freeze gate*, above |
| the tree's criterion is X, the version names Y | the criterion moved after the freeze. That is a new version, not a release of the old one |
| stale axes | *When loop A is open*, below |
| `<run>` is labelled but no result file at the digest judged it | `.venv/bin/python3 judge/run_labelled.py --run <run>`, about $0.43 per run |
| `labels.py check` | fix what it lists |
| `card.md`: not set, or TODOs left | answer them in `dataset/<audience>/card.md`. That file is the prose of the card and is written by a person |
| e-mail address or token | remove it at the source, the note or the rendering. There is no flag for this one |

Then read `dist/hf/<audience>/<version>/README.md` as a stranger would, and run the two `hf` lines the export prints.
`dist/` is not committed; `export.json` in the release names the commit it was built from.

---

## When loop A is open

Only after a spot check said the judge drifted, or when a new audience is being brought up.
The full rules are stages 1 to 4 of [`pipeline.md`](pipeline.md); this is the order of the commands.

Every rubric change makes that axis stale, and a stale axis costs a re-pass of its human column.
So collect every change first, apply them in one commit, and re-pass once.

```bash
python3 judge/status.py                                # which axes are stale
python3 judge/axis_diff.py C3                          # what changed in the axis since the column was read
python3 tools/labels.py column --axis C3               # cut the column into a worksheet
# read every entry against the new axis text, fill in verdict: and note:
python3 tools/labels.py column --axis C3 --write       # read it back, stamps rubric_commit
python3 tools/labels.py sync && python3 tools/labels.py check
.venv/bin/python3 judge/run_separation.py              # cents; before any agreement run
.venv/bin/python3 judge/run_labelled.py --axis C3      # the agreement figure, about $0.16 per axis
```

Two rules that decide how much work a change costs:

- A change that makes an axis more permissive can only turn a fail into a pass, so re-pass the fails of that column only.
  A stricter change is the other way round.
- At most two judge runs per axis.
  An axis that has not settled in two is out of the gate, with a paragraph in `targets.md` saying why, and it gates nothing afterwards.
  That is a valid ending, not a failure.

Every disagreement between judge and label goes into `labels/customer/friction-log.md`, naming the result file.
When every axis is in with a figure or out with a paragraph, close the gate as above, with a new version number per the rules in `pipeline.md`.

---

## Other audiences

Everything above takes `--audience technical` or `--audience product` and defaults to `customer`.
Where the other two stand:

| Audience | Criterion | Labels | Separation run | Judge runs |
|---|---|---|---|---|
| customer | v2.0.0, frozen | 13 runs, 280 entries | passed 2026-08-31 | many |
| technical | written, untagged | one run, `opus-5-out`, 30 entries | not run | none |
| product | written, untagged | none | not run | none |

Bringing one up means stages 1 to 4 for that audience: label a sample of 12 to 15 entries from one run, run separation, run agreement per axis, decide in or out per axis, tag.
Do not start it while loop B is open on customer.

Before any judging on `product`, rebuild its calibration set, which is generated and not committed:

```bash
python3 tools/build_calibration_set.py --audience product
```

---

## What things cost

Measured, not estimated, with `claude-sonnet-5` as the judge.

| | |
|---|---|
| one judge call | $0.0035 |
| rendering the release in Chartula, one audience | about $0.62 |
| one item axis over 20 entries | $0.07 |
| all nine axes over 20 entries | $0.43 |
| a turn over one rendering, every axis | about $0.70 |
| a turn over three renderings, every axis | about $3.15 |
| the separation run | $0.14 |
| the spot check | nothing |

The judge model is the largest lever and the easiest to get wrong.
`claude-opus-5` costs three times as much per call and produces figures that cannot be compared with anything here.

---

## Glossary

| Term | Meaning |
|---|---|
| axis | one question the rubric asks of an entry or a document, with a pass and a fail condition. Customer has nine: A1, B1 to B3, C1 to C5. |
| item axis, document axis | an item axis is judged per entry (C1 to C5, and A1 on an entry). A document axis is judged once per rendering (A1 for the whole, B1 to B3). |
| run | one rendering of one release, named in `test-runs/`. |
| turn | one change to Chartula, rendered and judged. One section of `measurements.md`. |
| draw | one rendering of an unchanged commit. The same prompt has produced 19, 24 and 25 entries, so one draw is not a measurement. |
| stale | an axis whose text changed after its human labels were read. Cannot be judged until re-passed. |
| re-pass | reading one axis down one run again, against the current axis text. |
| digest | a hash of the exact criterion text the judge was shown. Two results are comparable only if their digests match. |
| gate | stage 4's decision per axis. In: the judge reproduces a person's verdict well enough to trust. Out: it does not, and the axis gates nothing. |
| noise floor | the movement an unchanged prompt produces on its own. Currently: a movement of one is not a result. |
| let through | an entry the judge passed and a person would have failed. The instrument figure, target at most 2 in 100. |
| ships | an entry with no failing C axis. The tracked product figure, which blocks nothing. |
| separation | can the judge tell the axes apart at all, on constructed documents. Cents, no labels. |
| agreement | does the judge reach the person's verdict on labelled entries. |
| freeze | the criterion gets a version and a git tag, and no axis is edited afterwards. |
