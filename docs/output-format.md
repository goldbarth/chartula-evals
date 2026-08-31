# Output format

The shape a rendering is built to.

`rubric-customer.md` says how a rendering is judged; this file says what it is
supposed to look like. Form rules live here only, and the rubric points at them
rather than restating them - two documents describing the same form is how the
C3 split reading happened.

## Templates

Format is meant to be selectable, one template per audience, so that a project
can keep its house style. This file holds the defaults.

| Audience  | Default template            | Status                                    |
|-----------|-----------------------------|-------------------------------------------|
| Customer  | `customer/plain` (below)    | strawman, not agreed                      |
| Technical | Common Changelog            | not written; see the note at the bottom   |
| Product   | thematic                    | not written                               |

A template fixes the form: headings, groups, entry shape, what may appear at
all. It does not fix quality. "The most consequential item leads its group" and
"no marketing adjectives" hold whichever template is chosen, and stay in the
rubric.

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

Front matter fields: `title`, `description`, `publishedAt`, `tags`. See
**Tags** below for where the tags come from.

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

### Template options

Settings a project chooses once. They change the form, never whether an entry
is any good, so no rubric axis reads them.

| Option        | Values                                  | Default      |
|---------------|-----------------------------------------|--------------|
| `voice`       | `impersonal`, `first-person-plural`     | `impersonal` |
| `boldLabel`   | `on`, `off`                             | `on`         |
| `tags`        | `on`, `off`                             | `on`         |

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

### Open decisions

- Whether `publishedAt` is the tag date or the date the notes were published.
- Whether the release heading carries a name as well as a number.
- Whether an empty release - every change filtered out - produces a document
  saying so, or no document at all. It produces one, and the text is written by
  hand: a filler line configured by the project, not generated. Slack's
  maintenance releases are the model. What is still open is where it is
  configured and whether more than one can be held and rotated.

---

## Technical and product

Not written. The technical rendering should start from Common Changelog rather
than from a template of our own: it is a strict subset of Keep a Changelog,
it requires a reference per entry instead of merely allowing one, and it
forbids copying commit or pull request titles verbatim - which is exactly the
failure `sonnet-5-no-thinking-out` produced in its technical section.

Two of its rules are quality, not form, and belong in a technical rubric when
one exists: entries in the imperative mood, and every entry self-describing as
if no category heading were there.
