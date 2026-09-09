# Rubric: the technical rendering

What makes a technical changelog **document** shippable.
Written for the technical audience only.
The customer and product renderings are not covered here.

**Not covered here:** whether the content is factually correct.
That is the faithfulness check's job.
An entry can be perfectly grounded and still fail every axis below.

The reader is a developer reading a repository. They meet the source, so a
class, a method, a file or a configuration key in an entry is not a defect
here, and no axis below asks about one. That is the difference from
`customer.md`, where three format rules forbid exactly those.

The shape this rubric judges conformance to is
[`../docs/output-format.md`](../docs/output-format.md), section
*Technical: `technical/common-changelog`*. It is never restated here, per rule 4
of [`how-a-rubric-is-built.md`](how-a-rubric-is-built.md).

## Levels

Criteria sit on three levels. Each axis belongs to exactly one.
The level tells you which pipeline stage to fix when an axis fails.

| Level             | What it judges                     | Fix belongs in     |
|-------------------|------------------------------------|--------------------|
| **A - Selection** | which changes appear at all        | curation           |
| **B - Document**  | how the release is built           | rendering template |
| **C - Entry**     | the individual line                | prompt             |

An entry that fails level A is removed, not rewritten.
An entry that fails level C is rewritten.
A document that fails level B is re-assembled from unchanged entries.

**Where the axes come from.** Common Changelog carries two rules that judge
rather than shape, and the format document hands both to this rubric: they are
C4 and C5 below. The rest of what a technical reader needs is form, and form is
judged as conformance rather than restated. Rule 3 of
`how-a-rubric-is-built.md` says an axis that can fail nothing is a defect, so
an axis nobody could write a fail example for is not written - which is why the
format's author rule has no axis, as *Level C* says.

---

## Units

The levels apply to different things, so the document has to be cut into units
before anything can be judged. One release of a technical rendering is made of
four kinds of text, and only one of them is an entry.

| Unit                | What it is                                                              | Judged by    |
|---------------------|-------------------------------------------------------------------------|--------------|
| **Release heading** | the line that opens a release, carrying version and date                | B1           |
| **Notice**          | a single-sentence paragraph under the release heading                   | B1, B2       |
| **Group heading**   | the label over a set of entries                                         | B1           |
| **Entry**           | one line reporting one change, with its reference and any authors       | A1, C1 to C5 |

**What makes a piece of text an entry**

1. It reports a change to the product, and it sits under a group heading. If it
   can be read as a row in a table of changes, it is an entry.
2. It carries a description. A line consisting of a reference and nothing else
   is still an entry; it fails C4 and is scored as one.
3. Headings are never entries, whatever they contain. A heading carrying the
   only description of a change is a B1 finding, and the change counts as
   missing at level A.
4. Anything under a group heading that is not an entry - a verification
   paragraph, a nested list, a separator rule, prose about the work - is
   **not** an entry. It gets no row in the entry table and is judged by B2.

**Two cases the runs have already produced**

*The multi-line block.* Where a rendering gives one change a heading and then
several bullets under it, the change has produced no entry at all: the heading
is a B1 finding, the bullets are a B2 finding, and the change counts as
missing at level A only if no other entry carries it.

*The paragraph entry.* A bullet that runs for a paragraph is one entry and is
judged as it stands. That it packs several changes into one line is a C1
finding, not a reason to cut it into several rows.

A run that has no group headings at all is still judged: B1 fails, and
everything a reader would call a change entry is still an entry.

---

## Level A - Selection

### A1 - Belongs in the rendering

**Judges:** whether the release carries the changes this reader needs, and
nothing else.

**Does not judge:** how a change is worded once it is there - that is C1 to C5 -
nor which group it sits in, which is B1. A change can belong here and be
described badly; the entry is then rewritten, not removed.

The axis has two halves and both are judged. An entry that should not be there
is visible in the document. A change that should be there and is missing is not
visible in the document at all - it can only be found against the release's
facts.

