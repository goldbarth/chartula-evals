# Rubric: the product rendering

What makes a product changelog **document** shippable.
Written for the product audience only.
The customer and technical renderings are not covered here.

**Not covered here:** whether the content is factually correct.
That is the faithfulness check's job.
An entry can be perfectly grounded and still fail every axis below.

The reader is a product manager, inside the project or close enough to be
handed a roadmap - reading to track what shipped and to frame it for people
who were not in the room. They meet the product the way the customer does,
never by reading the source, so an axis below that restricts vocabulary reads
the same way C5 of `rubric/customer.md` does. What they read *for* is
different from either other audience: not whether they can act on it, which is
the customer's question, and not what changed in the code, which is the
technical reader's. It is what a change means for a decision they are
tracking.

## Levels

Criteria sit on three levels. Each axis belongs to exactly one.
The level tells you which pipeline stage to fix when an axis fails.

| Level             | What it judges                   | Fix belongs in     |
|-------------------|-----------------------------------|---------------------|
| **A - Selection** | which changes appear at all      | curation            |
| **B - Document**  | theme structure, length, tone    | rendering template  |
| **C - Entry**     | the individual entry             | prompt              |

An entry that fails level A is removed, not rewritten.
An entry that fails level C is rewritten.
A document that fails level B is re-assembled from unchanged entries.

What each axis owns, and what it leaves to a neighbour, is stated in the axis
itself - see [`how-a-rubric-is-built.md`](how-a-rubric-is-built.md) for why
that is the first thing written.

**Why this rubric has seven axes and `customer.md` has nine.** The product
entry carries two slots, not four: nobody is asked to act on a product
rendering, so it has no scope clause to hedge and no action to withhold. Rule
3 of `how-a-rubric-is-built.md` says an axis nobody could write a fail example
for is not written, and a scope axis or an action axis has no entry here that
could fail it. The two slots this template does carry - what changed, and why
it matters - are C1 and C2 below.

The shape this rubric judges conformance to is
[`../docs/output-format.md`](../docs/output-format.md), section
*Product: `product/thematic`*. It is never restated here, per rule 4 of
[`how-a-rubric-is-built.md`](how-a-rubric-is-built.md).

**This rubric has no labelled corpus yet.** No product rendering has been
generated, labelled or judged at the time it was written - `rubric/customer.md`
and `rubric/technical.md` both draw their examples from real runs in
`test-runs/`, and this one cannot. Every example below is constructed rather
than observed, on the same reasoning `how-a-rubric-is-built.md` gives for a
minimal pair: it shows the procedure being applied, not a case recognised by
its words. Stage 2 of [`../docs/pipeline.md`](../docs/pipeline.md) is what
turns a constructed example into an observed one, and it has not run against
this audience.

---

## Units

The levels apply to different things, so the document has to be cut into
units before anything can be judged. A product rendering is made of two kinds
of text.

| Unit               | What it is                                              | Judged by  |
|---------------------|----------------------------------------------------------|-------------|
| **Theme heading**  | the label over a set of entries - a project's own label vocabulary, or `Other` | B1, B2 |
| **Entry**          | one bullet reporting one change, built from the two slots | A1, C1-C3 |

**What makes a piece of text an entry**

1. It reports a change to the product, and it sits under a theme heading. If
   it can be read as a row in a table of changes, it is an entry.
2. It carries slot 1. An entry with no stated change is still an entry; it
   fails C1 and is scored as one.
3. Headings are never entries, whatever they contain. A heading carrying the
   only description of a change is a B2 finding, and the change counts as
   missing at level A.
4. Anything under a theme heading that is not an entry - a paragraph, a
   nested list, a note about the release as a whole - is **not** an entry. It
   gets no row in the entry table and is judged by B2, which is stricter here
   than in either other template: this format carries no release-level notice
   at all, so there is no exception for B2 to make room for.

A run with only the `Other` heading is still judged: B1 and B2 read it like
any other heading, and every entry under it is still an entry.

---

## Level A - Selection

### A1 - Tracks a decision or a claim about the product

**Judges:** whether the rendering carries the changes that could move a
decision this reader makes, or a description of the product they would give
someone else, and nothing else.

**Does not judge:** how a change is worded once it is there - that is C1 and
C2 - nor which theme it sits under, which is B1. A change can belong here and
be described badly; the entry is then rewritten, not removed.

