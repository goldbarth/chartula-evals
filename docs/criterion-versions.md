# Versions of the criterion

One entry per frozen version: what moved, what it invalidated, and which
figures stopped being comparable. The friction log records cases; this records
versions, and it is the file to read before comparing two numbers that were
produced weeks apart.

What the digits mean, and the tag that carries them, are in the freeze gate of
[`pipeline.md`](pipeline.md).

**The digest is the durable name, not the tag and not the commit.** A tag can be
moved and a commit can be amended away - two of this repository's own rubric
commits already were, and the `rubric_commit` stamps naming them resolve today
only because git has not pruned them yet. The digest is taken over the text the
judge is actually shown: every axis section, `Units`, the format sections
inlined beside an axis, and both halves of `judge/axis-prompt.md`. Every result
file carries it, and

    python3 judge/status.py --verify

says which existing results were produced against the criterion in the tree.

---

## customer-criterion-v2.0.0

Not tagged yet. Digest `sha256:8c213cdc9828d107`.

**What moved.** B2 judges the document's opening, and the front matter is part
of it. The rule that a missing `tags` field is *correct* when the fact base
carries no labels lives in the format document's `Tags` section, and that
section was not among the ones handed to B2 - it saw `Two serialisations` and
`Groups` only. So the judge failed a document for omitting a field whose
omission rule it had never been shown. `Tags` is now in the set.

**Why a major bump for a defect fix.** The rule in the freeze gate is
mechanical: a change that can move a verdict is major. This one can, and did -
run `labelled-B2-claude-opus-5-2026-09-03T120021.json` is the verdict it
produced, and it is not comparable with anything judged after this change.

**What is not affected.** Only B2's input changed. No axis text moved and no
other axis is shown the format at all, so the figures for the other eight stand
on their own; the digest covers the criterion as one text, so it moves for all
of them regardless. Re-judging B2 for one run is one call.

**What it changed, measured.** B2 was re-judged on the same document under this
version and passes: "opening header contains title/description/publishedAt as
required (missing tags is separately fine since no tags)". Run
`labelled-B2-claude-sonnet-5-2026-09-03T120649.json`. The axis now reaches the
question it is for, and the answer it gives about that document is a finding
about Chartula rather than about the harness.

**Before it can be tagged**, the gate asks for a separation run since the last
edit.

**Known and not repaired.** What this version is wrong about, kept here because
a reader comparing two figures has to know it. None of it blocks a measurement,
and each repair edits the criterion, which is frozen.

- **`output-format.md` rule 8 permits an omission C3 never allows.** The rule
  reads "Scope, outcome and action are omitted when they do not apply, per C2 to
  C4", and C3 has no not-applicable case at all: `n/a` is defined by C4 alone,
  and C2 calls its not-applicable case a pass in as many words. The permission
  reached Chartula's customer prompt word for word and cost seven of twenty
  entries on 2026-09-04; the prompt is fixed there, the sentence here is not.
- **C4's `n/a` example names a case its own procedure fails.** The example is "a
  metrics summary printed at the end of every run", which is `s5-01` of
  `sonnet-5-out`, and that entry closes by handing the reader a decision with
  nowhere to act on it. The `s5-01` label and the worked example in
  `labels/customer/what-is-labelled.md` carry the same reading, so one reading
  sits in three places and was checked in none. Repairing it makes C4 stale and
  costs a re-pass of its 31 `n/a` rows; C4 is the strongest axis of the set,
  caught all eight of the person's fails, so the repair buys accuracy in the rule
  and nothing in the figure. Found by
  `judge/results/customer/labelled-C4-claude-sonnet-5-2026-09-02T141038.json`,
  and `labels/customer/friction-log.md` carries the row.
- **A judgement statement lives in the format document.** `output-format.md`
  rule 11 says of the collapsed line that "scope, outcome and action are usually
  `n/a` on it", and the `Units` section of `rubric/customer.md` says the same.
  Rule 4 of `rubric/how-a-rubric-is-built.md` gives judgement to the rubric
  alone, so one of the two has to give it up.
- **The `rubric_commit` on B1 and C4 rows names an unreachable commit.**
  `labels/customer/items.csv` carries `7213389`, the pre-amend version of
  `47b5f34`; `git diff 7213389 47b5f34` is empty, so the two name the same text.
  `status.py` resolves the object and reports both columns comparable. It becomes
  a real problem only if the object is garbage-collected.

## customer-criterion-v1.0.0

Tagged 2026-09-03 on `ea0788c`. Digest `sha256:2fc4dcea96c3afad`.

The first freeze. `rubric/customer.md` - three levels, nine axes - together
with `docs/output-format.md`, which the axes judge conformance to rather than
restating.

**What it was measured at.** 53 labelled entries across three runs, $3.95 of
judge runs, figures in [`targets.md`](targets.md):

| | |
|---|---|
| In the gate | C4, B2, B3 |
| Out of it | C1, C3, C5, C2, B1, A1, each with a reason |
| Product | 0 of 3 renderings ship whole |
| Instrument | 7.5 of 100 entries let through that a person would send back |

**Known and not repaired.** What this version was wrong about is listed under
v2.0.0 above, which carries the same defects: none of them was repaired by that
version, and the list is kept once rather than twice.

**Results produced before this version** carry no digest and are reported as
unknown by `--verify`. They were made against commits, two of which have since
been amended away, so they cannot be placed either way. That is the reason the
digest exists.
