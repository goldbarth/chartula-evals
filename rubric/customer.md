# Rubric: the customer rendering

What makes a customer-facing changelog **document** shippable.
Written for the customer audience only.
The technical and product renderings are not covered here.

**Not covered here:** whether the content is factually correct.
That is the faithfulness check's job.
An entry can be perfectly grounded and still fail every axis below.

## Levels

Criteria sit on three levels. Each axis belongs to exactly one.
The level tells you which pipeline stage to fix when an axis fails.

| Level             | What it judges                | Fix belongs in     |
|-------------------|-------------------------------|--------------------|
| **A - Selection** | which changes appear at all   | curation           |
| **B - Document**  | order, grouping, length, tone | rendering template |
| **C - Item**      | the individual entry          | prompt             |

An item that fails level A is removed, not rewritten.
An item that fails level C is rewritten.
A document that fails level B is re-assembled from unchanged items.

What each axis owns, and what it leaves to a neighbour, is stated in the axis
itself - see [`how-a-rubric-is-built.md`](how-a-rubric-is-built.md) for why that
is the first thing written.

---

## Units

The levels apply to different things, so the document has to be cut into units
before anything can be judged. A customer rendering is made of four kinds of
text, and only one of them is an item.

| Unit                | What it is                                                                                        | Judged by    |
|---------------------|---------------------------------------------------------------------------------------------------|--------------|
| **Header**          | version, date, one sentence on what the release is about                                          | B3 rule 4    |
| **Group heading**   | the label over a set of items - what needs action, new, improved, fixed                           | B1, B2       |
| **Item**            | one entry reporting one change, built from the four slots                                         | A1, C1 to C5 |
| **Connective text** | prose that is not about one change: a lead-in, a closing note, a remark on the release as a whole | B1, B2, B3   |

**What makes a piece of text an item**

1. It reports a change to the product, and it is about that change rather than
   about the release. If it can be read as a row in a table of changes, it is
   an item.
2. It carries slot 1. An entry with no observable event is still an item; it
   fails A1 or C1 and is scored as one.
3. Headings are never items, whatever they contain. A heading that carries the
   only description of a change is a B2 finding, and the change counts as
   missing at level A.
4. A paragraph about several changes at once, about something that was *not*
   changed, or about the release as a whole is connective text. It gets no row
   in the item table and is judged at level B.

**Two cases the runs have already produced**

*One entry, two changes.* An entry that reports two unrelated changes stays one
item and is judged as it stands - the axes are applied to the entry, not to
each change inside it. That an entry bundles two changes is a B2 finding, since
grouping is a document-level property.

*The collapsed line.* Where the format gathers minor changes into a single
closing line, that line is an item: it reports changes, a reader reads it as
content, and its slot 1 covers the group it stands for. C2 to C4 are usually
`n/a` on it, which is the point of collapsing them.

A run that has no group headings at all is still judged: B1 and B2 fail, and
every entry is still an item.

---

## Level A - Selection

### A1 - Product surface relevance

**Judges:** whether the rendering carries the changes a reader could notice,
and nothing else.

**Does not judge:** how a change is worded once it is there - that is C5 - nor
whether the entry opens on the right thing, which is C1, nor where it sits,
which is B1 and B2. A change can belong here and be described badly; the entry
is then rewritten, not removed.

The axis has two halves and both are judged. An entry that should not be there
is visible in the document. A change that should be there and is missing is not
visible in the document at all - it can only be found against the release's
facts, and it is the more expensive omission, because a reader cannot ask about
something they were never told.

**Decision procedure, half one: is anything here that should not be**

1. For each entry, ask what a reader would have to do to notice this change by
   using the product: run something, look at an output, meet a different
   behaviour, set something that was not there. If nothing they do can bring
   them into contact with it, the entry fails.
2. The question is about the change, not about the words. An entry describing
   internal work in faultless prose still fails; an entry describing an
   observable change in jargon passes here and fails C5.

**Decision procedure, half two: is anything missing**

3. Only when the facts of the release are given alongside the document. Without
   them this half cannot be judged and is not guessed at.
4. Go through the facts, not through the document. For each fact, apply rule 1:
   could a reader come into contact with this change? If yes, find the entry
   that carries it.
