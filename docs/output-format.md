# Output format

The shape a rendering is built to.

`rubric/customer.md` says how a rendering is judged; this file says what it is
supposed to look like. Form rules live here only, and the rubric points at them
rather than restating them - two documents describing the same form is how the
C3 split reading happened.

## Templates

Format is meant to be selectable, one template per audience, so that a project
can keep its house style. This file holds the defaults.

| Audience  | Default template            | Status                                    |
|-----------|-----------------------------|-------------------------------------------|
| Customer  | `customer/plain` (below)    | strawman, not agreed                      |
| Technical | `technical/common-changelog` (below) | adopted, not written here             |
| Product   | `product/thematic` (below)  | drafted, not agreed                       |

A template fixes the form: headings, groups, entry shape, what may appear at
all. It does not fix quality. Whether an entry opens on what the reader meets,
whether it says what they can rely on, whether a claim of degree can be checked
- those hold whichever template is chosen, and stay in the rubric.

The release heading carries only the version number, never a name. Naming
releases is a marketing pattern for platforms with their own release cadence,
not for a tool a project runs against its own tags.

---

## Customer: `customer/plain`

Established changelog formats do not fit this audience. Keep a Changelog,
Common Changelog and the Conventional Commits generators all group by change
type and are written for developers reading a repository. The customer
rendering groups by what the reader has to do about it. This template is
therefore written here rather than adopted.

### Two serialisations

The same content is written out in two shapes, because it has two destinations.

*Published* - a page on a site, one file per release:

```markdown
---
title: Release 0.2.0
description: One sentence on what this release is about.
publishedAt: 2026-06-14
tags:
  - configuration
  - release notes
---

### What's New
...
```

*File* - `CHANGELOG.md`, many releases in one document. No front matter, the
metadata becomes a heading: `## 0.2.0 - 2026-06-14`, newest release first, and
`description` becomes the sentence under it.

Front matter fields: `title`, `description`, `publishedAt`, `tags`. `title` and
`publishedAt` follow from the git tag: the version number, and the tag's own
date - not the date the notes happen to go out, which drifts with a delayed
publish or a retried run and gives one release two dates for the same fact. See
**Tags** and **Description** below for the other two.

### Groups

1. Groups are third-level headings, in this order, and only those that have
   items:

   | Group                   | What belongs in it                                    |
   |-------------------------|-------------------------------------------------------|
   | **What needs action**   | anything the reader has to do: a migration, a rename, a setting that must be set |
   | **What's New**          | capabilities that did not exist before                |
   | **What's Changed**      | behaviour that existed and now works differently, better included |
   | **Bug Fixes**           | something was broken and is not any more              |

2. Group names are audience-facing. `Added`, `Changed`, `Removed` describe what
   happened to a codebase; a customer wants to know whether something is
   expected of them.
3. Improvements do not get a group of their own. For a reader, "better than
   before" and "different from before" are the same question - did the thing I
   rely on change - and one group answers it.
4. Mapping from the categorised change: a breaking change goes to **What needs
   action** whatever its category; `feat` goes to **What's New**; `fix` goes to
   **Bug Fixes**; `perf` and behaviour-affecting `refactor` go to **What's
   Changed**; `docs`, `chore`, `ci`, `build`, `test` and `style` do not appear
   at all, per A1.
5. Nothing after the last group. A migration guide link is an action and
   belongs in its entry, not in a footer - a link under the last group is the
   one thing the reader must act on, placed where B1 says it may not be.

### Entry

6. One bullet per entry, one entry per change.
7. A bold lead-in is allowed and is a **label, not the beginning of the
   sentence**. `- **Batch requests:** You can now send several requests in one
   call...` is correct. The text after the colon opens on what the reader can
   observe, never on `We've added`, `Added`, `New support for` or `Fixed an
   issue where` - that shape is what produced most C1 failures in the labelled
   runs.
8. Slots in order: observation, scope, outcome, action. Scope, outcome and
   action are omitted when they do not apply, per C2 to C4.
