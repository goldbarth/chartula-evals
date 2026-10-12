---
title: Release 0.1.0-preview.4
description: Chartula adds clearer previews and run reporting, protects published release notes, and improves how release facts are collected and presented.
publishedAt: 2026-10-07
---

### What needs action

- **Breaking:** The published `changelog.json` no longer contains pull request descriptions, and its schema version is now 2. The run record keeps the complete facts, including descriptions; consumers of version 1 changelog files must get descriptions from the run record instead.
- **Breaking:** `preview` now shows the facts, which renderings include them, dropped changes and why they were dropped, and what `generate` would send, without making a model call or writing files. You can rely on its prompt character counts matching the prompts `generate` would send, and no model key is needed.

### What's New

- **Run summaries:** The run summary now opens with whether generation completed, had review flags, partially failed, or produced no renderings. You can identify how the run went from its first line, with each rendering shown under its audience name.
- **Doctor report:** `doctor` now groups its checks and marks each status with a symbol and word in terminal output. You can tell whether warnings will stop a run, including when a GitHub write warning prevents `generate` from starting; plain output keeps the status words without symbols.
- **Run progress:** Run progress now shows the active step and its status, with a spinner in supported terminals and plain lines otherwise. You can follow steps as they run, and `--plain` keeps command output free of terminal styling and control characters.
- **Quoted pull request text:** Pull request titles and descriptions are now quoted in the model prompts, and descriptions longer than 8,000 characters are cut in the prompt. You can rely on the model being told that this text is material to rephrase, not instructions; longer descriptions are marked as continuing beyond the text shown.
- **Published release protection:** `generate` now stops before its first model call if the release is already published, unless you explicitly allow replacement. You can rely on published release notes not being replaced during a run by default; pass `--replace-published` to replace them, or `--no-publish` to write files without publishing.
- **Configuration template:** When `doctor` finds no `chartula.yaml`, it now points to the template for the installed version. You can use that version-specific template to configure Chartula.
- **Run progress:** A run now reports each step as it starts, including pull request reading, rendering and checks. You can follow the run's progress in the terminal or from plain lines when output is not attached to a terminal.
- **Setup checks:** `chartula doctor` now checks the setup a run needs before you start one. You can use its results to identify setup failures and warnings, and its exit code indicates whether any checks failed.
- **Issue numbers:** Closed issue numbers now come from the title and description text used at each fact depth, including the default depth. You can rely on the rule-based check accepting issue numbers that appear in the text the model reads; the old `title-description-and-issues`, `full` and `issues` values continue to mean `title-and-description`.
- **Direct commits:** Commits without a merged pull request now appear as individual changes alongside pull requests, while merge commits without a pull request are skipped. You can see direct commits in the release output and summary, with the run record also reporting the number of direct commits and skipped merge commits.
- **Installed version:** `chartula --version` now prints the installed informational version. You can check it from any directory without a checkout, configuration, key or token.
- **First-tag ranges:** A first tag now uses the range from the first commit, and a first-tag or large range prompts for confirmation before any GitHub request or model call. You can rely on unconfirmed ranges not being read or sent to the model; use `--yes` to confirm up front, including in non-interactive runs.

### What's Changed

- The Anthropic, coverlet.collector and Microsoft.Extensions.AI.OpenAI dependencies were updated.

### Bug Fixes

- **Help options:** The help now lists each option once under its correct group. You can find `--replace-published` under “What a run writes,” with no duplicate `--audience` option.
- **Faithfulness check:** The rule-based check no longer flags names that the facts support when whitespace or fenced code blocks change their formatting. You can rely on it matching names with whitespace folded and code fences removed, without matching across separate facts.
- **Empty technical releases:** A release with no technical changes now gets a sentence explaining that it has no features, fixes, performance improvements or breaking changes in `CHANGELOG.md` and the release notes. You can rely on an empty technical rendering remaining empty in `changelog.json`.
- **Readable JSON:** Backticks and non-ASCII text in `changelog.json` and the run record are now written in readable form rather than escaped unnecessarily. You can rely on both files still parsing to the same values.
- **Review flags:** Review flags now appear after a blank line under their own heading, rather than directly beneath a rendering's last entry. You can read flags without mistaking them for part of that entry.
- **Credential status:** The run header now says when a credential variable is unset or blank, rather than implying a token or key is available. You can see which variable needs to be set without exposing its value.
- **Command-line validation:** Invalid or unsupported command-line options now stop the command before it starts, and `-h` or `--help` displays help wherever it appears after a command. You can rely on mistyped options and missing values being rejected rather than silently ignored.
- **GitHub API URLs:** A GitHub API base URL without a trailing slash now works as well as one with a slash. You can use either form and rely on requests and the run header using the same URL.
- **Empty category filters:** An empty `filter.excludeCategories` list now excludes no categories instead of retaining the default exclusion. You can set it to `[]` in `chartula.yaml` or with `Chartula__Filter__ExcludeCategories=[]` to include every category.
- **Model response errors:** When a model endpoint responds but its answer cannot be read, the error now identifies the answer as unreadable rather than reporting the endpoint as unreachable. You can distinguish an unreadable response from a request that received no response.
- **Configuration file ambiguity:** A run now stops if both `chartula.yaml` and `chartula.yml` are present. You can resolve the error by keeping one file and moving the settings you want into it.
- **Publishing permission check:** `generate` now checks whether the token can publish before reading pull requests or making model calls. You can rely on a token that cannot publish stopping the run before model calls; use `--no-publish` to write files without publishing.
- **No-publish help:** The `--no-publish` help now says it writes every file and skips only GitHub release notes. You can rely on the help text reflecting that the run record and other output files are still written.
