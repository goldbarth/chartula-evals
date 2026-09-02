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

**The cases.** [`test-runs/`](test-runs) - six renderings of the same release across four models and two reasoning settings, plus the release's facts.
Three are labelled by hand; three are held out on purpose and stay unlabelled until a judge is trusted.

**The verdicts.** [`labels/customer/`](labels/customer) - 53 entries scored per axis with the passage each verdict points at, and a friction log of everything the rubric did not decide on its own.

**Two measurements.** Separation asks whether a model can tell the axes apart at all, against constructed cases where one axis is broken in each.
Agreement asks whether it reaches the verdicts a person reached, on the labelled entries.
Both run one axis on one subject at a time, from a single prompt that never sees a human verdict.

## How the work is ordered

[`docs/pipeline.md`](docs/pipeline.md) is the entry point.
It exists because building the instrument and measuring with it ran at the same time, and each kept invalidating the other.
Its one rule is that the two loops are never open at once, with a freeze between them, and every stage has a budget fixed before it is entered and a condition that ends it.

`PLAN.md` holds the targets those stages are measured against and where the work currently stands.
It is kept out of the repository on purpose, so the figures below are quoted here rather than linked.
[`judge/how-the-loop-works.md`](judge/how-the-loop-works.md) holds the day-to-day loop and the staleness invariant:
a human label and a judge verdict are comparable only if both were made against the same version of that axis.

## Status

The criterion is written and the judge applies it.
Nine axes have a figure against a rubric none of them is older than, for $3.95 of judge runs in total.
Three of the nine measure well enough to gate on; the other six are recorded as out, with the reason, rather than left in a queue.

The next work is not in this repository.
Of 53 labelled entries, 19 state no outcome the reader can use, and 15 name a configuration key or a file path.
Both are already forbidden in writing here and neither rule reaches the model.
Findings that belong in Chartula are filed there as issues and collected at the end of `PLAN.md`.

## Licence

MIT, see [LICENSE](LICENSE).
