---
title: Release 0.1.0-preview.4
description: This release makes generate safer and easier to check before it spends model calls, and it splits pull request descriptions out of the published changelog file.
publishedAt: 2026-10-07
---

### What needs action

- **Breaking:** Pull request descriptions are no longer in changelog.json, which is the published release payload and now schema version 2. Titles, numbers, links, categories, flags, labels, closed issues, renderings and provenance remain. The full descriptions are kept in the run record, which stays on schema version 3 and is written only locally.
- **Breaking:** preview makes no model call and needs no key. It shows each fact with the audiences it appears in, each dropped change with the setting that dropped it, and what generate would send: the number of model calls and the prompt's characters per audience. The output is in characters, not tokens. preview no longer prints renderings; generate --no-publish shows the prose without publishing.

### What's New

- **Run summary:** The first line of a run's summary now states how the run went: generated, generated with review flags, partially generated with the number of failed audiences, or no audience rendered. Each rendering sits under its audience's name, and the command name opens the output.
- **Doctor output:** doctor groups its checks under Repository, Model and GitHub, marks each status with a symbol and a word, and ends with a verdict that says whether a run would start and which warnings would stop generate.
- **Run progress:** A run's progress shows a spinner in a terminal, and plain lines when output is redirected, in CI, or with the new --plain option. A step that fails is marked as failed rather than done.
- **Quoted pull request text:** Pull request titles and descriptions are now quoted between tags in the prompt and cut at 8,000 characters. This makes text written to steer the model less likely to succeed, but it cannot prevent it.
- **Published releases are protected:** generate stops before any model call when the release of the tag is already published, unless --replace-published is given. A published release's notes are no longer replaced silently. doctor warns about this case.
- **Config template hint:** When chartula.yaml is missing, doctor names the config template for this version so you can copy it.
- **Step-by-step progress:** A run shows each step as it works: reading pull requests, rendering each audience, and checking each rendering. In a terminal the current step's time updates each second; without one, each step prints one line as it starts.
- **Setup check command:** chartula doctor checks the setup a run needs, one line per check, before any changes are made. It names a failure that would stop a run and exits with code 1, so a CI job can run it before generate.
- **Closed issues at every depth:** Closed issue numbers are taken from the text the model reads at every depth, so a rendering that keeps a number such as #12 is no longer flagged at the default depth. The older setting value title-description-and-issues still works and reads as title-and-description.
- **Direct commits included:** A commit with no merged pull request is now rendered as its own change instead of being left out. A merge commit with no pull request is skipped, and the run summary says how many commits were handled this way.
- **Version flag:** chartula --version prints the installed version and exits 0, without needing a checkout, configuration, key or token.
- **First tag and large range confirmation:** A first tag now renders from the first commit by default, without the --whole-history flag. A large range, or a first tag, asks for confirmation before any GitHub request or model call. Without a terminal the run stops unless --yes is given.

### What's Changed

- **Dependency updates:** Dependency updates for the nuget minor and patch group: Anthropic 12.49.0 to 12.53.0, coverlet.collector 10.0.1 to 10.1.0, and Microsoft.Extensions.AI.OpenAI 10.10.0 to 10.10.1.

### Bug Fixes

- **Help text and roadmap:** chartula --help lists each option once, in its group, and the roadmap reflects the completed items.
- **Rule-based check with wrapped names:** The rule-based check now matches names that a rendering wraps across lines or puts in fenced code blocks, so those names are no longer flagged when the facts back them. A name the facts do not contain is still flagged.
- **Empty technical release:** A release with no changes for the technical reader gets a sentence saying so in CHANGELOG.md and the release notes, instead of an empty heading. changelog.json still has an empty technical rendering.
- **Readable JSON:** changelog.json and the run record are now easier to read: backticks, quotes and non-ASCII characters are written as themselves, and only what JSON requires is escaped.
- **Flags set apart:** The flagged-for-review block is now set apart from the last entry of its rendering by a blank line and a heading, so flags no longer look attached to the entry above them.
- **Header names missing credentials:** The run header says unauthenticated when GITHUB_TOKEN or the model key is not set, instead of naming a source for a credential that is missing.
- **Option checking and help:** Options a command does not take are refused before the run starts, with the closest valid option suggested, and --help works after a command name.
- **GitHub API URL:** A GitHub API URL without a trailing slash now works, so requests reach the right endpoint.
- **Empty category exclusion list:** An empty filter.excludeCategories list now drops no category, so internal work is kept when the list is set to [].
- **Unreadable model answer message:** A model answer the SDK cannot read is reported as unreadable, naming the answer, rather than as an endpoint that could not be reached.
- **Two config files refused:** A run stops with an error when both chartula.yaml and chartula.yml exist in the directory, naming both paths and how to fix it.
- **Publish permission checked early:** generate checks before the first model call that the token can publish release notes, so a run with a read-only or missing token stops before spending model calls.
- **No-publish help text:** The --no-publish help text says every file is written and only the GitHub release notes are skipped.