The test is wider than the customer template's A1, on purpose. A change with
no observable surface for a user of the product can still belong here: what a
team can now claim about a release's cost, its reliability, or what it is
allowed to promise a customer is not something a user ever meets, and it is
exactly what this reader tracks. That gap between the two audiences is the
whole reason this is a separate rendering rather than a shorter customer one.

The axis has two halves and both are judged. An entry that should not be
there is visible in the document. A change that should be there and is
missing is not visible in the document at all - it can only be found against
the release's facts, and it is the more expensive omission, because a reader
cannot ask about something they were never told.

**Decision procedure, half one: is anything here that should not be**

1. For each entry, ask whether the change it reports alters what the product
   can do, who it can serve, what it costs to run or operate, or what the
   team can now claim about it. If none of those, the entry fails.
2. The question is about the change, not about the words. A restructuring
   described as a capability still fails when nothing above changed; a real
   cost or reliability change described flatly still passes.
3. Test scaffolding, continuous integration, formatting, and a refactor with
   identical behaviour and no measured effect on cost or reliability do not
   reach any of the four questions and fail rule 1.

**Decision procedure, half two: is anything missing**

4. Only when the facts of the release are given alongside the document.
   Without them this half cannot be judged and is not guessed at.
5. Go through the facts, not through the document. For each fact, apply rule
   1: could it move a decision or a claim this reader makes? If yes, find the
   entry that carries it.
6. A fact that passes rule 1 and has no entry is a fail, and the fact is
   named. Several omissions are one verdict; the axis asks whether the
   rendering is complete, not how incomplete it is.

**Pass:** an entry for a change that cuts the cost of a run by roughly a
third - the team can now say something about running cost it could not say
before, whether or not a single user ever notices.

**Fail (present, should not be):** "Add the `Chartula.Cli.Tests` project so
CLI behaviour is covered by tests." Nothing about what the product does, costs
or can be trusted to do changed.

**Fail (absent, should be there):** the facts carry the cost reduction above,
and no entry mentions it.

*A refactor shows both sides: it fails rule 1 when behaviour and cost are
identical before and after, and passes when it measurably changed one of
them - described by what changed, never by the refactor.*

---

## Level B - Document

### B1 - Themes in order, and each entry under its own

**Judges:** whether the document's headings are the themes the release's own
facts establish, in alphabetical order with `Other` trailing, and whether
each entry sits under the theme its own facts name.

**Does not judge:** what an entry says, which is level C, nor whether
anything besides entries stands under a heading, which is B2. This axis reads
headings, their order, and which heading each entry sits under.

The theme a change belongs to is established by its labels, the same way a
customer tag is. What order the headings stand in, and how a theme is derived
from a label, are defined in
[`../docs/output-format.md`](../docs/output-format.md), section *Themes*, and
are not repeated here: a rule written in both documents is a contradiction
waiting for one of them to be edited. It is a fact about the change, not a
judgement call, so an entry sitting under the wrong heading is a structural
defect and not a difference of opinion.

**Decision procedure**

1. Read the theme headings in order and compare them with the order the
   format defines. Out of that order is a fail whatever the headings contain.
2. A heading with no entries is a fail: it should have been left out.
3. Only when the facts of the release are given alongside the document. For
   each entry, compare the theme its heading names with the allow-listed
   label or labels the facts give its change. An entry under a heading its
   own facts do not name is a fail, whichever heading would have been right.
4. Without the facts, rule 3 cannot be judged and is not guessed at; rules 1
   and 2 still apply.
5. A document with no theme headings at all fails: it cannot satisfy rule 1.

**Pass:** `Configuration` before `Release generation` before `Other`, each
heading's entries carrying only the labels that name it.

**Fail (order):** `Other` printed before a named theme.

**Fail (misplaced entry, needs facts):** an entry for a change labelled
`area:cost` printed under `Release generation`, where the facts name no such
label on that change.

### B2 - Nothing under a heading but entries

**Judges:** whether what stands under each theme heading is entries and
nothing else.

**Does not judge:** the headings themselves and their order, which is B1, nor
whether a single entry is shaped right, which is level C. This axis reads
what is between the headings.

This template carries no release-level notice at all - unlike the technical
template, which allows exactly one - so there is no case in which a paragraph
under a heading is anything but a defect.

**Decision procedure**

1. Go through the text under each heading. Anything that is not an entry is a
   fail: a paragraph, a nested list, a rule between entries, a remark on the
   release as a whole.
2. Nothing stands after the last heading of the document.
3. A document made only of entries under headings, nothing else, passes.

