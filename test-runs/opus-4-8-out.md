Preview changelog for v0.1.0

--- Technical ---
## Features

- Every `preview` and `generate` run now ends with a run-metrics summary reporting what the run did and what it cost. Rule-based and thorough checks, rephrasing, and totals are each broken out; the thorough check's cost is paired against the claims only it caught, so the keep-or-drop decision can be made from data across releases. `ChatModel` reports token usage attributed per `LlmOperation`; `ReleasePipeline` records both checks' findings in one call and returns the report on `ReleaseOutcome`. Measurement is a side channel — the sink is optional everywhere, and a run without one produces byte-identical output. See `docs/run-metrics.md`.
- Category presentation is now configurable via a `categories` section in `chartula.yaml`, alongside the existing `labels`, `factBase`, and `faithfulness` sections. `CategorySettings` holds category order, display names, and breaking-change prominence (`order`, `names`, `breakingProminent`, default `true`); unknown category names are rejected with a clear message. `GroundedFactsFactory` is extracted from `ReleaseChangelogGenerator` as the single home for audience filtering, category ordering, and display naming. Untouched sections keep their defaults. See `docs/configuration.md`.
- The CLI now reads `chartula.yaml` (or `.yml`) via `AddChartulaYaml`, flattening it into `Chartula:*` configuration keys layered before environment variables (env overrides YAML). All section options (`llm`, `github`, `labels`, `filter`, `factBase`, `faithfulness`, `review`) bind to their defaults with no file or env vars present; configuration is refining, never required. A minimal `chartula.example.yaml` ships at the repo root with everything commented out, and configuration errors are reported as a clear `Configuration error: ...` message. See `docs/configuration.md`.
- Added `chartula preview` and `chartula generate` commands wired to `ReleasePipeline`, which orchestrates the full flow over ports only: read commit range and PRs, build the fact base, render all audiences, run the rule-based and thorough faithfulness checks and review, then write outputs. Both take `--tag` and `--repo <owner/name>` and share the identical flow; `generate` writes `changelog.json`, `CHANGELOG.md`, and the GitHub release notes, while `preview` writes and publishes nothing. Includes a usage screen, a per-audience summary, and clear errors for unknown commands, missing options, and pipeline failures.
- All audience texts (`technical`, `customer`, `product`) are now stored in `changelog.json` under a `renderings` object written in a fixed order, rather than as separate marketing files in the repo. `ChangelogJsonSerializer.Serialize` and `IChangelogJsonWriter` take an optional renderings map; when none is provided, the object is present but empty. Change entries stay deterministic facts, only `renderings` are LLM-produced. `schemaVersion` stays `1` — adding an optional field is non-breaking. See `docs/changelog-json.md`.
- Generated text is now written back to GitHub release notes via the new `IReleaseNotesWriter` port and `GitHubReleaseNotesWriter` (GitHub REST API over plain `HttpClient`, source-generated JSON, AOT-friendly). A release is looked up by tag and updated in place when found or created when absent, so re-running the same tag never produces a duplicate; the release's `html_url` is returned, and API or network failures become clear `InvalidOperationException`s. GitHub `HttpClient` setup is extracted into a shared `GitHubHttpClientFactory` used by both the PR reader and the release-notes writer.
- Each release is now written as a new section at the top of `CHANGELOG.md`, preserving prior history verbatim. The new `ChangelogMarkdownComposer` (pure logic) prepends the section, adds a `# Changelog` title to a brand-new file, and replaces an existing tag's section in place rather than duplicating or reordering — running the same release twice yields a byte-identical file. Format logic lives in Core (`IChangelogMarkdownWriter`); file I/O lives in `FileChangelogMarkdownWriter` in `Chartula.Infrastructure`.
- Added an opt-in review mode for human sign-off before publishing, via `IReviewCoordinator`/`ReviewCoordinator`. When off (the default), text passes through approved as-is and the reviewer is never consulted; when on, an `IReviewer` approves or returns an edited version and the coordinator returns that `ReviewDecision`, whose `Text` is written. `ReviewPresentation` formats an item for a maintainer with the generated text and flagged passages from the rule-based and thorough checks highlighted. `AutoApproveReviewer` is the non-interactive default; the CLI binds the `Chartula:Review` toggle.
- Added a thorough second-pass LLM faithfulness check (`IThoroughFaithfulnessChecker`/`ThoroughFaithfulnessChecker`) that catches meaning-level hallucinations the rule-based check cannot, turning the fact base into grounded facts and flagging unsupported claims. It is on by default and disabled via the `Chartula:Faithfulness:Thorough` config key; when off or with nothing to check, it returns a faithful report with no LLM call. The faithfulness prompt moves from an inline placeholder in `ChatModel` into `IChangelogPromptBuilder.BuildFaithfulnessPrompt`, with an explicit meaning-level-distortion instruction.
- Added a rule-based faithfulness check (`IRuleBasedFaithfulnessChecker`/`RuleBasedFaithfulnessChecker`) that catches obvious hallucinations for free before any LLM call. It flags numbers in the output absent from the facts (PR numbers, linked issues, and numbers in titles/descriptions/tag are allowed), quoted or backticked names not appearing in the facts, and breaking-change claims when no fact is marked breaking. It has no `IChangelogModel` dependency, so it costs zero tokens and always runs; flags are advisory and feed review mode rather than failing the run. Uses source-generated regexes (AOT-friendly).
- Rendering now produces consistent formatting and tone per audience. `IChangelogFormatter`/`ChangelogFormatter` deterministically normalizes model output with conservative, structure-preserving rules (normalized line endings, a single `- ` bullet marker, trimmed trailing whitespace, collapsed blank-line runs) while leaving headings and prose intact, applied to every rendering. A new prompt rule instructs the model to write in one consistent voice and not carry over an individual author's tone or phrasing.
- Technical, customer, and product-manager versions of a release are now rendered from one `FactBase` via `IReleaseRenderer`/`ReleaseRenderer`, so they cannot contradict each other. Audience selection is deterministic in code: customer omits non-user-visible changes and their links, technical keeps the pull request link and full change set, and product sees the full set. A failure in one audience does not fail the others.
- Added a first-class prompt architecture (`IChangelogPromptBuilder`/`ChangelogPromptBuilder` producing a `ChangelogPrompt`) that rephrases facts and never invents them. The system prompt pins the model to rephrasing — never introducing a fact, number, or name not in the list; treating each fact's category and `(breaking)` marker as established; staying brief on thin facts; and omitting preamble or conclusion — plus per-audience guidance. The user prompt carries only the facts. Categories and flags reach the model as text and are not decided by it; `ChatModel` delegates to the builder.
- Changelog generation now works through the provider seam via `IReleaseChangelogGenerator`/`ReleaseChangelogGenerator` and `ChangelogGenerationResult`, while staying provider-agnostic. It turns the fact base into grounded fact statements and makes exactly one `IChangelogModel.RephraseAsync` call per release, with no call for an empty fact base. Provider failures are caught and returned as a failed result carrying the release tag and provider message; cancellation propagates. The generator depends only on `IChangelogModel`.
- The release fact base is now written to `changelog.json` as a durable, machine-readable record. `ChangelogDocument` is the stable on-disk shape (`schemaVersion` + `tag` + `changes`), kept separate from the domain `FactBase`; `ChangelogJsonSerializer` converts `FactBase` to and from JSON, deterministically and source-generated (AOT/trim-safe), writing category as its name. `IChangelogJsonWriter` lives in Core and `FileChangelogJsonWriter` in `Chartula.Infrastructure`. `schemaVersion` (currently `1`) is the contract; fields are always present including `null`, and nothing in the file is LLM-generated. See `docs/changelog-json.md`.
- Fact-base depth is now configurable via `Chartula:FactBase:Depth`, with `FactBaseDepth` offering three modes: `TitleOnly`, `TitleAndDescription` (the default), and `TitleDescriptionAndIssues`. `FactBaseBuilder` honors the depth — description from the middle mode up, linked issues only in the deepest mode. `FactBaseDepthParser` accepts canonical names plus aliases (`title`, `description`, `full`) and raises a clear error on an unknown value.
- Added `IFactBaseBuilder`/`FactBaseBuilder` and the `FactBase` container (tag plus one `ChangeFact` per included change) to transform curated changes into the release fact base. It resolves changes with the missing-PR fallback, drops filtered changes, and maps survivors to `ChangeFact`s. Category and breaking flag come from deterministic categorization (a label can force the category), `IsUserVisible` is derived from the category plus every breaking change, and `LinkedIssues` are parsed from GitHub closing keywords (`closes/fixes/resolves #n`). The builder has no LLM dependency.
- Added the `ChangeFact` data model — one structured, serializable object per change and the single source of truth the LLM may only rephrase from. It captures title, PR number, link, category (from deterministic categorization), user-visible flag, breaking flag, linked issues, and an optional description. Every field is derived deterministically with nothing LLM-generated; PR-only fields (number, link) are nullable so commit-based changes fit the same shape.
- Internal and chore changes are now dropped by default via `IChangeFilter`/`ChangeFilter` and `ChangeFilterRules`, combining deterministic categorization with label rules. The decision order: an excluding label wins outright, a breaking change is never dropped, otherwise a change is dropped when its effective category (a label-forced one, else the deterministic one) is in the excluded set. The default excluded set is `Internal`, overridable via `Chartula:Filter:ExcludeCategories` — an explicit (possibly empty) list replaces the default.
- Curation can now be steered with GitHub label rules from config, without touching code. `LabelRules` (excluded labels, label-to-category overrides, only-include-labeled mode) plus `ILabelRulePolicy`/`LabelRulePolicy` produce a `LabelDecision` (include plus optional forced category) with precedence: exclusion wins, then only-labeled drops unlabeled changes, otherwise included with the first matching label deciding a forced category. All rules are optional — `LabelRules.None` ignores labels so the tool works with none — and matching is case-insensitive. The CLI binds the `Chartula:Labels` section via `LabelRules.From`, with a clear error on an unknown category name.
- Categories are now assigned deterministically before any LLM call via `IChangeCategorizer` + `ConventionalCommitCategorizer`, so the model cannot invent what kind of change something is. It reads Conventional Commit conventions from the change title into `ChangeCategory` (Feature, Fix, Performance, Documentation, Refactor, Internal, and Other as the default for unrecognized titles). Breaking is tracked separately (`ChangeClassification.IsBreaking`) via a `!` marker, a `breaking` type, or a `BREAKING CHANGE` body note, so a breaking feature stays a feature but is still flagged. Pure, deterministic, and AOT-friendly (source-generated regex).
- Added `IReleaseChangeResolver` + `ReleaseChangeResolver` to degrade gracefully when clean PRs are missing, turning a `CommitRange` and merged `PullRequestInfo` list into `ReleaseChange` values (title, description, number, url, labels, `ChangeSource`, commit sha). Merged PRs yield one change per PR; with no PRs, one change per commit from the subject; a blank or uninformative PR title falls back to the body's first informative line, then to a generic `PR #n`; an empty release yields an empty set with no exception. Pure domain logic with no I/O.
- Merged pull requests for a release are now fetched from the GitHub API via the `IReleasePullRequestReader` port plus `PullRequestInfo` (number, title, description, labels, url) and `RepositoryCoordinates`. `GitHubPullRequestReader` queries GitHub's pull-requests-associated-with-a-commit endpoint for the commits in a `CommitRange`, keeps merged PRs only, and de-duplicates by number, parsing DTOs via a source-generated `System.Text.Json` context. Raw `HttpClient` + source-gen was chosen over Octokit for a native-AOT-friendly, mockable design; the GitHub token is read by env-var name (`GITHUB_TOKEN`) and is optional. API, network, and malformed-response failures raise a clear `InvalidOperationException`.
- The commit range for a release is now read from git via the `IReleaseCommitReader` port plus `CommitInfo` and `CommitRange` (with `IsFirstRelease`). The new `Chartula.Infrastructure` layer's `GitCliCommitReader` shells out to `git` for the range since the previous tag (`<prev>..<tag>`), or all history up to the tag on a first release, with clear errors for unknown or blank tags. The git CLI was chosen over LibGit2Sharp to avoid native dependencies that would conflict with planned native-AOT binaries; the pipeline depends only on the port.
- Added a provider-agnostic LLM seam in the new `Chartula.Core`: `IChangelogModel` (`RephraseAsync`, `CheckFaithfulnessAsync`) is the interface the pipeline depends on, `ChatModel` is the single implementation backed by a provider-agnostic `Microsoft.Extensions.AI.IChatClient`, alongside domain types `Audience`, `GroundedFacts`, `RephraseRequest`, `FaithfulnessRequest`, and `FaithfulnessReport`. Anthropic is wired as the first provider in the composition root — the only provider-specific code — with model and provider selectable via config and the API key read by env-var name.

