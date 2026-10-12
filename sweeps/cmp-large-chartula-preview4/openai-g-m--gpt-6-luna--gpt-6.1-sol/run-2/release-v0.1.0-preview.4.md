---
title: Release 0.1.0-preview.4
description: This release changes how previews, run status, and setup checks are presented, and adds safeguards around publishing and changelog inputs.
publishedAt: 2026-10-07
---

### What needs action

- **Breaking:** The published changelog no longer includes pull request descriptions, and its schema version is now 2. If you read facts from a changelog file, read them from the run record instead; migrate version 1 consumers using the guidance in `changelog-json.md`.
- **Breaking:** `preview` now shows the facts, what would be rendered, and what `generate` would send, without making a model call or writing files. Use `generate --no-publish` when you need to see the rendered prose.

### What's New

- **Run summaries:** The run summary now opens with a line describing whether generation completed, had review flags, failed for some audiences, or rendered none. You can read the run outcome from the first line, with each rendering grouped under its audience.
- **Doctor report:** `chartula doctor` now groups its checks by Repository, Model, and GitHub, and marks each status with a symbol and a word in terminal output. When a GitHub write warning means `generate` would stop, the verdict says so; plain output retains the status words without symbols.
- **Run progress:** A run now shows its active step and progress in a terminal, with completed or failed steps remaining in the output. Redirected output stays plain, and `--plain` requests plain output for any command.
- **Pull request text in prompts:** Pull request titles and descriptions are now quoted in rephrasing and thorough-check prompts, and descriptions longer than 8,000 characters are cut in the prompt. The model is told to treat the quoted text as material to rephrase, not instructions.
- **Replacing published releases:** `generate` now stops before its first model call if the release is already published, unless you explicitly allow replacement. Use `--replace-published` to replace it, or `--no-publish` to write files without publishing.
- **Config template hint:** When `chartula doctor` finds no `chartula.yaml`, it now points to the template for the installed version. Use that template to find the configuration options available in your version.
- **Run progress:** A run now reports when it is reading pull requests, rendering each audience, and checking renderings. You can follow the run's progress instead of waiting without output.
- **Setup checks:** You can run `chartula doctor` to check the setup needed for a release before generating changelog content. It reports which checks pass, warn, fail, or are skipped.
- **Closed issue numbers:** Closed issue numbers are now taken from the title and description the model reads, including at the default fact depth. Existing `title-description-and-issues`, `full`, and `issues` settings continue to work as `title-and-description`.
- **Commits without pull requests:** Changes from commits without a merged pull request now appear alongside pull request changes, while merge commits without a pull request are skipped. The run summary and run record also report these commits and skipped merges.
- **Installed version:** `chartula --version` now prints the installed version and exits successfully. You can run it from any directory without a checkout, configuration, key, or token.
- **First-tag ranges:** A first tag now includes commits from the first commit without requiring a flag, and large ranges ask for confirmation before any GitHub request or model call. If you run without a terminal, pass `--yes` to confirm the range up front.

### What's Changed

- **Dependency updates:** The Anthropic, coverlet.collector, and Microsoft.Extensions.AI.OpenAI dependencies have been updated.

### Bug Fixes

- **Help and roadmap:** The help now lists each option once in its correct group, and the roadmap reflects the completed work.
- **Faithfulness checks:** The rule-based check now recognizes names that wrap across lines or appear around fenced code blocks in a rendering. Names not present in the facts are still flagged.
- **Empty technical releases:** When a release has no technical changes to show, `CHANGELOG.md` and the release notes now say that it has no features, fixes, performance improvements, or breaking changes. The technical rendering in `changelog.json` remains empty.
- **Readable JSON:** `changelog.json` and the run record now leave characters such as backticks and non-ASCII text readable in the files. The parsed values remain unchanged.
- **Review flags:** Review flags now appear in a separate block after a blank line, rather than directly under the last entry. Multi-line flags remain grouped beneath their own flag.
- **Credential status:** The run header now says when a credential variable is unset or blank, while still naming the variable to set. It continues to show the credential source when the variable is set.
- **Command-line validation:** Commands now refuse unknown options, options used with the wrong command, and missing or repeated values before starting a run. Use `-h` or `--help` after a command to display help.
- **GitHub API URLs:** A GitHub API base URL without a trailing slash now works, and the run header shows the slash-normalized URL. You can enter the URL with or without its trailing slash.
- **Empty category filters:** An empty `filter.excludeCategories` list now means that no categories are dropped, instead of retaining the default exclusion. The same behavior applies when the list is set through the environment variable.
- **Unreadable model responses:** When a model endpoint responds but its answer cannot be read, the error now identifies the response as unreadable rather than unreachable. Failures with no response still report that the endpoint could not be reached.
- **Ambiguous configuration files:** A run now stops with an error if both `chartula.yaml` and `chartula.yml` are present, rather than silently choosing one. Keep one file and move the settings you want into it.
- **Publishing permission check:** `generate` now checks whether GitHub allows the run to publish before reading pull requests or making model calls. If publishing is not allowed, use `--no-publish` to write files without publishing.
- **`--no-publish` help text:** The help now explains that `--no-publish` writes every file and skips only GitHub release notes. Use it to generate files without publishing release notes.
