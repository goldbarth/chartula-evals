---
title: Release 0.1.0-preview.4
description: This release changes release data and generation workflows, while adding clearer run output and checks for common setup and publishing issues.
publishedAt: 2026-10-07
---

### What needs action

- **Breaking:** The published `changelog.json` no longer includes pull request descriptions, and its schema version is now 2. Use the run record’s `facts` to access complete descriptions; update consumers of version 1 files to read them from the run record.
- **Breaking:** `preview` now shows the facts, what would be sent for each audience, and the prompt’s character count without making a model call or writing files. Use `generate --no-publish` when you need to see the rendered prose without publishing it.

### What's New

- **Run summary:** The run summary now opens with a line that reflects whether generation succeeded, had review flags, or failed for some audiences. Audience renderings appear under their audience names, so you can see which audience each one belongs to.
- **Doctor report:** `chartula doctor` now groups its checks and shows each status with a symbol and word in terminal output. When a warning concerns GitHub write access, the verdict distinguishes whether `preview` and `generate --no-publish` can start from whether `generate` will stop.
- **Run progress:** While a run is in progress, its steps now appear on stderr, with a spinner in supported terminals and plain lines otherwise. Use `--plain` on any command for plain output.
- **Quoted pull request text:** Pull request titles and descriptions are now quoted in the prompts, with long descriptions cut in the prompt. The model is instructed to treat quoted text as material to rephrase, not as instructions.
- **Published release protection:** `generate` now stops before its first model call when the release is already published, unless you explicitly allow replacement. Pass `--replace-published` to replace it, or `--no-publish` to write files without publishing release notes.
- **Config template hint:** When `chartula doctor` finds no `chartula.yaml`, it now points to the template for the installed version. You can use that template to find the configuration options available for your version.
- **Run progress:** Run steps now appear on stderr as they start, with their progress and elapsed time in a terminal. You can follow a run without waiting for its final output.
- **Setup checks:** `chartula doctor` now checks the setup a run needs and reports which checks pass, warn, fail, or are skipped. You can run it before `generate` to identify setup issues first.
- **Closed issue numbers:** `linkedIssues` now includes closed issue numbers found in the text the model reads, including at the default depth. If your configuration uses `title-description-and-issues`, `full`, or `issues`, those values continue to work as `title-and-description`.
- **Direct commits:** Commits in the release range that are not part of a merged pull request now appear as changes alongside pull requests; merge commits without a pull request are skipped. The run summary and record report the counts of direct and skipped merge commits.
- **Version command:** `chartula --version` now prints the installed version and exits successfully. You can check it from any directory without a checkout, configuration, key, or token.
- **First-tag ranges:** A first tag now includes commits from the first commit without an extra flag, and large ranges require confirmation before GitHub is contacted. In non-interactive runs, pass `--yes` to confirm the range up front.

### What's Changed

- **Dependency updates:** The Anthropic, coverlet.collector, and Microsoft.Extensions.AI.OpenAI dependencies have been updated. You do not need to take any action.

### Bug Fixes

- **Help options:** The command help now lists each option once under its correct group. You can refer to the help for an accurate list of command options.
- **Faithfulness checks:** The rule-based check now recognizes names in rendered text when whitespace differs or fenced code blocks are present. Names absent from the facts remain flagged.
- **Empty technical releases:** When a release has no technical changes to show, `CHANGELOG.md` and the release notes now say that it has no features, fixes, performance improvements, or breaking changes. The technical rendering in `changelog.json` remains empty.
- **Readable JSON files:** `changelog.json` and the run record now leave characters such as backticks and non-ASCII text readable in the files. Their parsed values remain the same.
- **Review flags:** Review flags now appear after a blank line under their own heading, rather than directly beneath the last rendering entry. Multi-line flags keep their continuation lines aligned under the flag.
- **Credential status:** The run header now says when a credential variable is unset or blank, while naming the variable to set. When it is set, the header continues to name the variable without showing its value.
- **Command-line validation:** Commands now stop on unknown, misplaced, repeated, or incomplete options instead of proceeding with arguments they cannot read as intended. Use `-h` or `--help` after a command to show help and exit successfully.
- **GitHub API URL:** A GitHub API base URL without a trailing slash now works, and the run header shows the URL used for requests. You can enter the URL with or without its trailing slash.
- **Empty category filter:** An empty `filter.excludeCategories` list now means no categories are excluded, including when set through the environment variable. You can keep internal changes by setting the list to empty.
- **Model response errors:** When the model endpoint answers but its response cannot be read, the error now identifies it as an unreadable answer rather than an unreachable endpoint. You can distinguish a response-format problem from a connectivity problem.
- **Conflicting config files:** A run now stops if both `chartula.yaml` and `chartula.yml` are present, naming both paths and explaining how to resolve the conflict. Keep one file and move the settings you want into it.
- **Publish permission check:** `generate` now checks whether the token can publish release notes before making model calls. If the check fails, use `--no-publish` to write files without publishing, or address the reported permission issue.
- **`--no-publish` help:** The help now clarifies that `--no-publish` writes every file and skips only GitHub release notes. You can use it to generate files without publishing release notes.