## Fixes

- Fixed two release blockers found by dogfooding v0.1.0. In `ChatModel`, calls went out without `ChatOptions`, so `MaxOutputTokens` was never set and the provider substituted its default of 1024, truncating all three audience texts mid-word; the ceiling is now always sent, configurable via `llm.maxOutputTokens` and defaulting to 16000. In `ConventionalCommitCategorizer`, `MentionsBreakingChange` searched the whole body for `BREAKING CHANGE` as a case-insensitive substring, so prose discussing breaking changes falsely declared them (six of thirty-three v0.1.0 changes mislabelled); it now matches the Conventional Commits footer — uppercase, start of line, colon-terminated.

## Documentation

- Brought the documentation up to what Chartula actually is now that Phase 1 is complete. `Usage` is now runnable, showing `chartula preview` with the required `--tag` and `--repo`; the `docs/` folder is now linked from a README documentation index; `chartula.example.yaml` now shows all eight supported sections (adding `github`, `labels`, `categories`, and `review`); the status badge reflects the closed Phase 1 issues; and CONTRIBUTING names the required SDK for `net10.0` and the commit scopes actually in use. Added `docs/architecture.md` stating the inward-pointing dependency rule, why facts are established before an LLM sees them, and where each concern lives. The README leads with the wordmark, switched by `prefers-color-scheme`, and long-celled tables became prose.

