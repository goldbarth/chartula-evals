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

A change appears in the customer rendering only if a user could notice it
without reading the source.

**Decision procedure**

1. Could a user observe this change by using the product - different output,
   different behaviour, a new command, a new setting? If no, exclude.
2. Refactors, test changes, CI changes, dependency bumps without behaviour
   change: exclude.
3. A dependency bump *with* observable behaviour change: include, described by
   the behaviour, not the dependency.
4. If a change is excluded here but a user might still ask about it, it belongs
   in the technical rendering, not here.

**Pass:** a change to how much text the tool generates before stopping.

**Fail:** a change to which internal class performs the categorisation, with
identical output.

---

## Level B - Document

### B1 - Action first

Anything requiring the user to do something appears before anything that does
not. Breaking changes lead the document.

**Decision procedure**

1. Does any item have a non-empty action slot other than "nothing to do"?
2. If yes, does it appear above the informational groups? If no, fail.

**Pass:** breaking changes, then new, then improved, then fixed.

**Fail:** a migration step listed under "Fixed", four groups down.

### B2 - Grouping and order

Items are grouped by kind and the most consequential item leads each group.

**Decision procedure**

1. Groups present in this order: what needs action, new, improved, fixed.
2. Empty groups are omitted, not shown empty.
3. Within a group, the item affecting the most users comes first.

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

The item opens with what the user can observe, not with what was changed.
The cause, if given, follows.

**Decision procedure**

1. Does the first clause describe something a user could have noticed?
2. If the first clause names a change, a setting, or a mechanism: fail.

**Pass:** "Generated text could be cut off mid-sentence because no output length
limit was set."

**Fail:** "There is now a configurable output length limit, so text no longer
gets cut off mid-sentence."

*This is the only axis this example violates: no jargon, outcome stated, length
fine. It fails on order alone.*

### C2 - Scope stated or deliberately absent

The reader can tell whether they were affected.

**Decision procedure**

1. Did this affect everyone, always? If yes, slot 2 is correctly absent.
2. Did it affect a subset? Then the condition is named in plain terms.
3. Is the condition **unknown** - the source data does not say? Then slot 2 is
   omitted entirely and the item is marked for review.
   Vague hedges are a fail, not a fallback.

**Pass (condition known):** "…on releases containing more than about thirty
pull requests."

**Pass (not applicable):** no scope clause at all, because it affected every run.

**Fail:** "…in some runs." - a hedge standing in for a condition nobody looked up.

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

- **Breaking:** Release notes are now written to the GitHub release itself, so
  a project that published them elsewhere has to change where it looks. Point
  your publishing step at the release page.

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

> - **Category order:** The order categories appear in follows your own
>   preference now rather than a fixed one. Set the order you want in the
>   configuration file.

The document then carries an action below two informational groups. Group order
itself stays correct, so B2 is untouched - which is the only way to separate
the two axes, since both of them are about where things sit.

**B2 - grouping and order.** Swap the two items in **What's New**, so the
preview entry comes first. Both are still in the right group, the groups are
still in the right order, and no action has moved: B1 passes, B3 passes, every
item is unchanged. It fails on rule 3 alone, the most consequential item no
longer leading its group.

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

- The minimal pairs are written for every axis except the wrongly-included half
  of A1, which cannot be isolated from C1 - see the note there. C3 has an
  observed pair from `sonnet-5-out`; the rest are constructed.
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
