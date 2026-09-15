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

## 2026-09-04 - spot check: the judge stands

Stage 6 of [`pipeline.md`](pipeline.md), the first one, and overdue by three
turns. It is not a turn of stage 5 and moves no product figure; it is the mark
the turn count starts again from.

**What was read.** Ten entries of `sonnet-5-rules-out` against
`judge/results/customer/labelled-all-claude-sonnet-5-2026-09-04T142930.json`, on
the five item axes: 50 cells, cut by `tools/spot_check.py` and read back by it.
`s5r-01`, `-02`, `-03`, `-05`, `-07`, `-11`, `-13`, `-14`, `-19`, `-20` - seven
the judge let through and three it failed, chosen from the verdicts before any
of the text was read.

**The result: 50 of 50 agreed. No disagreement in either direction.**

- **Let through: 0.** Nothing the judge passed was one a person would send back.
  That is the instrument target of [`targets.md`](targets.md), at most 2 in 100,
  and it is met with room.
- **Too strict: 0.** Nothing the judge failed was one a person would have passed.

**The judge stands, so stage 5 continues.** The instrument loop stays closed.

**What this does not establish.** The 50 cells are 42 passes, 4 `n/a` and 4
fails, and three of the five axes carry no failure at all in the sample: C1, C2
and C5 are ten passes each. Agreement on a column with one class in it measures
the class, which is the argument `targets.md` already makes about agreement
figures generally. What the check does establish is the direction that costs a
release: of the seven entries the judge let through, none should have been sent
back.

The four fails a person confirmed are three on C3 and one on C4, which are the
two axes the plan is about to work on. Those verdicts being right is what makes
the next turns worth running.

## 2026-09-04 - the noise floor: three axes move when nothing changes

Not a turn. The same release rendered twice from the same Chartula commit
`38b8be8`, nothing changed in between, both judged against the same criterion by
the same model. Whatever moves is what a turn has to beat to mean anything.

**How.** `test-runs/sonnet-5-rules-repeat-out.md`, 25 entries against the 24 of
`sonnet-5-rules-out`, judged by
`judge/results/customer/labelled-all-claude-sonnet-5-2026-09-04T162030.json`.

| axis | first | second | |
|------|-------|--------|---|
| A1 | 0 | 0 | |
| B1 | 0 | 0 | |
| B2 | 0 | 0 | |
| B3 | 1 | 0 | moved |
| C1 | 2 | 2 | |
| C2 | 0 | 0 | |
| C3 | 10 | 11 | moved |
| C4 | 1 | 0 | moved |
| C5 | 0 | 0 | |

Entries that ship: 13 of 24, then 13 of 25.

**The floor is one. Three of the nine axes moved by one with nothing changed.**
A movement of one is not a result on any axis, in either direction, and this
document has called such a movement noise twice before on nothing but
conviction. Now it has a figure behind it.

**It also changed the plan before a change was made.** B3 went from 1 to 0 on
its own. Step 1 of the plan was a rewording of the claim-of-degree rule, aimed at
exactly that one entry, and had it been made, the next count would have shown
1 to 0 and the change would have been credited with it. The rendering does not
carry a claim of degree every time; the entry it failed on last time is not in
this rendering at all.

**What moves and what does not.** The document axes and C2 and C5 sat still.
C3 moved by one at a count of ten, which is a tenth of itself, and C1 sat still
at two. The rendering itself is not stable either: 24 entries and 7,343
characters, then 25 entries and 8,223.

**What it costs to know this.** One render and one judge run, and it has already
paid for itself by removing a turn from the plan.

## 2026-09-08 - a third draw, and the floor under C3 itself

Not a turn. `sonnet-5-customer-only-out`, rendered from the branch of
goldbarth/chartula#116 with `--audience customer`, before the prompt change of
#118 existed. So it carries no change in what the model is told, and it was
judged on C3 alone:
`judge/results/customer/labelled-C3-claude-sonnet-5-2026-09-08T090934.json`,
25 entries, 9 failures, same digest as the two before it.

**Three renderings of the same prompt, and C3 gives three answers:**

| Rendering | entries | C3 |
|-----------|---------|----|
| `sonnet-5-rules-out` | 24 | 10 |
| `sonnet-5-rules-repeat-out` | 25 | 11 |
| `sonnet-5-customer-only-out` | 25 | 9 |

