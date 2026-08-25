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

The verdicts are not repeated here. They live in row `s5-01` of the item table,
which is the only place any item is scored. This section shows how the reasons
behind them are written, one per axis:

- **kind**: a new capability, not a repair.
- **A1**: a summary printed at the end of a run is product surface.
- **C1**: opens on `"Every preview and generate run now ends with a metrics
  report"`, observable, not on what was built.
- **C2**: affects every run, so slot 2 is correctly absent - which the rubric
  calls a pass, not `n/a`.
- **C3**: `"Use this to decide whether the thorough check is worth keeping on"`
  is a consequence, not a restatement.
- **C4**: the report ends every run and there is nothing to switch, so there is
  no action to state.
- **C5**: `"the deeper (thorough) check"` names an internal stage. `preview` and
  `generate` are fine, those are typed by the user; `thorough` is the mode
  value, and a reader who has only used the product cannot tell what it means.

## Run table (level B)

One row per run.

| run                      | B1 action first | B2 grouping and order | B3 length and tone | shippable     | note                                                                                                                                                                                                                                              |
|--------------------------|-----------------|-----------------------|--------------------|---------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| haiku-4-5-out            | ?               | ?                     | ?                  | ?             |                                                                                                                                                                                                                                                   |
| sonnet-5-no-thinking-out | ?               | ?                     | ?                  | ?             |                                                                                                                                                                                                                                                   |
| sonnet-5-out             | fail            | fail                  | fail               | not shippable | The Items wherent grouped in order and the most consequential item wasnt leading.<br/>The length of the items were in general 3-5 sentences, and s5-04, s5-13, s5-15 and s5-21 keep going after their outcome is stated - counted here under B3 rule 1, not on C3. The opening of the document has the "Preview Changelog" note and version, anything else was missing. |
| opus-4-8-out             | ?               | ?                     | ?                  | ?             |                                                                                                                                                                                                                                                   |
| opus-5-no-thinking-out   | ?               | ?                     | ?                  | ?             |                                                                                                                                                                                                                                                   |
| opus-5-out               | ?               | ?                     | ?                  | ?             |                                                                                                                                                                                                                                                   |

## Item table (level C, plus A1 for wrongly included changes)

One row per entry in the customer rendering.
`kind` is `fix`, `feature` or `breaking` and decides how slots 2 to 4 are read.
`A1` is `fail` when the entry should not have appeared at all.

Seeded with the twenty-six entries of `sonnet-5-out`, in document order, as the
first run to label. The other five runs get their rows when they are labelled.

The C3 and C4 columns were re-judged after the friction log was applied to the
rubric: C4 is `n/a` where nothing can be set, C3 asks only whether an outcome
is there. A1, C1, C2 and C5 are untouched from the first pass.

