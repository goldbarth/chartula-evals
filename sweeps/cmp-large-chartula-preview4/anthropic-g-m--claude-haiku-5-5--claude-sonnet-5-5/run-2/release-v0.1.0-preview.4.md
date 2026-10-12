---
title: Release 0.1.0-preview.4
description: This release makes runs easier to start, check and follow, and keeps pull request descriptions out of the published changelog file.
publishedAt: 2026-10-07
---

### What needs action

- **Breaking:** Changelog entries no longer include pull request descriptions. Change entries in changelog.json now carry no description field, so version 1 consumers that read it there must read the run record instead. The run record keeps the full facts, including descriptions, so you can review what a run used without publishing the file.
- **Breaking:** Preview is now free to run. It shows the facts, what each audience carries, which changes were dropped and the setting that dropped them, and what generate would send, without a model call and without a key. Use it to check a release before spending on generate.

### What's New

- **Run summary and help:** The first line of each run's summary now says how the run went: generated, generated with review flags, partially generated with failed audiences, or no audience rendered. Each audience's text now sits under its name. The help groups its options under three headings.
- **Doctor report:** chartula doctor groups its checks under Repository, Model and GitHub, and marks each as ok, warn, fail or skip. Its last line now says whether a run would start, and when a warning under GitHub write would stop generate, it says so.
- **Run progress and --plain:** The progress of a run is shown with a spinner in a terminal, and --plain gives plain lines for logs and redirected output. Each step shows its time as it runs.
- **Pull request text in prompts:** Pull request titles and descriptions are quoted in the prompt between tags, and a description longer than 8,000 characters is cut in the prompt with a note that it continues. This makes instructions written in pull request text less likely to steer the model, though it does not rule that out.
- **Published releases are protected:** generate stops before any model call when the release already exists as published, and says what to do. Pass --replace-published to replace its notes on purpose.
- **Config template link in doctor:** When chartula doctor finds no chartula.yaml, it now names this version's config template with a link, so you can find the settings to copy.
- **Steps shown during a run:** A run now shows each of its steps while it works: reading pull requests, rendering each audience, and checking each rendering. In a terminal, the current step updates in place with its count and time.
- **Setup check with doctor:** chartula doctor checks the setup a run needs, before anything is spent: git, the checkout, the tag, the repository, the configuration, the model endpoint, GitHub read and write access, and pull request titles. It exits with 1 when a check fails, so a CI job can stop before generate.
- **Closed issues read at every depth:** Closed issue numbers in the pull request text are now read at every depth, so a rendering keeps references like Closes #12 without being flagged. The old depth setting still works and reads as title-and-description.
- **Direct commits in the release:** Commits pushed straight to the main branch, without a pull request, now appear in the release as changes of their own. Merge commits without a pull request are skipped, and the run summary says how many commits had no pull request.
- **Version command:** chartula --version now prints the installed version and the commit it was built from, and works from any directory without a configuration or token.
- **First tag and large ranges:** A first tag now renders from the first commit without a flag. A large range, a first tag or one above 200 commits, asks you to confirm before any request is made, and --yes confirms it up front for unattended runs.

### What's Changed

- **Dependency updates:** Updated the NuGet minor and patch dependencies, Anthropic, coverlet.collector and Microsoft.Extensions.AI.OpenAI, to their newer versions.

### Bug Fixes

- **Help text and roadmap:** chartula --help lists each option once under its group. The roadmap is updated to show what is done before the announcement.
- **Rule-based check and wrapped names:** A name in a rendering that wraps across lines in the pull request description is no longer flagged as unsupported, and fenced code blocks are compared fairly. Names the facts do not contain are still flagged.
- **Empty technical release:** A release with nothing for the technical reader now says so in CHANGELOG.md and in the release notes, instead of leaving an empty heading. The sentence is written by Chartula, not the model, and changelog.json keeps an empty technical rendering for that release.
- **Readable JSON files:** changelog.json and the run record now keep backticks, quotes and non-ASCII characters readable instead of escaping them. The files still parse the same way for any consumer.
- **Flags set apart in the output:** Flagged entries are set apart from the last entry of their rendering under a Flagged for review heading, so a flag no longer looks attached to the entry above it.
- **Header when credentials are missing:** The run header now says unauthenticated, naming the variable to set, when no GitHub token or model key is present, instead of naming a source for a credential the run lacks.
- **Stricter command line:** Command lines are checked before a run starts: options a command does not take are refused with a suggestion, --help works after a command, and a value option without a value stops the run instead of taking the next word.
- **GitHub API URL without slash:** A GitHub API URL set without a trailing slash now works, so requests reach the API paths they are meant for.
- **Empty exclude list:** An empty excludeCategories list in chartula.yaml now drops no category, instead of silently keeping the default Internal exclusion.
- **Unreadable model answers:** When a model returns an answer the SDK cannot read, the error now says the endpoint was reached and names what could not be read, instead of reporting that it could not be reached.
- **Two configuration files refused:** A run now refuses to start when both chartula.yaml and chartula.yml are in the directory, and names both paths and how to fix it, instead of silently ignoring one.
- **Publish permission checked early:** generate checks that the GitHub token may publish release notes before the first model call, so a token that cannot publish stops the run at once instead of after every model call.
- **No-publish help text:** The help text for --no-publish now states that every file is written and only the GitHub release notes are skipped.
