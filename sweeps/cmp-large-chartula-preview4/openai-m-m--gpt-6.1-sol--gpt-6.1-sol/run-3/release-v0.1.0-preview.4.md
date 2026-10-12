---
title: Release 0.1.0-preview.4
description: This release makes runs easier to inspect before generation and protects published release notes from unintended replacement.
publishedAt: 2026-10-07
---

### What needs action

- **Breaking:** `changelog.json` schema version 2 no longer includes pull request descriptions; the local run record retains the complete facts, keeping full author descriptions out of the published payload. Update consumers that need descriptions to read the run record, following [changelog-json.md](changelog-json.md).
- **Breaking:** `preview` now shows facts, filtering reasons and planned model calls instead of rendered prose, with exact rephrasing prompt character counts and no model key, model calls or file writes. Use `generate --no-publish` to see rendered prose without publishing, as described in [docs/cli.md](docs/cli.md).

### What's New

- **Run summaries:** Each command opens with its name, and generation summaries lead with review flags or audience failures when present. You can read the run's outcome from the first summary line, while redirecting stdout keeps the report plain without stopping terminal progress on stderr.
- **Setup check results:** `doctor` now groups checks under Repository, Model and GitHub, with a word alongside each terminal status symbol. Its verdict distinguishes warnings that allow a run from GitHub write warnings that would stop publishing, so you can tell whether `preview`, `generate --no-publish` or `generate` would start.
- **Terminal progress:** Active run steps now show a spinner in live terminals, and a step ending in an exception is marked as failed rather than done. Redirected output and CI keep plain lines without terminal controls; use `--plain` on the command line to request plain output.
- **Pull request text:** Pull request titles and descriptions are quoted in model prompts, and descriptions longer than 8,000 characters are cut there while remaining complete in the run record. The product now tells both the rephrasing model and the thorough check to treat quoted text as material, not instructions, and not to guess omitted text; this does not guarantee that attempts to steer the model cannot work.
- **Published release protection:** `generate` now stops before its first model call if the tag already has a published release, and checks again before writing so notes published during rendering are protected too. To replace published notes, pass `--replace-published` to `generate`; drafts still update without it.
- **Configuration template:** `doctor` now shows a configuration template link when no `chartula.yaml` is found. The link targets the installed version's tag rather than `main`, so released binaries point to a template for their version.
- **Run progress:** Runs now show when they are reading pull requests, rendering audiences and checking renderings, with commit counts and elapsed time in a terminal. Progress stays on stderr, so a changelog redirected from stdout contains no progress lines.
- **Setup diagnosis:** `chartula doctor` now checks the repository, configuration, model endpoint and GitHub access before generation, marking failed prerequisites and skipping dependent checks. You can use its exit code in CI to detect setup failures without writing files or publishing; the checks make a capped model call per model used and three GitHub requests.
- **Closed issue references:** Closed issue numbers now come from the same title and description text the model reads, including at the default depth. The rule-based check accepts those references, and existing configurations using `title-description-and-issues`, `full` or `issues` continue to work as `title-and-description` without reading issue content.
- **Direct commits:** Commits without a merged pull request now appear alongside pull requests, subject to the same filtering rules, while merge commits without a pull request are skipped. Releases can now include directly pushed fixes even when they also contain pull requests, without bringing back commits from reverted pull requests.
- **Installed version:** `chartula --version` now prints the installed build's informational version and exits successfully from any directory, without a checkout, configuration or credentials. Its output matches the version recorded in `changelog.json`, so reports and run files identify the same build.
- **First-tag releases:** A first tag can now be rendered from the first commit without `--whole-history`, with confirmation before GitHub requests or model calls for first tags and ranges above the confirmation threshold. You can review the range and its cost before proceeding; pass `--yes` on the command line to confirm an unattended run.

### What's Changed

- **Dependency updates:** The release uses Anthropic 12.53.0, coverlet.collector 10.1.0 and Microsoft.Extensions.AI.OpenAI 10.10.1.

### Bug Fixes

- **Help option groups:** `chartula --help` listed `--audience` twice and placed `--replace-published` under appearance options. Each option now appears once in its appropriate group, with publishing options together under “What a run writes.”
- **Quoted-name checks:** Names supported by descriptions could receive review flags when the descriptions contained wrapped lines or fenced code blocks. The rule-based check now compares the text in the rendering's whitespace form while keeping facts separate, so supported names are recognized without accepting matches across different facts.
- **Releases without technical changes:** A release with no changes for technical readers could produce only a heading in `CHANGELOG.md` and empty release notes. Those outputs now state that the release has no features, fixes, performance improvements or breaking changes, making the empty result explicit without a model call.
- **Readable JSON:** Backticks and non-ASCII text in `changelog.json` and run records were obscured by character escapes when reading the raw files. Both files now retain readable characters while preserving the same values for JSON consumers.
- **Review flag layout:** Review flags appeared directly beneath a rendering's last entry, making them look attached to that entry even when they concerned another. A separate “Flagged for review:” block now identifies them as flags for the rendering.
- **Credential status:** Run headers claimed a key or token came from a credential variable even when it was unset or blank. The header now reports unauthenticated access and names the missing variable, matching whether requests carry credentials without exposing their values.
- **Command-line validation:** Mistyped, incomplete or unsupported options could start unintended runs, and `generate --help` could generate and publish a draft. Invalid arguments now stop before configuration or repository access with a corrective message, while `-h` and `--help` after a known command show help without starting a run.
- **GitHub API addresses:** A GitHub API address without a trailing slash could send requests to the wrong path and report a misleading 404. Addresses with or without the slash now resolve to the same request paths, and the header shows the address actually used.
- **Empty category exclusions:** An empty category exclusion list kept the default Internal exclusion instead of excluding nothing. You can now count on an explicit empty list to retain every category; set `filter.excludeCategories: []` in `chartula.yaml` or `Chartula__Filter__ExcludeCategories=[]` in the environment.
- **Unreadable model responses:** A model response the provider SDK could not read was reported as an unreachable endpoint. Error messages now distinguish a received but unreadable answer from a connection failure, showing the response status and unreadable value when available so you can identify the kind of failure.
- **Conflicting configuration files:** When `chartula.yaml` and `chartula.yml` existed together, settings in the latter were silently ignored. The run now stops before GitHub requests or model calls and names both paths; keep one file, move the wanted settings into it and delete the other.
- **Publishing permission check:** `generate` could spend on every model call before discovering that its token could not publish. Publishing permission is now checked before pull requests are read or models are called, though a later write can still fail; use `generate --no-publish` to write files without requiring publishing permission.
- **No-publish help:** The help for `--no-publish` named only `changelog.json` and `CHANGELOG.md`, leaving out the release Markdown file and run record. It now states that every file is written and only GitHub release-note publication is skipped, so the help describes the command's actual output.