| run          | item  | kind    | A1   | C1 observation | C2 scope | C3 outcome | C4 action | C5 no codebase | shippable | note                                                                                                                                                                                                                                                                                                                                                                                                     |
|--------------|-------|---------|------|----------------|----------|------------|-----------|----------------|-----------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| sonnet-5-out | s5-01 | feature | pass | pass | pass | pass | n/a | fail | no | Reasons for every axis are in the worked example above, not repeated here. |
| sonnet-5-out | s5-02 | feature | pass | fail | pass | fail | pass | fail | no | C1: opens with "Added a categories section to chartula.yaml" (mechanism, not observation). C3: no outcome beyond enumerating settings. C4: names the section and the file, concrete enough to act on. C5: "categories" named as a raw key, not framed in prose. |
| sonnet-5-out | s5-03 | feature | pass | pass | pass | fail | pass | pass | no | C3: "letting you customize behavior without touching code" is slot 1 rephrased, not a step out; strip slot 1 and only "clear error message instead of crashing" is left. The rubric's observed C3 minimal pair. |
| sonnet-5-out | s5-04 | feature | pass | pass | pass | pass | pass | pass | yes | C3: "so you can see the result first" is a consequence one step out - pass on substance; the trailing feedback sentence is counted under B3. C4: both commands are named. |
| sonnet-5-out | s5-05 | feature | pass | pass | pass | fail | pass | pass | no | C3: closing ("instead of being written as separate files...") restates the location contrast, no "so you can..." payoff. C4: the file the texts now live in is named. |
| sonnet-5-out | s5-06 | feature | pass | pass | pass | pass | fail | pass | no | C4: writing to GitHub release notes needs credentials, and the item names none. |
| sonnet-5-out | s5-07 | feature | pass | pass | pass | pass | n/a | pass | yes | C4: n/a - happens with each release, nothing to enable; the file is named. |
| sonnet-5-out | s5-08 | feature | pass | pass | pass | pass | fail | pass | no | C4: "You can now enable a review step" plus "off by default" announces the option and never says where it is turned on. |
| sonnet-5-out | s5-09 | feature | pass | fail | pass | pass | fail | pass | no | C1: opens with "Added an optional second-pass check" - names the mechanism, not what the user observes. C4: "can be turned off" without saying where. |
| sonnet-5-out | s5-10 | feature | pass | fail | pass | fail | n/a | pass | no | C1: opens with "Added a lightweight check" (mechanism). C3: closing ("doesn't use the AI model at all") restates mechanism. C4: n/a - always on, nothing to switch. |
| sonnet-5-out | s5-11 | feature | pass | pass | pass | fail | n/a | pass | no | C3: no forward outcome - ends describing robustness, not what this lets you skip. C4: n/a - automatic. |
| sonnet-5-out | s5-12 | feature | pass | pass | pass | pass | n/a | pass | yes | C4: n/a - all three versions are always generated, nothing to enable. |
| sonnet-5-out | s5-13 | feature | pass | fail | pass | pass | n/a | pass | no | C1: opens with "Reworked how instructions are sent to the AI model" (mechanism). C3: "only rephrases the given facts and never invents details" is what can be trusted - pass on substance; the trailing brevity sentence is B3. C4: n/a. |
| sonnet-5-out | s5-14 | feature | pass | pass | pass | fail | fail | pass | no | C3: closing ("handled gracefully instead of crashing") restates the negative event. C4: generation needs a provider key and this item names no setup - s5-25 mentions it, this one does not. |
| sonnet-5-out | s5-15 | feature | pass | pass | pass | pass | n/a | pass | yes | C3: "durable, machine-readable record that can also feed future outputs" is a real outcome - pass; the format-and-versioning footnote behind it is B3. C4: n/a. |
| sonnet-5-out | s5-16 | feature | pass | pass | pass | fail | fail | pass | no | C3: closing ("default is title plus description") states a setting value, not a consequence. C4: "You can now configure how much information..." without saying where it is configured. |
| sonnet-5-out | s5-17 | feature | pass | pass | pass | fail | n/a | pass | no | C3: "ready to feed into generation" restates internal process purpose, not a user-facing consequence. C4: n/a. |
| sonnet-5-out | s5-18 | feature | pass | pass | pass | pass | n/a | pass | yes | C3: "ensuring nothing in the generated text is made up" is what can be trusted - pass on substance; that it duplicates s5-13's promise is a document-level finding, not C3. |
| sonnet-5-out | s5-19 | feature | pass | fail | pass | fail | fail | pass | no | C1: opens with the internal categorization ("Internal and maintenance-only changes"). C3: no outcome anywhere, closes on an edge-case caveat - fails on substance, not on position. C4: "This can be customized" without saying where. |
| sonnet-5-out | s5-20 | feature | pass | pass | pass | fail | fail | pass | no | C3: closes on a no-op clarification ("no effect if you don't use labels"), no outcome stated. C4: "all configurable" without naming the setting or the labels. |
| sonnet-5-out | s5-21 | feature | pass | pass | pass | pass | n/a | pass | yes | C3: "so the kind of change is never guessed by the model" is an outcome - pass; the breaking-change detail behind it is B3. C4: n/a. |
| sonnet-5-out | s5-22 | feature | pass | fail | pass | fail | n/a | pass | no | C1: opens with condition + fallback mechanism ("falls back to commit messages..."), not an observed problem. C3: closes with negation ("rather than failing"). C4: n/a. |
| sonnet-5-out | s5-23 | feature | fail | pass | pass | fail | n/a | pass | no | A1: describes an internal data-source change (PR API vs. raw commits) with no user-observable output difference - belongs in the technical rendering. C3: closes on a source contrast, not an outcome. C4: n/a. |
| sonnet-5-out | s5-24 | feature | pass | pass | pass | fail | n/a | pass | no | C3: no consequence stated (e.g. the changelog never omits or double-counts changes) - ends on the first-release edge case. C4: n/a. |
| sonnet-5-out | s5-25 | feature | fail | fail | pass | fail | fail | pass | no | A1: internal scaffolding ("added the underlying support..."), not observable behaviour distinct from s5-14. C1: opens naming the internal work. C3: closes on an env-var detail. C4: setup exists (provider key) and neither variable nor reference is named. |
| sonnet-5-out | s5-26 | fix | pass | pass | fail | fail | fail | pass | no | The rubric's own worked example (fix section, v0.1.0). C2: "in some runs" - the hedge the rubric names as the C2 fail pattern. C3: "so text completes properly" restates the negation; the breaking-change fix states no outcome either. C4: "a configurable ceiling" without saying where it is set. |