## Refactoring

- `ChangelogPromptBuilder` is now a `partial` class split into `ChangelogPromptBuilder.Prompts.cs` (the prompt strings only — system header, the four rules, per-audience guidance) and `ChangelogPromptBuilder.cs` (the composition logic). Iterating on prompt wording is now text-only work in one file. The prompt text is byte-for-byte unchanged.

--- Customer ---
## New Features

- **Run metrics on every run.** Each `preview` and `generate` run now finishes with a summary of what it did and what it cost: how many times each check ran, how many findings each produced, and the tokens spent. One line highlights the claims that only the thorough check caught, alongside the tokens it took to catch them, so you can judge whether the thorough check is worth its cost. See `docs/run-metrics.md` for how to read it and decide whether to keep the thorough check on.

- **Configurable category presentation.** A new `categories` section in `chartula.yaml` lets you set the order categories appear in, their display names, and whether breaking changes are shown prominently (on by default). An unknown category name is reported with a clear error. Documented in `docs/configuration.md`.

- **Configuration from `chartula.yaml`.** The tool now reads settings from `chartula.yaml` (or `.yml`), while still running with sensible defaults when no file is present. A config file only refines behavior and is never required. Environment variables override file values. A shipped `chartula.example.yaml` gives you a minimal starting point to copy and uncomment. Invalid configuration values now produce a clear `Configuration error: ...` message instead of an unhandled crash. Full options are documented in `docs/configuration.md`.

