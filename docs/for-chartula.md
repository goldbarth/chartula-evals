# What flows back into Chartula

Findings this evaluation produced that are not fixable here. They are filed as
issues in [Chartula](https://github.com/goldbarth/chartula) and listed here so
that the measurement they came from stays attached to them.

A finding leaves this file when its issue is closed.

## The customer prompt carries none of the output format

**goldbarth/chartula#96** - the output format is left to the model.

`ChangelogPromptBuilder.Prompts.cs` gives the customer audience one sentence:
"Audience: Customer. Focus on what changed for the user in plain language."
Five general rules accompany it - rephrase only, stay sparse, no preamble, one
voice, categories as given - and none of them describes the shape of an entry.

[`output-format.md`](output-format.md) is the specification that issue is
missing. What the labels measured on 2026-09-02, over 53 entries of three runs:

| What the entries do | Count | The rule that forbids it |
|---------------------|-------|--------------------------|
| The closing clause restates the opening rather than stating an outcome: "so text completes properly", "instead of crashing", "rather than failing" | 19 of 53 | rule 8, the four slots in order |
| A raw configuration key or a file path: `Chartula:Labels`, `schemaVersion`, `docs/configuration.md` | 15 of 53 | rules 12 to 14 |
| The entry opens on the mechanism: "Added a ...", "Reworked how ..." | 8 of 53 | rule 7, which names those openings and forbids them |
| An option is announced without the place it is set: "can be turned off", "all configurable" | 8 of 53 | rule 14, the place named as a place |

Every one of those rules existed in writing and none reached the model.

**What has landed against it since.** #99 put the format into the prompt, #112
added the four rules it still left out - the order entries stand in, claims of
degree, the collapsed `Also:` line, nothing after the last group - and #118 said
that the place a setting is reached comes after the outcome rather than instead
of it. Measured on the rendering of 2026-09-08, the first row of that table is
down from 19 of 53 to 3 of 19, and the axes for the other three sit at one, zero
and zero. The issue is still open; what is left of it is the outcome of a fix,
which closes on the negation of its own opening.

The outcome rule is the one exception that needs more than the format
document: `output-format.md` names the four slots but not the test that decides
whether a closing clause is an outcome. That test is in `rubric/customer.md`
under C3 - strike the opening and read what is left, and ask whether it still
tells the reader something they did not already have.

## A change is user-visible because of its type, not because a reader meets it

**goldbarth/chartula#119** - `FactBaseBuilder.IsUserVisible` decides from the
conventional-commit category alone, so everything typed `feat:` reaches the
customer prompt. On v0.1.0 that is 26 of 28 changes, among them
`feat(output): store all audience texts in changelog.json` and
`feat(formatting): consistent formatting and tone per audience`.

The prompt is then told to carry every fact it is given, so it writes about the
tool's own serialisation and the formatting of the changelog itself. Two entries
of the rendering of 2026-09-08 are that, and they cost the coverage axis three
failures where it had none, which alone makes the rendering unshippable.

Not fixable here: the prompt already says to drop a fact the reader cannot come
into contact with, and it cannot apply that to a fact handed to it as
user-visible without overruling the fact base.

The issue is filed against the category being the wrong source for the decision,
which holds for any repository, rather than against a list of changes to
reclassify, which holds only for this one. Why this case set cannot say whether
a given change should have reached the prompt is *The limitation of the case
set* in [`targets.md`](targets.md), which owns that and is not repeated here.

## The fact base has no place for a setting

**goldbarth/chartula#98** - labels are missing from the fact base, so tags
cannot be rendered from anything the faithfulness check would accept. Pulled
forward because the output format specifies tags.

Related, and not filed: an entry cannot say where a setting lives if the fact
base does not carry the place. Where it does not, the correct rendering is to
leave the option out rather than to announce it without a place, and that is a
prompt rule rather than a data one.

## The fact base collapses two states into one

Not filed.

Scope, outcome and action need three states, not two: present, not applicable,
and unknown. Collapsing the last two is what produces hedges like "in some
runs" - the model has no way to say that it was not told.