## Friction log

Where the rubric did not decide the case on its own. One line per occurrence,
written during the pass, applied to the rubric afterwards.

| item  | axis | what was unclear | how it was decided |
|-------|------|------------------|--------------------|
| s5-01 | C4   | For an always-on feature, "where to find it" collapses into slot 1. Is that a pass, or does C4 not apply to features that need no action? | C4 is `n/a` where there is no action. Applied to the rubric. |
| s5-02 to s5-26 | C4 | Same call repeated 23 of 26 times: the item names no location, no setting and no default status, so C4 fails. Read that way the axis fails almost everything and separates nothing. Does C4 need an action only where the user has one to take (opt-in, setting, command), with an explicit "works without setup" counting as satisfying it? | Same decision: the axis judges a withheld action, not a missing sentence. Fails remain where something can be set and the item does not say where. Applied to the rubric. |
| s5-04, s5-13, s5-15, s5-18, s5-21 | C3 | Two different defects fire the same axis. Some of the 20 C3 fails state a real outcome and then trail past it into an edge case, a caveat or a footnote, so they fail on position, not on substance. The decision procedure only covers the other shape (closing restates slot 1 or the mechanism). Is "the item ends on the outcome" part of C3, or is a trailing caveat a B3 length finding? | C3 measures substance only, or no minimal pair can be built for it. The six items pass C3; the trailing sentences are B3 rule 1 and are named in the run-table note. No new axis: one run is too little to justify one. Applied to the rubric. The re-pass then moved five items, not the six first suspected: s5-19, s5-20, s5-24 and s5-25 state no outcome at all and stay `fail`, while s5-04, s5-13 and s5-18 turned out to have the same defect and were not on the list. |
| s5-01 | C5 | `"the deeper (thorough) check"`: `deeper` is explanatory prose, `thorough` is the mode value. The rubric allows product surface a user encounters and forbids internal stage names and configuration values, and this expression is both at once. | `fail`. It survives the paste test in rule 2 - `thorough` could be written into a configuration file as it stands - and `deeper` in front of it does not make the word mean anything to someone who has only used the product. Recorded because the opposite reading is defensible: the item does explain the stage in prose rather than only naming it. |
| s5-02, s5-10, s5-13, s5-22 | C3 | Not independent of C1. Where the item opens on the mechanism, the closing tends to restate the mechanism, and the same defect is counted twice, on C1 and again on C3. The minimal pairs are supposed to keep the axes separable; these items separate nothing. Does C3 judge the closing on its own terms once C1 has already failed? | No rubric change. The claim is that each axis has an item failing it alone, not that no item may fail two: s5-09 fails C1 with C3 passing, s5-03 fails C3 alone. Separability holds on observed items. Double counting changes nothing under the aggregation rule. |

## Missing (level A1, the other half)

Changes that should have appeared in the customer rendering and have no entry.
One row per finding, grouped by run.
If a run has none, put `-` in `change`.

| run | change | why the user would notice |
| --- | --- | --- |
| | | |