The general floor measured on 2026-09-04 was one, over all nine axes at once.
This is the same figure taken three times on the axis the work is actually
about, and it says the same thing more precisely: **C3 varies by one either way
around ten with nothing changed.** A turn that takes it to nine or eleven has
shown nothing. Seven or below is the first count that means the prompt moved.

**It also answers a question nobody had paid to ask.** #116 renders one audience
instead of three, and the customer rendering it produces sits inside the range
of the two full renders. Rendering one audience does not change what that
audience gets, which is what the tests said and is now also what a rendering
says.

**On the result file's `-dirty`.** The label tables were being written when the
run started, so the tree was not clean. The digest is the criterion's own and is
unchanged, so the comparison holds; nothing about the criterion moved.

## 2026-09-08 - the place moved behind the outcome, and coverage paid for it

**What was changed.** goldbarth/chartula#118 alone, one sentence: the place a
setting is reached is the fourth part of an entry, so it comes after what the
reader can now rely on and never instead of it.

**How.** `test-runs/sonnet-5-place-out.md`, rendered from Chartula `ddbe859`
with `--audience customer`, 19 entries. Judged over every axis by
`judge/results/customer/labelled-all-claude-sonnet-5-2026-09-08T110558.json`,
against `labelled-all-claude-sonnet-5-2026-09-04T142930.json`.

| axis | before | after | |
|------|--------|-------|---|
| A1 | 0 | 3 | **worse** |
| B1 | 0 | 0 | |
| B2 | 0 | 0 | |
| B3 | 1 | 0 | inside the floor |
| C1 | 2 | 1 | inside the floor |
| C2 | 0 | 0 | |
| C3 | 10 | 3 | **better** |
| C4 | 1 | 0 | inside the floor |
| C5 | 0 | 1 | inside the floor |

**C3 falls by seven, and it is the seven the change was aimed at.** Not one of
the five entries that closed on where a setting lives is left: `s5r-01`,
`s5r-10`, `s5r-14`, `s5r-15` and `s5r-16` have no counterpart in this rendering.
The three that remain are the other shape, entries about a fix that close on the
negation of their own opening, which is what the next step of the work is for.

Seven is far outside the floor. Three renderings of the unchanged prompt put C3
at 10, 11 and 9.

**A1 rises by three, and nothing aimed at it. That is the finding.** It is also
outside the floor, and A1 is a document axis: one of those failing makes the
whole rendering unshippable however good its entries are. So the 15 of 19 above
is not the product figure, and this rendering does not ship.

- `s5p-12` describes the changelog's own formatting - normalised bullet markers
  and line endings - which is not something a reader meets by using the product.
- `s5p-19` describes where the audience texts are stored, likewise.
- On the document row: the run-metrics summary printed at the end of every
  `preview` and `generate` is in the fact base and in no entry at all.

**The rendering is 19 entries against 24 and 25 before it.** Six fewer, two of
the survivors describing internals, and one observable change carried by no
entry. Whether the sentence about the fourth part caused that, or whether the
same prompt simply renders shorter some days, this turn cannot say: the entry
count of an unchanged prompt was 24, 25 and 25, so 19 is outside that range too.

**What this turn cost that it did not have to.** C3 was judged on its own first,
in `labelled-C3-claude-sonnet-5-2026-09-08T104515.json`, and then judged again
inside the full run. Stage 5 of `pipeline.md` says every axis is counted here,
and the plan's own collision rule says to read every axis in the output. Judging
one was advice from the cost section of `pipeline.md`, which is a note about not
asking the same question nine times, not a procedure. Had the full run been made
first, A1 would have been visible immediately and the C3-only run would not have
been paid for.

## 2026-09-08 - the label decides visibility, and C3's fall turns out to be the rendering

**What was changed.** goldbarth/chartula#120 carries a change's labels into the
fact base, and #121 decides `IsUserVisible` from a label rather than from the
conventional-commit category, with the category as the fallback and the names
configured in `chartula.yaml`. Both were needed together: #120 alone changes no
output.

Three pull requests of v0.1.0 were labelled `visibility:internal` on GitHub, so
23 of the 28 changes now reach the customer prompt where 26 did.

**How.** `test-runs/sonnet-5-labels-out.md`, 24 entries, judged over every axis
by `judge/results/customer/labelled-all-claude-sonnet-5-2026-09-08T130715.json`
against `labelled-all-claude-sonnet-5-2026-09-08T110558.json`.

