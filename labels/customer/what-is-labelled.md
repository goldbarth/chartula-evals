# Labels: customer rendering

Measured with the axes from [`../../rubric/customer.md`](../../rubric/customer.md).
Process shared with every audience: [`../how-to-label.md`](../how-to-label.md).

| file | what it holds |
|------|-----------------|
| [`items.csv`](items.csv) | level C verdicts, plus A1 - one row per (run, item, axis) |
| [`runs.csv`](runs.csv) | level B verdicts - one row per (run, axis) |
| [`run-summary.csv`](run-summary.csv) | overall shippable / not shippable per run - written by `labels.py sync`, never by hand |
| [`missing.md`](missing.md) | level A1, the other half - changes with no entry at all |
| [`friction-log.md`](friction-log.md) | where the rubric did not decide a case on its own |

## Runs labelled so far

<!-- labels.py sync: runs labelled -->

| run                      | items | shippable     |
|--------------------------|-------|---------------|
| sonnet-5-out             | 26    | not shippable |
| opus-5-out               | 25    | not shippable |
| sonnet-5-no-thinking-out | 2     | not shippable |

<!-- labels.py sync: end -->

`sonnet-5-no-thinking-out` carries only two item rows because the run produced
no feature entries at all - that absence is an A1 finding, recorded in
`missing.md`, not a gap in the item table.

## Worked example

First entry of `sonnet-5-out`, as the pattern for the rest:

> - **Run metrics summary**: Every `preview` and `generate` run now ends with a
> metrics report showing how many checks ran, how many issues each found, and how
> many tokens were spent - including whether the deeper (thorough) check caught
> anything the free check missed. Use this to decide whether the thorough check
> is worth keeping on.

The verdicts are not repeated here. They live in the `s5-01` rows of
`items.csv`, which is the only place any item is scored. This shows how the
reasons behind them are written, one per axis:

- **kind**: a new capability, not a repair.
- **A1**: a summary printed at the end of a run is product surface.
- **C1**: opens on "Every preview and generate run now ends with a metrics
  report", observable, not on what was built.
- **C2**: affects every run, so slot 2 is correctly absent - which the rubric
  calls a pass, not `n/a`.
- **C3**: "Use this to decide whether the thorough check is worth keeping on"
  is a consequence, not a restatement.
- **C4**: the report ends every run and there is nothing to switch, so there
  is no action to state.
- **C5**: "the deeper (thorough) check" names an internal stage. `preview`
  and `generate` are fine, those are typed by the user; `thorough` is the
  mode value, and a reader who has only used the product cannot tell what it
  means.