The reader is a developer, so the line is not "could a user notice this". It is
whether the change reaches anyone outside the work itself: released behaviour,
an interface something else calls, or what a consumer installs.

**Decision procedure, half one: is anything here that should not be**

1. For each entry, ask what the change does outside the repository it was made
   in: does released behaviour differ, does an interface differ, does what a
   consumer installs differ? If none of those, the entry fails.
2. The question is about the change, not about the words. A restructuring
   described in faultless imperative prose still fails when behaviour is
   identical; a released behaviour change described as a work report passes
   here and fails C4.
3. Test scaffolding, continuous integration, formatting and documentation of
   existing behaviour do not reach the reader and fail rule 1. The format
   document names one route by which such a change can still belong - a label
   on its pull request - and that route is not visible in the document. With no
   facts alongside, rule 1 decides; with facts, a change the facts mark as
   carried in on a label passes.

**Decision procedure, half two: is anything missing**

4. Only when the facts of the release are given alongside the document. Without
   them this half cannot be judged and is not guessed at.
5. Go through the facts, not through the document. For each fact, apply rule 1,
   then find the entry that carries it.
6. A fact that passes rule 1 and has no entry is a fail, and the fact is named.
   Several omissions are one verdict; the axis asks whether the release is
   complete, not how incomplete it is.

**Pass:** an entry for a ceiling now sent on every model call. Released
behaviour differs: long output stops being truncated.

**Fail (present, should not be):** "Add the `Chartula.Cli.Tests` project so CLI
behaviour is covered by tests." Nothing outside the repository differs.

**Fail (absent, should be there):** the facts carry a change that stops the tool
failing when a release has no pull requests attached, and no entry mentions it.

*A restructuring shows both sides: it fails rule 1 when behaviour is identical,
and passes when the move changed what a caller gets - described by what
differs, never by the move.*

---

## Level B - Document

### B1 - Shape of the release

**Judges:** whether the release is built from the heading and the groups the
format defines, in the order it defines, with breaking entries first in their
group.

**Does not judge:** what an entry says, which is level C, nor whether material
that is not an entry has been printed under a group, which is B2. This axis
reads headings and the order of things.

The release heading, the group set, their order and the position of a breaking
entry are defined in
[`../docs/output-format.md`](../docs/output-format.md). They are not repeated
here: a group name written in two documents is a contradiction waiting for one
of them to be edited.

**Decision procedure**

1. Read the release heading and compare it with the shape the format requires:
   its level, its version, its date. A missing release heading is a fail.
2. Read the group headings in order and compare them with the set and the order
   the format defines. A group out of that order is a fail whatever it
   contains.
3. A heading the format does not define is a fail, whether it names a change,
   a category the format does not carry, or anything else. A group with no
   entries is omitted, not printed empty.
4. Within each group, every entry marked breaking stands above every entry that
   is not. One below one is a fail.
5. A document with no group headings at all fails: it cannot satisfy rule 2.

**Pass:** the groups the format defines, in its order, under a release heading
carrying version and date, with the empty ones left out.

**Fail:** `## Features` as the first heading of the rendering, with no release
heading above it - `opus-5-out` line 4. Wrong level, a name the format does not
define, and rule 1 unsatisfied.

**Fail (a heading per change):** `### Feature: Report what a run does and what
it costs` - `sonnet-5-out` line 4. Rule 3: it is a heading the format does not
define. What stands under it is B2's finding.

### B2 - Entries and nothing else

**Judges:** whether what stands under a group heading is entries and nothing
else.

**Does not judge:** the headings themselves and their order, which is B1, nor
whether a single entry is shaped right, which is C1, nor whether an entry
carries its reference, which is C2. This axis reads what is between the
headings.

A release may carry one notice, and the format says where and how long. Every
other paragraph, nested list or rule between the entries is material that
belongs to the work rather than to the changes.

**Decision procedure**

1. Go through the text under each group heading. For each piece that is not an
   entry, ask what it is: a notice the format allows, or something else.
2. A paragraph reporting how the work was verified - builds, test counts, what
   was covered - is a fail. It describes the making of the change.