5. A fact that passes rule 1 and has no entry is a fail, and the fact is named.
   Several omissions are one verdict; the axis asks whether the rendering is
   complete, not how incomplete it is.
6. A fact no reader could come into contact with needs no entry. Its absence is
   correct.

**Pass:** a change to how much text the tool generates before stopping, carried
by an entry - a reader meets it by generating a long release.

**Fail (present, should not be):** an entry about which internal component
performs the categorisation, with identical output. Nothing the reader does
brings them into contact with it.

**Fail (absent, should be there):** the facts carry a change that stops the tool
failing when a release has no pull requests attached, and no entry mentions it.

*A dependency upgrade shows both sides: it fails rule 1 when nothing observable
changed, and passes when it did - described by what changed for the reader,
never by the dependency.*

---

## Level B - Document

### B1 - Action first

**Judges:** whether every entry that asks something of the reader stands above
every entry that does not.

**Does not judge:** whether an entry says clearly enough what to do - that is
C4 - nor which group an entry sits in, which is B2. Both axes use the same test
for what counts as asking something; B1 asks where it stands, C4 asks whether
it is stated.

An entry asks something when not doing it costs the reader: their setup stops
working, their output changes under them, they have to move or rename
something. An optional setting, or where a new feature can be reached, costs
them nothing if ignored.

**Decision procedure**

1. Go entry by entry. Group headings decide nothing here: a group called "What
   needs action" can stand at the top while an entry that asks something sits
   three groups below it, and that is the failure this axis is for.
2. Mark every entry where the test above says the reader pays for ignoring it.
3. No marked entry: pass. There is no order to get wrong.
4. Every marked entry must stand above every unmarked one. One marked entry
   below one unmarked entry is a fail, whichever groups the two sit in.
5. A breaking change always costs the reader something and comes first of all.

**Pass:** the only entry carrying a migration is the first entry of the
document.

**Fail:** an entry saying the old configuration section stops being read, placed
below two entries that ask nothing.

### B2 - Grouping and order

**Judges:** whether the document is built out of the groups the format defines,
in the order it defines, and whether the document opens the way the format
says.

**Does not judge:** what an entry says, which is level C, nor whether an entry
that asks something sits high enough, which is B1. This axis reads structure
only.

The groups, their order and the opening are defined in
[`../docs/output-format.md`](../docs/output-format.md). They are not repeated
here: a group name written in two documents is a contradiction waiting for one
of them to be edited.

**Decision procedure**

1. Read the group headings in order and compare them with the set and order the
   format defines. A group out of that order is a fail whatever it contains.
2. A group the format does not define is a fail. A group with no entries is
   omitted, not printed empty.
3. Compare the document's opening with what the format requires of it for the
   serialisation at hand. A missing or incomplete opening is a fail.
4. A document with no group headings at all fails: it cannot satisfy rule 1.

**Pass:** the groups the format defines, in its order, with the ones that have
no entries left out.

**Fail:** fixes printed above the new entries; or a rendering that is one flat
list of bullets with no headings.

### B3 - Length and tone

**Judges:** whether the document can be scanned, and whether it claims more
than it can show.

**Does not judge:** whether an entry contains an outcome, a scope or an action -
those are C2 to C4 - nor the groups and the opening, which are B2. This axis
reads how much is written and in what register.

**Decision procedure**

1. Count the sentences of each entry. One or two is the shape; three needs a
   reason a reader would accept; four or more is a fail however good the
   content is. Sentences that follow the outcome count here: C3 is satisfied
   once the outcome is stated, and what trails behind it is length.
2. Minor changes are gathered into one closing line of their group rather than
   listed one by one. A run of entries a reader would not act on, each with its
   own bullet, is a fail.
3. Take every claim of degree - faster, smaller, more reliable - and ask what
   in the entry lets a reader check it. A claim with nothing to check it
   against is a fail, whether it is written as a superlative, an adjective or
   an exclamation.

**Pass:** "Generation is roughly twice as fast on releases with more than 50
pull requests."

**Fail:** "We've completely reimagined generation performance - it's blazingly
fast now!" - nothing in it can be checked.

