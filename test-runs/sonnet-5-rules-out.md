sonnet-5-rules-out, rendered by Chartula from v0.1.0

--- Technical ---

**Feature: Report what each run does and costs**
Every `preview` and `generate` run now closes with a run-metrics summary covering the rule-based check, the thorough check, and rephrasing, including run counts, findings, claims, and token usage. A dedicated line isolates the claims caught only by the thorough check against the tokens spent finding them, so the check's value versus its cost can be judged from real releases rather than assumption. Metrics are captured via a new `IRunMetrics` sink (with a `NullRunMetrics` no-op) and a `RunReport`/`RunReportFormatter` pair; the sink is optional throughout, so a run without one produces identical output. `docs/run-metrics.md` explains how to read the summary. Closes #26. (https://github.com/goldbarth/chartula/pull/66)

**Feature: Add a `categories` configuration section**
`chartula.yaml` gains a `categories` section controlling category order, display names, and breaking-change prominence (`order`, `names`, `breakingProminent`, defaulting to `true`). Unknown category names are rejected with a clear error. `CategorySettings` parsing lives in the domain, and audience filtering, ordering, and naming are consolidated into a new `GroundedFactsFactory`. Closes #25. (https://github.com/goldbarth/chartula/pull/65)

**Feature: Read `chartula.yaml` with sensible defaults**
The CLI now loads an optional `chartula.yaml` (or `.yml`), flattening it into configuration keys layered before environment variables, so env still overrides YAML. With no file and no environment variables, every option falls back to its default. A minimal `chartula.example.yaml` and `docs/configuration.md` document the full option set, and configuration errors now surface as a clear message instead of an unhandled exception. Closes #24. (https://github.com/goldbarth/chartula/pull/64)

**Feature: Wire `generate` and `preview` commands to the pipeline**
Adds `chartula preview` and `chartula generate`, each taking `--tag` and `--repo <owner/name>`, backed by a `ReleasePipeline` that runs the full flow — commit range, PRs, fact base, all-audience rendering, faithfulness checks, and review — before diverging only at the final write step. `generate` writes `changelog.json`, `CHANGELOG.md`, and the GitHub release notes; `preview` runs the same flow but writes and publishes nothing. Pipeline errors are caught and reported rather than crashed. Closes #23. (https://github.com/goldbarth/chartula/pull/63)

**Feature: Store all audience texts in `changelog.json`**
`changelog.json` now carries a `renderings` object keyed by audience (`technical`, `customer`, `product`), keeping generated texts in one durable file instead of separate marketing files. `schemaVersion` remains `1`, since the addition is optional and non-breaking for existing consumers. Closes #22. (https://github.com/goldbarth/chartula/pull/62)

**Feature: Write generated text to GitHub release notes**
Adds a `GitHubReleaseNotesWriter` that publishes the generated text to the release's actual notes via the GitHub REST API: an existing release is updated in place (`PATCH`), a missing one is created (`POST`). Re-running for the same tag updates rather than duplicates. The GitHub `HttpClient` setup is now shared with the PR reader via a `GitHubHttpClientFactory`. Closes #21. (https://github.com/goldbarth/chartula/pull/61)

**Feature: Write `CHANGELOG.md`, prepending and preserving history**
Each release is now written as a new section prepended to the top of `CHANGELOG.md`; existing sections are kept verbatim, and re-running the same tag replaces that section in place rather than duplicating it. A brand-new file gets a `# Changelog` title. Format logic lives in Core (`ChangelogMarkdownComposer`); file I/O lives in Infrastructure. Closes #20. (https://github.com/goldbarth/chartula/pull/60)

**Feature: Add opt-in review mode for human sign-off**
Introduces an `IReviewCoordinator` that gates each rendering behind an opt-in toggle: off by default (text passes through unreviewed), or on, sending the item to an `IReviewer` who approves or edits it. Flagged passages from both faithfulness checks are highlighted for the reviewer. An `AutoApproveReviewer` is the non-interactive default. Closes #19. (https://github.com/goldbarth/chartula/pull/59)

