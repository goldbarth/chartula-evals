# The targets

The figures the stages of [`pipeline.md`](pipeline.md) are measured against.
Decided here and nowhere else, so that a stage can end.

Three figures, in two kinds, and they are never traded against each other:

- **The product figures.** What has to be true of a rendering before it goes
  out, and how good it is otherwise. There are two, and only the first blocks a
  release. This is what the work is for.
- **The instrument figure.** How often the judge reaches the verdict a person
  reached. It is a tool for understanding *why* an entry does not ship. It is
  never the target, and no stage waits on it improving.

Without these figures there is no "good enough", and without "good enough" no
stage can end. Agreement per axis fills the vacuum when they are missing, and
agreement per axis has no ceiling. That is what produced the three days of
2026-08-31 to 2026-09-02.

---

## The product target

Two figures. One of them blocks a release and the other does not.

> **Blocking, and it is zero: no entry states something the fact base does not
> support.** Checked by the faithfulness check inside Chartula, not by an axis
> of this rubric.
>
> **Tracked, and it blocks nothing: the share of entries that go out without a
> person editing them.** Read as a direction across releases. Its current value
> is in [`measurements.md`](measurements.md), which owns where things stand.

**Why the blocking figure is not in this rubric.** An entry that states
something the facts do not support is a different kind of failure from an entry
that is merely thin. The first is a false sentence in a released document; the
second is a weak sentence a reader rewrites. Only the first is worth stopping a
release for, and Chartula already has the check that finds it. The rubric judges
the second kind, which is why it feeds the tracked figure and blocks nothing.

### What this replaced, and why

Until 2026-09-09 there was one product figure:

> A rendering ships when no entry of it fails. **At least four of five
> renderings ship without a person editing them.**

Each half is reasonable alone. Together, at the length these renderings have,
they are not reachable. A rendering carries about 25 entries, so four of five
renderings shipping whole asks for `p^25 >= 0.8`, which is **99.1 per cent of
entries**. The best rendering measured ships 46 per cent. That is not a distance
a prompt closes, and it sits below the resolution of the instrument: *The noise
floor* below says a movement of one is not a result, while a gate of this shape
turns a whole rendering on a single entry.

It also had an effect nobody chose. A shorter rendering fails fewer entries on
every axis at once, and the same prompt has produced 19, 24 and 25 entries, so
an all-or-nothing gate over a document of variable length rewards brevity as
much as it rewards quality.

**This changes no axis**, so it makes no column stale and no result
incomparable. It changes what the figures are for, not what a verdict means.

### Where the old figure stood when it was replaced

On 2026-09-02, over the three labelled runs, judged on C1 to C4:

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

> **A movement of one is not a result.** Measured 2026-09-04: the same release
> rendered twice from the same commit with nothing changed moved three of the
> nine axes by one - B3 from 1 to 0, C3 from 10 to 11, C4 from 1 to 0.

Stage 5 of [`pipeline.md`](pipeline.md) says to read a large movement and ignore
a small one, and until this was measured neither word had a size. No run is
deterministic - `judge/how-the-loop-works.md` says so in as many words - and the
rendering is not stable either: 24 entries and 7,343 characters, then 25 and
8,223, from the same commit.

The document axes, C2 and C5 sat still. What moved, moved by one. So a turn that
moves an axis by one has shown nothing, whichever direction it went, and a turn
aimed at an axis carrying a count of one or two cannot be read at all.

The measurement is in [`measurements.md`](measurements.md), and it removed a
turn from the work the first time it was looked at.

## The spot check

> Every five turns of stage 5, and once more at the end of a turn budget
> whatever the count stands at, one person reads ten entries against the judge's
> verdicts. A judge that has drifted is the only thing that reopens the
> instrument loop.

The count is read off [`measurements.md`](measurements.md), per stage 6 of
[`pipeline.md`](pipeline.md). Twice it has been read late, by three turns and by
five, both times because nobody counted.

**The end of a budget is the second trigger and it is not an interval.** Stage 5
runs to a fixed count of turns, three at present, which never reaches an
interval of five. Without it a phase closes on figures from an instrument
nothing has checked since before the phase began, and those figures are the ones
written into this file as the state at release.

Where it stood on 2026-09-08: two checks read, 50 of 50 and 46 of 49 in
agreement, the second on `sonnet-5-labels-out`. No turn has been taken since, so
none is owed on the interval.

---

## What these figures do not account for

Three things that were not true when the figures above were produced, or were
never true and are not written down anywhere else.

**The judge and the writer are now the same model.** `chartula.yaml` pins
`claude-sonnet-5` and both runners here default to it. A model scoring its own
output is a documented source of inflated agreement, and the figures in this
file were produced when that was not the case: the labelled renderings came from
`claude-opus-4-8` and Opus 5. Nothing here corrects for it, and the correction
is not free - a second judge model cannot be compared with these figures either.

**The prompt is tuned on the only case that is measured.** Every change to
Chartula's customer prompt since the freeze was derived from failures on v0.1.0
of this repository and measured on v0.1.0 of this repository. That is
overfitting by construction, and the usual symptom is a rising overall figure
with a category quietly getting worse underneath it. The three held-out
renderings do not cover it: they are old renderings from other models, not a
second case a prompt change can be tested against. A second release from another
repository is what would, and it is the same fix the case-set limitation below
asks for.

**The judge was validated once, in another epoch.** The agreement figures in
this file are from 2026-09-02, against criterion v1.0.0 and against renderings
written by Opus. The criterion has moved to v2.0.0 and the writer has moved to
`claude-sonnet-5`. Six of the nine axes were out of the gate then and nothing
has re-checked them since. That is what the spot check above is for, and it is
overdue.

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

**A1 has the same defect, found 2026-09-08.** The axis asks whether a reader
could come into contact with a change, and on this case set that question has no
answer for a whole class of them: `feat(output): store all audience texts in
changelog.json` is product surface to whoever consumes that file and an internal
detail to whoever only reads the changelog. A1 failed three entries of
`sonnet-5-place-out` on exactly that, where it had failed none before.

It is the second concrete reason to widen the case set, and it costs more than
C5's version did: C5's overlap only muddies a figure, while A1's decides what
reaches the customer prompt at all. goldbarth/chartula#119 will have to make
that call per change, and nothing here can say whether it was made rightly - see
[`for-chartula.md`](for-chartula.md).