---

## Level C - Item

Every item is built from four slots, in this order.
The slots are the same for every change type; only what fills them differs.

| Slot                | Fix                                 | Feature                          | Breaking change                        |
|---------------------|-------------------------------------|----------------------------------|----------------------------------------|
| **1 - Observation** | what went wrong, as the user saw it | what is now possible             | what no longer works as before         |
| **2 - Scope**       | when it occurred                    | who it is for, if not everyone   | who is affected                        |
| **3 - Outcome**     | what you can now rely on            | the detour that disappears       | what holds once the migration is done  |
| **4 - Action**      | usually "nothing to do"             | what to set, where, if anything  | the migration step - carries the entry |

Slots 2, 3 and 4 may be absent. Slot 1 never is.
Slot 4 is absent when there is nothing to set: see C4.

### C1 - Observation leads

**Judges:** whether the opening of the entry says what the reader meets, or
what was built.

**Does not judge:** which words appear in it - a setting, a file, a command may
all stand in an opening that is about the reader, and whether they are named
well enough to act on is C4, whether they are prose or a raw key is C5. Nor
does it judge what follows the opening: the outcome is C3, the length is B3.

What counts as what the reader meets depends on the change type, and it is the
same thing slot 1 of the item is for:

| Change type     | The reader meets                                        |
|-----------------|---------------------------------------------------------|
| Fix             | what went wrong, as they ran into it                     |
| Feature         | what they can now do or now see                          |
| Breaking change | what no longer works the way it did                      |

A feature does not need a problem. "You can now preview a release before
anything is published" is something the reader meets: they can do it, and can
see that they can.

**Decision procedure**

1. Ignore a bold label and the colon after it. It names the entry, not the
   sentence, and the format specifies it that way. Judge the first clause of
   the text that follows.
2. Try to rewrite that clause as "you can now …" or "this happened to you
   when …", using only what the clause already contains.
3. If the rewrite works, the opening is about the reader: pass.
4. If the rewrite has to invent the reader's side - because the clause is about
   the work that was done, whoever or whatever its grammatical subject is -
   fail.
5. Grammatical shape does not decide it. "Chartula now writes the customer and
   product texts into the same file" and "the customer and product texts are
   now written into the same file" are one statement, and both rewrite cleanly
   as "you can now find both texts in one file".

**Pass (fix):** "Generated text could be cut off mid-sentence because no output
length limit was set."

**Pass (feature):** "You can see the finished notes before anything is written
or published."

**Pass (feature, stated as a property):** "Technical, customer and product notes
are written from the same set of facts." The reader has the three renderings in
front of them; this says what is true of them now.

**Fail:** "There is now a configurable output length limit, so text no longer
gets cut off mid-sentence." The rewrite would have to invent what the reader
ran into.

*This is the only axis that example violates: no jargon, outcome stated, length
fine. It fails on order alone.*

**Fail (feature):** "Support for previewing a release was added." Same fact as
the feature pass above, opened on the building of it.

### C2 - Scope stated or deliberately absent

**Judges:** whether the reader can tell whether they were affected.

**Does not judge:** whether the condition is true - that is the faithfulness
check, not this rubric - nor how it is worded, which is C5.

**Decision procedure**

1. Did this affect everyone, always? Then slot 2 is correctly absent: pass.
2. Did it affect a subset? Then the entry names the condition, and a reader can
   put themselves inside or outside it. "On longer releases" and "if you
   publish from a fork" do that without a number.
3. Does the entry gesture at a condition without naming one, so that a reader
   cannot tell which side they are on? Fail. "In some runs" is the shape: every
   run is some run.
4. Is the condition unknown, because the source data does not say? Then slot 2
   is omitted entirely and the item is marked for review. An unknown condition
   is not written as a guess.

**Pass (condition known):** "…on releases containing more than about thirty
pull requests."

**Pass (not applicable):** no scope clause at all, because it affected every run.

**Fail:** "…in some runs."

### C3 - Outcome present

**Judges:** whether the item says what the reader can now rely on or do.

**Does not judge:** where in the item that sits - trailing sentences are B3's
length problem - nor whether the opening was right, which is C1.

