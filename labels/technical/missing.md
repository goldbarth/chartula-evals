# Missing entries (level A1, second half)

Companion to [`items.csv`](items.csv), which only carries A1 for entries that
are wrongly *included*. This file is the other half: changes wrongly *absent*.

Changes that should have appeared in the technical rendering and have no entry.
One row per finding, grouped by run. If a run has none, put `-` in `change`.

The test is A1's own: does the change reach anyone outside the work it was made
in - released behaviour, an interface something else calls, or what a consumer
installs. The reader here meets the source, so the line sits further out than
in `../customer/missing.md`: a type's public behaviour counts even when no
command changes.

| run        | change | why it reaches this reader |
|------------|--------|----------------------------|
| opus-5-out | `#67`, filed as `chore: replay stored fact bases so the pipeline is tested for free` (`test-runs/v0.1.0-facts.md` lines 760 to 786). Two changes to public behaviour sit inside it and neither has an entry anywhere in the rendering. | `DeserializeFactBase` is new and is the inverse of `Serialize`, so a `changelog.json` can be read back at all, and it refuses unknown schema versions and categories with a message rather than silently. And `ChangeFact` and `FactBase` compared by list identity, so two fact bases holding identical facts came out unequal; they compare by content now. Both are visible to anyone calling `Chartula.Core` without reading its tests. |

**What was checked and is not a finding.**

`#68`, filing the CLI project under the `/src/` solution folder, moves a project
between virtual folders in `Chartula.slnx`. No file moved, no behaviour changed
and nothing a consumer installs differs, so its absence is correct under rule 1.

`#70`, the two release blockers, is in the rendering: `o5-26` announces it and
`o5-27` and `o5-28` carry the two fixes. That none of the three prints a
reference is a C2 finding and is scored there, not here. The change is present.

`#69`, the documentation pass, and `#54`, the prompt-text refactor, are the
opposite case: both have entries, `o5-29` and `o5-30`, and both fail A1 in
`items.csv` for being there at all.

Every other pull request of the release, `#41` to `#66`, has exactly one entry,
matched by the reference each entry carries.
