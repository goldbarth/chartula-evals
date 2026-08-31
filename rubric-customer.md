# Rubric: the customer rendering

What makes a customer-facing changelog **document** shippable.
Written for the customer audience only.
The technical and product renderings are not covered here.

**Not covered here:** whether the content is factually correct.
That is the faithfulness check's job.
An entry can be perfectly grounded and still fail every axis below.

## Levels

Criteria sit on three levels. Each axis belongs to exactly one.
The level tells you which pipeline stage to fix when an axis fails.

| Level             | What it judges                | Fix belongs in     |
|-------------------|-------------------------------|--------------------|
| **A - Selection** | which changes appear at all   | curation           |
| **B - Document**  | order, grouping, length, tone | rendering template |
| **C - Item**      | the individual entry          | prompt             |

An item that fails level A is removed, not rewritten.
An item that fails level C is rewritten.
A document that fails level B is re-assembled from unchanged items.

A1 judges the subject of an entry, C5 its language. The two are independent:
a change that is internal in substance can be described in faultless customer
language, and then A1 fails while C5 passes. Failing A1 does not drag C5 with
it, and the item is removed rather than rephrased.

---

## Units

The levels apply to different things, so the document has to be cut into units
before anything can be judged. A customer rendering is made of four kinds of
text, and only one of them is an item.

| Unit                | What it is                                                                                        | Judged by    |
|---------------------|---------------------------------------------------------------------------------------------------|--------------|
| **Header**          | version, date, one sentence on what the release is about                                          | B3 rule 4    |
| **Group heading**   | the label over a set of items - what needs action, new, improved, fixed                           | B1, B2       |
| **Item**            | one entry reporting one change, built from the four slots                                         | A1, C1 to C5 |
| **Connective text** | prose that is not about one change: a lead-in, a closing note, a remark on the release as a whole | B1, B2, B3   |

**What makes a piece of text an item**

1. It reports a change to the product, and it is about that change rather than
   about the release. If it can be read as a row in a table of changes, it is
   an item.
2. It carries slot 1. An entry with no observable event is still an item; it
   fails A1 or C1 and is scored as one.
3. Headings are never items, whatever they contain. A heading that carries the
   only description of a change is a B2 finding, and the change counts as
   missing at level A.
4. A paragraph about several changes at once, about something that was *not*
   changed, or about the release as a whole is connective text. It gets no row
   in the item table and is judged at level B.

**Two cases the runs have already produced**

*One entry, two changes.* An entry that reports two unrelated changes stays one
item and is judged as it stands - the axes are applied to the entry, not to
each change inside it. That an entry bundles two changes is a B2 finding, since
grouping is a document-level property.

*The collapsed line.* B3 rule 2 asks for minor changes to be gathered into a
single closing line. That line is an item: it reports changes, a reader reads
it as content, and its slot 1 covers the group it stands for. C2 to C4 are
usually `n/a` on it, which is the point of collapsing them.

A run that has no group headings at all is still judged: B1 and B2 fail, and
every entry is still an item.

---

## Level A - Selection

### A1 - Product surface relevance

The rendering carries every change the reader could notice, and nothing else.

The axis has two halves and both are judged. An entry that should not be there
is visible in the document. A change that should be there and is missing is not
visible in the document at all - it can only be found against the release's
facts, and it is the more expensive omission, because a reader cannot ask about
something they were never told.

**Decision procedure, half one: is anything here that should not be**

1. For each entry, could a reader observe this change by using the product -
   different output, different behaviour, a new command, a new setting? If no,
   the entry fails.
2. Refactors, test changes, CI changes, dependency bumps without behaviour
   change: they do not belong here.
3. A dependency bump *with* observable behaviour change does belong, described
   by the behaviour, not the dependency.
4. A change excluded here belongs in the technical rendering, not nowhere.

**Decision procedure, half two: is anything missing**

5. Only when the facts of the release are given alongside the document. Without
   them this half cannot be judged and is not guessed at.
6. Go through the facts, not through the document. For each fact a reader could
   observe, find the entry that carries it. Reading the document and asking
   whether it looks complete finds nothing - an omission has no text to notice.
7. A fact with no entry is a fail, and the fact is named. Several omissions are
   one verdict; the axis asks whether the rendering is complete, not how
   incomplete it is.
8. A fact that no reader could observe needs no entry. Its absence is correct.

**Pass:** a change to how much text the tool generates before stopping, carried
by an entry.

