---
title: Release 0.1.0-preview.4
description: This release makes release generation easier to inspect before model calls and protects published notes from unrequested replacement.
publishedAt: 2026-10-07
---

### What needs action

- **Breaking:** `changelog.json` now uses schema version 2 and no longer contains pull request descriptions; complete descriptions remain in the local run record, though reviewer notes can still appear in rendered text. If you consume descriptions or reload facts, switch to the run record’s `facts` array as described in [changelog-json.md](changelog-json.md); older run records have no facts.
- **Breaking:** `preview` no longer prints rendered changelog prose: it shows facts, excluded changes with their reasons, and the model calls and prompt character counts that generation would use, without a model key or writing anything. Use `generate --no-publish` when you need rendered prose without publication, as described in [docs/cli.md](docs/cli.md).

### What's New

- **Run summaries:** Commands now open with their name, and generation summaries lead with review flags or failed audiences when present. You can identify the run’s outcome from its first line and redirect the summary to a plain file while terminal progress remains live.
- **Setup report:** `doctor` now groups checks under Repository, Model and GitHub, with a word alongside each terminal status symbol. Its verdict distinguishes warnings that allow a run from GitHub write warnings that stop publication, so you can tell whether `preview`, `generate --no-publish` or `generate` would start.
- **Terminal progress:** Active run steps now show a spinner in supported terminals, and a step that ends with an exception is marked as failed rather than done. Redirected and CI output remains plain; pass `--plain` on the command line to request plain output.
- **Pull request text:** Pull request titles and descriptions are now quoted in model prompts, with descriptions cut at 8,000 characters while the run record retains the complete text. The product tells the model to treat quoted text as material to rephrase, not instructions, and not to guess beyond a cut; this does not guarantee that attempts to steer the model will fail.
- **Published release protection:** `generate` now stops before its first model call if the tag already has a published release, and checks again before writing. Published notes remain untouched unless you pass `--replace-published` to `generate`; use `--no-publish` instead to write files without publication.
- **Configuration template:** `doctor` now displays a configuration-template link when no `chartula.yaml` is found. For installed releases, the link targets that version’s tag, so the template does not introduce settings from a newer version.
- **Run activity:** Runs now show progress while reading pull requests, rendering audiences and checking their text; `preview` shows only the reading step. Progress goes to stderr, leaving stdout available for the changelog, with elapsed time in a terminal and plain step lines outside one.
- **Setup checks:** You can now run `chartula doctor` to check repository, configuration, model and GitHub setup before generating a release. It reports failures and warnings without writing or publishing anything, using a small model request for each model a run uses and three GitHub requests.
- **Closed issue references:** Closed issue numbers now come from the text the model reads: title and description by default, or the title alone at `title-only` depth. The rule-based check accepts those references, and existing `title-description-and-issues`, `full` and `issues` values continue to work as `title-and-description` without fetching issue content.
- **Direct commits:** Commits without a merged pull request now appear alongside pull requests in release order, subject to the same filtering rules. You can count on direct pushes being considered even when the release contains pull requests, while merge commits and commits belonging to reverted pull requests are not brought back as separate changes.
- **Installed version:** `chartula --version` now prints the installed build’s version from any directory, without a checkout, configuration or credentials. Its output matches the version recorded in `changelog.json`, so a report and a run file identify the same build.
- **First-tag releases:** A first tag now includes commits from the first commit through that tag without requiring `--whole-history`. First-tag and large ranges require confirmation before GitHub requests or model calls, so unattended runs stop unless you pass `--yes`; use `--since <ref>` to start later.

### What's Changed

- **Dependency updates:** Dependencies now use Anthropic 12.53.0, coverlet.collector 10.1.0 and Microsoft.Extensions.AI.OpenAI 10.10.1.

### Bug Fixes

- **Help organization:** `chartula --help` listed `--audience` twice and placed `--replace-published` under appearance options. Each option now appears once in its group, with publication controls under “What a run writes.”
- **Name checks:** Names supported by descriptions could receive review flags when line breaks or fenced code blocks changed how the text appeared in a rendering. The rule-based check now recognizes those names across whitespace differences while still flagging absent names and preventing matches across separate facts.
- **Releases with nothing to render:** Releases with no changes for technical readers produced a bare heading in `CHANGELOG.md` and empty release notes. Those outputs now explain that the release has no features, fixes, performance improvements or breaking changes, without a model call; the technical rendering in `changelog.json` remains empty.
- **Readable JSON:** Backticks and non-ASCII text in `changelog.json` and run records were written as escapes that made raw files difficult to read. Both files now retain readable characters such as backticks and accented letters while JSON parsers receive the same values as before.
- **Review flag layout:** Review flags appeared directly beneath a rendering’s last entry, making them look attached to that entry even when they concerned another one. A separate “Flagged for review:” block now identifies them as applying to the rendering rather than its final entry.
- **Credential status:** Run headers named a credential source even when its environment variable was unset or blank. They now report “unauthenticated” and name the missing variable, so the header agrees with whether a credential is sent without exposing its value.
- **Command-line validation:** Mistyped or incomplete options could start a run with unintended settings, and `generate --help` could generate and publish a draft. Invalid arguments now stop before configuration or repository access, while `-h` and `--help` after a known command display help without starting a run.
- **GitHub Enterprise URLs:** A GitHub API URL without a trailing slash could send requests to the wrong path and produce a misleading 404. URLs such as an Enterprise `/api/v3` endpoint now resolve requests to the same path with or without that slash, and the header shows the URL used.
- **Empty category exclusions:** An empty category-exclusion list still excluded Internal changes because it was treated as an absent setting. An explicit empty list now excludes no category; set `filter.excludeCategories: []` in the configuration file or `Chartula__Filter__ExcludeCategories=[]` in the environment.
- **Unreadable model answers:** A model response the provider’s SDK could not read was reported as an unreachable endpoint. Errors now distinguish an unreadable answer from no response and include the response status and unreadable value when available, so the message identifies whether the endpoint answered.
- **Conflicting configuration files:** When both `chartula.yaml` and `chartula.yml` existed, settings in the latter were silently ignored. The run now stops before GitHub requests or model calls and names both paths; move the wanted settings into one file and delete the other.
- **Publication permission check:** `generate` could complete every model call before discovering that its token could not publish release notes. It now checks permission before reading pull requests or calling the model, so a refused token does not spend on generation; `generate --no-publish` still writes files without requiring publication permission.
- **No-publication help:** The help for `--no-publish` named only `changelog.json` and `CHANGELOG.md`, omitting other files it writes. It now states that every file is written and only GitHub release-note publication is skipped, matching the command’s behavior.
