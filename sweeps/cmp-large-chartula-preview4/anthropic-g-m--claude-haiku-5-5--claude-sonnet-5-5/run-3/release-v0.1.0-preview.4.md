---
title: Release 0.1.0-preview.4
description: This release makes changelog.json safe to publish by moving pull request descriptions to the run record, and makes preview free of model calls, with clearer run output, guards for published releases and a new doctor command.
publishedAt: 2026-10-07
---

### What needs action

- **Breaking:** Changelog files no longer carry pull request descriptions. A change entry in changelog.json has no description field; the file is now schema version 2 and is safe to publish. The full facts, descriptions included, are kept in the run record, in a new facts field. A version 1 consumer finds the description there.
- **Breaking:** preview no longer makes model calls, so it costs only the GitHub requests and needs no API key. It shows each fact with the outputs that carry it, each dropped change with the setting that dropped it, and what generate would send: the number of model calls and the prompt size in characters. Use generate --no-publish to see the rendered text without publishing.

### What's New

- **Run header and summary:** Each run now opens with a header naming the command, and its summary's first line says how the run went: generated, generated with review flags, partially generated, or no audience rendered. Each rendering stands under its audience's name.
- **Grouped doctor report:** chartula doctor groups its checks under Repository, Model and GitHub, marks each as ok, warn, fail or skip, and ends with a verdict saying whether a run would start or stop. A warning under GitHub write says what it means for generate.
- **Live progress and --plain:** Run progress is shown with a spinner and a colour fade in a terminal. Redirected output, CI and TERM=dumb get plain lines. The new --plain option forces plain output for any command.
- **Quoted pull request text:** Pull request titles and descriptions are quoted between tags in the model's prompt, and the model is told they are material to rephrase, not instructions. Descriptions longer than 8,000 characters are cut in the prompt. This makes steering the model by pull request text less likely, but does not rule it out.
- **Published releases are protected:** generate now stops before any model call when the release is already published, instead of replacing its notes. Pass --replace-published to replace them on purpose. Drafts from earlier runs are still updated without the option.
- **Config template link in doctor:** When no chartula.yaml is found, doctor now names this version's config template so you can find it.
- **Visible progress steps:** While a run works, each step shows on stderr: reading pull requests, rendering each audience, and checking each rendering. A slow run no longer looks like a hanging one, and stdout is unchanged.
- **New doctor command:** chartula doctor checks the setup a run needs (git, checkout, tag, repository, configuration, model endpoint, GitHub read and write, and pull request titles) and reports each check as ok, warn, fail or skip. It names variables but never prints their values, writes nothing and publishes nothing, so you can run it before generate.
- **Closed issue numbers at every depth:** factBase.depth now controls only what the model reads. Closed issue numbers are taken from the title and description at every depth, so a rendering that keeps a closed issue number is no longer flagged. The old value title-description-and-issues still works and is read as title-and-description.
- **Direct commits are rendered:** Commits without a pull request, such as a fix pushed straight to main, now appear in the release as their own changes. Merge commits without a pull request are skipped. The run summary counts both.
- **Version command:** chartula --version now prints the installed version and its commit, so you can check which build you have without starting a run.
- **First tag and large range confirmation:** A first tag now renders from the first commit without a flag. Before a run reads a first tag or a range longer than 200 commits, it asks you to confirm, and --yes confirms it in CI. The range is named in the run header.

### What's Changed

- **Dependency updates:** Updated the nuget-minor-and-patch dependency group: Anthropic, coverlet.collector and Microsoft.Extensions.AI.OpenAI.

### Bug Fixes

- **Help lists each option once:** chartula --help lists each option once, under its group, with no duplicates.
- **Faithfulness check matches wrapped names:** The rule-based faithfulness check now matches names across line breaks and around fenced code blocks, so a name a description wraps over two lines is no longer flagged when the facts back it.
- **Empty technical release:** A release with nothing for the technical reader now gets a sentence saying so in CHANGELOG.md and the release notes, instead of an empty heading. changelog.json still holds an empty technical rendering.
- **Readable JSON:** changelog.json and the run record now write characters such as backticks, quotes and non-ASCII letters as themselves instead of escaping them, so the files are easier to read.
- **Flags set apart:** Flags in a rendering are set apart from its last entry, under a Flagged for review heading, so they no longer look like part of that entry.
- **Run header for missing credentials:** The run header says unauthenticated, naming the unset variable, when no GitHub token or model key is set, instead of naming a source for a missing credential.
- **Stricter option checking:** The CLI refuses an option a command does not take, a value option without a value, and a repeated single-value option, before any work starts. --help works after a command name. Errors suggest the closest valid option.
- **GitHub API URL without trailing slash:** A GitHub API URL written without a trailing slash now works, because the trailing slash is added automatically.
- **Empty excludeCategories:** An empty excludeCategories list in chartula.yaml now drops no category, instead of silently keeping the default Internal exclusion.
- **Unreadable model answer message:** A model answer the SDK cannot read is now reported as an unreadable answer, naming the value, instead of as an endpoint that could not be reached.
- **Two config files refused:** A run now stops with an error when both chartula.yaml and chartula.yml exist in the directory, naming both paths, instead of silently ignoring one.
- **Publish permission checked first:** generate now checks before the first model call that the token may publish release notes, so a read-only or missing token stops the run without spending on model calls. preview and --no-publish do not check.
- **--no-publish help text:** The --no-publish help line now says it writes every file and skips only the GitHub release notes.
