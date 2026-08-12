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
That half needs a written criterion before it needs any code.
A first version of that criterion now exists for the customer rendering; it has not been calibrated against a judge.

## Status

The runs to be judged are in [`test-runs/`](test-runs), seven renderings of the same release across four models and two reasoning settings.
A first criterion for the customer rendering is in [`rubric-customer.md`](rubric-customer.md), derived from one of them.
Labelling the remaining runs against it is the open work, and nothing here is automated until that criterion holds up.

## Licence

MIT, see [LICENSE](LICENSE).
