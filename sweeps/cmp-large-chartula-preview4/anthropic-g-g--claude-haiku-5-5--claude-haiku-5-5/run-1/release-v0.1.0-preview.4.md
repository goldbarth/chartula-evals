---
title: Release 0.1.0-preview.4
description: This release makes runs safer to share and easier to read, with a free preview, a setup check and clearer progress and summary output.
publishedAt: 2026-10-07
---

### What needs action

- **Breaking:** Changelog files published by a release no longer carry pull request descriptions, which could hold internal notes and links, so they can be published safely. Each change entry in changelog.json now omits its description and the file is schema version 2, so consumers that read the description must now read it from the run record, where a new facts field keeps the complete facts and no longer shares the publishable file.
- **Breaking:** Running preview now shows the facts a release is built from, each change dropped with the setting that dropped it, and what generate would send to the model, without making any model call. It needs no model key, and writes and publishes nothing, so you can check a release before paying for it. Preview output no longer includes rendered text, so use generate --no-publish to see the prose without publishing it.

### What's New

- **Run summary and headings:** The first line of a run's summary now states how the run went: Generated, Generated with review flags, Partially generated with the number of audiences that failed, or No audience rendered. Each audience's rendering is headed by its name, and the command is shown at the top of the output.
- **Doctor report layout:** The doctor report is now grouped into Repository, Model and GitHub checks, with a status symbol and word for each check. The verdict says whether a run would start, and when a warning would stop generate, it says so instead of promising a run that would fail.
- **Live run progress and --plain:** A run now shows its progress with an animated spinner in a terminal, and each step is listed as it completes. A failed step is marked as failed, not done. Pass --plain to get plain output without colour or animation, for logs and pasted reports.
- **Pull request text sent to the model:** Pull request text is now wrapped in tags and marked as material to rephrase rather than instructions, and descriptions beyond 8,000 characters are cut in the prompt. This makes it less likely that text written to steer the model changes a rendering, though it cannot rule that out.
- **Replacing published release notes:** generate now stops before calling the model if the release for the tag is already published, unless you pass --replace-published. This lets you avoid losing hand-written notes on a published release without knowing to check first.
- **Config template hint in doctor:** When chartula.yaml is missing, doctor now names the config template for the installed version, so you can find the settings to copy.
- **Visible progress during a run:** While a run is working, each step it is on is shown on stderr, so a slow run no longer looks like a hanging one. Output redirected to a file or CI log stays plain, one line per step.
- **Setup check with doctor:** chartula doctor checks the setup a run needs, one line per check, before any model call or release is produced. It sends one minimal request to the model and a few GitHub requests, and writes and publishes nothing. It exits with 1 when a check fails, so a CI job can run it before generate.
- **Closed issues at every depth:** Closed issue numbers are now read from the title and description at every depth setting, so a rendering that keeps a closed issue reference is no longer flagged. The factBase.depth setting now only controls what the model reads, and the old value title-description-and-issues is still accepted.
- **Commits without a pull request:** A commit pushed directly to the default branch, outside any merged pull request, is now included in the release as a change of its own. Merge commits without a pull request are skipped. The run summary reports how many commits were included this way.
- **Printing the installed version:** chartula --version prints the installed version, the same text that changelog.json records. It runs without a checkout, configuration or token, so you can check an install right after installing.
- **Rendering a first tag:** A first tag now renders every commit up to it, with no extra flag. Before the run reads GitHub or calls the model, it asks you to confirm a first tag or a range above 200 commits, and stops with a clear message if you decline or are not at a terminal. Pass --yes to confirm up front in CI. --whole-history no longer has any effect.

### What's Changed

- **Dependency updates:** The NuGet minor and patch dependencies were updated: Anthropic to 12.53.0, coverlet.collector to 10.1.0 and Microsoft.Extensions.AI.OpenAI to 10.10.1.

### Bug Fixes

- **Help text fixes:** chartula --help now lists each option once under its group. --replace-published appears under What a run writes, and the duplicated --audience entry is removed.
- **Rule-based check on wrapped names:** A name in a rendering that a pull request description wraps over several lines, or that sits beside a fenced code block, is now matched to the facts, so it is no longer flagged for review when the facts back it.
- **Releases with nothing for technical readers:** A release with no changes for the technical reader now gets a sentence saying so in CHANGELOG.md and the release notes, instead of an empty heading. changelog.json still holds an empty technical rendering, and the customer rendering is unchanged.
- **Readable changelog.json and run record:** changelog.json and the run record are now easier to read as written: backticks, quotes and non-ASCII characters appear as themselves instead of escape sequences, while the JSON structure is unchanged.
- **Review flags layout:** Flagged-for-review notes now appear after a blank line under a Flagged for review heading, so they are no longer indented as if they belonged to the last entry.
- **Run header when unauthenticated:** The run header now reads unauthenticated, with the variable's name, when GITHUB_TOKEN or the model key is not set, instead of naming a token source that is missing.
- **Refusing unknown or misplaced options:** An option a command does not take, a misspelled option, a repeated single-value option or a value option without a value now stops the run with an error before any work begins. --help or -h anywhere on the command line prints the help without starting a run.
- **GitHub API URL without a trailing slash:** A GitHub API URL set without a trailing slash now reaches the correct endpoints, so the run no longer fails with a misleading not-found error.
- **Empty excludeCategories list:** An empty excludeCategories list now drops no category, so changes in the default Internal category are kept when you set it to an empty list.
- **Unreadable model answers:** When a model call returns an answer the SDK cannot read, the run now says the endpoint was reached and names what could not be read, instead of reporting that the endpoint could not be reached.
- **Both config file names present:** A run now refuses to start if both chartula.yaml and chartula.yml exist in the directory, and names both paths so you can keep one.
- **Checking publish permission early:** generate now checks before the first model call that the token can publish release notes, so a run with a read-only or missing token stops early instead of at the end. The check costs one GitHub request and is not run for preview or --no-publish.
- **--no-publish help text:** The --no-publish option help now says it writes every file but publishes no GitHub release notes, instead of listing only some files.
