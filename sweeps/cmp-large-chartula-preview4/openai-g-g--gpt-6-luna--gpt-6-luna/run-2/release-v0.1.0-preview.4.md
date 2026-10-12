---
title: Release 0.1.0-preview.4
description: Chartula adds clearer run previews and status reporting, while changing how pull request descriptions are stored and used.
publishedAt: 2026-10-07
---

### What needs action

- **Breaking:** The published `changelog.json` no longer includes pull request descriptions, and its schema version is now 2. To keep reading facts with their descriptions, load them from the run record instead; update consumers of version 1 files to use the description in the run record.
- **Breaking:** `preview` now shows the facts, what would be sent for each audience, and prompt character counts without making a model call or writing files. Use `generate --no-publish` when you need to see the rendered prose; preview no longer prints renderings.

### What's New

- **Run summary:** The run summary now opens with a line showing whether it generated successfully, has review flags, or failed for some audiences. You can read each rendering under its audience heading and identify how the run went from the first line.
- **Doctor report:** `doctor` now groups its checks into Repository, Model, and GitHub sections and marks each status with a symbol and word in terminals. When a warning is about GitHub write, the verdict distinguishes whether `preview` and `generate --no-publish` can start from whether `generate` will stop.
- **Run progress display:** During a run, the active step now appears with a spinner in a live terminal, while redirected output remains plain; `--plain` keeps output plain in every command. You can follow the run's steps as they happen, and failed steps are marked as failures.
- **Pull request text in prompts:** Pull request titles and descriptions are now quoted in the rephrasing and thorough-check prompts, and descriptions longer than 8,000 characters are cut in the prompt. The model is told to treat this text as material to rephrase, not instructions, so you can rely on the prompt retaining the full description in the run record while limiting what is shown to the model.
- **Published release protection:** `generate` now stops before its first model call when the release is already published, unless replacing it was requested. To replace published release notes, pass `--replace-published`; use `--no-publish` to write files without publishing.
- **Configuration template hint:** When `doctor` finds no `chartula.yaml`, it now points to the configuration template for the installed version. You can use that template to configure Chartula for that version.
- **Run progress:** The run now reports when it is reading pull requests, rendering each audience, and checking renderings. You can follow progress on stderr without progress lines appearing in stdout.
- **Setup checks:** `chartula doctor` now checks the setup needed for a run and reports each check as `ok`, `warn`, `fail`, or `skip`. You can use its exit code to decide whether to start a run; it writes and publishes nothing.
- **Closed issue numbers:** Closed issue numbers are now taken from the title and description the model reads, including at the default fact depth; at `title-only`, they come from the title. You can keep existing `title-description-and-issues`, `full`, and `issues` configuration values, which now read as `title-and-description`.
- **Commits without pull requests:** A commit not included in a merged pull request now appears as its own change, unless it is a merge commit, which is skipped. You can see the number of commits without pull requests and skipped merge commits in the release summary and run record.
- **Installed version:** `chartula --version` now prints the installed informational version and exits successfully. You can check the version from any directory without a checkout, configuration, key, or token.
- **First-tag release range:** A first tag now uses the range from the first commit by default, and large ranges or first-tag ranges require confirmation before GitHub is contacted or a model call is made. To confirm without an interactive terminal, pass `--yes`; otherwise the run stops, and you can use `--since <ref>` to start later.

### What's Changed

- **Dependency updates:** The Anthropic, coverlet.collector, and Microsoft.Extensions.AI.OpenAI packages have been updated. You can rely on the updated package versions.

### Bug Fixes

- **Help option groups:** The help now lists each option once under its command group, with `--replace-published` under “What a run writes.” You can refer to the help for an up-to-date list of options.
- **Faithfulness check formatting:** The rule-based check now recognizes names in facts when whitespace differs or fenced code blocks are present, while still flagging names the facts do not contain. You can rely on the check comparing text in the folded form used by the rendering.
- **Empty technical rendering:** When a release has no technical changes to render, `CHANGELOG.md` and the release notes now say, “This release has no features, fixes, performance improvements or breaking changes.” You can distinguish an empty technical rendering from missing text; the `changelog.json` technical rendering remains empty.
- **Readable JSON:** `changelog.json` and the run record now leave characters unescaped unless JSON requires escaping. You can read code spans and non-ASCII text directly in both files while parsers continue to read the same values.
- **Review flags layout:** Review flags now appear after a blank line under their own heading, rather than directly beneath the rendering’s last line. You can tell that flags apply to the rendering, not just its final entry.
- **Credential status in run header:** When a credential variable is unset or blank, the run header now says it is unauthenticated and names the variable. You can tell whether a credential is set without seeing its value.
- **Command-line option validation:** The CLI now refuses unknown options, options that do not belong to a command, and options missing a value before a run starts; `-h` and `--help` work after a command. You can correct malformed commands without risking an unintended run.
- **GitHub API URL:** A GitHub API base URL without a trailing slash now works, and the run header shows the URL with the slash added. You can use either form of the URL and rely on requests resolving to the same API path.
- **Empty category exclusion list:** An empty `filter.excludeCategories` list now means that no categories are excluded, including when set through the environment variable. You can override the default excluded categories with an empty list.
- **Unreadable model response:** When the model endpoint responds but its answer cannot be read, the error now says the answer was unreadable instead of reporting that the endpoint could not be reached. You can distinguish an unreadable response from a connection failure.
- **Duplicate configuration files:** A run now stops if both `chartula.yaml` and `chartula.yml` are present, instead of silently choosing one. Keep one file and move the settings you want into it before running Chartula.
- **Check publishing permission early:** `generate` now checks whether the token can publish before reading pull requests or making model calls. If the check fails, use `--no-publish` to write files without publishing; `preview` and `generate --no-publish` do not perform this check.
- **`--no-publish` help text:** The `--no-publish` help now says it writes every file but skips GitHub release notes. You can rely on the option to write the run record and other files without publishing release notes.
