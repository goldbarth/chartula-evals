---
title: Release 0.1.0-preview.4
description: This release improves release previews and run visibility, adds safeguards for publishing and configuration, and changes how release facts are stored and checked.
publishedAt: 2026-10-07
---

### What needs action

- **Breaking:** Published `changelog.json` files no longer include pull request descriptions, while run records retain the complete facts and descriptions. If you consume schema version 1, read descriptions from the run record instead; update your consumer for schema version 2.
- **Breaking:** `preview` now shows the facts, filtering decisions, and what `generate` would send without making model calls or writing files. You can use it without a model key; run `generate --no-publish` to see rendered prose without publishing.

### What's New

- **Run summaries:** Run summaries now open with a line that reports whether generation completed, had review flags, or failed for some audiences, and each rendering appears under its audience name. You can read the run outcome from the first line.
- **Doctor report:** `chartula doctor` now groups its checks, marks each status, and explains whether warnings let a run proceed. When a warning is about GitHub write access, the verdict distinguishes commands that can start from `generate`, which would stop there.
- **Terminal progress:** Runs now show their current step and elapsed time in a live terminal, while redirected output stays plain. Use `--plain` on any command to request plain output.
- **Pull request text in prompts:** Pull request titles and descriptions are quoted in model prompts, and descriptions longer than 8,000 characters are cut in the prompt. The model is instructed to treat that text as material to rephrase, not as instructions, so you can rely on the quoted text having a clear boundary.
- **Published release protection:** `generate` now stops before its first model call when the release is already published. To replace its notes, pass `--replace-published`; use `--no-publish` to write files without publishing.
- **Configuration template hint:** When `chartula doctor` finds no `chartula.yaml`, it now points to the template for the installed version. You can use that template to configure Chartula.
- **Run progress:** While a run is in progress, its pull request reading, rendering, and checking steps are shown in order, with progress in a terminal or plain lines otherwise. You can follow which step is running instead of waiting without updates.
- **Setup checks:** `chartula doctor` now checks the setup needed for a run and reports each check as ok, warn, fail, or skip. You can run it before `generate` to identify setup problems and whether they would stop a run.
- **Issue numbers at every depth:** Closed issue numbers are now included from the text the model reads, including at the default depth; at `title-only`, numbers come from the title. Existing `title-description-and-issues`, `full`, and `issues` values continue to work as `title-and-description`.
- **Commits without pull requests:** Commits in a release range that are not part of a merged pull request now appear as changes of their own, while merge commits without pull requests are skipped. You can see the direct-commit and skipped-merge counts in the run summary and record.
- **Installed version:** `chartula --version` now prints the installed informational version and exits successfully. You can check the version from any directory without configuration or credentials.
- **First-tag ranges:** A first tag now covers commits from the first commit without an extra flag, and first-tag or large ranges require confirmation before GitHub is contacted. In non-interactive runs, pass `--yes` to confirm up front, or `--since <ref>` to start later.

### What's Changed

- **Dependency updates:** Anthropic, coverlet.collector, and Microsoft.Extensions.AI.OpenAI dependencies have been updated. You can rely on the updated package versions in this release.

### Bug Fixes

- **Help option grouping:** The help now lists each option once under its correct group. You can find `--replace-published` under “What a run writes,” with no duplicate `--audience` entry.
- **Faithfulness check matching:** The rule-based check now recognizes names repeated in facts even when whitespace differs or the text includes fenced code blocks. You can rely on names supported by the facts not being flagged just because of line breaks or code fences.
- **Empty technical releases:** When a release has no technical changes to render, `CHANGELOG.md` and the release notes now say that it has no features, fixes, performance improvements, or breaking changes. The technical rendering in `changelog.json` remains empty, so you can still distinguish releases with nothing to render.
- **Readable JSON files:** `changelog.json` and run records now leave characters such as backticks and non-ASCII text readable in the file. You can read and diff their text without JSON escaping obscuring it.
- **Review flag layout:** Review flags now appear in their own block after a blank line, rather than directly beneath the last rendering entry. You can see that flags apply to the rendering rather than appearing attached to its final entry.
- **Credential status in run headers:** Run headers now say when a credential variable is unset or blank, while still naming the variable and never printing its value. You can tell which variable to set when authentication is missing.
- **Command-line option validation:** Commands now stop on unknown or unsupported options, missing or repeated single-value options, and options written with `=`; errors suggest a nearby option when available. Use `-h` or `--help` after a command to show help without starting the command.
- **GitHub API URL:** A GitHub API base URL without a trailing slash now works, and the run header shows the normalized URL. You no longer need to add the slash yourself.
- **Empty category filter:** An empty `excludeCategories` list now means no categories are excluded, including when set in the environment. You can use an empty list to include changes from every category.
- **Unreadable model responses:** When a model endpoint responds but its answer cannot be read, the error now identifies the response as unreadable rather than unreachable. You can distinguish an answer-format problem from a connection problem.
- **Conflicting configuration files:** A run now stops with an error if both `chartula.yaml` and `chartula.yml` are present, naming both files and explaining how to resolve the conflict. Keep one configuration file and move the settings you want into it.
- **GitHub write permission check:** `generate` now checks whether GitHub allows publishing before reading pull requests or making model calls. If the check fails, no model calls or files are produced; use `--no-publish` to render and write files without publishing.
- **`--no-publish` help text:** The `--no-publish` help now says that it writes every file and skips only GitHub release notes. You can rely on the option description to distinguish writing files from publishing.