- **`preview` and `generate` commands.** The CLI now offers `chartula preview` and `chartula generate`, each taking `--tag` and `--repo <owner/name>`. `generate` produces and writes the changelog outputs; `preview` runs the identical flow so you see the real result, but writes and publishes nothing. Both give a readable per-audience summary, a usage screen, and clear messages for unknown commands or missing options. Errors are reported rather than crashing.

- **All audience texts stored in `changelog.json`.** The customer and product-manager texts are now kept inside `changelog.json` in a new `renderings` field, rather than as separate marketing files in your repo. Documented in `docs/changelog-json.md`.

- **Release notes written back to GitHub.** The generated text is now written to the GitHub release's notes. Re-running for the same tag updates that release's notes in place rather than creating a duplicate.

- **`CHANGELOG.md` with preserved history.** Each release is written as a new section at the top of `CHANGELOG.md`, keeping existing content intact. Re-running the same release replaces its section in place, so running twice never duplicates or corrupts the file and never reorders history.

- **Opt-in review mode.** An optional review mode lets a maintainer review generated texts before publishing, with flagged passages highlighted. The reviewer can approve the text as-is or edit it before it's written. Review is off by default and never forced on a release.

- **Thorough second-pass faithfulness check.** A second, meaning-level check now catches subtle hallucinations the rule-based check can't see (for example, "bug fixed" rendered as "security hole closed"), flagging claims the fact base doesn't support. It's on by default and can be turned off with a single toggle (`Chartula:Faithfulness:Thorough`). When disabled or when there's nothing to check, it makes no LLM call.