**Feature: Add a thorough second-pass faithfulness check**
Adds an `IThoroughFaithfulnessChecker` that runs a second LLM pass to catch meaning-level hallucinations the rule-based check can't see. Enabled by default via `Chartula:Faithfulness:Thorough`; when disabled, or when there's nothing to check, it makes no LLM call. The faithfulness prompt moves from an inline placeholder into the shared prompt builder. Closes #18. (https://github.com/goldbarth/chartula/pull/58)

**Feature: Add a rule-based check for obvious hallucinations**
Adds a zero-cost, always-on `IRuleBasedFaithfulnessChecker` that flags numbers, quoted/backticked names, and breaking-change claims not present in the fact base, before any LLM check runs. It has no model dependency, so it makes no LLM call. Flags are advisory, feeding review mode rather than failing a run. Closes #17. (https://github.com/goldbarth/chartula/pull/57)

**Feature: Enforce consistent formatting and tone per audience**
A deterministic `IChangelogFormatter` normalizes every rendering's line endings, bullet markers, trailing whitespace, and blank-line runs while leaving headings and prose intact, applied to all model output regardless of provider phrasing. A new prompt rule directs the model toward one consistent voice per audience rather than carrying over individual authors' tone. Closes #16. (https://github.com/goldbarth/chartula/pull/56)

**Feature: Render technical, customer, and PM audiences from one fact base**
Adds an `IReleaseRenderer` that produces technical, customer, and product-manager renderings from the same `FactBase`, so the three can never contradict each other; a failure in one audience does not fail the others. Customer omits non-user-visible changes and their links; technical keeps the pull request link and full change set; product sees the full set. Closes #15. (https://github.com/goldbarth/chartula/pull/55)

**Feature: Establish a prompt architecture that rephrases facts, never invents**
Replaces the placeholder prompt with an `IChangelogPromptBuilder` producing a system/user `ChangelogPrompt`. The system prompt pins the model to rephrasing only — never introducing facts, numbers, or names not in the list; treating category and breaking markers as established; staying brief on thin facts rather than padding; no preamble or conclusion — plus per-audience guidance. Categories and flags reach the model as text, not decisions it makes itself. Closes #14. (https://github.com/goldbarth/chartula/pull/53)

**Feature: Generate a changelog through the provider interface**
Adds an `IReleaseChangelogGenerator` that turns the fact base into grounded statements and makes exactly one `IChangelogModel.RephraseAsync` call per release; an empty fact base makes no call at all. Provider failures are caught and returned as a failed result rather than crashing, and cancellation propagates correctly. Closes #13. (https://github.com/goldbarth/chartula/pull/52)

**Feature: Write the fact base to `changelog.json`**
Adds a `ChangelogJsonSerializer` and `IChangelogJsonWriter` that write the release fact base to `changelog.json` as a durable, machine-readable record, kept as a stable on-disk shape separate from the evolving domain `FactBase`. `schemaVersion` (currently `1`) is the versioning contract; every field is a deterministic fact, none LLM-generated. Documented in `docs/changelog-json.md`. Closes #12. (https://github.com/goldbarth/chartula/pull/51)

**Feature: Make fact-base depth configurable**
Adds `FactBaseDepth` with three modes — title only, title and description (default), or title, description, and linked issues — set via `Chartula:FactBase:Depth`, so a maintainer can match the tool's source material to their team's PR style. An unknown depth value fails with a clear error. Closes #11. (https://github.com/goldbarth/chartula/pull/50)

**Feature: Transform curated changes into the release fact base**
Adds an `IFactBaseBuilder` that assembles the complete `FactBase` for a release: resolving changes with the missing-PR fallback, dropping filtered-out changes, and mapping each survivor to a `ChangeFact` with category, breaking flag, user-visibility, and linked issues all derived deterministically — no LLM involvement. Closes #10. (https://github.com/goldbarth/chartula/pull/49)

