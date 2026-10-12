---
title: Release 0.1.0-preview.4
description: This release makes release generation easier to inspect before model calls and protects published notes from unintended replacement.
publishedAt: 2026-10-07
---

### What needs action

- **Breaking:** `changelog.json` schema version 2 no longer includes pull request descriptions; complete descriptions remain in the local run record, so the published payload does not carry full reviewer notes. If you consume version 1 descriptions or reload facts, switch to the run record's `facts` array as described in [changelog-json.md](changelog-json.md); older run records have no facts.
- **Breaking:** `preview` no longer prints generated prose: it shows facts, excluded changes and planned model calls with exact rephrasing prompt character counts, without a model key, model calls or file writes. Use `generate --no-publish` to see generated prose without publishing, as described in [the CLI guide](docs/cli.md).

### What's New

- **Run summaries:** Each command now opens with its name, and generation summaries lead with review flags or audience failures when present. You can read the run's outcome from the first line, while redirecting the summary to a file preserves plain output there and live progress on the terminal.
- **Setup report:** `doctor` now groups checks under Repository, Model and GitHub, with status words and terminal symbols. Its verdict distinguishes warnings that allow a run from GitHub write warnings that allow only `preview` and `generate --no-publish`.
- **Terminal progress:** Active run steps now show a spinner in a live terminal, and a step ending in an exception is marked as failed rather than done. You can keep plain ASCII progress without control characters in redirected output or CI, or request it with `--plain` on the command line.
- **Pull request text:** Pull request titles and descriptions are now quoted in model prompts, and descriptions longer than 8,000 characters are cut there while remaining complete in the run record. The model and thorough check are told to treat quoted text as material rather than instructions and not to guess beyond a cut description; this does not guarantee that attempts to steer the model will fail.
- **Published release protection:** `generate` now stops before its first model call when the tag already has a published release, and checks again before writing. Published notes remain protected unless you pass `--replace-published` to `generate`; use `--no-publish` instead to write files without publishing.
- **Configuration template:** `doctor` now shows a configuration template link when no `chartula.yaml` is found. For installed releases, the link targets that version's tag rather than `main`, so the template does not introduce settings from a later version.
- **Run progress:** You can now see pull request reading, audience rendering and checking steps while a run is working, with commit counts and elapsed time in a terminal. Progress goes to stderr, so redirected changelog text on stdout stays separate; preview shows only the reading step.
- **Setup checks:** You can now run `chartula doctor` to check repository, configuration, model and GitHub setup before generation. It reports failures and skipped dependent checks without writing or publishing, using one small model call per model and three GitHub requests.
- **Closed issue references:** Closed issue numbers now come from the text the model reads: title and description by default, or the title alone at title-only depth. The rule-based check accepts those references, and existing issue-depth configuration values continue to work as title-and-description without reading issue contents.
- **Direct commits:** Commits without a merged pull request now appear alongside pull requests in release order, subject to the same filtering rules. Direct changes can reach the changelog even when the release has pull requests, while merge commits and commits belonging to reverted pull requests stay out.
- **Installed version:** You can now run `chartula --version` from any directory without a checkout, configuration or credentials. Its output identifies the same build recorded in `changelog.json`, so a report and a run file can name the same version.
- **First-tag releases:** A first tag now includes commits from the first commit through that tag without requiring `--whole-history`, and first-tag or large ranges ask for confirmation before GitHub requests or model calls. You can review the range before spending on it, or confirm an unattended run with `--yes` on the command line.

### What's Changed

- **Dependency updates:** Dependencies now use Anthropic 12.53.0 instead of 12.49.0, coverlet.collector 10.1.0 instead of 10.0.1, and Microsoft.Extensions.AI.OpenAI 10.10.1 instead of 10.10.0.

### Bug Fixes

- **Help option groups:** `chartula --help` listed `--audience` twice and placed `--replace-published` under appearance options. Each option now appears once in its intended group, so you can find publishing controls under “What a run writes”.
- **Name checks:** Names backed by descriptions could be flagged when line breaks or fenced code changed how the text appeared in a rendering. The rule-based check now accepts names supported within one fact regardless of whitespace or fences, while still flagging names absent from the facts.
- **Releases without technical changes:** Releases with nothing for technical readers could produce a bare changelog heading and empty release notes. `CHANGELOG.md` and release notes now explicitly say the release has no features, fixes, performance improvements or breaking changes, without a model call; the technical rendering in `changelog.json` remains empty.
- **Readable JSON:** Backticks and non-ASCII text in `changelog.json` and run records could appear as escape sequences that made raw files hard to read. Both files now preserve readable characters while parsed values remain unchanged; consumers must still escape text when displaying it in HTML.
- **Review flag layout:** Review flags appeared directly beneath the last rendering entry, making them look attached to that entry even when they concerned another. A separate “Flagged for review:” block now makes their scope the rendering rather than its last line.
- **Credential notices:** Run headers claimed a key or token came from a variable even when that variable was unset or blank. Headers now identify unauthenticated requests consistently with the warnings and requests, naming the variable without revealing its value.
- **Command-line validation:** Misspelled, misplaced or incomplete options could start an unintended run, and `generate --help` could generate and publish a draft. Invalid arguments now stop before configuration or repository access with guidance, while `-h` or `--help` after a known command shows help without starting a run.
- **GitHub Enterprise URLs:** A GitHub API base URL without a trailing slash could send requests to the wrong path and produce misleading 404 errors. URLs with or without that slash now reach the same API path, and the run header shows the URL actually used.
- **Empty category exclusions:** An empty category exclusion list in configuration incorrectly kept the default exclusion of Internal changes. An explicit `[]` now excludes no category, so your choice to retain internal work takes effect when set under `filter.excludeCategories` in the configuration file or through `Chartula__Filter__ExcludeCategories`.
- **Unreadable model answers:** A model endpoint that answered with a body the SDK could not read was reported as unreachable. Errors now distinguish an unreadable answer from no response and include the reading failure, so you can identify an answer-format problem rather than a network problem.
- **Duplicate configuration files:** When both `chartula.yaml` and `chartula.yml` existed, settings in the latter were silently ignored. The run now stops before GitHub requests or model calls and names both paths; keep one file, move the settings you want into it and delete the other.
- **Publishing permission check:** `generate` could finish every model call before discovering that its token could not publish release notes. It now checks permission before reading pull requests or calling the model, so a refused token does not incur those calls; use `generate --no-publish` to write files without publishing.
- **No-publish help:** The help for `--no-publish` named only `changelog.json` and `CHANGELOG.md`, leaving other written files unmentioned. It now states that every file is written and only GitHub release-note publication is skipped, so the help describes the command's full output behavior.