**Fail (present, should not be):** an entry about which internal class performs
the categorisation, with identical output.

**Fail (absent, should be there):** the facts carry a change that stops the tool
failing when a release has no pull requests attached, and no entry mentions it.

---

## Level B - Document

### B1 - Action first

An entry that asks something of the reader stands above every entry that does
not. Breaking changes lead the document.

An entry asks something when ignoring it costs the reader: a migration, a
rename they have to follow, a setting they must set for things to keep working.
Telling a reader where a new feature lives, or how to reach it, is not asking
something of them - that is C4's subject, and an optional setting is not an
obligation.

**Decision procedure**

1. Go entry by entry. Group headings decide nothing here: a group called "What
   needs action" can stand at the top while an entry that asks something sits
   three groups below it, and that is the failure this axis is for.
2. Mark every entry that asks something of the reader, in the sense above.
3. No marked entry: pass. There is no order to get wrong.
4. Every marked entry must stand above every unmarked one. One marked entry
   below one unmarked entry is a fail, whichever groups the two sit in.
5. A breaking change is always marked, and comes first of all.

**Pass:** the only entry carrying a migration is the first entry of the
document, under the group for it.

**Fail:** an entry saying the old configuration section stops being read, placed
under "What's Changed", below two entries that ask nothing.

### B2 - Grouping and order

Groups are the ones the format defines, in the order it defines, and the ones
with nothing in them are not there.

**Decision procedure**

1. Groups appear in this order: what needs action, new, changed, fixed. A group
   out of order is a fail whatever it contains.
2. A group with no entries is omitted, not printed empty.
3. No group outside the defined set.

This axis does not judge which group an entry belongs in when the entry asks
something of the reader - that is B1. It also no longer judges the order of
entries inside a group: see the note in Open.

**Pass:** what needs action, then new, then fixed, with changed absent because
the release has none.

**Fail:** fixes printed above the new entries.

### B3 - Length and tone

The document is scannable and does not oversell.

**Decision procedure**

1. Each item is one or two sentences. Three is the ceiling and needs a reason.
   Sentences that follow the outcome count here: C3 is satisfied once the
   outcome is stated, and what trails behind it is a length problem.
2. Minor items are collapsed into a single closing line rather than listed
   individually.
3. No superlatives, no marketing adjectives, no exclamation marks.
   "Faster" needs a number or it is not claimed.
4. The document opens with version, date, and one sentence on what this release
   is about.

**Pass:** "Generation is roughly twice as fast on releases with more than 50
pull requests."

**Fail:** "We've completely reimagined generation performance - it's blazingly
fast now!"

---

## Level C - Item

Every item is built from four slots, in this order.
The slots are the same for every change type; only what fills them differs.

| Slot                | Fix                                 | Feature                          | Breaking change                        |
|---------------------|-------------------------------------|----------------------------------|----------------------------------------|
| **1 - Observation** | what went wrong, as the user saw it | what is now possible             | what no longer works as before         |
| **2 - Scope**       | when it occurred                    | who it is for, if not everyone   | who is affected                        |
| **3 - Outcome**     | what you can now rely on            | the detour that disappears       | secondary, may be omitted              |
| **4 - Action**      | usually "nothing to do"             | what to set, where, if anything  | the migration step - carries the entry |

Slots 2, 3 and 4 may be absent. Slot 1 never is.
Slot 4 is absent when there is nothing to set: see C4.

### C1 - Observation leads

The item opens with what the reader can observe. What was built, changed or
configured comes later, or not at all.

What counts as an observation depends on the change type, and it is the same
thing slot 1 of the item is for:

| Change type     | The observation is                                     |
|-----------------|--------------------------------------------------------|
| Fix             | what went wrong, as the user ran into it               |
| Feature         | what the reader can now do or now sees                  |
| Breaking change | what no longer works the way it did                     |

A feature does not need a problem. "You can now preview a release before
anything is published" opens on an observation: the reader can do it, and can
see that they can. Requiring a symptom there is a misreading of this axis.

**Decision procedure**

1. Ignore a bold label and the colon after it. It names the entry, it is not
   the opening of the sentence, and the format specifies it that way. Judge the
   first clause of the text that follows it.
2. Does that clause describe something the reader can observe - a thing that
   happens to them, something they can now do, something they ran into? If yes,
   pass.
3. If it instead names what was built or altered - a component, a setting, an
   implementation, "we added", "support was introduced" - fail.
4. The test: could the clause be rewritten as "you can now …" or "X happened to
   you when …" without inventing anything that is not already in it? If yes, it
   is an observation, whatever its grammatical shape.

