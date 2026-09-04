# The targets

The figures the stages of [`pipeline.md`](pipeline.md) are measured against.
Decided here and nowhere else, so that a stage can end.

Two of them are not the same thing and are never traded against each other:

- **The product figure.** How much of a rendering goes out without a person
  editing it. This is what the work is for.
- **The instrument figure.** How often the judge reaches the verdict a person
  reached. It is a tool for understanding *why* an entry does not ship. It is
  never the target, and no stage waits on it improving.

Without these figures there is no "good enough", and without "good enough" no
stage can end. Agreement per axis fills the vacuum when they are missing, and
agreement per axis has no ceiling. That is what produced the three days of
2026-08-31 to 2026-09-02.

---

## The product target

> A rendering ships when no entry of it fails. **At least four of five
> renderings ship without a person editing them.**

Measured on renderings, not on entries, because a release goes out whole.

Where it stood on 2026-09-02, over the three labelled runs, judged on C1 to C4:

| Run | Entries | Ship by the labels | Ship by the judge |
|-----|---------|--------------------|-------------------|
| `opus-5-out` | 25 | 19 | 15 |
| `sonnet-5-out` | 26 | 8 | 7 |
| `sonnet-5-no-thinking-out` | 2 | 2 | 0 |

**Renderings that ship whole: 0 of 3.** Not one of four models produces a
customer changelog that goes out unedited. The reason is not the model: 19 of
53 entries state no outcome and 15 name a configuration key or a file path,
and both are already forbidden in [`output-format.md`](output-format.md),
which Chartula's prompt does not carry. See [`for-chartula.md`](for-chartula.md).

## The instrument target

> The judge lets through **at most 2 of 100** entries a person would have sent
> back.

This is the figure that decides whether a person still has to read the output.

Being too strict is not counted here. A judge that blocks a good entry costs a
turn; a judge that passes a bad one costs the release. The two errors are not
worth the same and are not averaged.

Where it stood on 2026-09-02: **7.5 of 100**, four of 53, all four on C1 and
C3, the two axes that have not settled. The judge errs the other way eleven
times, which is the harmless direction.

## The stage 4 threshold, per axis

> An axis is **in** the gate when it catches at least three quarters of the
> person's fails and produces at most two false fails per fifty entries.
> Otherwise it is **out**, with a written reason, and gates nothing.

Applied to the figures of 2026-09-02:

| Axis | Caught | False | In or out |
|------|--------|-------|-----------|
| C4 | 8 of 8 | 1 | in |
| B2 | 3 of 3 | 0 | in, on three document rows only |
| B3 | 3 of 3 | 0 | in, on three document rows only |
| C1 | 6 of 8 | 9 | out - rule 4 produces nine false fails from one sentence |
| C3 | 13 of 19 | 5 | out - the disagreement runs both ways, so the procedure is at fault rather than a sentence |
| C5 | 4 of 14 | - | out - the corpus defect below |
| C2 | 1 of 1 | 1 | out - one human fail in 53, so the figure measures the majority class |
| B1 | 1 of 2 | - | out - no entry of any run is marked, so there is nothing to catch |
| A1 | 5 of 8 | - | out - one call asks two questions and the judge answers the first, so the second half is unanswered |

**Three in, six out.** An axis that is out is finished, not queued. Out of the
gate does not mean out of the trend, though: see stage 5 of
[`pipeline.md`](pipeline.md).

## The noise floor

> Not yet measured. Until it is, no movement of any size can be called noise.

Stage 5 of [`pipeline.md`](pipeline.md) says to read a large movement and ignore
a small one. Which is which has never been established here. No run is
deterministic - `judge/how-the-loop-works.md` says so in as many words - so a
turn that changes nothing at all still moves the counts, and by an unknown
amount.

It is measured by rendering the same release twice from the same commit with
nothing changed, judging both, and comparing them. Whatever moves is the floor.
It costs one render and it makes every figure after it readable; without it,
"that is within noise" is a guess wearing the word, and it has already been said
twice in this repository about movements of one.

## The spot check

> Every five turns of stage 5, one person reads ten entries against the judge's
> verdicts. A judge that has drifted is the only thing that reopens the
> instrument loop.

---

## The limitation of the case set

Every run describes the same release of Chartula itself. For most axes that is
only a narrowness. For C5 it is a defect in the case: the product whose surface
the axis judges is the tool whose internals the entries name, so `chartula.yaml`
and `GITHUB_TOKEN` are product surface and source at the same time, depending on
who is reading. A changelog about any other repository would not have that
overlap.

C5 can be applied here and the labels are consistent, but its figure measures
the case as much as the axis. A second release from a repository other than
this one is what would fix it, and widening the case set is out of scope for
issue #1 deliberately. This is the first concrete reason to reopen that.