| axis | before | after | |
|------|--------|-------|---|
| A1 | 3 | 0 | **better** |
| B1 | 0 | 0 | |
| B2 | 0 | 0 | not comparable, see below |
| B3 | 0 | 0 | |
| C1 | 1 | 2 | inside the floor |
| C2 | 0 | 0 | |
| C3 | 3 | 10 | **worse** |
| C4 | 0 | 0 | |
| C5 | 1 | 2 | inside the floor |

**A1 goes to zero and that is the change working.** No entry describes the
tool's internals any more, and no observable change is left without one. The
three failures of the previous turn are gone, which is what labelling the three
pull requests was for.

**B2 sat this turn out.** `release-v0.1.0.md` was deleted before the case was
built, and the release description exists nowhere else, so the customer section
was cut from `renderings.customer` and carries no front matter. B2 judges the
opening, so its pass here says nothing. Rebuilding the front matter by hand
would have judged a document Chartula never wrote.

## What C3 says about the method

C3 is back where it was before #118, and the sentence #118 added is still in the
prompt. As a share of the entries judged, every run since the freeze:

| Rendering | C3 | share |
|-----------|----|-------|
| `sonnet-5-format-out` | 7 of 20 | 35% |
| `sonnet-5-outcome-out` | 10 of 19 | 53% |
| `sonnet-5-rules-out` | 10 of 24 | 42% |
| `sonnet-5-rules-repeat-out` | 11 of 25 | 44% |
| `sonnet-5-customer-only-out` | 9 of 25 | 36% |
| `sonnet-5-place-out` | 4 of 19 | 21% |
| `sonnet-5-place-out`, judged again | 3 of 19 | 16% |
| `sonnet-5-labels-out` | 10 of 24 | 42% |

**The one rendering that changed the figure is the one that came out short.**
`sonnet-5-place-out` has 19 entries where every other rendering has 24 or 25,
and both judge runs over it agree, so it is the document and not the judging. A
rendering with a fifth fewer entries has a fifth fewer chances to fail an item
axis.

**So the fall from 10 to 3 was not the effect of #118.** It was measured on one
rendering, and the next rendering of the same prompt is back at 42 per cent. The
sentence may still be right - it is the reasoning that was wrong.

**What this says about the loop.** One rendering per turn cannot separate a
prompt change from the variation between renderings. The noise floor of
2026-09-04 compared axis counts over two renderings of 24 and 25 entries; that
a third would come out at 19 was not in it, and the floor of one was read as
covering a variation it had never seen.

Every figure in this file that rests on a single rendering carries that, and the
turns before this one are not exempt: #112's four rules were read the same way.

## 2026-09-08 - spot check: the judge stands, and C3's failures are real

Stage 6 of [`pipeline.md`](pipeline.md), the second one, and overdue by five
turns. Not a turn of stage 5 and it moves no product figure.

**What was read.** Ten entries of `sonnet-5-labels-out` against
`judge/results/customer/labelled-all-claude-sonnet-5-2026-09-08T130715.json` on
the five item axes: 50 cells, 49 filled in. Cut with `--passed 5 --failed 5`
rather than the usual seven and three, because the open question was not only
what the judge lets through but whether its ten C3 failures are real.

**The result: 46 of 49 agreed.**

**C3's failures are real, and that is the answer this was cut for.** Five of the
ten C3 cells were failures, and four of the five are confirmed:

| entry | judge | person |
|-------|-------|--------|
| `s5l-01` | fail | fail |
| `s5l-04` | fail | fail |
| `s5l-08` | fail | fail |
| `s5l-17` | fail | fail |
| `s5l-21` | fail | pass |

So the 42 per cent is not an artefact of an axis that stage 4 put out of the
gate. The entries are weak, and the work aimed at them is aimed at something.

**Let through: 2, which is 4.1 per 100 cells read.** The instrument target in
[`targets.md`](targets.md) is at most 2 in 100, and the first spot check found
none. Two cases:

- `s5l-09` on C3: "and it stays off by default so nothing is held up unless you
  turn it on" - passed by the judge, failed by the person.
- `s5l-01` on C4: "Provide an API key for that provider through an environment
  variable before running either command" - the same.

Two cases in 49 cells is a thin basis for a rate, and it is over the target
rather than under it, which is the direction that costs a release rather than a
turn. It is recorded and not acted on: one spot check at 0 and one at 4.1 is not
a trend.

