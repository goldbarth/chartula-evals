# Missing entries (level A1, second half)

Companion to [`items.csv`](items.csv), which only carries A1 for entries that
are wrongly *included*. This file is the other half: entries wrongly *absent*.

Changes that should have appeared in the customer rendering and have no entry.
One row per finding, grouped by run.
If a run has none, put `-` in `change`.

| run                      | change                                                                                                                                                                                             | why the user would notice                                                                                                                                                                                                                                                      |
|--------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| sonnet-5-out             | The documentation pass (`#69`). Present in the technical rendering (`test-runs/sonnet-5-out.md` line 262) and in the product rendering (line 363), with no entry anywhere in the customer section. | The usage section did not run as written - it called the commands "planned entry points" and omitted the required `--tag` and `--repo`, so a reader who copied it got an error. `chartula.example.yaml` showed 4 of 8 sections, so copying it silently lost half the settings. |
| opus-5-out               | The documentation pass (`#69`). Present in the technical rendering (`test-runs/opus-5-out.md` line 66) and in the product rendering (line 202), with no entry anywhere in the customer section.    | Same change, same run source: the documented commands could not be run as printed, and the example configuration file covered half the sections it claimed to. Both are noticed by using the product, not by reading the source.                                               |
| sonnet-5-no-thinking-out | Every new feature or change was completely omitted from the customer section, and only fixes were listed.                                                                                          | 1. As a result, the list in the features section is empty. 2. Changes, such as new settings, appear in the application but are not explained to the customer or user.                                                                                                          |

Every other change in the fact base has an entry in both runs. Two absences were
checked and are **not** findings: the prompt-text refactor (`#54`) is internal
and correctly excluded by A1 in both runs, and the known-limitation note that
`opus-5-out` carries as `o5-25` reports no change at all - the run that omits it
is the one that got A1 right.

Where two source changes share one entry - `o5-08` covering the commit range and
the pull request read, `o5-17` covering the generator and the provider seam -
nothing is missing at level A. That is a grouping finding under B2, and the runs
are already marked `fail` there.
