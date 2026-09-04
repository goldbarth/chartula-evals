# Measurements

One section per turn of stage 5 of [`pipeline.md`](pipeline.md): what was
changed in Chartula, what the rendering of it measured, and what the figure
turned out to be caused by.

**This is a record, not a list of work.** Nothing leaves this file. A finding
that has since been fixed stays where it is, because the point of the entry is
that the failure happened and what it cost, and a fixed row removed is a fixed
row that cannot be looked up the next time the same shape appears. The lists
that do empty themselves are [`parked.md`](parked.md), whose rows leave when
they are done or written off, and [`for-chartula.md`](for-chartula.md), whose
rows leave when the issue closes.

Figures from before this file existed are in [`targets.md`](targets.md), and
what each version of the criterion changed is in
[`criterion-versions.md`](criterion-versions.md).

---

## 2026-09-04 - the outcome slot was optional in the prompt

**What was measured.** `test-runs/sonnet-5-format-out.md`, rendered by Chartula
on 2026-09-03 from the release `v0.1.0` of its own repository. The rendering
carries goldbarth/chartula#99, which put the output format into the customer
prompt, and #101, which writes a run's artefacts without publishing a release.
It does not carry #102 or #104, both of which were merged after it was
rendered.

**How.** `judge/results/customer/labelled-all-claude-sonnet-5-2026-09-04T100752.json`,
124 calls, judge `claude-sonnet-5` at effort `low`. Criterion v2.0.0, digest
`sha256:8c213cdc9828d107`, at commit `761ae30` with a clean tree. No axis was
judged stale.

| axis | judged | failed |
|------|--------|--------|
| A1 | 21 | 0 |
| B1 | 1 | 0 |
| B2 | 1 | 0 |
| B3 | 1 | 0 |
| C1 | 20 | 1 |
| C2 | 20 | 0 |
| C3 | 20 | 7 |
| C4 | 20 | 0 |
| C5 | 20 | 0 |

**The figure: 13 of 20 entries ship, so the rendering does not ship whole.**

**What carried it.** C3 alone. The seven entries it fails are exactly the seven
that do not ship; the single C1 failure sits on `s5f-09`, which fails C3 as
well, so it costs no further entry. Every document axis passes, which is the
first time that has been true here: A1 finds no observable change left out, and
B1, B2 and B3 all pass.

The seven, with the passage the judge held against each:

| entry | what the judge read |
|-------|---------------------|
| `s5f-03` | "an invalid setting now produces a clear configuration error message instead of a crash" - the negation of the opening |
| `s5f-09` | "It runs by default and can be turned off in the faithfulness section of `chartula.yaml`" - configuration, not an outcome |
| `s5f-13` | the mechanism of fact-grounded generation, stated a second time |
| `s5f-15` | no candidate outcome anywhere in the entry |
| `s5f-17` | "This is entirely optional and configured in the labels section of `chartula.yaml`" - configuration, not an outcome |
| `s5f-18` | "rather than leaving the changelog empty" - the negation of the opening |
| `s5f-20` | "so labeling reflects the actual change" - the opening turned positive |

**What caused it.** Two sentences of the `CustomerFormat` constant in
Chartula's `ChangelogPromptBuilder.Prompts.cs`, which described a four-part
entry and then allowed the third part to be dropped:

- "Leave out any of the last three that does not apply." The last three are
  scope, outcome and action, so the outcome was optional. `s5f-15` is that
  permission used to the letter: the entry has no outcome sentence at all.
- "Say what the reader can now rely on instead, or leave it out." This one
  stands directly after C3's own test, which the prompt already carries word for
  word. The model applied the test, found the clause wanting, and took the
  cheaper of the two repairs offered. The other six entries are that.

The prompt was not wrong about its source. `docs/output-format.md` rule 8 says
the same in as many words: "Scope, outcome and action are omitted when they do
not apply, per C2 to C4."

**What was changed.** Both sentences, in Chartula. The outcome is now always
written, and striking the clause is named as not being a way out. Only scope and
action may be absent.

**What was left open.** The sentence in `output-format.md` that the permission
came from. C3 has no not-applicable case at all: `n/a` is defined by C4 alone,
and C2 calls its not-applicable case a pass in as many words. So rule 8 permits
an omission the axis it points at never allows. Repairing it edits the
criterion, which is frozen, so it waits for a cycle where the instrument loop is
open. The row is in [`parked.md`](parked.md).
