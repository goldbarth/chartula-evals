# What flows back into Chartula

Findings this evaluation produced that are not fixable here. They are filed as
issues in [Chartula](https://github.com/goldbarth/chartula) and listed here so
that the measurement they came from stays attached to them.

A finding leaves this file when its issue is closed.

## The customer prompt carries none of the output format

**goldbarth/chartula#96** - the output format is left to the model.

When it was filed, `ChangelogPromptBuilder.Prompts.cs` gave the customer audience
one sentence: "Audience: Customer. Focus on what changed for the user in plain
language." Five general rules accompanied it - rephrase only, stay sparse, no
preamble, one voice, categories as given - and none of them described the shape
of an entry.

[`output-format.md`](output-format.md) is the specification that issue was
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
of it.

**What is left of it is the first row of that table, and it is the largest thing
left in this project.** On `sonnet-5-labels-out`, the newest rendering, 10 of 24
entries still state no outcome the reader can use, and nine of the thirteen
entries held back from shipping fail on that and nothing else. The other three
rows of the table are down to one, zero and zero.

The shape that remains is narrow: an entry about a fix that closes on the
negation of its own opening - "no longer gets cut off", "never skipped for that
reason". A person read five of those failures back in the spot check of
2026-09-08 and agreed with four, so they are real rather than an artefact of an
axis that gates nothing.

This is not a background item waiting behind the others. It is the next turn of
the production loop, and `docs/plan.md` carries it as such.

The outcome rule is the one exception that needs more than the format
document: `output-format.md` names the four slots but not the test that decides
whether a closing clause is an outcome. That test is in `rubric/customer.md`
under C3 - strike the opening and read what is left, and ask whether it still
tells the reader something they did not already have.

**The material for that sentence is in the fact base, so this is the prompt and
not the curation.** Checked on 2026-09-09, free, against
`test-runs/v0.1.0-facts.md`: for each of the nine entries of
`sonnet-5-labels-out` that fail on C3 and nothing else, does the outcome the
entry is missing stand in the facts at all?

| Entry | Subject | PR | The outcome in the facts |
|-------|---------|----|--------------------------|
| `s5l-01` | API key required | #41 | "API keys are read from environment/config, never hardcoded"; "model + provider selectable via config" |
| `s5l-04` | Configuration file | #64 | "A present config refines behavior; it is never required"; env overrides YAML |
| `s5l-06` | Fact base depth | #50 | "Lets a maintainer choose how much source material feeds the fact base, to fit their team's PR style" |
| `s5l-08` | Label rules | #46 | "steer curation with GitHub labels ... without touching code"; an unknown category fails at startup with a clear error |
| `s5l-17` | Linked issues | #48, #49, #50 | **not there.** The facts say closing keywords are parsed and that the deepest depth feeds them in. What the reader gets is nowhere |
| `s5l-18` | Fallback for missing PR data | #44 | "never hard-fails solely because PR discipline is imperfect"; "uses the best available source" |
| `s5l-19` | Grouped by pull request | #43 | thin: de-duplication by number and a link per pull request are more than slot 1; the rest of that section is slot 1 |
| `s5l-21` | Empty release | #44, #52 | "Empty release -> empty set, never an exception"; "an empty fact base makes no call at all" |
| `s5l-22` | Configuration errors | #64, #46, #50 | the run stops at startup rather than partway, and the message names the valid values |

Eight of nine. The sentence the entries do not write can be written from the
material they were given, usually from the pull request's own "What" line or its
acceptance criteria, so a further prompt turn is aimed at something reachable.

Two things that keep the count from carrying more than it can. C3 gates nothing,
so eight of nine is a direction and not a figure. And one of the nine,
`s5l-21`, is already recorded in [`measurements.md`](measurements.md) as a
verdict the judge got too strict and a person passed, so the real number of
blocked entries behind this is eight, not nine. `s5l-17` is the only candidate
for curation rather than phrasing, and it is a single case.

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

## The technical prompt carries none of the output format either

Not filed.

The same defect as #96, on the other audience. Every rendering in `test-runs/`
fails B1 of [`../rubric/technical.md`](../rubric/technical.md) outright: not one
carries a release heading, and none uses the group set
[`output-format.md`](output-format.md) defines. `## Features`, `### Feature: …`
and `## Fixes` stand where `## VERSION - DATE` with **Changed**, **Added**,
**Removed** and **Fixed** belong. The required reference is missing as well: of
the 28 technical entries of `opus-4-8-out`, none carries one.

Recorded rather than filed, because the technical rendering is not what the
production loop is working on. It is here so that B1 having no observed pass is
read as a fact about the renderings and not about the axis.

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
