# Judge prompt: one axis, one document

The prompt for the separation run. One call judges one axis on one document,
which is how the judge will be used later, so the run measures the thing that
will actually ship rather than a quiz format invented for the test.

Substituted before sending:

| Placeholder            | Filled with                                                                 |
|------------------------|-----------------------------------------------------------------------------|
| `{{AXIS_ID}}`          | `A1`, `B1`, `B2`, `B3`, `C1` … `C5`                                          |
| `{{AXIS_SECTION}}`     | that axis's section of `rubric/{audience}.md`, verbatim, headings included   |
| `{{UNITS_SECTION}}`    | the `## Units` section of `rubric/{audience}.md`, verbatim, in the system block |
| `{{ALLOWED_VERDICTS}}` | `pass`, `fail`, and `n/a` only for the axes whose section defines it          |
| `{{SUBJECT_LABEL}}`    | `The document` for A1 and B1 to B3, `The entry` for C1 to C5                  |
| `{{SUBJECT}}`          | the document, or the single entry when judging a C axis                       |
| `{{FACTS_BLOCK}}`      | the fact base, for A1 only; omitted for every other axis                      |

Nothing from `labels/{audience}/` is ever substituted in. The judge does not
see a human verdict, a reason written by a human, or an example drawn from a
labelled run - those are what it is being measured against.

Run at temperature 0.

---

## System

You judge one axis of a changelog rubric. Nothing else.

You are given the definition of a single axis and a piece of a changelog. You
decide whether it passes that axis, and you point at the passage that decides
it.

Rules:

- Judge only the axis you are given. A changelog can be wrong in ways this axis
  does not cover. Those are judged in other calls and are not yours to report.
- A pass is a normal result. Do not look for a defect that is not there, and do
  not lower a verdict because the text could have been better written.
- Follow the decision procedure in the axis definition in the order it is
  written. Where it names a verdict for a case, use that verdict.
- Point at a passage. Quote it verbatim from what you were given, character for
  character, so it can be found again by searching. If no passage supports a
  fail, the verdict is a pass.
- For a `fail`, the quote is the passage that fails. For a `pass`, it is the
  passage that satisfies the axis. Where an axis is satisfied by something
  being correctly absent, quote nothing and say so in the reason.
- When the finding is that something is missing from the changelog, there is no
  passage to quote - quote the fact it is missing from instead, verbatim from
  the fact base you were given. Never write a sentence of your own in the quote
  field.
- Do not rewrite, improve or continue the text. Do not comment on anything
  outside the axis.

How the changelog is cut into units, from the rubric:

{{UNITS_SECTION}}

Answer with JSON and nothing else:

```json
{
  "quote": "verbatim passage, or empty when the axis is satisfied by an absence",
  "reason": "one sentence, naming the rule in the decision procedure you applied",
  "verdict": "one of the allowed verdicts"
}
```

The order matters: quote first, reason second, verdict last. Decide after you
have found the evidence, not before.

## User

Axis to judge: **{{AXIS_ID}}**

Allowed verdicts: {{ALLOWED_VERDICTS}}

The axis, from the rubric:

{{AXIS_SECTION}}

{{FACTS_BLOCK}}

{{SUBJECT_LABEL}} to judge:

```markdown
{{SUBJECT}}
```

---

## Expected result of the separation run

From `calibration/{audience}/manifest.json`. Every cell not named below is
expected to pass.

| Document  | A1   | B1   | B2   | B3   |
|-----------|------|------|------|------|
| `base.md` | pass | pass | pass | pass |
| `a1.md`   | fail | pass | pass | pass |
| `b1.md`   | pass | fail | pass | pass |
| `b2.md`   | pass | pass | fail | pass |
| `b3.md`   | pass | pass | pass | fail |

Then C1 to C5 on the four entries of `base.md`: every one expected to pass.

Twenty calls, and twenty more: C1 to C5 on each of the four entries of
`base.md`, which are written to pass every one of them. Those measure how often
the item axes fail something that is sound, which the four documents above
cannot show.

Two failure shapes are worth telling apart when the run does not separate:

*A fail that spreads.* The `b3.md` entry judged `fail` on C3 as well as B3
means the judge is reading the trailing sentences as a missing outcome - the
confusion this rubric already had once, now in the model rather than in the
text.

*A fail on the base.* The base passes every axis by construction, so a fail
there is a disagreement about what the axis says. Read the quote and the reason
before concluding anything: in the first run, five of the six such fails were
defensible readings of an underspecified axis, with a verbatim quote and sound
reasoning, and sharpening the axis removed them. Only a fail with no quote, or
with a quote that has nothing to do with the axis, is the judge scoring overall
impression instead.

The quotes matter as much as the verdicts. A correct verdict with a quote that
points at the wrong passage is a coincidence, not a measurement, and it will
not hold on the 53 labelled items.
