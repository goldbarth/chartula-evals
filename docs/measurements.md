# Measurements

One section per turn of stage 5 of [`pipeline.md`](pipeline.md): what was
changed in Chartula, what the rendering of it measured, and what the figure
turned out to be caused by.

**This is a record, not a list of work.** Nothing leaves this file. A finding
that has since been fixed stays where it is, because the point of the entry is
that the failure happened and what it cost, and a fixed row removed is a fixed
row that cannot be looked up the next time the same shape appears. The one list
that does empty itself is [`for-chartula.md`](for-chartula.md), whose rows leave
when the issue closes.

Figures from before this file existed are in [`targets.md`](targets.md), and
what each version of the criterion changed is in
[`criterion-versions.md`](criterion-versions.md).

---

## 2026-09-04 - the outcome slot was optional in the prompt

**What was measured.** `test-runs/sonnet-5-format-out.md`, rendered by Chartula
on 2026-09-03 from the release `v0.1.0` of its own repository. The rendering
carries goldbarth/chartula#99, which put the output format into the customer
prompt, and #101, which writes a run's artefacts without publishing a release.
It does not carry #102 or #104, both of which were merged after it was
rendered.

**How.** `judge/results/customer/labelled-all-claude-sonnet-5-2026-09-04T100752.json`,
124 calls, judge `claude-sonnet-5` at effort `low`. Criterion v2.0.0, digest
`sha256:8c213cdc9828d107`, at commit `761ae30` with a clean tree. No axis was
judged stale.

| axis | judged | failed |
|------|--------|--------|
| A1 | 21 | 0 |
| B1 | 1 | 0 |
| B2 | 1 | 0 |
| B3 | 1 | 0 |
| C1 | 20 | 1 |
| C2 | 20 | 0 |
| C3 | 20 | 7 |
| C4 | 20 | 0 |
| C5 | 20 | 0 |

**The figure: 13 of 20 entries ship, so the rendering does not ship whole.**

**What carried it.** C3 alone. The seven entries it fails are exactly the seven
that do not ship; the single C1 failure sits on `s5f-09`, which fails C3 as
well, so it costs no further entry. Every document axis passes, which is the
first time that has been true here: A1 finds no observable change left out, and
B1, B2 and B3 all pass.

The seven, with the passage the judge held against each:

| entry | what the judge read |
|-------|---------------------|
| `s5f-03` | "an invalid setting now produces a clear configuration error message instead of a crash" - the negation of the opening |
| `s5f-09` | "It runs by default and can be turned off in the faithfulness section of `chartula.yaml`" - configuration, not an outcome |
| `s5f-13` | the mechanism of fact-grounded generation, stated a second time |
| `s5f-15` | no candidate outcome anywhere in the entry |
| `s5f-17` | "This is entirely optional and configured in the labels section of `chartula.yaml`" - configuration, not an outcome |
| `s5f-18` | "rather than leaving the changelog empty" - the negation of the opening |
| `s5f-20` | "so labeling reflects the actual change" - the opening turned positive |

**What caused it.** Two sentences of the `CustomerFormat` constant in
Chartula's `ChangelogPromptBuilder.Prompts.cs`, which described a four-part
entry and then allowed the third part to be dropped:

- "Leave out any of the last three that does not apply." The last three are
  scope, outcome and action, so the outcome was optional. `s5f-15` is that
  permission used to the letter: the entry has no outcome sentence at all.
- "Say what the reader can now rely on instead, or leave it out." This one
  stands directly after C3's own test, which the prompt already carries word for
  word. The model applied the test, found the clause wanting, and took the
  cheaper of the two repairs offered. The other six entries are that.

The prompt was not wrong about its source. `docs/output-format.md` rule 8 says
the same in as many words: "Scope, outcome and action are omitted when they do
not apply, per C2 to C4."

**What was changed.** Both sentences, in Chartula. The outcome is now always
written, and striking the clause is named as not being a way out. Only scope and
action may be absent.

**What was left open.** The sentence in `output-format.md` that the permission
came from. C3 has no not-applicable case at all: `n/a` is defined by C4 alone,
and C2 calls its not-applicable case a pass in as many words. So rule 8 permits
an omission the axis it points at never allows. Repairing it edits the
criterion, which is frozen, so it waits for a cycle where the instrument loop is
open. It is written down under that version in
[`criterion-versions.md`](criterion-versions.md).

## 2026-09-04 - the turn that produced nothing to measure

**What was changed.** goldbarth/chartula#106, the entry above: the outcome slot
became a part an entry may not drop. Two other changes were in a rendering for
the first time, both merged after the run this file's first entry measured:
#102, which pins the model, and #104, which writes the customer rendering as a
page of its own.

