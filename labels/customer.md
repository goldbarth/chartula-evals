# Labels: customer rendering

Measured with the axes from `../rubric-customer.md`.

Values: `pass`, `fail`, `?` (not judged yet), `n/a` (the axis does not apply to this entry).
Item IDs run per run, in the order the entries appear in that run.

The previous table was discarded: it measured feature entries against the fix criteria,
and the axis numbers C1 to C3 mean something else since the rubric was reworked.

## Run table (level B)

One row per run.

| run                      | B1 action first | B2 grouping and order | B3 length and tone | shippable | note |
|--------------------------|-----------------|-----------------------|--------------------|-----------|------|
| haiku-4-5-out            | ?               | ?                     | ?                  | ?         |      |
| sonnet-5-no-thinking-out | ?               | ?                     | ?                  | ?         |      |
| sonnet-5-out             | ?               | ?                     | ?                  | ?         |      |
| opus-4-8-out             | ?               | ?                     | ?                  | ?         |      |
| opus-5-no-thinking-out   | ?               | ?                     | ?                  | ?         |      |
| opus-5-out               | ?               | ?                     | ?                  | ?         |      |

## Item table (level C, plus A1 for wrongly included changes)

One row per entry in the customer rendering.
`kind` is `fix`, `feature` or `breaking` and decides how slots 2 to 4 are read.
`A1` is `fail` when the entry should not have appeared at all.

| run | item | kind | A1 | C1 observation | C2 scope | C3 outcome | C4 action | C5 no codebase | shippable | note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| | | | | | | | | | | |

## Missing (level A1, the other half)

Changes that should have appeared in the customer rendering and have no entry.
One row per finding, grouped by run.
If a run has none, put `-` in `change`.

| run | change | why the user would notice |
| --- | --- | --- |
| | | |
