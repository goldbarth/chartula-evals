# Labels: customer rendering

Measured with the axes from `../rubric-customer.md`.

Values: `pass`, `fail`, `?` (not judged yet), `n/a` (the axis does not apply to this entry).
Item IDs run per run, in the order the entries appear in that run.

The previous table was discarded: it measured feature entries against the fix criteria,
and the axis numbers C1 to C3 mean something else since the rubric was reworked.

## How to label

Fixed before the first row is filled, so that the labels stay comparable
across runs and can serve as a reference set later.

**Aggregation.** An item is `shippable` only if no C axis is `fail`.
No weighting, no overall impression. A single failed axis is enough.
A run is `shippable` only if no B axis is `fail` and no item is `not shippable`.

**Order of work.**

1. One axis at a time, down the whole run, not one item at a time across all
   axes. Judging C1 for twenty-six items in a row compares the same question
   against itself; judging one item across five axes lets the first verdict
   colour the rest.
2. Items before the run. The document axes are only judgeable once the items
   are known, not the other way round.
3. The rubric is not edited during a pass. Friction goes into the friction log
   at the bottom and is applied afterwards, in one go.

**Reasons.** The note quotes the passage the verdict points at, not an
adjective describing it. `"the deeper (thorough) check"` is a reason.
"too technical" is not.

**Item IDs.** Run prefix plus the position of the entry in the rendering,
in document order, counted from one: `s5-01`, `s5-02`.

**Worked example**, first entry of `sonnet-5-out`, as the pattern for the rest:

> - **Run metrics summary**: Every `preview` and `generate` run now ends with a
> metrics report showing how many checks ran, how many issues each found, and how
> many tokens were spent - including whether the deeper (thorough) check caught
> anything the free check missed. Use this to decide whether the thorough check
> is worth keeping on.

| axis | verdict | why                                                                                                                     |
|------|---------|-------------------------------------------------------------------------------------------------------------------------|
| kind | feature | a new capability, not a repair                                                                                          |
| A1   | pass    | a summary printed at the end of a run is product surface                                                                |
| C1   | pass    | opens on `"Every preview and generate run now ends with a metrics report"`, observable, not on what was built           |
| C2   | n/a     | affects every run, so slot 2 is correctly absent                                                                        |
| C3   | pass    | `"Use this to decide whether the thorough check is worth keeping on"` is a consequence, not a restatement               |
| C4   | pass    | where to find it is stated: at the end of every run. Weak, see friction log                                             |
| C5   | fail    | `"the deeper (thorough) check"` names an internal stage; `preview` and `generate` are fine, those are typed by the user |

Verdict: not shippable, on C5 alone.

## Run table (level B)

One row per run.

| run                      | B1 action first | B2 grouping and order | B3 length and tone | shippable     | note                                                                                                                                                                                                                                              |
|--------------------------|-----------------|-----------------------|--------------------|---------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| haiku-4-5-out            | ?               | ?                     | ?                  | ?             |                                                                                                                                                                                                                                                   |
| sonnet-5-no-thinking-out | ?               | ?                     | ?                  | ?             |                                                                                                                                                                                                                                                   |
| sonnet-5-out             | fail            | fail                  | fail               | not shippable | The Items wherent grouped in order and the most consequential item wasnt leading.<br/>The length of the items were in general 3-5 sentences, and s5-15, s5-19, s5-20, s5-21, s5-24 and s5-25 keep going after their outcome is stated - counted here under B3 rule 1, not on C3. The opening of the document has the "Preview Changelog" note and version, anything else was missing. |
| opus-4-8-out             | ?               | ?                     | ?                  | ?             |                                                                                                                                                                                                                                                   |
| opus-5-no-thinking-out   | ?               | ?                     | ?                  | ?             |                                                                                                                                                                                                                                                   |
| opus-5-out               | ?               | ?                     | ?                  | ?             |                                                                                                                                                                                                                                                   |

## Item table (level C, plus A1 for wrongly included changes)

One row per entry in the customer rendering.
`kind` is `fix`, `feature` or `breaking` and decides how slots 2 to 4 are read.
`A1` is `fail` when the entry should not have appeared at all.

Seeded with the twenty-six entries of `sonnet-5-out`, in document order, as the
first run to label. The other five runs get their rows when they are labelled.