**What came out.** Nothing that can be judged. The run of 12:52, from `ce2c6ea`:

```
technical  26320 characters
customer       0 characters
product     4327 characters
```

No `release-v0.1.0.md`, and a clean exit with no error. The turn produced no
figure at all, which is the result being recorded here.

**What carried it.** `ReleaseDescription.SplitOff`, added by #104. It takes the
labelled first line as the description and everything after it as the body, so
an answer that is a single `Description:` line leaves an empty body and the
whole rendering becomes a field of the page. Every step after that behaved as
designed: an empty customer body means a release with nothing to say to that
audience, so no page is written and nothing is flagged.

Four candidates were ruled out before that one, all by reading rather than by
running: the no-statements path in `ReleaseChangelogGenerator` makes no call at
all and the run metrics report three rephrasing calls; `ChangelogFormatter` only
normalises line endings and bullet markers; `ReviewCoordinator` passes the text
through while review is off, and it is off; the customer prompt is intact and
all 386 tests of that commit pass. #104's own test suite pinned the behaviour:
`A_description_on_its_own_leaves_an_empty_body`.

**What was changed after.** goldbarth/chartula#108 and #109. A description with
nothing under it is no longer lifted out; the text stays the body.

**What is kept, and why.** `test-runs/sonnet-5-outcome-empty.changelog.json` is
the run's own record, and no `.md` was made from it because there is no customer
section to cut out. It is committed anyway: a turn that produced no rendering is
still a turn, and the file is the evidence for what the customer field held.

**What this cost the measurement.** The C3 change of #106 is still unmeasured.
When it is rendered again, the turn will carry #102, #104, #106 and #109 at
once, and the difference from the first entry above cannot be attributed to any
one of them.

## 2026-09-04 - the outcome rule reached the model and the figure fell

**What was measured.** `test-runs/sonnet-5-outcome-out.md`, rendered from
`55fccc1`. The first rendering to carry the outcome rule, and the first whose
customer section is the published page rather than the `renderings.customer`
field: `tools/from_chartula_run.py` gained a `--page` option for it, so B2 is
shown the opening #104 produces instead of a document Chartula never writes.

Five changes are in it at once, four of them for the first time: #102 pins the
model, #104 writes the page, #106 makes the outcome slot compulsory, #109 keeps
the rendering when the description is all the model wrote, #110 warns about a
missing token.

**How.** `judge/results/customer/labelled-all-claude-sonnet-5-2026-09-04T130521.json`,
118 calls, judge `claude-sonnet-5` at effort `low`. Criterion v2.0.0, digest
`sha256:8c213cdc9828d107`, the same the entry above was produced against, so the
two compare. The tree was dirty at `9d5aaef` - the `--page` option was written
and not yet committed - which the result file records.

| axis | before | after | |
|------|--------|-------|---|
| A1 | 0 | 1 | worse |
| B1 | 0 | 1 | worse |
| B2 | 0 | 0 | |
| B3 | 0 | 1 | worse |
| C1 | 1 | 1 | |
| C2 | 0 | 0 | |
| C3 | 7 | 10 | worse |
| C4 | 0 | 0 | |
| C5 | 0 | 0 | |

**The figure: 8 of 19 entries ship, against 13 of 20 before.**

**C3 got worse on the axis the change was for.** Ten of nineteen entries fail
it, and `s5o-02` names no outcome anywhere - the case the rule was written to
forbid. The rule reached the model: the prompt carries it, and
`ChangelogPromptBuilderTests` asserts that it does.

**Three document axes fail that did not before**, and each one alone makes the
rendering unshippable:

- **A1**: the fallback to commits when a release has no pull requests, from #44,
  has no entry at all.
- **B1**: `s5o-06` says separate marketing files are no longer written, which
  costs a reader who relies on them, and it sits below unmarked entries.
- **B3**: "defaults to a much higher value" is a claim of degree with no number.

**What this turn cannot say.** The rendering is 5,285 characters over 19 entries,
against 25,457 over 20 before. It is a fifth of the length. Five changes and a
rendering of a different shape moved together, so no part of the movement can be
attributed to any one of them. That is the cost of letting four changes queue up
behind a turn that produced nothing, and it is the reason a turn of stage 5
changes one thing.

### What the diff says about that fall

Only two things changed in what the model is told, between the rendering that
shipped 13 of 20 and the one that shipped 8 of 19:

```
- Leave out any of the last three that does not apply.
+ Leave out the second or the fourth when it does not apply;
+ what they can now rely on is always written.

- Say what the reader can now rely on instead, or leave it out.
+ Say what the reader can now rely on instead. Striking the clause is not the way out.

+ CustomerDescription, appended to the customer prompt: one "Description:" line
+ before the entries, then a blank line, then the entries.
```