9. Two sentences. A third needs a reason, and a fourth is a defect regardless
   of how good the content is.
10. A breaking change carries `**Breaking:**` as its label, lives in **What
    needs action**, and comes first there. The marker is borrowed from Common
    Changelog, which is where readers already know it from. Its action slot
    carries the migration link if there is one.
11. Minor changes are gathered into one closing bullet of their group, opening
    with `Also:`. It is an item and is scored as one; scope, outcome and action
    are usually `n/a` on it, which is the point of collapsing them.

### Never appears

12. Pull request numbers, commit hashes, issue references, author names,
    compare links.
13. Configuration keys, file paths, class or method names, concrete default
    values.
14. A setting is named in prose - "how much detail feeds the release notes" -
    and where it is set is named as a place, not as a key.

### Tags

Tags come from the labels on the pull requests behind the release, filtered
through an allowlist in the configuration. Nowhere else.

*Not from the categories.* A category is a change type, and the change type is
already the group heading. A tag reading `Feature` above a group called What's
New tells the reader nothing. Reliable, and redundant.

*Not from a fixed vocabulary.* Mapping a change onto a vocabulary means
classifying it. A lookup table goes stale the moment a project works on
something new, and letting the model do it puts a word in the document that
does not appear in the facts - which is what the rule-based faithfulness check
exists to flag. It would be a hallucination source built into the one place
where nothing new is supposed to appear.

*What labels give* is subject matter, which is what a tag is for: show me
everything about the API, everything about security. It is the project's own
vocabulary, it is deterministic, and label rules are already configurable.

**When there are no labels there are no tags.** The field is omitted, not
emitted empty, and never filled from categories as a substitute. A project
without label discipline gets a document without tags, and that is the honest
output rather than a defect - the same distinction C2 draws between a condition
that does not apply and one nobody looked up.

The allowlist is not optional. Without it `good first issue` and `needs-review`
end up in front of customers.

### Description

The description is one sentence on what the release is about, written from the
facts of that release and from nothing else.

It is the field that had no source. `title` and `publishedAt` follow from the
tag and its date, `tags` has the section above, and this one said what it
contained without ever saying where it came from - so nothing produced it and
the opening could not be assembled. Naming the source is what makes the field
buildable rather than aspirational.

*Written by the model, in the same pass as the audience texts.* It is a
rephrasing of facts already in front of it, which is the one thing the
generation step is for, and the faithfulness check covers it exactly as it
covers everything else the model writes. That check is why the source has to be
stated: a sentence built from anything outside the release's facts is
unsupported by construction, and the check would be right to flag it.

*Not from configuration, and not by hand.* Either means someone has to remember
it at every release, and a field nobody remembers is a field that goes stale or
stays empty. The whole point of generating a changelog is that the release does
not depend on anyone recalling a step.

*Not the first entry reworded.* The description says what the release is about;
the first entry says what one change is. A release whose description is its
largest feature tells the reader nothing they will not read one line further
down, and it silently makes the ordering of the entries decide the summary.

**When it cannot be written from the facts, the field is omitted**, on the same
rule as tags: omitted, not emitted empty, and never filled with a placeholder.
A release with nothing to summarise is a release whose customer section has no
entries either, and that is the empty release below rather than a document with
an invented sentence at the top.

### An empty release

A release where every change was filtered out still produces a document, and
that document says so. Slack's maintenance releases are the model: the reader
who came looking gets an answer, not a missing page.

The line is fixed and configured by the project, not generated - it is the
`emptyReleaseNotice` option below, a single string under `customer` in
`chartula.yaml` alongside `voice` and `boldLabel`. It does not rotate. A fixed
notice is what the other template options already commit to, and a rotating one
would put a sentence in front of the reader that no release fact produced.

The document has no groups and no entries, so `description` and `tags` are
omitted with them.

### Template options

Settings a project chooses once. They change the form, never whether an entry
is any good, so no rubric axis reads them.