**Feature: Define the fact-base data model**
Adds `ChangeFact`, the structured, serializable object per change — title, PR number, link, category, user-visible flag, breaking flag, linked issues, and an optional description — that the LLM may only rephrase from. Every field is derived deterministically; PR-only fields are nullable so commit-based changes fit the same shape. Closes #9. (https://github.com/goldbarth/chartula/pull/48)

**Feature: Drop internal/chore changes by default**
Adds an `IChangeFilter` combining deterministic categorization and label rules: an excluding label always wins, a breaking change is never dropped, and otherwise a change is dropped when its effective category is in the excluded set (`Internal` by default, overridable via `Chartula:Filter:ExcludeCategories`). Closes #8. (https://github.com/goldbarth/chartula/pull/47)

**Feature: Steer curation with label rules from configuration**
Adds `LabelRules` and an `ILabelRulePolicy` letting a maintainer exclude labeled PRs, force a category via label, or restrict to only-labeled PRs, all configured under `Chartula:Labels` with case-insensitive matching. All of it is optional — `LabelRules.None` leaves labels out of the decision entirely. Closes #7. (https://github.com/goldbarth/chartula/pull/46)

**Feature: Assign categories deterministically before the LLM**
Adds `IChangeCategorizer`/`ConventionalCommitCategorizer`, reading Conventional Commit prefixes from the change title to assign `Feature`, `Fix`, `Performance`, `Documentation`, `Refactor`, `Internal`, or the `Other` default for unrecognized titles. Breaking status is tracked separately via a `!` marker, a `breaking` type, or a `BREAKING CHANGE` note, so category assignment happens purely in code, with no LLM call. Closes #6. (https://github.com/goldbarth/chartula/pull/45)

**Feature: Degrade gracefully when clean PRs are missing**
Adds `IReleaseChangeResolver`, mapping a commit range and merged PRs into `ReleaseChange` values with a fallback chain: one change per PR when PRs exist, per commit when none do, and a fallback to the PR body's first informative line (then a generic label) for blank or uninformative PR titles. An empty release yields an empty set rather than an error. Closes #5. (https://github.com/goldbarth/chartula/pull/44)

**Feature: Fetch merged PRs for a release from the GitHub API**
Adds `IReleasePullRequestReader`/`GitHubPullRequestReader`, querying GitHub's PRs-associated-with-a-commit endpoint for each commit in a range, keeping merged PRs only and de-duplicating by number. Built on a raw `HttpClient` with source-generated JSON for native-AOT friendliness; API and network failures raise a clear error rather than crashing. Closes #4. (https://github.com/goldbarth/chartula/pull/43)

**Feature: Read the commit range for a release from git**
Adds `IReleaseCommitReader`/`GitCliCommitReader`, shelling out to the `git` CLI to determine the commit range since the previous tag, or all history when there is no previous tag (first release). Introduces the `Chartula.Infrastructure` layer for concrete I/O adapters, keeping Core pure domain. Closes #3. (https://github.com/goldbarth/chartula/pull/42)

**Feature: Abstract the LLM provider behind `IChangelogModel`**
Adds the provider-agnostic seam the pipeline depends on: `IChangelogModel` (`RephraseAsync`, `CheckFaithfulnessAsync`) implemented by a single `ChatModel` backed by `Microsoft.Extensions.AI.IChatClient`. The composition root wires Anthropic as the first provider, with model, provider, and API key all read from configuration/environment rather than hardcoded. Closes #2. (https://github.com/goldbarth/chartula/pull/41)

