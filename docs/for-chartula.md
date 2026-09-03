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

Every one of those rules exists in writing and none reaches the model. No
rendering from any of the four models ships whole, which is the product figure
in [`targets.md`](targets.md).

The outcome rule is the one exception that needs more than the format
document: `output-format.md` names the four slots but not the test that decides
whether a closing clause is an outcome. That test is in `rubric/customer.md`
under C3 - strike the opening and read what is left, and ask whether it still
tells the reader something they did not already have.

## The customer rendering has no opening

Not filed.

`ChangelogMarkdownComposer` contributes the `## {tag}` heading and joins the
sections; the customer text in `changelog.json` is the model's output and
nothing else. The published serialisation in
[`output-format.md`](output-format.md) opens with YAML front matter - `title`,
`description`, `publishedAt`, `tags` - and nothing produces it.

Measured rather than assumed. B2 failed the rendering of 2026-09-03 on the
missing opening; the same document with front matter prepended by hand passes
the axis, and nothing else about it changed. So the opening is the whole of what
that axis fails on.

Two things are missing, not one:

- **The scaffolding.** Front matter is the composer's output, not the model's.
  `title` and `publishedAt` are derivable from the tag and its date. `tags` is
  correctly absent while the fact base carries no labels, which is #98.
- **A source for `description`.** One sentence on what the release is about.
  There is no field for it in the fact base and no rule for who writes it. The
  sentence used in the test above was written by hand, which is why that half of
  the finding is not answered by adding a composer step.

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