- **Rule-based faithfulness check.** A no-cost check now runs before any LLM check to catch obvious hallucinations: numbers, quoted or backticked names, and breaking-change claims that aren't present in the fact base. It uses no LLM call, always runs, and surfaces passages for review rather than failing the run.

- **Consistent tone and formatting per audience.** Each rendering now reads as one coherent document regardless of how individual pull requests were written, with a single consistent voice and normalized formatting throughout.

- **Technical, customer, and PM versions from one source.** A release's technical, customer, and product-manager versions are now produced from a single fact base, so they can't contradict each other. The technical version keeps jargon, links, and precise breaking changes; the customer version is benefit-focused and omits changes that aren't user-visible; the product-manager version is grouped by theme. A failure in one version doesn't fail the others.

- **Trustworthy prompting.** The prompt architecture now pins the model to rephrasing the established facts only: it never introduces a fact, number, or name not in the list, treats each change's category and breaking marker as fixed, and stays brief on thin facts rather than padding or inventing detail.

- **Changelog generation through the provider interface.** Generation now works through a provider-agnostic interface, making exactly one call per release and no call at all for an empty fact base. Provider failures are handled gracefully and returned as a failed result rather than crashing.

- **Fact base written to `changelog.json`.** The release fact base is now written to `changelog.json` as a durable, machine-readable record. The format is versioned via `schemaVersion` (currently `1`), stable, documented in `docs/changelog-json.md`, and every field holds a deterministic fact.

- **Configurable fact-base depth.** You can now choose how much source material feeds the fact base via `Chartula:FactBase:Depth`: title only, title plus description (the default), or title plus description plus linked issues. An unknown value raises a clear error.

- **Release fact base assembly.** Curated changes are now assembled into a complete fact base for a release: each included change becomes one fact, with category and breaking flag from deterministic categorization (a label can force the category), user visibility derived from the category, and linked issues parsed from GitHub closing keywords. None of this comes from an LLM.

- **Fact-base data model.** A structured data model now captures the established facts for each change — title, PR number and link, category, user-visible and breaking flags, linked issues, and an optional description — as the single source of truth the LLM may only rephrase from. Nothing in it is LLM-generated, and it's serializable.

- **Internal and chore changes filtered by default.** Internal and chore changes are now dropped from the changelog by default, based on category and labels rather than guesswork. The excluded set is overridable in configuration (`Chartula:Filter:ExcludeCategories`). Breaking changes are never dropped, though an explicit label exclusion still takes precedence.

- **Label-driven curation from config.** GitHub labels can now steer curation from configuration (`Chartula:Labels`), with no code changes: a label can exclude a pull request, force it into a given category, or restrict the changelog to labeled pull requests only. All of this is optional — the tool works with no labels at all — and an unknown category name in the config fails at startup with a clear error.