**Fix: Two release blockers found by dogfooding v0.1.0**
`ChatModel` sent no `MaxOutputTokens`, so the provider silently applied its own 1024-token default and truncated all three audience texts mid-word; the thorough check then flagged the severed sentence as an unsupported claim rather than the truncation being visible as a bug. The output ceiling is now always sent, configurable via `llm.maxOutputTokens` (default 16000). Separately, `ConventionalCommitCategorizer` matched `BREAKING CHANGE` as a case-insensitive substring anywhere in the body, mislabelling prose that merely discussed breaking changes as breaking; it now matches only the Conventional Commits footer format. Both fixes were confirmed against a real run rather than tests alone. A related issue in `RuleBasedFaithfulnessChecker`, which flags the word "breaking" anywhere in output regardless of whether it forms an actual claim, is filed separately rather than rushed into this fix. (https://github.com/goldbarth/chartula/pull/70)

**Documentation: Bring the docs up to what Chartula actually is**
Corrects documentation that still described a planned project rather than the completed Phase 1: `Usage` now shows runnable commands with their required `--tag` and `--repo` options; the `docs/` folder is linked from the README; `chartula.example.yaml` now shows all eight supported sections instead of four; the status badge and CONTRIBUTING's SDK requirement and commit-scope list are corrected to match reality. Adds `docs/architecture.md` covering the layering and dependency reasoning. Long two-column tables in the README were converted to prose for readability on narrow screens. (https://github.com/goldbarth/chartula/pull/69)

**Refactor: Move prompt text into a partial class**
Splits `ChangelogPromptBuilder` into a partial class: prompt strings (system header, rules, per-audience guidance) live in `ChangelogPromptBuilder.Prompts.cs`, separate from the composition logic in `ChangelogPromptBuilder.cs`. The prompt text itself is unchanged, so existing prompt-content tests pass unmodified. (https://github.com/goldbarth/chartula/pull/54)

--- Customer ---

---
title: Release 0.1.0
description: This release introduces Chartula, a command-line tool that turns your commits, pull requests, and labels into checked, audience-specific release changelogs and publishes them to `CHANGELOG.md`, `changelog.json`, and your GitHub release notes.
publishedAt: 2026-07-17
---

### What needs action

- **LLM API key required**: `chartula preview` and `chartula generate` call an LLM provider to write the text, so both need an API key. Set the key as an environment variable before running either command; the provider and model themselves are configured separately.

### What's New

- **Commands**: `chartula preview --tag <tag> --repo <owner/name>` and `chartula generate --tag <tag> --repo <owner/name>` are now available. Preview runs the full process and shows what would be produced without writing or publishing anything, while generate writes `changelog.json`, updates `CHANGELOG.md`, and updates the GitHub release notes; running with no arguments shows a usage screen, and missing or invalid options produce a clear error instead of a crash.
- **changelog.json facts**: Each release now produces a `changelog.json` file recording the deterministic facts about every change — title, category, breaking status, and linked issues — in a versioned format. The version number lets other tools detect format changes safely, so new optional fields added later won't break anything already reading the file.
- **changelog.json renderings**: The `changelog.json` file also stores the generated technical, customer, and product-manager text for the release, alongside the facts. Everything for a release now lives in one file instead of scattered outputs.
- **CHANGELOG.md**: Running `generate` writes a `CHANGELOG.md` file, adding each release as a new section at the top. Earlier sections are kept untouched, and re-running for the same release replaces just that section instead of duplicating it.
- **GitHub release notes**: Running `generate` also publishes the generated text to the release's notes on GitHub. Re-running for the same tag updates that release's notes in place rather than creating a duplicate release.
- **Audience-specific text**: Every release now produces three versions of its changelog from the same set of facts: technical, customer, and product-manager. The customer version leaves out internal-only changes and their links, the technical version keeps full detail and links, and the product-manager version groups changes by theme, so the three can never contradict each other.
- **Consistent formatting**: Generated changelog text is now formatted consistently, with a single bullet style and no stray blank lines, and written in one voice regardless of how the original pull requests were worded. Each rendering reads as one coherent document rather than a patchwork of styles.
- **Rule-based accuracy check**: A free, always-on check now looks at the generated text for obviously invented details — numbers, quoted or backticked names, or breaking-change claims — that don't appear in the underlying facts. These flags don't stop a run; they're advisory and feed into review mode when it's turned on.
- **Thorough accuracy check**: A second, more careful check now reviews the generated text against the source facts for subtler errors, such as a fix being reworded into something it wasn't. It's on by default and can be turned off in the faithfulness section of `chartula.yaml`.
- **Review mode**: An opt-in review mode lets you see each generated text together with any flagged passages, and approve it as-is or edit it before anything is written. It's off by default and can be turned on in the review section of `chartula.yaml`.
- **Run metrics**: Every `preview` and `generate` run now ends with a summary of what each check did and what it cost, including how many tokens the thorough check spent on claims that only it caught. You can use this to judge whether the thorough check is worth keeping.
- **Configuration file**: A `chartula.yaml` (or `.yml`) file can now be created to customize behaviour — including the LLM provider, GitHub access, labels, filtering, fact-base depth, faithfulness checks, and review — while the tool still runs with sensible defaults if the file is absent. Environment variables always override values from the file, and an example file, `chartula.example.yaml`, is provided to copy from.
- **Category display**: A categories section in `chartula.yaml` lets you set the order and display names for change categories, and whether breaking changes are shown prominently, which is on by default.
- **Fact-base depth**: You can control how much source material feeds each change's description — title only, title plus pull request description (the default), or title, description, and linked issues. This is set in the factBase section of `chartula.yaml`.
- **Filtering internal changes**: Internal and chore-type changes, such as build, CI, or test-only commits, are now left out of the changelog by default. Breaking changes are never left out even if their category is normally excluded, and the excluded categories can be changed in the filter section of `chartula.yaml`.
- **Label-based curation**: A label on a pull request can now exclude it from the changelog, force it into a specific category, or, if you choose, restrict the changelog to only labeled pull requests. This is optional and configured in the labels section of `chartula.yaml`; with no labels set, nothing changes.
- **Automatic categorization**: Each change is automatically placed into a category — feature, fix, performance, documentation, refactor, internal, or other — based on a Conventional Commits-style title such as `feat:` or `fix:`, with unrecognized titles falling under "other". Whether a change is breaking is tracked separately, so a breaking feature still shows as a feature but is flagged as breaking too.
- **Fallback to commit data**: If a release has no linked pull requests, or a pull request has a blank or uninformative title like "WIP" or "update", the changelog entry still gets usable content. It falls back to the commit message or the pull request's description, so a change is never skipped for that reason.
- **GitHub authentication**: You can supply a GitHub token via an environment variable named `GITHUB_TOKEN` so chartula can read pull requests without hitting anonymous rate limits. This is optional — public repositories work without a token, just subject to GitHub's standard rate limits.
- Also: generated text is built only from the established facts about your changes and will not invent numbers, names, or details that aren't present in your commits, pull requests, or issues, even when the source material is thin.

### What's Changed

- Configuration errors — such as an invalid category name, label category, filter category, or fact-base depth value — now show a clear "Configuration error: ..." message and stop the run, instead of crashing with an unhandled exception. You can immediately see what needs fixing without digging through a stack trace.

### Bug Fixes

- Generated text no longer gets cut off mid-sentence in any of the three audience versions. The token limit sent to the model now defaults to a much larger value, and you can adjust it via `llm.maxOutputTokens` in `chartula.yaml` if you need to.
- Changes are no longer marked as breaking just because their description mentions the phrase "breaking change" in ordinary text. Only a properly formatted `BREAKING CHANGE:` footer, as used by Conventional Commits, marks a change as breaking now, so unrelated mentions no longer produce false breaking-change labels.

--- Product ---

## Run Metrics & Cost Visibility

- Feature: Every `preview` and `generate` run now ends with a metrics summary showing how many checks ran, how many findings and claims they produced, and the token cost of each step — so the value of the thorough check can be weighed against what it costs.

## Configuration

- Feature: A `chartula.yaml` file lets you refine Chartula's behavior; the tool still runs with sensible defaults when no file or settings are present.
- Feature: A new `categories` configuration section controls category order, display names, and whether breaking changes are shown prominently.
- Feature: Internal/chore changes are now excluded from the changelog by default, with the excluded categories overridable in configuration.
- Feature: Label rules let you steer curation directly from GitHub labels — excluding a change, forcing its category, or restricting output to only labeled changes — all optional.
- Feature: How much source material feeds each change (title only, title and description, or title, description and linked issues) is now configurable, defaulting to title and description.

## Faithfulness & Review

- Feature: A free, always-on rule-based check flags obvious hallucinations — invented numbers, invented names, or unsupported breaking-change claims — before any LLM check runs.
- Feature: An optional second-pass LLM check catches subtler hallucinations the rule-based check misses, such as a fix rendered as something more dramatic than it was. Enabled by default, with a single toggle to turn it off.
- Feature: An opt-in review mode lets a maintainer see flagged passages alongside the generated text and approve or edit it before anything is published.

## Output & Publishing

- Feature: All three audience texts (technical, customer, and product-manager) are now stored inside `changelog.json` alongside the underlying facts, rather than as separate files.
- Feature: Each release is now written as a new section at the top of `CHANGELOG.md`, with prior history preserved and safe re-running for the same release.
- Feature: Generated release text can now be written directly to a GitHub release's notes, creating a new release or updating the existing one for the same tag.

## Rendering & Generation

- Feature: Chartula's LLM connection is provider-agnostic, so a provider can be swapped without affecting the rest of the tool; Anthropic is the first supported provider.
- Feature: Chartula now generates release text through a live LLM connection, working only from the established facts of a release.
- Feature: A structured prompting approach ensures the model only rephrases established facts — never inventing numbers, names, or categories — and stays brief when the facts are thin.
- Feature: Technical, customer, and product-manager versions of a release are now all rendered from the same set of facts, so they can never contradict each other.
- Feature: Generated text is now formatted and toned consistently across a release, regardless of how the original pull requests were written.

## Core Pipeline (Facts & Curation)

- Feature: Chartula can now read the exact commit range belonging to a release directly from git, including the first release with no prior tag.
- Feature: Chartula can now fetch merged pull requests for a release from GitHub, summarizing by pull request rather than by raw commit.
- Feature: When pull request data is missing or unhelpfully titled, Chartula now falls back gracefully to commit data or the pull request description instead of failing.
- Feature: Each change is now assigned a category (feature, fix, performance, docs, refactor, internal, or other) automatically from conventional commit conventions, with breaking changes flagged separately.
- Feature: A structured fact model now captures every established detail of a change — title, number, link, category, visibility, breaking flag, and linked issues — as the single source of truth for generation.
- Feature: Curated changes are now assembled into a complete, structured fact base for each release, combining categorization, labels, and filtering.

## CLI

- Feature: Chartula now has `preview` and `generate` commands; both produce the full release output, but `preview` shows the result without writing or publishing anything.

## Fixes

- Fix: Fixed a bug where release text could be silently cut off mid-sentence because no output length limit was set; a limit is now always applied and is configurable.
- Fix: Fixed a bug where prose merely discussing breaking changes could be mislabeled as a breaking change itself; detection now matches only genuine breaking-change declarations.

## Documentation

- Documentation: Updated the README and contributing guide, and added a new architecture document, to reflect what Chartula actually is and does, including a full walkthrough of configuration and setup.

## Internal

- Refactor: Reorganized how prompt wording is stored internally, separating prompt text from the logic that assembles it, with no change in behavior.