**Pass (fix):** "Generated text could be cut off mid-sentence because no output
length limit was set."

**Pass (feature):** "You can see the finished notes before anything is written
or published."

**Pass (feature, stated as a property):** "Technical, customer and product notes
are written from the same set of facts." The reader sees the three renderings;
this says what is true of them now.

**Fail:** "There is now a configurable output length limit, so text no longer
gets cut off mid-sentence."

*This is the only axis that example violates: no jargon, outcome stated, length
fine. It fails on order alone.*

**Fail (feature):** "Support for previewing a release was added." Same fact as
the feature pass above, opened on the building of it.

### C2 - Scope stated or deliberately absent

The reader can tell whether they were affected.

**Decision procedure**

1. Did this affect everyone, always? If yes, slot 2 is correctly absent.
2. Did it affect a subset? Then the condition is named in plain terms.
3. A condition may be qualitative. "On longer releases" and "if you publish
   from a fork" name a condition; they do not become hedges for lacking a
   number. What fails is a phrase that names no condition at all.
4. Is the condition **unknown** - the source data does not say? Then slot 2 is
   omitted entirely and the item is marked for review.
   Vague hedges are a fail, not a fallback.

**Pass (condition known):** "…on releases containing more than about thirty
pull requests."

**Pass (not applicable):** no scope clause at all, because it affected every run.

**Fail:** "…in some runs." - names no condition at all: every run is some run.
Contrast rule 3, where "on longer releases" passes although it carries no
number.

### C3 - Outcome present

The item says what the user can now rely on or do.
Anywhere in the item, not necessarily at the end.

**Decision procedure**

1. Does the item name an outcome at all - what becomes possible, what no longer
   needs checking, what can be trusted, what detour disappears? If no, fail.
2. A candidate that only restates slot 1 is not an outcome. Two shapes recur:
   slot 1 with "no longer" or "instead of" in front of it, and a repetition of
   the mechanism the item already described. Both are fail.
3. Position is not this axis. An item that names its outcome and then keeps
   going - an edge case, a caveat, a footnote - passes C3. The trailing
   sentences are a length finding under B3 rule 1.
4. One outcome is enough. C3 does not ask whether it is the strongest one
   available.

**Pass:** "…so you can generate notes for a large release without checking the
output for truncation."

**Pass (outcome not last):** "…so you see the real result before anything is
written, and the same flags apply as in a normal run."
The outcome is stated; what follows it is B3's problem, not C3's.

**Fail:** "…so text is no longer cut off." - the negation of slot 1.

**Observed pair**, `sonnet-5-out` item `s5-03`, the same violation from a real
run rather than constructed:

> Configuration mistakes now show a clear error message instead of crashing.

The item names no outcome anywhere. Its only candidate, "instead of crashing",
restates the negative event of slot 1. C1, C2, C4 and C5 all pass on that item.

### C4 - Action explicit

The reader is never left wondering whether they must do something.
The axis judges a withheld action, not a missing sentence.

**Decision procedure**

1. Does this change give the user anything to do or decide - a migration, a
   setting, an opt-in, a command to run, a place they have to go to reach it?
2. If not - it runs by itself, always, with nothing to configure - C4 is
   **n/a**. Not a pass, not a fail. There is no action to withhold, and a line
   saying so is optional, not required.
3. If yes, the action is the last slot, concrete enough to act on: the setting
   by its plain name, the command, the place. Announcing that an option exists
   without saying where it is set is a fail.
4. C4 asks for the plain name, never for the key. "How much detail feeds the
   facts is set in the configuration file" satisfies this axis; the raw key
   does too, but fails C5 for it. The two axes are satisfiable at once, and an
   item that names the setting in prose passes both. Where an item gives only
   the key, C4 passes and C5 fails, and the finding belongs to C5.
5. For a breaking change, slot 4 is mandatory and explicit. Never n/a.
6. For a fix whose only action is "nothing to do", C4 is n/a, provided the
   document says so once, globally.

**Pass:** "Existing configuration files keep working; the new setting is
optional."

**Pass (stated redundantly):** "No configuration change is needed." - allowed
where nothing has to be done, never demanded.

**n/a:** a metrics summary printed at the end of every run. It is on, it is
where the run ends, and there is nothing to switch.

**Fail (option withheld):** "How much detail each entry carries can be
customised." - the reader now knows a setting exists and not where it is.