**Too strict: 1.** `s5l-21` on C3, failed by the judge and passed by the person.
That direction costs a turn, not a release, and `targets.md` does not count it
against the target.

**The judge stands, so stage 5 continues** and the instrument loop stays closed.

## 2026-09-15 - the outcome of a fix reaches the prompt, and C3 drops below the floor

**What was changed.** goldbarth/chartula#122, the second half of #96 named as
step 3 of [`plan.md`](plan.md). Two pull requests land against it, both in
this rendering and neither measured on its own: #123 (merged 2026-09-09)
rewrites C3's target so a bug-fix entry no longer closes on the bug being
gone but on what the reader no longer has to do about it, and #126 (f7cda42)
adds the two worked examples and aligns the prompt with the rest of the
rubric - an opening chosen by the change's own type, action stated after the
outcome, scope, breaking change.

The comparison run, `sonnet-5-labels-out`, was rendered on 2026-09-08, before
either #123 or #126 existed. So this turn measures the two together, and
`plan.md`'s own rule for step 3 - that two changes landing on one axis in one
turn cannot be told apart afterwards - applies to itself: the fall from 10 to
4 cannot be credited to "the outcome of a fix" alone, and the C1 movement
below may be the new per-type opening rather than anything about C3.

**How.** `test-runs/sonnet-5-fix-outcome-v010-out.md`, rendered by Chartula
`c72f068` from `v0.1.0` at `8061f46`, 28 changes. Judged over every axis by
`judge/results/customer/labelled-all-claude-sonnet-5-2026-09-15T160931.json`
(run `sonnet-5-fix-outcome-v010-out`), against
`labelled-all-claude-sonnet-5-2026-09-08T130715.json` (run
`sonnet-5-labels-out`). Same criterion, digest `sha256:8c213cdc9828d107`, no
axis judged stale.

| axis | before | after | |
|------|--------|-------|---|
| A1 | 0 | 0 | |
| B1 | 0 | 0 | |
| B2 | 0 | 0 | |
| B3 | 0 | 0 | |
| C1 | 2 | 3 | inside the floor |
| C2 | 0 | 0 | |
| C3 | 10 | 4 | **better** |
| C4 | 0 | 0 | |
| C5 | 2 | 1 | inside the floor |

**The figure: 12 of 19 entries ship, against 11 of 24 before.**

**C3 falls by six, from 10 of 24 to 4 of 19.** As a share that is 42 per cent
to 21 per cent, outside the floor of one either way around ten set from three
renderings of an unchanged prompt: 10 and 11 on 2026-09-04, and a third, 9,
from `sonnet-5-customer-only-out` on 2026-09-08. C3 is out of the gate (see
[`targets.md`](targets.md)), so this is a direction, not a ship-blocking
figure on its own - and, per the note above, a direction with two candidate
causes rather than one.

**The same share once meant nothing, so it is checked here rather than
assumed.** `sonnet-5-place-out` also had 19 entries and a C3 count of 4, and
the "What C3 says about the method" section above traced that fall to a
rendering a fifth shorter, not to the prompt change it was first credited to.
This rendering is not that case: at 6,788 characters against 7,240 for the
24-entry baseline (6,706 against 7,168 counting the customer section alone),
it is 94 per cent of the length over five fewer entries, so entries got
longer, not cut. Still, one rendering is one draw, and this figure rests on
one. No second draw is taken in this phase: goldbarth/chartula#122 was
rescoped for the alpha to a single rendering followed by a circuit breaker,
so the figure is recorded as that single draw, not as a confirmed result.

**C1 and C5 moved inside the floor.** C1 up by one to 3 of 19, C5 down by one
to 1 of 19. Both are out of the gate and neither is a count stage 5 asks to
read.

**A1, B1, B2 and B3 sat still at zero.** No entry describes the tool's own
internals, no claim of degree stands without a number to check it against, and
both single-checked document axes hold.

**What was kept alongside it.** `test-runs/sonnet-5-fix-outcome-out.md` and
`.changelog.json`, rendered from the same Chartula commit `c72f068` - so the
same prompt, #123 and #126 both in it - but from `v0.1.0` as it stands today
at `0d4f6f4`: 44 changes through #112, not 28. A different release, so this is
neither a turn nor a draw of this one. It is judged in
`labelled-all-claude-sonnet-5-2026-09-15T135746.json` and kept because a
render of the current prompt against the larger release exists and cost
nothing further to keep.