- **Deterministic categorization.** Each change is now assigned a category in code before any generation, from Conventional Commit conventions in its title: Feature, Fix, Performance, Documentation, Refactor, Internal, or Other as the default for unrecognized titles. Breaking is tracked separately, so a breaking feature stays a feature but is still flagged. No LLM is involved.

- **Graceful degradation when clean PRs are missing.** The pipeline now still produces useful results when pull request discipline is imperfect: it falls back to commit data when there are no associated PRs, and to the best available source when PR titles are blank or uninformative. An empty release yields an empty result rather than an error, so the tool never hard-fails solely because PR discipline is imperfect.

- **Merged PRs fetched from the GitHub API.** Changes are now summarized per merged pull request rather than per raw commit. For the commits in a release, the associated merged PRs are retrieved, each yielding its title, description, labels, number, and link. API failures produce a clear error rather than a crash. A GitHub token is read from `GITHUB_TOKEN` and is optional for public repositories.

- **Release commit range read from git.** The tool now finds exactly the commits belonging to a release: the range since the previous tag, or all history up to the tag for a first release. Unknown or blank tags produce clear errors.

- **Provider-agnostic LLM support.** The LLM provider now sits behind a single interface the rest of the tool depends on, with Anthropic as the first provider. The model and provider are selectable via configuration, and API keys are read from the environment rather than hardcoded. Swapping providers is a configuration change only.

## Fixes

- **Truncated output fixed.** Generated text was being cut off mid-word because no output-token ceiling was being sent, causing the provider to fall back to a low default. The ceiling is now always sent, is configurable via `llm.maxOutputTokens`, and defaults to 16000. This also stops the truncation from being silently reported as a success and misread as a hallucinated claim.

- **False breaking-change labels fixed.** Prose that merely mentioned "BREAKING CHANGE" was being labelled a breaking change. Detection now matches only the proper Conventional Commits footer, so text discussing breaking changes no longer becomes one.

--- Product ---
## Changelog generation and the LLM seam

- Changelog generation now runs through a provider-agnostic interface (`IChangelogModel`), so the rest of the tool depends only on that interface and switching LLM providers is a composition-root change. API keys are read from environment/config, never hardcoded.
- Each release is generated with a single call per audience, and an empty fact base makes no call at all. Provider failures are returned as a failed result rather than crashing, and cancellation is respected.
- Added a first-class prompt architecture that pins the model to rephrasing established facts: it never introduces a fact, number, or name that isn't in the list, treats each fact's category and breaking marker as given, and stays brief when the facts are thin rather than padding or inventing.

## Rendering for multiple audiences

- A release now renders in three versions — technical, customer, and product-manager — all derived from one fact base, so they cannot contradict each other. A failure in one audience does not affect the others.
- Audience selection is deterministic: the customer version omits non-user-visible changes and their links, the technical version keeps links and the full change set, and the product-manager version sees the full set grouped by theme.
- Output is normalized for consistent formatting and tone within each rendering, regardless of how individual pull requests were written.

## Building the fact base

- Introduced the fact-base data model — one structured record per change capturing title, PR number, link, category, user-visible and breaking flags, and linked issues. Every field is derived deterministically; nothing in the model is LLM-generated.
- The fact base is assembled from curated changes: category and flags come from the deterministic curation step, linked issues are parsed from GitHub closing keywords, and user visibility is derived from the category (with every breaking change treated as user-visible).
- Fact-base depth is configurable in three modes — title only, title plus description (the default), or title, description, and linked issues — set via the `Chartula:FactBase:Depth` configuration key.

## Curation: categorization, labels, and filtering

- Each change is assigned a category deterministically before any LLM is involved, based on Conventional Commit conventions in the title, with an `Other` default for unrecognized titles. Breaking changes are tracked separately, so a breaking feature stays a feature but is still flagged.
- Label rules, read from configuration, let a maintainer steer curation without touching code: a label can exclude a change, force it into a given category, or restrict the changelog to labeled changes only. Labels are entirely optional — the tool works with none.
- Internal and chore changes are dropped by default, with the excluded set overridable in configuration. A breaking change is never dropped, even when its category would otherwise be excluded.