The outcome may stand anywhere in the item, not necessarily at the end.

**Decision procedure**

1. Does the item name an outcome at all - what becomes possible, what no longer
   needs checking, what can be trusted, what detour disappears? If no, fail.
2. A candidate that only restates slot 1 is not an outcome. Strike slot 1 from
   the item and read what is left: does it still tell the reader something they
   did not already have? If no, fail. Wording does not enter into it - the
   negation of slot 1 and its positive twin are the same statement, and so is
   the mechanism described a second time. Do not look for particular phrases;
   there is no list of them that ends.
3. Position is not this axis. An item that names its outcome and then keeps
   going - an edge case, a caveat, a footnote - passes C3. The trailing
   sentences are a length finding under B3 rule 1.
4. One outcome is enough. C3 does not ask whether it is the strongest one
   available.
5. A breaking change is not exempt. Its outcome is what holds once the reader
   has done what the entry asks - what they get for the migration, not what
   they lose without it. "Once your publishing step points at the release page,
   the notes and the release stay in one place" is an outcome; "you have to
   change where it looks" is the action restated.

**Pass:** "…so you can generate notes for a large release without checking the
output for truncation."

**Pass (outcome not last):** "…so you see the real result before anything is
written, and the same flags apply as in a normal run."
The outcome is stated; what follows it is B3's problem, not C3's.

**Fail:** "…so text is no longer cut off." - the negation of slot 1.

**Fail (the same statement, positively):** "…so text completes properly."
Slot 1 said the text broke off. Saying it now does not is the same fact worded
the other way round, and a reader learns nothing from the second half they did
not have from the first.

**Pass (a contrast that adds something):** "…updates the existing release notes
instead of creating a duplicate." Slot 1 said the notes are written. That
re-running leaves one release rather than two is not in it, so the clause
carries information of its own - the contrast is not what decides it.

**Observed pair**, `sonnet-5-out` item `s5-03`, the same violation from a real
run rather than constructed:

> Configuration mistakes now show a clear error message instead of crashing.

The item names no outcome anywhere. Its only candidate, "instead of crashing",
restates the negative event of slot 1. C1, C2, C4 and C5 all pass on that item.

### C4 - Action explicit

**Judges:** whether an entry that requires something of the reader says what,
concretely enough to act on.

**Does not judge:** where that entry stands in the document - B1 - nor whether
the name it uses is prose or a raw key, which is C5. B1 and C4 use the same
test for what counts as requiring something; B1 asks where it stands, C4 asks
whether it is stated.

**Decision procedure**

1. Does this change require anything of the reader - is there something they
   pay for not doing, or a step without which the change does not reach them?
2. If not, C4 is **n/a**. Not a pass, not a fail: there is no action to
   withhold, and a line saying so is allowed but never demanded.
3. If yes, the entry names it, and a reader could act on the naming without
   looking anywhere else: the setting by a name they can find, the command,
   the place. Announcing that something can be set, without saying where, is a
   fail - the reader now knows a decision exists and cannot reach it.
4. For a breaking change there is always something to do, so C4 is never n/a
   there.

**Pass:** "Existing configuration files keep working; the new setting is
optional."

**Pass (stated redundantly):** "No configuration change is needed."

**n/a:** a metrics summary printed at the end of every run. Nothing is asked of
the reader and nothing stands between them and it.

**Fail (option withheld):** "How much detail each entry carries can be
customised." - a decision the reader cannot reach.

**Fail:** a breaking change described entirely in slots 1-3, with no statement
of what to change.

### C5 - No codebase knowledge required (cross-slot)

**Judges:** whether every expression in the item is one the reader could have
met by using the product.

**Does not judge:** whether the change itself belongs in the rendering - that is
A1, and an internal change can be described in faultless language - nor whether
a named place is concrete enough to act on, which is C4.

Applies to the whole item, not to one slot. The reader is a user of the product
the changelog is about, never the person who built it: what is familiar from
writing the source does not count as familiar.

**Decision procedure**

1. Take each expression that is not ordinary language - a name, an identifier,
   a value, a marker, a format.
2. Ask how the reader would have met it: typed it themselves, seen it in their
   own repository, seen it on screen while using the product. If they would
   have, it passes.
