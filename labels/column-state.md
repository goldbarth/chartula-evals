# Column state: customer rendering

Which version of each axis a column was last passed against, by hand. The date
of the file does not answer this: editing the friction log over one axis would
otherwise mark every other column as freshly checked.

Update the row when a column has been read against the current text of its
axis - whether or not a verdict moved. "Checked, nothing moved" is a result and
belongs in the friction log next to it.

| axis | column passed against | note                                                                                          |
|------|-----------------------|-----------------------------------------------------------------------------------------------|
| A1   | 83e9d24               | half two was added in 9d61351 and is not judgeable per entry; half one unchanged in substance |
| B1   | ce900ac               | re-read against the rewrite; all three runs moved from fail to pass |
| B2   | ce900ac               | rewritten in ce900ac, run rows not re-read                                                    |
| B3   | 1f94446               | unchanged since                                                                               |
| C1   | 83e9d24               | rewritten in 9d61351, column not re-read                                                      |
| C2   | f34e11b               | re-read after the widening; one of the two fails moved                                        |
| C3   | 1f94446               | re-passed after the substance rewrite; rule 2 changed again in c57ec89                        |
| C4   | d9dad7f               | re-passed after the n/a rule, and checked when C4/C5 were reconciled                          |
| C5   | 83e9d24               | unchanged since; only s5-01 revisited                                                         |

The verdicts are in [`customer.md`](customer.md), what was found while reading a
column in [`friction-log.md`](friction-log.md). `judge/status.py` reads the table
below to decide whether an axis can be compared with a judge run at all.