The first two are #106, the third is #104. Nothing else in the prompts moved.

**Two of the three new document failures are on rules the prompt has never
carried.** They did not get worse; they were never covered, and a rendering of a
different shape exercised them for the first time.

| Rule | Where it is written | In the prompt |
|------|---------------------|---------------|
| Every entry that asks something of the reader stands above every entry that does not | B1, `output-format.md` rule 10 | absent - "order" appears twice, both times about group order and slot order |
| A claim of degree needs something in the entry to check it against | B3 rule 3 | absent - the prompt forbids superlatives and marketing, and "much higher value" is neither |
| Minor changes are gathered into one closing `Also:` line of their group | B3 rule 2, `output-format.md` rule 11 | absent - "Also:" appears nowhere |
| Nothing after the last group | `output-format.md` rule 5 | absent |

A1 is not one of these: the coverage rule is in the prompt in full, and the
model dropped a change anyway.

**Where the prompt now diverges from the documents.** #106 requires an outcome
on every entry. `output-format.md` rule 8 says outcome is omitted when it does
not apply, and rule 11 says the collapsed `Also:` line usually has no outcome at
all. The prompt is now stricter than the document it implements. The divergence
is on the document's side - C3 defines no not-applicable case - and it waits
for a cycle where the instrument loop is open. It is written down under that
version in [`criterion-versions.md`](criterion-versions.md) rather than left to
be rediscovered.

**The model changed too, and that is not in the diff.** At `cda2ddf`, the commit
the first rendering was made from, there was no `chartula.yaml` in the tree and
`LlmProviderDefaults` named `claude-opus-4-8` for Anthropic. #102 pinned
`claude-sonnet-5` afterwards, for cost: the previous model could not be paid for
without ending the testing. So the two renderings were written by two different
models, and `changelog.json` records no model, so no artefact can settle it after
the fact.

**What that costs.** The two figures are not comparable, and the drop cannot be
read as the effect of the prompt. Everything from `sonnet-5-outcome-out` onward
is on one model, so this entry is the new baseline and the one above it is
history.

**What it teaches about the loop.** A turn of stage 5 changes one thing. This
turn carried five, plus a model, plus a rendering a fifth of the length, and the
result is a number that names no cause. `pipeline.md` says this in its stage 5
section; this is what ignoring it produces.

## 2026-09-04 - the four missing rules, and which of them bit

**What was changed.** goldbarth/chartula#112 alone, in what the model is told:
the four rules of `output-format.md` the customer prompt had never carried.
Order of entries, claims of degree, the collapsed `Also:` line, and nothing
after the last group.

#114 is in the rendering too and changes no content. It raised the output
ceiling from 16,000 to 32,000 tokens, which only takes effect when the ceiling
is reached; the run this is compared against did not reach it. Same model as
that run, same criterion, same digest.

**How.** `judge/results/customer/labelled-all-claude-sonnet-5-2026-09-04T142930.json`,
against `labelled-all-claude-sonnet-5-2026-09-04T130521.json`. Rendering
`test-runs/sonnet-5-rules-out.md` from Chartula `38b8be8`, 24 entries.

| axis | before | after | |
|------|--------|-------|---|
| A1 | 1 | 0 | better |
| B1 | 1 | 0 | better |
| B2 | 0 | 0 | |
| B3 | 1 | 1 | |
| C1 | 1 | 2 | worse |
| C2 | 0 | 0 | |
| C3 | 10 | 10 | |
| C4 | 0 | 1 | worse |
| C5 | 0 | 0 | |

**The figure: 13 of 24 entries ship, against 8 of 19. 54 in a hundred against
42.**

**Two of the four rules did what they were written for.** B1 goes to zero, and
the judge's reason is the rule read back: the only entry whose ignoring costs
the reader, a missing API key, is the first entry of the document. A1 goes to
zero as well. The `Also:` line appears, at line 122 of the rendering, and the
four groups stand in the order the format defines.

**One rule reached the model and did not bite.** B3 fails on the same shape as
before: "The token limit sent to the model now defaults to a much larger value",
where the previous rendering said "a much higher value". The prompt has carried
the claim-of-degree rule since #112 and the model wrote one anyway. That is a
finding about how the rule is worded, not about it being absent, and it is the
same kind of finding as C3.

B3 is one of the three axes stage 4 put **in** the gate, so this verdict can be
read as a figure rather than as a direction.

**C3 stands at 10 over more entries**, so better as a share and unchanged as a
count. It remains the largest single item, and it is out of the gate, so it is a
direction only.

**C1 and C4 gain one each.** Five more entries and a movement of one is what
stage 5 says to ignore.

**The rendering still does not ship whole**, and one sentence decides it: B3.
