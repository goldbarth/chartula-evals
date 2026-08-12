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
| **4 - Action**      | usually "nothing to do"             | where to find it, what to enable | the migration step - carries the entry |

Slots 2, 3 and 4 may be absent. Slot 1 never is.

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

### C3 - Outcome beyond the negation

The closing states what the user can now rely on or do. Restating slot 1 in the
negative does not count.

**Decision procedure**

1. Remove slot 1 from the sentence. Does the closing still say something?
2. If the closing is slot 1 with "no longer" in front of it: fail.
3. The outcome names a consequence one step out - what becomes possible, what
   no longer needs checking, what can be trusted.

**Pass:** "…so you can generate notes for a large release without checking the
output for truncation."

**Fail:** "…so text is no longer cut off." - the negation of slot 1.

*This example passes C1, C2, C5 and only fails here.*

### C4 - Action explicit

The reader is never left wondering whether they must do something.

**Decision procedure**

1. Is an action required - update, configuration change, migration? If yes, it
   is stated as the last slot.
2. If no action is required and the item is a fix, "nothing to do" may be
   implicit only when the document says so once, globally.
3. For a feature, slot 4 is where to find it. It is not optional.
4. For a breaking change, slot 4 is mandatory and explicit.

**Pass:** "Existing configuration files keep working; the new setting is
optional."

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

Each axis above carries an example that violates **only** that axis. Those are
the calibration set: a judge that cannot separate them is not scoring axes, it
is scoring overall impression.

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

Fails C1 (opens with the change), C3 (ends on the mechanism), C4 (no action
statement), C5 (identifiers, values, "the categorizer", the format spec).
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

- The minimal pairs exist for C1, C3 and C5. A1/B-level pairs are not written.
- The remaining five runs in `test-runs/` are not labelled.
- Not yet calibrated against a judge. The first calibration run should test
  axis separation on the minimal pairs before anything else.
- Feature and breaking-change items have no labelled reference case yet; the
  slot table is derived, not observed.