| Option        | Values                                  | Default      |
|---------------|-----------------------------------------|--------------|
| `voice`       | `impersonal`, `first-person-plural`     | `impersonal` |
| `boldLabel`   | `on`, `off`                             | `on`         |
| `tags`        | `on`, `off`                             | `on`         |
| `emptyReleaseNotice` | any string                       | `No customer-facing changes in this release.` |

`voice` decides between "Release notes are now written to the GitHub release"
and "We now write release notes to the GitHub release". Both are defensible and
the choice belongs to the project, not to this file. What is not optional is
that one run does not switch between them.

### Worked shape

```markdown
---
title: Release 0.1.0
description: The first release you can point at a repository and get release notes out of.
publishedAt: 2026-06-14
tags:
  - release notes
  - configuration
---

### What needs action

- **Breaking:** Release notes are now written to the GitHub release itself, so
  a project that published them elsewhere has to change where it looks. Point
  your publishing step at the release page - see the [migration guide](link).

### What's New

- **Preview before publishing:** You can see the finished release notes before
  anything is written or published, so the first real result is not the one
  your users read.
- **Three audiences from one source:** Technical, customer and product notes
  are written from the same set of facts, so they cannot disagree about what
  changed.
- Also: labels can steer what is included, internal work is left out by
  default, and how much detail feeds the notes can be set in the configuration
  file.

### What's Changed

- **Consistent wording across releases:** Notes now read in one voice
  regardless of how the underlying pull requests were written, so a release
  does not sound like whoever happened to write it.

### Bug Fixes

- **Text no longer cut off:** Generated text could stop mid-sentence on longer
  releases, because no output length limit was set. There is a limit now, so
  you can generate notes for a large release without checking the end of the
  text.
- **Breaking changes labelled correctly:** Changes that only mentioned breaking
  changes in their description were sometimes labelled breaking themselves.
  Only an actual breaking-change declaration counts now, so the notes stop
  warning about breaks that are not there.
```

---

## Technical: `technical/common-changelog`

