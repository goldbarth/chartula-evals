# Labels: technical rendering

Measured with the axes from [`../../rubric/technical.md`](../../rubric/technical.md).
Process shared with every audience: [`../how-to-label.md`](../how-to-label.md).

| file | what it holds |
|------|-----------------|
| [`items.csv`](items.csv) | level C verdicts, plus A1 - one row per (run, item, axis) |
| [`runs.csv`](runs.csv) | level B verdicts - one row per (run, axis) |
| [`run-summary.csv`](run-summary.csv) | overall shippable / not shippable per run - written by `labels.py sync`, never by hand |
| [`missing.md`](missing.md) | level A1, the other half - changes with no entry at all |
| [`friction-log.md`](friction-log.md) | where the rubric did not decide a case on its own |

Eight axes here, not nine, and the letters mean what they mean in
`customer.md`: A1 selection, B1 and B2 document, C1 to C5 entry. None of them
defines `n/a`, so every cell of `items.csv` is `pass`, `fail` or `?`.

## Runs labelled so far

<!-- labels.py sync: runs labelled -->

| run        | items | shippable     |
|------------|-------|---------------|
| opus-5-out | 30    | not shippable |

<!-- labels.py sync: end -->

Nothing yet: `labels.py init --audience technical --run <run> --prefix <p>`
lays out the rows, and `sync` fills the table above. Everything between those
two markers is written by `sync` and nothing else, so a note put there is lost
on the next run of it.

**Two things to know before choosing a run.** Entries are read as `- ` bullets,
and the technical renderings disagree about what a bullet is. `opus-5-out`
writes one bullet per change, 30 of them. `sonnet-5-out` gives each pull
request a heading and several bullets under it, which reads as 137. Under the
*Units* section of the rubric those bullets are not entries at all, so a table
laid out from them would be scoring something the rubric does not recognise.
`sonnet-5-rules-out` and `sonnet-5-rules-repeat-out` use bold lines and
paragraphs and have no bullets at all, which `init` refuses with a message
saying so.

Three renderings are held out on purpose and are not labelled here:
`haiku-4-5-out`, `opus-4-8-out`, `opus-5-no-thinking-out`. Three more carry no
`--- Technical ---` section at all, being customer experiments:
`sonnet-5-customer-only-out`, `sonnet-5-labels-out`, `sonnet-5-place-out`.

## Worked example

The first entry of `opus-5-out`, line 6, quoted to its first three sentences -
it runs to nine. Nothing is scored yet, so this shows how the reasons are
written rather than pointing at rows that exist:

> - **Run metrics for every `preview` and `generate` run** - Each run now ends
> with a `Run metrics` summary covering rule-based check runs/findings/claims,
> thorough check runs/findings/claims and token usage, rephrasing calls, and a
> token total. The indented line pairs the claims **only** the thorough check
> caught with the tokens spent catching them; claims found by both checks are
> excluded, since the thorough check adds nothing there. Adds
> `Chartula.Core/Observability/` with `IRunMetrics`, the `RunMetrics` sink,
> `NullRunMetrics`, `RunReport` and `RunReportFormatter`. [...] Closes #26
> ([#66](https://github.com/goldbarth/chartula/pull/66))

- **kind**: a new capability, not a repair.
- **A1**: every run reports what it did and what it cost, which is released
  behaviour a caller sees. It belongs here.
- **C1**: `fail`. One change per line is the question, and this line carries the
  summary, the observability namespace, the token accounting on `ChatModel` and
  the pipeline wiring. It is also a paragraph rather than a line.
- **C2**: `pass`. The reference is on the entry, at its end, not standing on a
  line of its own.
- **C3**: `pass`. The fact base gives pull request #66 the title "feat: report
  what a run does and what it costs"; the description here was written, not
  lifted.
- **C4**: `pass`. Read without the `## Features` heading above it, the line
  still says what is different: runs now end with a metrics summary.
- **C5**: `fail`. Past the bold label, the description opens on "Each run now
  ends", not on a verb in the imperative.

Two fails on one entry and they are not the same finding: C1 is repaired by
splitting the line, C5 by rewriting its first three words. That is the split
the C axes exist for.