3. If they would only meet it by reading the source or the developer
   documentation, it fails.
4. A setting is a case of rule 2, and its two forms differ: the name a reader
   types or reads in their own configuration passes, the internal key that
   names it in the source does not. That a raw key would satisfy C4 does not
   rescue it here.

**Pass:** `changelog.json` - the tool writes it into the reader's repository
and they open it.

**Pass:** the name of an environment variable the reader sets themselves to run
the tool.

**Fail:** `(breaking)`, a marker that exists inside the fact base and never
reaches a screen.

**Fail (this axis only):** "Generated text could be cut off mid-sentence because
`llm.maxOutputTokens` defaulted to 1024, so you can now generate a large release
without checking the output for truncation."

*Correct order, scope handled, real outcome - jargon alone sinks it.*

*Where the changelog is about the tool being evaluated, this axis is applied but
not cleanly measurable: the product whose surface it judges is the tool whose
internals the entries name. See the corpus note in the friction log.*

---

## Reference cases

### Minimal pairs

Each axis carries an example that violates **only** that axis. Those are the
calibration set: a judge that cannot separate them is not scoring axes, it is
scoring overall impression.

The item-level pairs sit with their axes above: C1 at its Fail example, C2 at
the hedge, C3 with the observed pair from `s5-03`, C4 at the withheld option,
C5 at the jargon example.

The document-level pairs cannot be single sentences, because A1 and B1 to B3
judge a whole document. They are given below as one base document that passes
every axis, plus one change per axis. Written as deltas rather than as four
near-identical documents on purpose: five copies of the same text drift apart,
which is the failure this rubric already had once.

**Base document** - passes A1, B1, B2, B3 and every C axis on every item:

```markdown
## 0.1.0 - 2026-06-14

The first release you can point at a repository and get release notes out of.
Nothing here needs a configuration change unless the entry says so.

### What needs action

- **Breaking:** Release notes published anywhere but the GitHub release itself
  stop being updated, so a project that read them from a file no longer sees
  new ones. Point your publishing step at the release page and the notes stay
  with the release they belong to.

### What's New

- **Three audiences from one source:** Technical, customer and product notes
  are written from the same set of facts, so they cannot disagree about what
  changed.
- **Preview before publishing:** You can see the finished notes before anything
  is written or published, so the first real result is not the one your users
  read. Ask for a preview instead of a full run.

### Bug Fixes

- **Text no longer cut off:** Generated text could stop mid-sentence on longer
  releases, because no output length limit was set. There is a limit now, so
  you can generate notes for a large release without checking the end of the
  text.
```

**B1 - action first.** Add to a new **What's Changed** group, below What's New:

> - **Label rules moved:** A project that steers curation with labels has to
>   move those rules into the new section of the configuration file. The old
>   section stops being read after this release.

An entry that asks something of the reader then sits below two entries that ask
nothing. The groups themselves stay in the defined order and none is empty, so
B2 is untouched - which is the only way to separate the two axes, since both of
them are about where things sit.

**B2 - grouping and order.** Swap the **What's New** and **Bug Fixes** groups,
so the fixes are printed first. Every entry is unchanged and stays in its own
group, no group is empty, and the only entry that asks anything of the reader
is still the first in the document: B1 passes, B3 passes, the item axes are
untouched. It fails on rule 1 alone.

**B3 - length and tone.** Replace the Bug Fixes entry with:

> - **Text no longer cut off:** Generated text could stop mid-sentence on
>   longer releases, because no output length limit was set. There is a limit
>   now, so you can generate notes for a large release without checking the end
>   of the text. The limit can be raised if your releases are unusually large.
>   Truncation is completely gone and generation is blazingly reliable now.

Four sentences and a superlative without a number. C3 still passes - the
outcome is stated and what trails behind it is B3's problem, not C3's - and
that is exactly what this pair tests.

**A1, the missing half.** Not a change to the document but to what is handed with it:
the base document plus the fact base for the release, in which one user-visible
change has no entry. Say, a change that stops the tool failing when a release
has no pull requests at all. Every entry present is correct; the question is
only whether the missing one is noticed.

