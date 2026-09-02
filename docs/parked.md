# Parked

Incidental findings. Things noticed while doing something else, that block
nothing and are not worth interrupting the work for.

Read **once per freeze cycle**, per mechanism 3 of
[`pipeline.md`](pipeline.md). Not in between, and never added to the open list
of whatever is currently being worked on - that is how a list comes to measure
how much has been looked at rather than how much is left.

A row leaves this file in one of two ways: it is done, or it is written off
with a reason. Both remove it.

| Found | What | Why it is parked |
|-------|------|------------------|
| 2026-09-02 | The `rubric_commit` on the B1 and C4 rows of `labels/customer/items.csv` is `7213389`, a commit that is not reachable from `HEAD`. It is the pre-amend version of `47b5f34`; `git diff 7213389 47b5f34` is empty, so the two name the same rubric text. | Nothing reads it wrong today - `status.py` resolves the object and reports both columns comparable. It becomes a real problem only if the object is ever garbage-collected. |
| 2026-09-02 | `docs/output-format.md` rule 11 says of the collapsed line that "scope, outcome and action are usually `n/a` on it". The Units section of `rubric/customer.md` says the same. | A judgement statement living in the format document, which rule 4 of `how-a-rubric-is-built.md` says belongs to the rubric alone. One of the two has to give it up, and deciding which is a rubric change - so it waits for a cycle where the rubric is open. |
| 2026-09-02 | The `n/a` example of axis C4 in `rubric/customer.md` names "a metrics summary printed at the end of every run". That is `s5-01` of `sonnet-5-out`, whose closing sentence hands the reader a decision and names nowhere to act on it, so the axis prints `n/a` beside a case its own procedure fails. The `s5-01` label and the worked example in `labels/customer/what-is-labelled.md` both carry the same reading. | Repairing it edits an axis, which makes C4 stale and costs a re-pass of its 31 `n/a` rows plus a judge run. C4 is the strongest axis of the set as it stands - 52 of 53, all eight of the person's fails caught - so the repair buys accuracy in the rule and nothing in the figure. It waits for a cycle where the rubric is open. The judge found it: `judge/results/customer/labelled-C4-claude-sonnet-5-2026-09-02T141038.json`, and `labels/customer/friction-log.md` carries the row. |