**Fail:** a breaking change described entirely in slots 1–3, with no statement of
what to change.

### C5 - No codebase knowledge required (cross-slot)

Applies to the whole item, not to one slot.
Understandable to someone who uses the product and has never seen its source.

**Allowed - product surface:** settings, commands, features and outputs a user
encounters by using the tool; version numbers; dates; commands the user actually
types.
Settings are referred to in prose ("the output length limit"), not by key.

**Not allowed - internals:** code-style identifiers; concrete configuration
values; internal component or stage names; file, class or module references;
format specifications.

**Decision procedure**

1. Could a user who has only ever used the product know what this refers to?
   If no, fail.
2. If unsure: could the expression be pasted into a configuration file or source
   file as written? If yes, fail - **unless** it is a version number, a date, or
   a command the user is meant to type.
3. Describing what changed in plain language is not an internal reference.
   "No output length limit was set" passes.
   "`max_tokens` was omitted" fails.

**Fail (this axis only):** "Generated text could be cut off mid-sentence because
`llm.maxOutputTokens` defaulted to 1024, so you can now generate a large release
without checking the output for truncation."

*Correct order, scope handled, real outcome - jargon alone sinks it.*

---

## Reference cases

### Minimal pairs

Each axis carries an example that violates **only** that axis. Those are the
calibration set: a judge that cannot separate them is not scoring axes, it is
scoring overall impression.

The item-level pairs sit with their axes above: C1 at its Fail example, C2 at
the hedge, C3 with the observed pair from `s5-03`, C4 at the withheld option,
C5 at the jargon example.

The document-level pairs cannot be single sentences, because A1 and B1 to B3
judge a whole document. They are given below as one base document that passes
every axis, plus one change per axis. Written as deltas rather than as four
near-identical documents on purpose: five copies of the same text drift apart,
which is the failure this rubric already had once.

**Base document** - passes A1, B1, B2, B3 and every C axis on every item:

```markdown
## 0.1.0 - 2026-06-14

The first release you can point at a repository and get release notes out of.
Nothing here needs a configuration change unless the entry says so.

### What needs action

- **Breaking:** Release notes published anywhere but the GitHub release itself
  stop being updated, so a project that read them from a file no longer sees
  new ones. Point your publishing step at the release page.

### What's New

- **Three audiences from one source:** Technical, customer and product notes
  are written from the same set of facts, so they cannot disagree about what
  changed.
- **Preview before publishing:** You can see the finished notes before anything
  is written or published, so the first real result is not the one your users
  read. Ask for a preview instead of a full run.

### Bug Fixes

- **Text no longer cut off:** Generated text could stop mid-sentence on longer
  releases, because no output length limit was set. There is a limit now, so
  you can generate notes for a large release without checking the end of the
  text.
```

**B1 - action first.** Add to a new **What's Changed** group, below What's New:

> - **Label rules moved:** A project that steers curation with labels has to
>   move those rules into the new section of the configuration file. The old
>   section stops being read after this release.

An entry that asks something of the reader then sits below two entries that ask
nothing. The groups themselves stay in the defined order and none is empty, so
B2 is untouched - which is the only way to separate the two axes, since both of
them are about where things sit.

**B2 - grouping and order.** Swap the **What's New** and **Bug Fixes** groups,
so the fixes are printed first. Every entry is unchanged and stays in its own
group, no group is empty, and the only entry that asks anything of the reader
is still the first in the document: B1 passes, B3 passes, the item axes are
untouched. It fails on rule 1 alone.

**B3 - length and tone.** Replace the Bug Fixes entry with:

> - **Text no longer cut off:** Generated text could stop mid-sentence on
>   longer releases, because no output length limit was set. There is a limit
>   now, so you can generate notes for a large release without checking the end
>   of the text. The limit can be raised if your releases are unusually large.
>   Truncation is completely gone and generation is blazingly reliable now.

Four sentences and a superlative without a number. C3 still passes - the
outcome is stated and what trails behind it is B3's problem, not C3's - and
that is exactly what this pair tests.

**A1 - selection.** Not a change to the document but to what is handed with it:
the base document plus the fact base for the release, in which one user-visible
change has no entry. Say, a change that stops the tool failing when a release
has no pull requests at all. Every entry present is correct; the question is
only whether the missing one is noticed.