Adopted, not written. [Common Changelog](https://common-changelog.org) is a
strict subset of Keep a Changelog: it requires a reference per entry instead of
merely allowing one, it fixes the order of the groups instead of listing them,
and it forbids copying commit or pull request titles verbatim. Every rule below
is its rule, cited so that a later reader can tell what was adopted from what
was decided here.

The reader is a developer reading a repository, which is the audience those
formats were written for, so the reasoning that made the customer template
necessary does not apply here. Where this file says something Common Changelog
does not, it is marked as such.

### Serialisation

One shape, not two. The technical rendering is what `CHANGELOG.md` is written
from and what the GitHub release notes carry, and both are the same document:
many releases in one file, newest first, no front matter.

### Release

15. A release opens on a second-level heading, `## VERSION - DATE`. The version
    is semver with no `v` prefix and matches the git tag; the date is ISO 8601,
    `YYYY-MM-DD`.
16. A release may carry one notice and no more: a single-sentence paragraph
    directly under the heading, for context that belongs to the release rather
    than to any one entry - a yanked release, or why a release has no entries.

A release with no entries is published with such a notice, not skipped. An
empty heading with nothing under it is not a valid release per Common
Changelog, and dropping the release would contradict how the customer template
resolves the same question one section above.

### Groups

17. Groups are third-level headings, in this fixed order, and only those that
    have entries:

    | Group       | What belongs in it              |
    |-------------|---------------------------------|
    | **Changed** | changes in existing functionality |
    | **Added**   | new functionality               |
    | **Removed** | removed functionality           |
    | **Fixed**   | bug fixes                       |

    The order is Common Changelog's and is not alphabetical or chronological:
    what a reader already depends on comes before what is new to them.
18. There are no other groups. A release with nothing but new functionality has
    one heading, not four.
19. Mapping from the categorised change: `feat` to **Added**, `fix` to
    **Fixed**, `perf` and behaviour-affecting `refactor` to **Changed**, a
    removal to **Removed** whatever its type.

Which changes reach this rendering at all is the customer template's
categorical default, unchanged: `docs`, `chore`, `ci`, `build`, `test` and
`style` do not appear. The one case Common Changelog treats differently - a
production dependency bump, or a newly-written doc for a feature that had none
- is not solved by the type filter, and it does not get a mechanism of its own:
it goes through the same label allowlist the tags already use.

### Entry

20. One line per entry, one entry per change. Not a paragraph, and nothing
    nested under it.
21. The line is a change description, then one or more references in
    parentheses, then zero or more authors in parentheses. The reference is
    required, and it is the rule that separates this format from Keep a
    Changelog.
22. Authors are omitted only on a release where every entry is by the same
    single contributor. As soon as a second author appears, every entry in that
    release carries its author - not a setting a project turns off, because the
    reader cannot tell an omitted author from a sole one. A bot-authored change
    is attributed to whoever merged the pull request.
23. A breaking change is prefixed in bold with `**Breaking:**` and stands
    before the other entries of its group. The same marker as the customer
    template, for the same reason: readers already know it from here.

### Never appears

24. A commit or pull request title carried over verbatim. Common Changelog
    forbids it, and it is the failure the technical section of
    `sonnet-5-no-thinking-out` produced.
25. The verification block of a pull request: build status, test counts, what
    was covered. It describes the work rather than the change, and
    `sonnet-5-out` carried one into 28 of its entries.
26. A heading of its own per change. The groups above are the only headings
    inside a release.

Class, method, file and configuration names do appear here, and links are kept.
That is the difference from the customer template, where rules 13 and 14 forbid
them: this reader meets the source.

Rule 12 is the sharper difference. Two of the things it withholds from the
customer are not merely allowed here, they are required: a reference on every
entry (rule 21), and an author on every entry of a release with more than one
contributor (rule 22). Commit hashes, issue references and compare links are
allowed and not required. The same fact is kept from one reader and owed to the
other, which is what one template per audience is for.

### What is not form, and is not decided here

Two of Common Changelog's rules judge an entry rather than shape it, and they
belong to a technical rubric when one is written: **imperative mood**, so a
description opens on a present-tense verb - `Add`, `Fix`, `Bump`, `Document` -
and **self-describing**, so an entry reads correctly as if its group heading
were not there. They are named here so that whoever writes `rubric/technical.md`
does not have to rediscover them, and they are not numbered as form rules.

### Worked shape

```markdown
## 0.1.0 - 2026-06-14

### Added

- Report what a run does and what it costs at the end of every `preview` and
  `generate` run ([#66](https://github.com/goldbarth/chartula/pull/66))
- Read `chartula.yaml`, layered before environment variables, with every option
  falling back to its default when no file is present
  ([#64](https://github.com/goldbarth/chartula/pull/64))
- Add a `categories` section controlling category order, display names and
  breaking-change prominence ([#65](https://github.com/goldbarth/chartula/pull/65))

### Fixed

- Send `MaxOutputTokens` on every model call, so generated text is no longer
  truncated at the provider default of 1024
  ([#70](https://github.com/goldbarth/chartula/pull/70))
- Match the Conventional Commits footer when detecting a breaking change, so
  prose that discusses one no longer declares one
  ([#70](https://github.com/goldbarth/chartula/pull/70))
```

---

## Product: `product/thematic`

The reader is neither this document's other two. Not the customer template's
user, who meets the product by running it, and not the technical template's
developer, who meets it by reading it: a product manager, inside the project
or close enough to it to be handed a roadmap, reading to track what shipped
and to frame it for people who were not in the room. They meet the source no
more than the customer does - they were never a contributor either - so rules
36 to 38 below are close cousins of rules 12 to 14, for the same reason and not
a coincidence.

Grouping by change type, the technical template's axis, answers "what kind of
change was this," which this reader did not ask. Grouping by what the reader
has to do, the customer template's axis, answers a question this reader does
not have - nobody hands a product manager a migration. What this reader asks
is "which part of the product moved," so the document groups by theme, which
is why this template earns its own name rather than becoming a third option
under the customer one.

### Serialisation

One document, no front matter. Unlike the other two renderings this one has no
file of its own: the text lives only in `renderings.product` of
`changelog.json` (see [`changelog-json.md`](changelog-json.md)) until a
destination is decided for it. Writing the shape ahead of the file keeps the
order `docs/architecture.md` already put this rendering in - "the product
rendering has no template yet, so it has no file" - and nothing here decides
where it goes once it gets one.

### Themes

27. Groups are third-level headings, one per **theme**, in alphabetical order
    by the theme's own name, and only those with entries. A fixed trailing
    heading, **Other**, holds every entry no theme claims, and stands last
    whenever it is not empty.
28. A theme is a label on the pull requests behind a change, filtered through
    the same allowlist the customer template's tags already use - see *Tags*
    above. One vocabulary for both audiences rather than a second one invented
    here keeps a label meaning one thing across the document set, and keeps
    this template out of the trap that section already names: a fixed lookup
    table goes stale the moment the project works on something it has no word
    for, and a model asked to classify puts a word in the document the facts
    never gave it.
29. A change carrying more than one allow-listed label appears once, under the
    first of its labels in the release's alphabetical order. It is not
    repeated under a second theme - a reader comparing this release with the
    last one has no way to tell a document that grew by one change from one
    that grew by two, once a change can appear twice.
30. **When there are no thematic labels there is one theme**, `Other`, holding
    every entry, and the document still opens correctly. Fixing a project's
    label discipline is not this template's job, on the reasoning the Tags
    section already gives for the same case: an honest single group is not a
    defect, and an invented taxonomy standing in for one would be.

### Entry

31. One bullet per entry, one entry per change.
32. Two slots, in order: what changed, stated as a fact about the product and
    never about the work that produced it, and why it matters - what it means
    for the people the product serves, or for a decision the reader is
    tracking. The second slot is the one neither of the other templates
    carries; it is this reader's whole reason to be reading a changelog
    rather than the pull requests themselves.
33. One sentence per slot, two per entry. A third sentence on either one needs
    a reason a reader would accept - the same ceiling the customer template
    sets, for the same reason: a document this reader can scan in a sitting is
    worth more than one that tries to say everything.
34. The second slot is drawn from the facts of the change and from nothing
    else - a linked issue's stated purpose, a pull request's own account of
    what it was for, a figure already in front of the model. It is a
    rephrasing exactly as the first slot is, and the faithfulness check covers
    it on the same footing as everything else the model writes.
35. A claim of impact needs something in the entry a reader could check it
    against - a number, a named group affected, what held before. "This
    matters a great deal" gives a reader nothing to hold; "cuts the cost of a
    run by roughly a third" does.

### Never appears

36. Pull request numbers, commit hashes, issue references, author names,
    compare links - the customer template's list, rule 12, for the same
    reason: this reader traces nothing back to a repository.
37. Configuration keys, file paths, class or method names, concrete default
    values. A setting this reader meets is named as a place and a purpose,
    never as a key.
38. A verb or a noun that reads correctly only to whoever wrote the change -
    "refactored," "introduced an abstraction for." This reader was not there
    for the work; only its result is theirs to read.

### An empty release

A release with nothing theme-worthy can still be a real document - `Other`
carries it, per rule 30. A release with no user-visible change at all is a
different case, and follows the rule the customer template already sets for
it: a fixed, configured notice, no groups, no entries.

### Template options

| Option               | Values     | Default                                  |
|-----------------------|-----------|-------------------------------------------|
| `emptyReleaseNotice`  | any string | `No changes to report in this release.`  |

### Worked shape

```markdown
### Configuration

- A project's own `chartula.yaml` now layers over environment variables
  instead of requiring one or the other. Teams that already keep configuration
  in a file no longer have to duplicate it as environment variables just to
  satisfy the tool.

### Release generation

- A release can be previewed before anything is written or published, from
  the same facts the real run would use. Reviewing a release no longer costs
  a real run to see what it would contain.

### Other

- Technical, customer and product notes are now written from one shared set
  of facts instead of three separate passes over the same pull requests. The
  three can no longer describe a release differently from each other, which a
  separate pass per audience could not promise.
```