3. A list nested under an entry is a fail, whatever it contains. So is a
   separator rule between changes, and prose introducing the entries that
   follow.
4. Nothing stands after the last group of a release.
5. A notice that is not directly under the release heading, or that runs longer
   than the format allows, is a fail. A release that carries no notice is not
   failed for that.

**Pass:** four groups, entries under each, nothing between them.

**Fail:** "Verification: build clean (0 warnings, 0 errors); 215 tests passing
(Core 177, Infrastructure 26, Cli 12), 21 new, covering check-fire counts …" -
`sonnet-5-out` line 12. It reports the work, not the change.

**Fail (nested list):** `What changed:` followed by five bullets -
`sonnet-5-no-thinking-out` line 8.

---

## Level C - Entry

An entry is one line: a description, then one or more references, then zero or
more authors. What each of those has to look like is in the format document.
The five axes below ask five different questions about that line, in the order
a reader meets them: is it one line about one change, does it carry its
reference, was the description written or copied, does it say what differs, and
is it in the imperative.

They are five and not one because the repairs differ. A paragraph packing three
changes is repaired by an instruction to the prompt; a missing reference is
repaired by handing the renderer the pull request number at all; a copied title
is repaired by telling the model not to copy. One axis failing on all three at
once would name none of them, and its figure would be decided by whichever of
the three a run happens to break on every entry.

**The format's author rule is not an axis.**
[`../docs/output-format.md`](../docs/output-format.md) requires an author on
every entry of a release written by more than one contributor, and leaves it
off a release written by one. That makes it a property of the release rather
than of the line: it could only be judged as one verdict repeated across every
entry, and on the releases this repository has, all written by a single
contributor, it can fail nothing. Rule 3 of
[`how-a-rubric-is-built.md`](how-a-rubric-is-built.md) says an axis that can
fail nothing is a defect, so it is not written.

### C1 - One change, one line

**Judges:** whether the line reports one change and stays a line.

**Does not judge:** whether that change belongs in the rendering, which is A1;
whether a reference is on it, which is C2; whether the description was copied
from a title, which is C3; whether it says what differs, which is C4; its verb
form, which is C5. Nor anything under a group heading that is not an entry at
all, which is B2.

The two questions are one axis because they break together and are repaired
together: a paragraph is what several changes on one line grow into, and the
same instruction answers both.

**Decision procedure**

1. Does the line report one change? A line reporting several independent
   changes fails. Two facts about one change - what it does and what it
   replaces - are one change.
2. Is it a line rather than a paragraph? A description that runs to several
   sentences of narrative fails; a long single statement does not.
3. Length alone decides neither. Read what the sentences are about: several
   sentences elaborating one change fail rule 2, and one sentence carrying
   three changes fails rule 1.

**Fail:** either question fails.

