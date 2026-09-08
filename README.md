# chartula-evals

How [Chartula](https://github.com/goldbarth/chartula) is measured.

Chartula turns the pull requests of a release into changelogs for several audiences.
An LLM does the rephrasing, which means every run costs money and every prompt change alters the output in ways no unit test catches.

This repository holds the part that answers whether a change was an improvement:
the cases Chartula is run against, what those runs cost, and how the resulting text is judged.

## Why it is separate

Chartula is a changelog tool.
Its users need a changelog, not an evaluation harness, so the harness does not belong in that repository.

What does belong in Chartula is the measurement of a single run, which already exists as the run metrics summary.
Everything that compares runs against each other lives here.

## The question this repository exists for

> Can a cheaper model still write a changelog worth shipping?

Cost per run is measured.
Six runs against the same release, four models, every figure confirmed against the invoice.

Quality now has a written criterion and something that applies it at scale.
What it says so far is that the question is premature:
not one rendering, from any of the four models, goes out without a person editing it.
The reason is not the model.
It is that Chartula's customer prompt is a single sentence and carries none of the format this repository specifies.

## What is here

**The criterion.** [`rubric/customer.md`](rubric/customer.md) - three levels and nine axes, each with the one question it answers, the questions it leaves to a neighbour, a procedure and an explicit fail condition.
[`rubric/how-a-rubric-is-built.md`](rubric/how-a-rubric-is-built.md) is the meta-rule the axes have to obey.
[`docs/output-format.md`](docs/output-format.md) owns form, so the rubric judges conformance to it rather than restating it.

**The cases.** [`test-runs/`](test-runs) - renderings of the same release, plus the release's facts.
Six of them compare models and reasoning settings; the rest are turns of the production loop, one per change to Chartula.
Three are labelled by hand; three are held out on purpose and stay unlabelled until a judge is trusted.

**The verdicts.** [`labels/customer/`](labels/customer) - entries scored per axis with the passage each verdict points at, and a friction log of everything the rubric did not decide on its own.
Rows for a production turn are left unscored on purpose: the judge scores those, and a person reads a sample of them back in a spot check.

**Two measurements.** Separation asks whether a model can tell the axes apart at all, against constructed cases where one axis is broken in each.
Agreement asks whether it reaches the verdicts a person reached, on the labelled entries.
Both run one axis on one subject at a time, from a single prompt that never sees a human verdict.

## How the work is ordered

[`docs/pipeline.md`](docs/pipeline.md) is the entry point.
It exists because building the instrument and measuring with it ran at the same time, and each kept invalidating the other.
Its one rule is that the two loops are never open at once, with a freeze between them, and every stage has a budget fixed before it is entered and a condition that ends it.

[`docs/targets.md`](docs/targets.md) holds the figures those stages are measured against, and what each one stood at when it was last measured.
[`docs/measurements.md`](docs/measurements.md) is the record of every turn since the freeze: what was changed, what moved, and what the movement turned out to be worth.
Nothing leaves that file, including findings that have since been fixed, because the point of an entry is that the failure happened.
[`docs/commands.md`](docs/commands.md) lists every script, what it is for and what it needs.

`python3 judge/status.py` opens with the four facts that decide how a count may be read: whether the criterion is frozen, what a movement has to beat to mean anything, when the next spot check is due, and which axes gate nothing.
[`judge/how-the-loop-works.md`](judge/how-the-loop-works.md) holds the day-to-day loop and the staleness invariant:
a human label and a judge verdict are comparable only if both were made against the same version of that axis.

## Status

The criterion is written, frozen at v2.0.0, and the judge applies it.
Nine axes have a figure against a rubric none of them is older than.
Three of the nine measure well enough to gate on; the other six are recorded as out, with the reason, rather than left in a queue, and a count from those is a direction rather than a figure.
Two spot checks have read a sample of the judge's verdicts back against a person: 50 of 50 and 46 of 49 agreed, so the judge has not drifted and the instrument loop stays closed.

The production loop is running and the work is in Chartula.
Six changes have been measured since the freeze.
The clearest is what a reader can meet: it was decided from the type of a commit, so the changelog carried entries about the tool's own file formats, and deciding it from a label instead took the coverage axis to zero.
The last of the four document axes went with it, which is the first rendering where none of them fails.

**No rendering ships whole yet.** The newest sends 11 of its 24 entries out unedited, and nine of the thirteen that are held back fail on one thing: the entry says what changed and never what the reader gets from it.

Two figures are known that were not before, and both cost turns to learn.
A movement of one on any axis happens without changing anything, so it is not a result.
And one rendering is not a measurement: the same prompt has produced 19, 24 and 25 entries, and a short rendering fails fewer entries on every axis at once, which is enough to look like an improvement.

Findings that belong in Chartula are filed there as issues and collected in [`docs/for-chartula.md`](docs/for-chartula.md).

## Licence

MIT, see [LICENSE](LICENSE).
