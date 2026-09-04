# The pipeline

The order the work is done in, what each stage costs before it is entered, and
what ends it. Written so that no stage can run without a stopping condition.

It exists because of what went wrong without it. Building the instrument and
measuring with it ran at the same time, and each invalidated the other: every
finding from a judge run changed an axis, every changed axis invalidated a
labelled column, every re-passed column allowed another judge run. Three days,
five rubric changes, six passes over the label tables, twenty-two judge runs,
and no defined point at which any of it was finished. None of that was wasted
work. It had no exit.

## What this file owns

| What | Where |
|------|-------|
| The stages, their budgets, and what ends each one | here |
| The four moves and the staleness invariant | [`../judge/how-the-loop-works.md`](../judge/how-the-loop-works.md) |
| What an axis may be | [`../rubric/how-a-rubric-is-built.md`](../rubric/how-a-rubric-is-built.md) |
| How one pass is carried out | [`../labels/how-to-label.md`](../labels/how-to-label.md) |
| The figures every stage is measured against | [`targets.md`](targets.md) |
| Findings that belong in Chartula, not here | [`for-chartula.md`](for-chartula.md) |
| What each frozen version changed | [`criterion-versions.md`](criterion-versions.md) |
| What each turn of stage 5 measured, and what caused the figure | [`measurements.md`](measurements.md) |

This file says when a stage is over. It does not restate how the work inside a
stage is done.

---

## The one rule

**Two loops, and never both open at once.**

|                  | Loop A - the instrument            | Loop B - the product              |
|------------------|------------------------------------|-----------------------------------|
| What changes     | the rubric, the format document, the labels | Chartula's prompt and fact base |
| Who does the work| a person, by hand                  | the machine                       |
| How often        | once, then frozen                  | as often as wanted                |
| What ends it     | a threshold, fixed before entering | the product figure from stage 0   |

While loop A is open, the product is not touched. While loop B runs, the
instrument is frozen. Both open at once is the spiral, and it is the only way
to produce it.

---

## Stage 0 - the target, as a number, before anything is built

One sentence and one figure, in [`targets.md`](targets.md), written before the
first axis:

> Shippable means: the judge lets through at most **N of 100** entries a person
> would have sent back. A release ships when no entry of it fails.

Two figures, and they are not the same thing:

- **The product figure.** How many entries of a rendering ship. This is what
  the work is for.
- **The instrument figure.** How often the judge reaches the verdict a person
  reached. This is a tool for understanding *why* an entry does not ship. It is
  never the target, and a stage never waits on it improving.

Without stage 0 there is no "good enough", and without "good enough" no later
stage can end. Agreement per axis fills the vacuum, and agreement per axis has
no ceiling.

**Ends when:** both figures are written down with a number in them.

## Stage 1 - the criterion

The rubric and the format document. Form in the format document, judgement in
the rubric, per rule 4 of `how-a-rubric-is-built.md`.

**Budget:** a fixed span, decided in advance.

**Ends when:** every axis has its *Judges* line, its *Does not judge* line, a
procedure, an explicit fail condition, and an example that has been run back
through the procedure.

## Stage 2 - a sample, not a census

Label **12 to 15 entries from one run**. Not the corpus.

This is the stage that cost the most when it was skipped. Labelling 53 entries
across 9 axes is 477 hand verdicts, and a single axis change invalidates a
column of 53 of them. A sample of fifteen is enough to find out whether an axis
carries, and cheap enough to throw away when it does not.

The rest of the corpus is labelled after the freeze, if at all. Most of it
never needs to be: the judge does that work, which is why the judge exists.

**Ends when:** every axis has been applied once to the sample, and the friction
log holds what the rubric did not decide on its own.

## Stage 3 - can a model separate the axes

`run_separation.py` against the constructed cases. No labels needed, and it
costs cents.

An axis that fails here is written wrong, and it is found for the price of one
run rather than a day of labelling. Run this **before** stage 4, always.

**Ends when:** each axis is identified in its own case and not in the others.

## Stage 4 - does the judge reach the person's verdict

Three limits, all fixed before the stage is entered:

1. **At most two judge runs per axis.** An axis that has not settled in two is
   a finding about the axis, not a reason for a third.
2. **One round of rubric changes, batched.** All decisions collected, applied
   in one commit, one re-pass, one round of judging. Never one axis at a time -
   that is what turns five changes into six passes.