**Pass:** "Send `MaxOutputTokens` on every model call, so generated text is no
longer truncated at the provider default of 1024 ([#70](…))." One change, one
sentence, whatever its length.

**Fail (several changes in one line):** `opus-5-out` line 6, eight sentences
carrying the run-metrics summary, a new namespace, per-operation token usage and
the pipeline's recording call. It carries its reference, so C2 is not what it
fails.

**Fail (a paragraph on one change):** `opus-4-8-out` line 6, four sentences on
the run-metrics summary and nothing else. One change, and still not a line.

### C2 - Reference on the entry

**Judges:** whether the entry carries at least one reference, in the shape the
format defines, on the entry itself.

**Does not judge:** what the description says, which is C4, nor how many changes
the line carries, which is C1, nor whether a reference standing as its own
paragraph belongs under the group at all, which is B2. A reference printed as
its own paragraph is therefore read twice, by two different questions: B2 asks
what that paragraph is doing there, this axis asks whether the entry it belongs
to carries a reference at all.

The reference is required, and what may stand in it - a pull request, a commit,
an issue, a compare link - is defined in
[`../docs/output-format.md`](../docs/output-format.md) and not repeated here.

**Decision procedure**

1. Read the entry to its end, wrapped lines included. A bullet continuing on the
   next line is one entry.
2. Does it carry at least one reference, in the shape the format defines? None
   is a fail.
3. A reference separated from the entry by a blank line is not on it, whatever
   it points at, and the entry fails. So does one standing after the last entry
   of a group, which could belong to any of them.
4. One is enough. The format allows more and requires one, so an entry naming
   only the pull request passes, and one naming the issue as well passes.

**Fail:** the entry carries no reference of its own.

**Pass:** "Report what a run does and what it costs at the end of every
`preview` and `generate` run ([#66](…))."

**Fail (none at all):** `opus-4-8-out` line 6. No entry of that rendering
carries a reference.

**Fail (off the entry):** `sonnet-5-out` line 6, a bullet with no reference;
`Closes #26 ([PR #66](…))` stands eight lines below it as its own paragraph,
after five further bullets, and could belong to any of them.

### C3 - Description, not a carried-over title

**Judges:** whether the description was written for the changelog or copied from
the pull request or commit that carried the change.

**Does not judge:** whether the description says what differs, which is C4 - a
copied title can say it perfectly well - nor its verb form, which is C5, nor how
many changes the line carries, which is C1.

The format forbids the copy outright. This is its own axis rather than a rule
inside C1 because it is the one form question about an entry that cannot be
answered from the document: the same sentence passes or fails depending on what
the release's titles say.

**Decision procedure**

1. A description carrying a commit-message prefix - `feat:`, `fix(config):` -
   is a copy with its packaging still on, and fails without further comparison.
   No entry of this format carries one.
2. Otherwise the release's pull request and commit titles are needed. Without
   them the axis is not judged and not guessed at: the verdict is `?`, not a
   pass.
3. Find the title of the change the entry reports. Compare it with the
   description, ignoring a bold marker and the reference. Word for word is a
   fail.
4. A description that merely resembles a title - short, imperative, one clause -
   is not a fail. That is the shape the format asks for.

**Fail:** the description repeats a title of the release word for word, or
carries a commit-message prefix.

**Pass:** "Report what a run does and what it costs at the end of every
`preview` and `generate` run ([#66](…))", against a fact base in which #66 is
titled `feat: report what a run does and what it costs`. Same subject, written
out rather than lifted.

**Fail:** `feat: report what a run does and what it costs` -
`sonnet-5-no-thinking-out` line 4, which is that title with its prefix intact.

### C4 - Self-describing

**Judges:** whether the description says what changed without its group heading
and without the reference being followed.

**Does not judge:** whether the change belongs here, which is A1, nor the verb
form, which is C5, nor how many changes the line carries, which is C1, nor
whether the description was copied from a title, which is C3.

This is Common Changelog's rule, named in the format document as judgement
rather than form and left to this rubric.

**Decision procedure**

1. Cover the group heading. Read the description alone.
2. Ask whether a reader can now say what is different about the product. Not
   why it was done, not how - what differs.
3. If the description only makes sense once the heading is put back - the
   reader could not otherwise tell whether the thing was added, repaired or
   removed - it fails.
4. If the description names a subject and nothing about it, it fails.
   "Category handling" and "Configuration" are subjects, not changes.
5. Following the reference is not allowed to rescue it. The reference is where
   a reader goes for detail they chose to want, not for the change itself.

**Pass:** "Read `chartula.yaml`, layered before environment variables, with
every option falling back to its default when no file is present." Under any
heading, it says what differs.

**Fail:** "Update the breaking-change detector." Under **Fixed** it reads as a
repair, under **Changed** as a behaviour change, and on its own it says only
that something was touched.

### C5 - Imperative mood

**Judges:** whether the description opens on a verb in the imperative.

**Does not judge:** anything about what the sentence then says. A description
in flawless imperative mood that says nothing fails C4 and passes here.

This is Common Changelog's second judgement rule, named in the format document
and left to this rubric. It is one question and it is narrow on purpose: an
axis that decides one thing is an axis whose disagreements can be settled.

**Decision procedure**

1. Ignore a bold marker and the colon after it. It labels the entry; the
   description is what follows.
2. Read the first word of the description. Is it a verb that would complete the
   sentence "This release will …"? `Add`, `Fix`, `Send`, `Bump`, `Document`,
   `Remove` all do.
3. A description opening on the same verb in another form fails: `Adds`,
   `Added`, `Adding`. So does one that opens on the subject instead of the
   verb: "The categoriser now matches …".
4. Grammatical shape is the whole question here. Whether the sentence is any
   good is C4's, and whether it belongs is A1's.

**Pass:** "Match the Conventional Commits footer when detecting a breaking
change, so prose that discusses one no longer declares one."

**Fail:** "Adds a `categories` section controlling category order, display
names and breaking-change prominence." Same statement, and it is the shape
every entry of `sonnet-5-out` opens on.


---

## Reference cases

### Minimal pairs

Each axis carries an example that violates **only** that axis. Those are the
calibration set: a judge that cannot separate them is not scoring axes, it is
scoring overall impression.

Written as one base release plus one change per axis, rather than six
near-identical documents, on purpose: copies of the same text drift apart.

**Base document** - passes every axis:

```markdown
## 0.1.0 - 2026-06-14

### Changed

- **Breaking:** Write release notes to the GitHub release itself rather than to
  a separate file, so a project that published them from that file repoints its
  publishing step ([#61](https://github.com/goldbarth/chartula/pull/61))
- Read `chartula.yaml`, layered before environment variables, with every option
  falling back to its default when no file is present
  ([#64](https://github.com/goldbarth/chartula/pull/64))

### Added

- Report what a run does and what it costs at the end of every `preview` and
  `generate` run ([#66](https://github.com/goldbarth/chartula/pull/66))

### Fixed

- Send `MaxOutputTokens` on every model call, so generated text is no longer
  truncated at the provider default of 1024
  ([#70](https://github.com/goldbarth/chartula/pull/70))
- Match the Conventional Commits footer when detecting a breaking change, so
  prose that discusses one no longer declares one
  ([#70](https://github.com/goldbarth/chartula/pull/70))
```

**B1 - shape of the release.** Swap the **Changed** and **Added** groups, so
what is new is printed above what a reader already depends on. Every entry is
unchanged and stays in its own group, none is empty, the breaking entry is
still first inside its group, and nothing but entries stands under any heading:
B2 passes, the entry axes are untouched. It fails on rule 2 alone.

**B2 - entries and nothing else.** Insert under the **Added** entry:

> Verification: build clean, 215 tests passing (21 new), covering per-operation
> token usage and concurrent recording.

The entries are untouched and every heading stays where it was, so B1 passes
and so do C1 to C5 on every line. The inserted paragraph is not an entry, which
is the one thing this pair tests.

**C1 - one change, one line.** Replace the **Added** entry with:

> - Report what a run does and what it costs at the end of every `preview` and
>   `generate` run, add a `categories` section covering category order and
>   display names, and send `MaxOutputTokens` on every model call so long output
>   is no longer truncated
>   ([#66](https://github.com/goldbarth/chartula/pull/66))

Three independent changes on one line. The reference stays where it was, so C2
passes; each of the three reaches the reader, so A1 passes; the verb is
imperative, so C5 passes; each clause says what differs, so C4 passes; and
nothing here is any title of the release, so C3 passes.

**C2 - reference on the entry.** Replace the **Added** entry with the same
sentence, minus its reference:

> - Report what a run does and what it costs at the end of every `preview` and
>   `generate` run

One change on one line, saying what differs, opening on an imperative verb, and
written rather than copied: C1, C3, C4 and C5 pass. The missing reference is
the one thing this pair tests.

**C3 - description, not a carried-over title.** As with A1's missing half, the
change is to what is handed alongside. Replace the second **Changed** entry
with the title the fact base gives its change:

> - Read `chartula.yaml` with sensible defaults
>   ([#64](https://github.com/goldbarth/chartula/pull/64))

The fact base for this pair carries that title without a commit-message prefix,
on purpose: a `feat:` left standing would fail C5 as well and the pair would
stop being minimal. As it is, the line is one change with its reference, it
says what differs, and it opens on an imperative verb, so C1, C2, C4 and C5
pass. Only the facts show that it was lifted.

**C4 - self-describing.** Replace the second **Fixed** entry with:

> - Update the breaking-change detector
>   ([#70](https://github.com/goldbarth/chartula/pull/70))

One change, one line, reference in place, imperative verb, and no title of the
release reads that way: C1, C2, C3 and C5 pass. A reader cannot say what is
different, which is the one thing left.

**C5 - imperative mood.** Replace the first **Fixed** entry with:

> - Sends `MaxOutputTokens` on every model call, so generated text is no longer
>   truncated at the provider default of 1024
>   ([#70](https://github.com/goldbarth/chartula/pull/70))

One verb form, nothing else. The line is still one change, still referenced,
and still says what differs.

**A1, the missing half.** Not a change to the document but to what is handed
with it: the base document plus the fact base for the release, in which one
change that reaches the reader has no entry. Say, a change that stops the tool
failing when a release has no pull requests attached.

**A1, the other half - an entry that should not be there.** Add to the
**Added** group:

> - Add the `Chartula.Cli.Tests` project so CLI behaviour is covered by tests
>   ([#64](https://github.com/goldbarth/chartula/pull/64))

Nothing outside the repository differs, so A1 fails. It is one change on one
line, so C1 passes; the reference is on it, so C2 passes; it is no title of the
release, so C3 passes; it says what differs without its heading, so C4 passes;
it opens on an imperative verb, so C5 passes; and it sits in a group the format
defines, so B1 and B2 are untouched.

### Realistic case

The opening of the technical section of `sonnet-5-out`, lines 4 to 14.
Retained because it shows what a real failure looks like - several axes at
once. Not usable for calibration for exactly that reason.

**Labelled not shippable** (`test-runs/sonnet-5-out.md`). Quoted as a code
block so the shape survives; the three bullets are cut at `...` where the
original runs on, and four bullets between them are left out:

```text
### Feature: Report what a run does and what it costs

- Every `preview` and `generate` run now ends with a run metrics summary covering the rule-based check (runs, findings, claims, token cost), the thorough check ...
- Adds `Chartula.Core/Observability/`: `IRunMetrics` with the `RunMetrics` sink, `NullRunMetrics`, `RunReport`, and `RunReportFormatter`.
- Verification: build clean (0 warnings, 0 errors); 215 tests passing (Core 177, Infrastructure 26, Cli 12), 21 new, ...

Closes #26 ([PR #66](https://github.com/goldbarth/chartula/pull/66))
```

Fails B1: there is no release heading, and `### Feature: …` is a heading the
format does not define. Fails B2: the verification paragraph reports the work,
and the reference stands as its own paragraph after the last bullet. Fails C2
on the bullets that survive as entries: the reference is not on any of them.
Fails C5: `Adds` rather than `Add`.

C1 and C4 are not among them. Each surviving bullet is one change on one line,
and each says what differs without needing its heading, which is the one thing
this rendering does well.

Two axes are not decidable from the excerpt, and both for the same reason:
whether every change of the release is carried, which is A1's second half, and
whether a description was lifted from its title, which is C3.

**Labelled shippable** (written by hand, not produced by a run): the **Added**
and **Fixed** entries of the base document above.

---

## Fact base implications

Two of the axes above cannot be applied to a document alone, and each needs one
thing from the facts:

- A1's second half needs the release's changes, to see what has no entry.
- C3 needs the pull request and commit titles, to see whether one was carried
  over word for word. Its rule 1 is the exception: a commit-message prefix is
  visible in the document and decides on its own.

Each is written to withhold rather than guess when the facts are absent. An
axis that answers from a document it cannot see the answer in is worse than an
axis that says it cannot.

---
