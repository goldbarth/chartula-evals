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

**Known and not repaired.** Three findings sit in [`parked.md`](parked.md)
rather than in this version, the largest being C4's `n/a` example, which names
an entry its own procedure fails. Repairing it edits an axis, which is a major
bump by the rule in the gate, and C4 is the strongest axis of the set as it
stands. It waits for a cycle where the instrument loop is open.

**Results produced before this version** carry no digest and are reported as
unknown by `--verify`. They were made against commits, two of which have since
been amended away, so they cannot be placed either way. That is the reason the
digest exists.