| run          | item  | kind    | A1   | C1 observation | C2 scope | C3 outcome | C4 action | C5 no codebase | shippable | note                                                                                                                                                                                                                                                                                                                                                                                                     |
|--------------|-------|---------|------|----------------|----------|------------|-----------|----------------|-----------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| sonnet-5-out | s5-01 | feature | pass | pass           | pass     | pass       | fail      | pass           | no        | Slot 4 gives no location/opt-in, only a usage recommendation for the report                                                                                                                                                                                                                                                                                                                              |
| sonnet-5-out | s5-02 | feature | pass | fail           | pass     | fail       | fail      | fail           | no        | C1: opens with "Added a categories section to chartula.yaml" (mechanism, not observation). C3: no outcome beyond enumerating settings - no stated friction removed. C4: says where but not that omitting the section keeps current behavior. C5: "categories" named as a raw key, not framed in prose.                                                                                                   |
| sonnet-5-out | s5-03 | feature | pass | pass           | pass     | fail       | pass      | pass           | no        | C3: closing ("clear error message instead of crashing") restates the negative event, not a consequence one step out.                                                                                                                                                                                                                                                                                     |
| sonnet-5-out | s5-04 | feature | pass | pass           | pass     | fail       | fail      | pass           | no        | C3: final clause ("clear feedback, including helpful errors...") restates baseline correctness, not a further consequence. C4: no invocation syntax given (e.g. exact command to run) - only what the commands do once run.                                                                                                                                                                              |
| sonnet-5-out | s5-05 | feature | pass | pass           | pass     | fail       | fail      | pass           | no        | C3: closing ("instead of being written as separate files...") restates the location contrast, no "so you can..." payoff. C4: no statement of where changelog.json lives or whether setup is needed.                                                                                                                                                                                                      |
| sonnet-5-out | s5-06 | feature | pass | pass           | pass     | pass       | fail      | pass           | no        | C4: no statement of what to enable or whether this runs automatically by default (token/permission requirement, opt-in status).                                                                                                                                                                                                                                                                          |
| sonnet-5-out | s5-07 | feature | pass | pass           | pass     | pass       | fail      | pass           | no        | C4: no statement of what to enable / default status, or where CHANGELOG.md must live in the repo.                                                                                                                                                                                                                                                                                                        |
| sonnet-5-out | s5-08 | feature | pass | pass           | pass     | pass       | pass      | pass           | yes       |                                                                                                                                                                                                                                                                                                                                                                                                          |
| sonnet-5-out | s5-09 | feature | pass | fail           | pass     | pass       | pass      | pass           | no        | C1: opens with "Added an optional second-pass check" - names the mechanism, not what the user observes (subtler mistakes no longer slipping through).                                                                                                                                                                                                                                                    |
| sonnet-5-out | s5-10 | feature | pass | fail           | pass     | fail       | fail      | pass           | no        | C1: opens with "Added a lightweight check" (mechanism). C3: closing ("doesn't use the AI model at all") restates mechanism, not a consequence. C4: "always on" only in the heading, not stated in the item body.                                                                                                                                                                                         |
| sonnet-5-out | s5-11 | feature | pass | pass           | pass     | fail       | fail      | pass           | no        | C3: no forward outcome - ends describing robustness, not what this lets you skip. C4: no statement that this is automatic/default, no setup mentioned.                                                                                                                                                                                                                                                   |
| sonnet-5-out | s5-12 | feature | pass | pass           | pass     | pass       | fail      | pass           | no        | C4: no statement of where to find each of the three versions or what to enable - only describes the differences between them.                                                                                                                                                                                                                                                                            |
| sonnet-5-out | s5-13 | feature | pass | fail           | pass     | fail       | fail      | pass           | no        | C1: opens with "Reworked how instructions are sent to the AI model" (mechanism). C3: closing ("stays brief instead of being padded out") restates negation. C4: no location/enable statement.                                                                                                                                                                                                            |
| sonnet-5-out | s5-14 | feature | pass | pass           | pass     | fail       | fail      | pass           | no        | C3: closing ("handled gracefully instead of crashing") restates the negative event, not a consequence. C4: no statement of setup needed (e.g. provider key) or what to enable.                                                                                                                                                                                                                           |
| sonnet-5-out | s5-15 | feature | pass | pass           | pass     | fail       | fail      | pass           | no        | C3: item doesn't end on the outcome ("durable, machine-readable record...") - trails into a documentation/versioning footnote. C4: no confirmation this needs no setup, or where in the repo the file appears.                                                                                                                                                                                           |
| sonnet-5-out | s5-16 | feature | pass | pass           | pass     | fail       | fail      | pass           | no        | C3: closing ("default is title plus description") states a setting value, not a consequence. C4: no statement of how/where to change the level of detail.                                                                                                                                                                                                                                                |
| sonnet-5-out | s5-17 | feature | pass | pass           | pass     | fail       | fail      | pass           | no        | C3: "ready to feed into generation" restates internal process purpose, not a user-facing consequence. C4: no location/enable statement.                                                                                                                                                                                                                                                                  |
| sonnet-5-out | s5-18 | feature | pass | pass           | pass     | fail       | fail      | pass           | no        | C3: closing repeats the general grounding promise (duplicate of s5-13's territory) rather than a consequence specific to this item. C4: no location/enable statement.                                                                                                                                                                                                                                    |
| sonnet-5-out | s5-19 | feature | pass | fail           | pass     | fail       | fail      | pass           | no        | C1: opens with the internal categorization ("Internal and maintenance-only changes"), not what the user notices. C3: closes on an edge-case caveat (breaking changes never hidden), not a consequence. C4: "can be customized" without saying where/how.                                                                                                                                                 |
| sonnet-5-out | s5-20 | feature | pass | pass           | pass     | fail       | fail      | pass           | no        | C3: closes on a no-op clarification ("no effect if you don't use labels"), not an outcome. C4: doesn't say which setting or label names control this.                                                                                                                                                                                                                                                    |
| sonnet-5-out | s5-21 | feature | pass | pass           | pass     | fail       | fail      | pass           | no        | C3: item trails past the outcome ("never guessed by the model") into an edge-case detail (breaking-change category retention) instead of ending there. C4: no location/enable or default-confirmation statement.                                                                                                                                                                                         |
| sonnet-5-out | s5-22 | feature | pass | fail           | pass     | fail       | fail      | pass           | no        | C1: opens with condition + fallback mechanism ("falls back to commit messages..."), not an observed problem. C3: closes with negation ("rather than failing") instead of a forward outcome. C4: no confirmation this needs no setup / where it applies.                                                                                                                                                  |
| sonnet-5-out | s5-23 | feature | fail | pass           | pass     | fail       | fail      | pass           | no        | A1: describes an internal data-source change (PR API vs. raw commits) with no described user-observable output difference - belongs in technical rendering. C3: closes on a source contrast, not an outcome. C4: no location/enable statement.                                                                                                                                                           |
| sonnet-5-out | s5-24 | feature | pass | pass           | pass     | fail       | fail      | pass           | no        | C3: no consequence stated (e.g. changelog never omits/double-counts changes) - ends on the first-release edge case instead. C4: no location/enable statement.                                                                                                                                                                                                                                            |
| sonnet-5-out | s5-25 | feature | fail | fail           | pass     | fail       | fail      | pass           | no        | A1: describes internal scaffolding ("added the underlying support..."), not an observable behavior distinct from the separate "Real changelog generation" item - belongs in technical rendering. C1: opens naming the internal work directly. C3: closes on an implementation/security detail (env-var key handling), not a consequence. C4: setup mentioned but no specific variable name or reference. |
| sonnet-5-out | s5-26 | fix     | pass | pass           | fail     | fail       | fail      | pass           | no        | This is the rubric's own worked example (fix section, v0.1.0). C2: "in some runs" — the hedge the rubric names as the C2 fail pattern. C3: "so text completes properly" restates the negation; no outcome stated for the breaking-change fix either. C4: no action statement for either sub-item.                                                                                                        |

## Friction log

Where the rubric did not decide the case on its own. One line per occurrence,
written during the pass, applied to the rubric afterwards.

| item  | axis | what was unclear | how it was decided |
|-------|------|------------------|--------------------|
| s5-01 | C4   | For an always-on feature, "where to find it" collapses into slot 1. Is that a pass, or does C4 not apply to features that need no action? | C4 is `n/a` where there is no action. Applied to the rubric. |
| s5-02 to s5-26 | C4 | Same call repeated 23 of 26 times: the item names no location, no setting and no default status, so C4 fails. Read that way the axis fails almost everything and separates nothing. Does C4 need an action only where the user has one to take (opt-in, setting, command), with an explicit "works without setup" counting as satisfying it? | Same decision: the axis judges a withheld action, not a missing sentence. Fails remain where something can be set and the item does not say where. Applied to the rubric. |
| s5-15, s5-19, s5-20, s5-21, s5-24, s5-25 | C3 | Two different defects fire the same axis. Six of the 20 C3 fails state a real outcome and then trail past it into an edge case, a caveat or a footnote, so they fail on position, not on substance. The decision procedure only covers the other shape (closing restates slot 1 or the mechanism). Is "the item ends on the outcome" part of C3, or is a trailing caveat a B3 length finding? | C3 measures substance only, or no minimal pair can be built for it. The six items pass C3; the trailing sentences are B3 rule 1 and are named in the run-table note. No new axis: one run is too little to justify one. Applied to the rubric. |
| s5-02, s5-10, s5-13, s5-22 | C3 | Not independent of C1. Where the item opens on the mechanism, the closing tends to restate the mechanism, and the same defect is counted twice, on C1 and again on C3. The minimal pairs are supposed to keep the axes separable; these items separate nothing. Does C3 judge the closing on its own terms once C1 has already failed? | No rubric change. The claim is that each axis has an item failing it alone, not that no item may fail two: s5-09 fails C1 with C3 passing, s5-03 fails C3 alone. Separability holds on observed items. Double counting changes nothing under the aggregation rule. |

## Missing (level A1, the other half)

Changes that should have appeared in the customer rendering and have no entry.
One row per finding, grouped by run.
If a run has none, put `-` in `change`.

| run | change | why the user would notice |
| --- | --- | --- |
| | | |
