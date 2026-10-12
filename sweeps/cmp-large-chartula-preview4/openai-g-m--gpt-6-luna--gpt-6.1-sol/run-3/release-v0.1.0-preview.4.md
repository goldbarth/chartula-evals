---
title: Release 0.1.0-preview.4
description: This release changes how preview and run progress are presented, adds safeguards around publishing and configuration, and updates how facts and rendered output are handled.
publishedAt: 2026-10-07
---

### What needs action

- **Breaking:** The published changelog no longer includes pull request descriptions, and its schema version is now 2. If you read facts from a version 2 changelog, use the run record instead; version 1 consumers can find the descriptions in the run record’s `facts` field.
- **Breaking:** `preview` now shows the facts, what would be sent for rendering, and prompt character counts without making a model call or writing files. To see the rendered prose without publishing it, run `generate --no-publish`.

### What's New

- **Run summaries:** The run summary now opens with a line that reports whether audiences rendered, failed, or had review flags, and each rendering appears under its audience name. You can read the run’s outcome at a glance.
- **Doctor report:** `doctor` now groups its checks into Repository, Model, and GitHub, and its verdict explains whether the run can start or would stop. You can use the status words in plain output and the symbols on a terminal to understand the result.
- **Terminal progress:** While a run is underway, its current step and elapsed time appear on stderr, with a spinner in supported terminals. Use `--plain` to get plain output without terminal control characters.
- **Pull request text in model prompts:** Pull request titles and descriptions are now quoted in model prompts, and descriptions longer than 8,000 characters are cut in the prompt. The model is told to treat the quoted text as material to rephrase, not instructions, so you can rely on the prompt marking its boundary and any cut.
- **Replacing published release notes:** `generate` now stops before the first model call when the release is already published, unless you explicitly allow replacement. Pass `--replace-published` to replace its notes, or `--no-publish` to write files without publishing.
- **Config template hint:** When `doctor` cannot find `chartula.yaml`, it now points to the template for the installed version. You can use that template to see the available configuration.
- **Run progress:** Run progress now shows pull request reading, audience rendering, and checks as they happen. You can follow which step is underway rather than waiting for the run to finish.
- **Setup checks:** `chartula doctor` now checks the setup a run needs and reports which checks pass, warn, fail, or are skipped. You can run it before `generate` to identify setup issues.
- **Closed issue numbers:** Closed issue numbers now come from the same pull request text the model reads, including at the default depth. If your configuration uses `title-description-and-issues`, `full`, or `issues`, update it to `title-and-description` to keep that behavior.
- **Commits without pull requests:** Commits not included in a merged pull request now appear as changes alongside pull requests, while merge commits without a pull request are skipped. You can see how many such commits were found in the run summary and run record.
- **Installed version:** `chartula --version` now prints the installed informational version and exits successfully. You can run it from any directory without a checkout, configuration, key, or token.
- **First-tag and large-range confirmation:** A first tag now starts at the repository’s first commit, and large ranges are confirmed before GitHub is contacted or a model is called. To run a range without an interactive prompt, pass `--yes`; without a terminal, the run stops unless you do.

### What's Changed

- **Dependency updates:** The Anthropic, coverlet.collector, and Microsoft.Extensions.AI.OpenAI packages have been updated. You can rely on the listed package versions for this release.

### Bug Fixes

- **Help option groups:** The help output now lists each option once under its correct group. You can use it to find the available options and their descriptions.
- **Faithfulness checks for wrapped names:** The rule-based check now matches names when whitespace differs or code fences surround the text. You can rely on it to recognize names supported by the facts even when their formatting changes.
- **Empty technical releases:** When a release has nothing for technical readers, `CHANGELOG.md` and the release notes now say, “This release has no features, fixes, performance improvements or breaking changes.” The technical rendering in `changelog.json` remains empty, so you can still distinguish releases with nothing to render.
- **Readable JSON files:** `changelog.json` and the run record now leave characters such as backticks and non-ASCII text readable instead of escaping them unnecessarily. You can read and compare the files more easily while parsers continue to read the same values.
- **Review flag layout:** Review flags now appear after a blank line under their own heading, rather than directly beneath the rendering’s last entry. You can tell that the flags apply to the rendering, not just its final line.
- **Unset credential indicators:** The run header now says when a credential variable is unset or blank, while still naming the variable and never printing its value. You can see which variable needs to be set when authentication is missing.
- **Command-line argument checks:** Commands now stop on unknown, repeated, or unsupported options and on value options without a value, before configuration or repository checks begin. Use `-h` or `--help` after a command to display help and exit successfully.
- **GitHub API base URL:** A GitHub API base URL now works whether or not it ends with a slash, and the run header shows the normalized URL. You can enter the URL without a trailing slash.
- **Empty excluded-category list:** Setting `filter.excludeCategories` to an empty list now excludes no categories instead of retaining the default exclusions. You can keep all categories by using an empty list in the configuration file or environment variable.
- **Unreadable model responses:** When the model endpoint responds but its answer cannot be read, the error now identifies the answer as unreadable rather than reporting that the endpoint could not be reached. You can distinguish an invalid response from a connection failure.
- **Conflicting configuration files:** A run now stops if both `chartula.yaml` and `chartula.yml` exist, instead of silently choosing one. Keep one file and move the settings you want into it before running Chartula.
- **Publishing permission check:** `generate` now checks whether the token can publish before making any model calls. If the check fails, use `--no-publish` to write the files without publishing, or provide a token that can publish.
- **`--no-publish` help text:** The `--no-publish` help now says that the command writes every file and skips only GitHub release notes. You can use it to write the files without publishing release notes.