## Reading commits and pull requests

- Chartula reads the commit range for a release from git — the commits since the previous tag, or all history for a first release — with clear errors for unknown or blank tags.
- For that commit range, associated merged pull requests are fetched from the GitHub API, each yielding title, description, labels, number, and link, de-duplicated across commits. API failures produce a clear error rather than crashing.
- When pull request discipline is imperfect, the tool degrades gracefully: it falls back to commit data when no pull requests are associated, and to the best available source when a pull request title is blank or uninformative. It never hard-fails solely because of missing clean pull requests.

## Outputs

- The fact base is written to `changelog.json` as a durable, machine-readable record in a stable, versioned, documented format. All three audience texts — technical, customer, and product-manager — are stored inside that same file rather than as separate marketing files. Adding these audience texts is a non-breaking format change.
- Each release is written as a new section at the top of `CHANGELOG.md`, preserving existing history verbatim. Re-running the same release replaces its section in place, so running twice produces a byte-identical file.
- The generated text is also written back to the GitHub release notes. Because GitHub keys a release by its tag, re-running updates the existing release rather than creating a duplicate.

## Review and faithfulness checks

- An opt-in review mode lets a maintainer approve or edit generated texts before publishing, presenting each rendering with flagged passages highlighted. Review is off by default; when off, text passes straight through.
- A rule-based faithfulness check runs always, at zero token cost, catching obvious hallucinations: numbers, quoted or backticked names, or breaking-change claims not present in the fact base. Its flags are advisory.
- A thorough second-pass LLM check catches subtle, meaning-level distortions that the rule-based check cannot see. It is on by default and can be disabled with a single toggle; when off — or when there is nothing to check — it makes no LLM call.

## Run metrics

- Every `preview` and `generate` run now ends with a run-metrics summary reporting how many checks fired, how many claims were found, and the tokens each stage spent. A dedicated line pairs the claims that only the thorough check caught with the tokens it spent catching them, so the thorough check's keep-or-drop decision can be made from data. Measurement is a side channel: without a metrics sink, output is byte-identical.

## Command surface

- The CLI has two commands, `preview` and `generate`, each taking `--tag` and `--repo`. `generate` produces and writes all outputs; `preview` runs the identical flow but writes and publishes nothing. Both give a readable per-audience summary, and pipeline errors are reported clearly rather than crashing.

## Configuration

- Chartula reads `chartula.yaml` (or `.yml`) when present and works with sensible defaults when absent — configuration refines behavior but is never required. Environment variables override file values, and configuration errors are reported as a clear message rather than an unhandled exception. A minimal example file ships in the repo, with the full option set in the docs.
- Added a `categories` configuration section controlling category order, display names, and breaking-change prominence, alongside the existing sections. Each section is independently editable and untouched sections keep their defaults.

## Fixes

- Fixed generated audience texts being cut off mid-word: the output-token ceiling is now always sent, configurable via `llm.maxOutputTokens` and defaulting to 16000.
- Fixed changes being falsely marked as breaking when their body merely discussed breaking changes; the check now matches only a proper Conventional Commits footer.

## Documentation

- Brought the documentation in line with the shipped tool: corrected the usage instructions and runnable commands, added an architecture document explaining the layering and dependency choices, filled in all supported configuration sections in the example file, and linked the previously unreferenced `docs/` folder.

## Internal

- Extracted prompt text into a partial class so prompt strings live in one place, separate from the composition logic. The prompt text is unchanged.

Preview only - nothing was written or published.

Run metrics
  Rule-based check: 3 runs, 0 with findings, 0 claims, no tokens
  Thorough check:   3 runs, 0 with findings, 0 claims, 67,031 in / 69 out
    caught 0 claims the rule-based check missed, for 67,100 tokens in 3 calls
  Rephrasing:       3 calls, 54,874 in / 11,009 out
  Total:            132,983 tokens