3. **A threshold per axis**, for example: finds at least three quarters of the
   person's fails and produces at most two false fails.

An axis that meets the threshold is in. **An axis that misses it is out**, with
one written paragraph saying why, and it does not gate anything afterwards.

That second outcome is the one that is usually missing, and its absence is what
sends every axis back into the queue. Three kinds of axis end here without
meeting any threshold, and all three are results:

- **The corpus carries no failures for it.** Its agreement figure measures the
  majority class and nothing else. It cannot be fixed by working harder.
- **The corpus is the wrong shape for it.** An axis judging product surface,
  applied to a changelog about the tool being evaluated, measures the case.
- **The axis produces both readings at once.** Disagreements running in both
  directions point at the procedure, not at a sentence.

**Ends when:** every axis is either in with a figure, or out with a paragraph.

## Gate - freeze

The criterion gets a version number and a git tag. From here no axis is edited.
Disagreements are recorded and not resolved.

Everything after this gate runs against a criterion that does not move. That is
the whole point of the gate: a figure from before it and a figure from after it
are not comparable, and a criterion that keeps moving can never say a product
got better.

**The tag** names the audience and the version: `customer-criterion-v1.0.0`.
The criterion is the rubric together with `output-format.md`, because the axes
judge conformance to that document rather than restating it, so freezing one
without the other freezes nothing.

The tag is the copy. `git show customer-criterion-v1.0.0:rubric/customer.md`
returns the frozen text, so no second copy is kept anywhere - a `frozen/`
directory would be a second source of truth, which is the defect rule 4 of
`how-a-rubric-is-built.md` names for the format document.

**What has to be true before a version is tagged**

1. The separation run passes. It is the regression test on the criterion
   itself: whether the axes can still be told apart is exactly what a rubric
   change can break, and it costs cents. A version is not tagged on a criterion
   that has not been through it since its last edit.
2. The working tree is clean. The prompt is built from the tree, so an
   uncommitted edit is judged as though it were committed. `run_labelled.py`
   already refuses to start on an uncommitted rubric.
3. The version has an entry in [`criterion-versions.md`](criterion-versions.md)
   saying what moved, what it invalidated, and which figures stopped being
   comparable.

**What every result carries afterwards.** `provenance` in each result file
holds `criterion_version` from the nearest tag and `criterion_digest`, a hash
of the text the judge was actually shown. The digest is the durable half: a
commit can be amended away and a tag can be moved, and both have happened here,
while the digest answers *were these two figures produced against the same
criterion* without consulting git at all.

    python3 judge/status.py --verify

reports which existing results were produced against the criterion in the tree.

**What the digits mean.** Not features and fixes. The question a version answers
here is whether two measurements can be compared, so the digits are cut along
what a change costs:

| | What changed | What it costs |
|---|---|---|
| **Major** | an axis changed so that a verdict can move | a re-pass of that column, and figures from either side of it are not comparable |
| **Minor** | an axis was added or removed, or text changed in a way that cannot move a verdict | nothing; older figures still hold for the axes that stayed |
| **Patch** | a typo, an example, a clarification that moves nothing | nothing |

Read that way the version number alone answers the question the staleness
invariant exists for: whether a figure from an earlier run still means anything.
A major bump says it does not.

## Stage 5 - the production loop, without a person in it

```
change Chartula's prompt
  -> re-render the release into test-runs/
  -> python3 tools/labels.py init --run <name> --prefix <p>   # rows, every verdict "?"
  -> .venv/bin/python3 judge/run_labelled.py --run <name>     # judges them anyway
  -> python3 judge/count.py <before.json> <after.json>        # what moved
```

No labelling, no re-pass, no rubric discussion. Minutes and cents per turn.

`init` lays out one row per (item, axis) with every verdict `?`, taken from the
rendering itself, and the runner builds a call for each regardless of whether a
person ever filled one in. Its own report compares against human verdicts and
so prints nothing here; `count.py` reports the judge's side and the difference
from the previous turn. It refuses to compare two runs whose criterion digests
differ, and refuses just as firmly when either run does not record one - two
files that name only a commit look alike whether or not the rubric moved
between them.

This is where the work lives from the freeze onward, and it is the loop the
whole instrument was built to make possible.

**Every axis is counted here, including the ones stage 4 put out of the gate.**
Out of the gate means the axis cannot be trusted to reproduce a person's
verdict. A turn of this loop compares a judge count with the previous judge
count, so a bias the axis carries sits in both and cancels. What it does not
cancel is noise: read a large movement, 19 fails to 3, and ignore a small one,
19 to 17. An axis that is out of the gate is a direction here, never a figure.

