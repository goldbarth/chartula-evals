# Labels

One folder per audience - [`customer/`](customer), plus `technical/` and
`product/` once those rubrics exist. Each holds `items.csv`, `runs.csv`,
`run-summary.csv`, `missing.md`, `friction-log.md` and a `what-is-labelled.md`
with the worked example for that audience. This file is what all of them share.

Values: `pass`, `fail`, `?` (not judged yet), `n/a` (the axis does not apply
to this entry).

**Item IDs.** Run prefix plus the position of the entry in the rendering, in
document order, counted from one: `s5-01`, `s5-02`.

## Aggregation

An item is `shippable` only if no C axis is `fail`. No weighting, no overall
impression. A single failed axis is enough.
A run is `shippable` only if no B axis is `fail` and no item is `not shippable`.

## Order of work

1. One axis at a time, down the whole run, not one item at a time across all
   axes. Judging C1 for twenty-six items in a row compares the same question
   against itself; judging one item across five axes lets the first verdict
   colour the rest.
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