That is the expensive half of A1, and the half a judge is actually needed for.

**A1, the other half - an entry that should not be there.** Add to a new
**What's Changed** group, below What's New:

> - **Categorisation:** Whether a change counts as a feature, a fix or internal
>   work is decided the same way for every release, from the title of the change
>   alone.

Nothing a reader does brings them into contact with this, so A1 fails. It opens
on a property they could state, so C1 passes; it says what they can rely on, so
C3 passes; it uses no expression from the source, so C5 passes; there is nothing
to do, so C4 is n/a. The group is in the order the format defines and no entry
asks anything of the reader, so B1 and B2 are untouched.

This pair could not be written before. While C1 failed anything that named what
was built, an internal change failed C1 and A1 together - `o5-10`, `o5-17`,
`o5-25` and `s5-23` all show that pattern. C1 now asks only whether the opening
rewrites as something that happened to the reader, and an internal change
stated as a property of the output passes that while still failing A1.

### Realistic case

The fix section of the v0.1.0 customer rendering.
Retained because it shows what a real failure looks like - several axes at once.
Not usable for calibration for exactly that reason.

**Labelled not shippable** (Haiku 4.5, `test-runs/haiku-4-5-out.md`, lines 260 to 264):

Quoted verbatim, as a code block rather than a blockquote so the line breaks
survive. The breaks inside `defaulting` and `Conventional` are the run's own
output, not a copy error.

```text
Fixed output truncation by setting `max_tokens` on LLM calls. Previously omitted, it defaulted to 1024 per provider, cutting off all three audience texts mid-word. Now configurable via `llm.maxOutputTokens`, default
ing to 16000.

Fixed false breaking-change detection. The categorizer was matching `BREAKING CHANGE` as a case-insensitive substring anywhere in the PR body, so prose discussing breaking changes declared one. Now matches the Conve
ntional Commits footer format: uppercase, start of line, colon-terminated.
```

Fails C1: "Fixed output truncation by setting `max_tokens`" cannot be rewritten
as what happened to the reader without inventing it - the clause is about the
work. Fails C3: strike slot 1 and what is left restates the mechanism. Fails
C5: `max_tokens`, `llm.maxOutputTokens`, 1024, "the categorizer" and the footer
specification are all expressions a reader meets only in the source.

C4 is not among them. The first item names where the ceiling is set and the
second requires nothing, so both are answered. That the first names it as a key
rather than as something the reader would meet is C5's finding.

C2 is absent in both items without it being clear whether the condition does
not apply or was never looked up - the case rule 4 exists for.

**Labelled shippable** (written by hand, not produced by a run):

> - Generated text could be cut off mid-sentence on longer releases; there is now
> a ceiling with a higher default, so you can generate notes for a large release
> without checking the output for truncation. No configuration change is needed.
>
> - Changes that merely mentioned breaking changes in their description were
> sometimes labelled as breaking themselves; only an actual breaking-change
> declaration is recognised now, so the notes no longer warn about breaks that
> are not there.

---

## Fact base implications

Slots 2, 3 and 4 need three distinguishable states in the fact base:
**present**, **not applicable**, **unknown**.

Collapsing the last two into one empty field is what produces hedges like
"in some runs" - the formulator finds nothing, cannot tell that nothing is the
correct answer, and fills the gap. *Unknown* omits the slot and flags the item.
*Not applicable* omits the slot silently.

---

## Open

- The minimal pairs are written for every axis. Whether the wrongly-included
  half of A1 can now carry one of its own is the open question - see the
  proposal at the end of the minimal pairs.
- Whether a scope condition has to be checkable by the reader - a number, a
  name, a version - or whether naming it qualitatively is enough, as C2 rule 2
  now allows.
- Whether an item that opens with an instruction rather than an observation
  passes C1. Seen once, on `o5-01`, which is too little to write a rule from.
- Feature and breaking-change items have no labelled reference case yet; the
  slot table is derived from best practice, not observed in a run. v0.1.0
  carries no breaking change, so that half is not reachable from this release.
- C5 is applied on a corpus where the product it judges is the tool the entries
  describe. It is judgeable there and not cleanly measurable; see the corpus
  note in the friction log.