**Where the line between large and small is.** In the figure named in
[`targets.md`](targets.md) under *The noise floor*, and nowhere else. No run
here has ever been deterministic, so a turn that changes nothing still moves the
count; until that movement has been measured, calling a small change noise is a
guess wearing the word.

**Ends when:** the product figure from stage 0 is met.

## Stage 6 - a spot check, on a calendar

Every few turns of stage 5, one person reads ten entries against the judge's
verdicts on them. Not continuously, and not because a figure looked odd.

A judge that stays put means stage 5 continues. A judge that has drifted is the
**only** trigger that reopens loop A.

---

## The four mechanisms

Each one exists because its absence produced the spiral.

**1. A budget is fixed before the stage is entered.** Runs, hours or dollars,
written down. When it is spent, a decision is made. Not "let us look a bit
further" - that is the same decision deferred, at full price. *What things
cost* below is what to fix it against.

**2. "Does not measure" is a valid ending.** An axis that cannot separate
anything on this corpus is finished the moment that is written down. Without
this, every axis returns to the queue forever, because a figure can always be
improved.

**3. An incidental finding is written down where it holds, not on a list.**
A stamp pointing at a commit that no longer exists, one sentence living in two
documents: these belong to the thing they are about. A finding about the
criterion goes under its version in
[`criterion-versions.md`](criterion-versions.md), a finding about a turn goes
under that turn in [`measurements.md`](measurements.md), and a finding about
Chartula leaves the repository entirely, per mechanism 4.

There is no list of them, and there was one: a file of parked rows collected
what nobody was going to read again, because a row on it belonged to no piece of
work. Written under the version or the turn it holds against, the same finding
is read by whoever is comparing two figures, which is exactly who needs it.

**4. Findings about Chartula leave this repository immediately.** They are
filed as issues there and appear here as a reference only. Work for another
project accumulating in this project's list is what makes the work look
endless when it is not.

---

## What things cost

Measured over 1,424 judge calls, not estimated. The question a budget answers is
never "what does a run cost" but "how many runs", so the figures are per turn of
a loop rather than per command.

| | |
|---|---|
| One judge call | $0.0035 with `claude-sonnet-5`, $0.0102 with `claude-opus-5` |
| Re-rendering a release in Chartula | about $0.62 |
| Judging one document axis, one run | $0.004 |
| Judging one item axis, 20 entries | $0.07 |
| Judging all nine axes, 20 entries | $0.43 |
| The separation run, 40 calls | $0.14 |

**A turn of stage 5 is the render plus the judging**, so a targeted turn is
about $0.70 and the render is nine tenths of it. Judging all nine axes when one
question is open triples the judging and answers nothing extra.

**The judge model is the largest single lever and the easiest to get wrong.**
It is three times the price between the two models, it is a flag nobody thinks
about, and a run judged by one model cannot be compared with a run judged by the
other - so the cheap mistake costs twice, once in money and once in a figure
that has to be produced again. Both runners default to `claude-sonnet-5`, which
is what every figure here was produced with.

---

## What this would have changed

Against the three days that produced it:

- Stage 2 would have cost 15 hand verdicts instead of 477.
- The five rubric changes would have been one batched round: one re-pass
  instead of six.
- The axes that cannot measure on this corpus would have left after the first
  run, each with a paragraph, instead of returning to the queue each round.
- Chartula's customer prompt - one sentence, carrying none of
  `docs/output-format.md` - would have surfaced in stage 5 on the first day
  rather than the third.

## Filling in the numbers

The figures below belong to the project, not to this file. They are decided
once, in [`targets.md`](targets.md), and this file only says that they have to
exist.

| Figure | Where it is decided | Currently |
|--------|---------------------|-----------|
| The product target - renderings that ship unedited | [`targets.md`](targets.md) | four of five; today 0 of 3 |
| The instrument target - entries let through per 100 | [`targets.md`](targets.md) | at most 2; today 7.5 |
| The stage 4 threshold per axis | [`targets.md`](targets.md) | catches three quarters, at most two false per fifty |
| The judge-run budget per axis | here, stage 4 | two |
| The stage 2 sample size | here, stage 2 | 12 to 15 |
| The spot-check interval | [`targets.md`](targets.md) | every five turns of stage 5 |
