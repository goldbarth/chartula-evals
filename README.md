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

Whether the cheap end writes something worth sending out is not.
That half needs a written criterion before it needs any code, and the criterion does not exist yet.

## Status

Empty, deliberately.
The first piece of work is writing down what a shippable changelog is, by labelling the runs that already exist.
Nothing here is automated until that criterion holds up.

## Licence

MIT, see [LICENSE](LICENSE).