That is the expensive half of A1, and the half a judge is actually needed for.
The other half - an entry that should not be there - has no minimal pair, and
the labelled runs say why: an internal change cannot produce an observable
opening, so it fails C1 along with A1 every time. `o5-10`, `o5-17`, `o5-25` and
`s5-23` all show the pattern. A pair isolating A1 from C1 would have to be
written against the grain of both axes, and would test nothing a judge will
meet.

### Realistic case

The fix section of the v0.1.0 customer rendering.
Retained because it shows what a real failure looks like - several axes at once.
Not usable for calibration for exactly that reason.

**Labelled not shippable** (Haiku 4.5, `test-runs/haiku-4-5-out.md`, lines 260 to 264):

Quoted verbatim, as a code block rather than a blockquote so the line breaks
survive. The breaks inside `defaulting` and `Conventional` are the run's own
output, not a copy error.

```text
Fixed output truncation by setting `max_tokens` on LLM calls. Previously omitted, it defaulted to 1024 per provider, cutting off all three audience texts mid-word. Now configurable via `llm.maxOutputTokens`, default
ing to 16000.

Fixed false breaking-change detection. The categorizer was matching `BREAKING CHANGE` as a case-insensitive substring anywhere in the PR body, so prose discussing breaking changes declared one. Now matches the Conve
ntional Commits footer format: uppercase, start of line, colon-terminated.
```

Fails C1 (opens with the change), C3 (names no outcome, only the mechanism),
C5 (identifiers, values, "the categorizer", the format spec).
C4 is not among them: the first item does say where the ceiling is set, the
second has nothing to set. That the first says it as a configuration key is
C5's finding, not C4's.
Scope is absent in both items without it being clear whether that is
*not applicable* or *unknown*.

**Labelled shippable** (written by hand, not produced by a run):

> - Generated text could be cut off mid-sentence on longer releases; there is now
> a ceiling with a higher default, so you can generate notes for a large release
> without checking the output for truncation. No configuration change is needed.
>
> - Changes that merely mentioned breaking changes in their description were
> sometimes labelled as breaking themselves; only an actual breaking-change
> declaration is recognised now, so the notes no longer warn about breaks that
> are not there.

---

## Fact base implications

Slots 2, 3 and 4 need three distinguishable states in the fact base:
**present**, **not applicable**, **unknown**.

Collapsing the last two into one empty field is what produces hedges like
"in some runs" - the formulator finds nothing, cannot tell that nothing is the
correct answer, and fills the gap. *Unknown* omits the slot and flags the item.
*Not applicable* omits the slot silently.

---

## Open

Decided against the material there was at the time, and meant to be argued
with. Anything here is a reasonable place for someone else to disagree from
experience, and several of these belong in configuration rather than in a
rubric once there is a reason to make them settable.

- The minimal pairs are written for every axis except the wrongly-included half
  of A1, which cannot be isolated from C1 - see the note there. C3 has an
  observed pair from `sonnet-5-out`; the rest are constructed.
- C2 allows a qualitative condition. Two runs disagreed with each other on
  "on longer releases" before this was written down, which is what an
  undecided rule looks like from the outside. Whether a condition should have
  to be checkable by the reader - a number, a name, a version - is the open
  half.
- Two cells of the separation set are unstable across four runs, both on the
  breaking-change entry: C1 and C3. C1 was the entry's fault and the entry is
  fixed. C3 is the contradiction below, still open.
- B2 no longer asks whether the most consequential entry leads its group. Two
  separation runs showed why: which of two entries is more consequential is not
  derivable from the text, so the axis could not be applied by a judge, and
  arguably not by a person either. It returns if a criterion is found that can
  be read off the entry rather than guessed at.
- The slot table calls the outcome "secondary, may be omitted" for a breaking
  change, while C3 fails an item that names no outcome at all. Nothing in the
  runs has hit it yet, since v0.1.0 has no breaking change.
- C4 and C3 were sharpened after the first pass over `sonnet-5-out`, and both
  columns have been re-judged since: C4 fails fell from 23 to 9, C3 fails from
  20 to 15, and 6 of 26 items are shippable instead of 1. A1, C1 and C2 are
  still first-pass verdicts; of C5 only `s5-01` was revisited, and it is now a
  fail on `(thorough)` as a mode value.
- Whether writing to GitHub (s5-06) and generating text (s5-14) count as
  actions the item must state, when the credential is set up once and not per
  release, is the next C4 borderline. Both are currently `fail`.
- Not yet calibrated against a judge. The first calibration run should test
  axis separation on the minimal pairs before anything else.
- Feature and breaking-change items have no labelled reference case yet; the
  slot table is derived, not observed.