**Pass:** every heading followed directly by its bullets, nothing else in the
document.

**Fail:** a paragraph opening a theme - "This section covers configuration
work" - before its first bullet.

### B3 - Length and checkable claims

**Judges:** whether entries stay within the sentence ceiling the format sets,
and whether every claim of impact in the document is one a reader could check.

**Does not judge:** whether an entry states an impact at all - that is C2 -
only its shape once it does. Nor whether the change itself belongs, which is
A1.

**Decision procedure**

1. Count the sentences of each entry. Two is the shape, one per slot; a third
   needs a reason a reader would accept, and a fourth is a fail regardless of
   content.
2. Take every claim of degree in the document - faster, cheaper, more
   reliable, a fraction, a proportion - and ask what in the entry lets a
   reader check it. A claim with nothing to check it against is a fail,
   whether it is a superlative, an adjective, or a bare assertion of
   importance.

**Pass:** "cuts the cost of a run by roughly a third."

**Fail:** "This is a huge improvement for how the team can plan releases." -
nothing in it can be checked.

---

## Level C - Entry

Every entry is built from two slots, in this order.

| Slot                | What it carries                                             |
|----------------------|---------------------------------------------------------------|
| **1 - What changed** | the change, stated as a fact about the product               |
| **2 - Why it matters** | what it means for the people the product serves, or for a decision the reader is tracking |

Both slots are present on every entry. Neither is optional here, unlike the
customer template's slots 2 to 4: this reader is never told to act, so there
is no case in which either slot has nothing to say - see *Why this rubric has
seven axes* above.

### C1 - Stated as a fact about the product, not about the work

**Judges:** whether slot 1 says what changed about the product, or what was
done to build it.

**Does not judge:** whether the change matters, which is C2, nor whether it
is written in language this reader would recognise, which is C3.

**Decision procedure**

1. Try to state the clause as a property of the product, true as of this
   release, using only what the clause already contains.
2. If that rewrite works without inventing anything, the clause is about the
   product: pass.
3. If the rewrite has to invent what the product now does or looks like -
   because the clause names only the work, whoever or whatever its
   grammatical subject is - fail.
4. Grammatical shape does not decide it, the same way it does not for C1 of
   `rubric/customer.md`. "The team refactored the preview pipeline to share
   code with the real run" and "the preview pipeline now shares code with the
   real run" can describe the same change; only the second states a property
   the reader can check against the product as it stands.

**Pass:** "Release previews and real runs are now built from the same
facts."

**Fail:** "Refactored the preview pipeline to share code with the real run
path." The rewrite would have to invent what a reader can now observe about
the product; the clause only reports the work.

### C2 - Says why it matters, and says something slot 1 did not

**Judges:** whether the entry states what the change means for the people the
product serves or for a decision the reader is tracking, beyond what slot 1
already said.

**Does not judge:** whether that statement is checkable - that is B3's claim-
of-degree rule - nor whether the change is worth including at all, which is
A1.

**Decision procedure**

1. Does the entry name a consequence at all - who benefits, what a reader can
   now decide, plan or claim that they could not before? If no, fail.
2. A candidate that only restates slot 1 is not framing. Strike slot 1 from
   the entry and read what is left: does it still tell the reader something
   they did not already have? If it only repeats the mechanism or its
   negation in different words, fail.
3. One consequence is enough. This axis does not ask whether it is the
   strongest one available.

**Pass:** "...so a preview can be trusted to match what the release actually
ships, without spending a real run to find out."

**Fail (restates slot 1):** "...because the same facts now feed both." Slot 1
already said the two are built from the same facts; this clause adds nothing
a reader did not already have.

### C3 - No implementation vocabulary (cross-slot)

**Judges:** whether every expression in the entry is one this reader could
have met without reading the source or the developer documentation.

**Does not judge:** whether the change belongs in the rendering, which is A1,
nor whether a claim in it is checkable, which is B3.

Applies to the whole entry, not to one slot. The reader tracks the product
from outside its repository, the same restriction `rubric/customer.md`
states for C5 and for the same reason: familiarity with the source does not
count as familiarity for this reader either, whatever their title.

**Decision procedure**

1. Take each expression that is not ordinary language - a name, an
   identifier, a value, a marker, a format.
2. Ask how this reader would have met it: in a specification they wrote, in a
   roadmap document, in the product as it runs, or only by reading the
   source. If they would have met it any way but the last, it passes.
3. If they would only meet it by reading the source or the developer
   documentation, it fails.
4. A setting is a case of rule 2, and its two forms differ exactly as they do
   for C5 of `rubric/customer.md`: a name this reader would recognise from a
   specification or from using the product passes; the internal key that
   names it in the source does not.

**Pass:** "how deep the fact base reaches into linked issues" - a decision a
product manager could have specified, whether or not they wrote the line that
implements it.

**Fail:** "`curation.factBaseDepth`" - the configuration key, met only by
reading the source.

*Where the changelog is about Chartula being evaluated by this project, this
axis carries the same corpus defect `rubric/customer.md` names for C5: the
product whose surface it judges is the tool whose internals the entries name.
See the corpus note there rather than repeating it.*

---

## Reference cases

### Minimal pairs

Each axis carries an example that violates **only** that axis. Constructed,
not observed - see *This rubric has no labelled corpus yet* above. Written as
one base document plus one change per axis, on the same reasoning
`rubric/customer.md` gives for that shape rather than near-identical copies:
copies of the same text drift apart, which is the failure that rubric already
had once.

The entry-level pairs sit with their axes above: C1 at its Fail example, C2 at
the restatement, C3 at the configuration key.

**Base document** - passes A1, B1, B2, B3 and every C axis on every entry:

```markdown
### Configuration

- A project's own configuration file now layers over environment variables
  instead of requiring one or the other. Teams that already keep
  configuration in a file no longer have to duplicate it as environment
  variables to satisfy the tool.

### Release generation

- A release can be previewed before anything is written or published, from
  the same facts the real run would use. Reviewing a release no longer costs
  a real run to find out what it would contain.

### Other

- Technical, customer and product notes are now written from one shared set
  of facts rather than three separate passes over the same pull requests. The
  three can no longer describe a release differently from one another.
```

**B1 - themes in order.** Swap `Release generation` and `Configuration`, so
the document reads `Release generation`, `Configuration`, `Other`. Every
entry stays under its own heading and every heading still has entries, so B2
is untouched and the entry axes are untouched. It fails on order alone.

**B2 - nothing under a heading but entries.** Insert under `Release
generation`, after its bullet:

> This section covers what changed in how a release comes together.

The headings are unchanged and in order, so B1 passes, and every entry axis
passes on the one entry present. The inserted sentence is not an entry, which
is the one thing this pair tests.

**B3 - length and checkable claims.** Replace the `Configuration` entry with:

> - A project's own configuration file now layers over environment variables,
>   which is a massive quality-of-life improvement that teams are going to
>   love. It also makes onboarding dramatically easier and cuts down on
>   duplicated setup work across the board.

Four sentences, and "massive," "dramatically," and "across the board" have
nothing in the entry to check them against. C1 and C2 still pass - the change
is stated as a product property and a consequence is named - which is exactly
what this pair tests: a claim can be well-formed under C1 and C2 and still
fail on shape and checkability.

**A1, the missing half.** Not a change to the document but to what is handed
alongside it: the base document plus the fact base for the release, in which
one change that cuts the cost of a run by roughly a third has no entry. Every
entry present is correct; the question is only whether the missing one is
noticed.

**A1, the other half - an entry that should not be there.** Add to `Other`:

> - Add the `Chartula.Cli.Tests` project so CLI behaviour is covered by
>   tests. The team can now be confident that command-line regressions are
>   caught before a release.

Nothing about what the product does, costs, or can be trusted to do changed,
so A1 fails. It states a property ("the project now has CLI test coverage"),
so C1 passes; it names a consequence beyond slot 1, so C2 passes; nothing in
it requires reading the source, so C3 passes; it sits under `Other`, correctly
in alphabetical last place, so B1 and B2 are untouched.

### Realistic case

None yet. No release has been rendered for the product audience at the time
this rubric was written, so there is nothing here to draw a labelled failure
from - the same gap *This rubric has no labelled corpus yet* names above.
Stage 2 of [`../docs/pipeline.md`](../docs/pipeline.md) is what fills this
section in, once a run exists to sample from.

---

## Fact base implications

Two of the axes above cannot be applied to a document alone, and each needs
one thing from the facts:

- A1's second half needs the release's changes, to see what has no entry.
- B1's entry-placement rule needs the labels on each change, to see whether
  an entry sits under the theme its own facts name.

Each is written to withhold rather than guess when the facts are absent. An
axis that answers from a document it cannot see the answer in is worse than
an axis that says it cannot.

---
