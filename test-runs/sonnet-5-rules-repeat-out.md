sonnet-5-rules-repeat-out, rendered by Chartula from v0.1.0

--- Technical ---

**Feature — Report what a run does and what it costs**
Every `preview` and `generate` run now ends with a run-metrics summary covering rule-based checks, the thorough check, and rephrasing, including run counts, findings, claims, and token usage. The summary's key line isolates the claims caught only by the thorough check against the tokens spent catching them, so the check's value can be judged from real releases rather than assumed. Implemented via `IRunMetrics`/`RunMetrics`/`NullRunMetrics`/`RunReport`/`RunReportFormatter` in `Chartula.Core/Observability/`; `ChatModel` attributes token usage per `LlmOperation`; `ReleasePipeline` records both checks' findings in one place and exposes the report on `ReleaseOutcome`. The metrics sink is optional throughout, and a run without one is byte-identical to one with it. Documented in `docs/run-metrics.md`. Build clean; 215 tests passing (Core 177, Infrastructure 26, Cli 12), 21 new. Closes #26. (https://github.com/goldbarth/chartula/pull/66)

**Feature — Add configuration sections for categories**
Adds a `categories` configuration section (`order`, `names`, `breakingProminent`, default `true`) alongside the existing `labels`, `factBase`, and `faithfulness` sections. `CategorySettings.From(...)` parses these values and rejects unknown category names with a clear error. `GroundedFactsFactory` is extracted from `ReleaseChangelogGenerator` to hold audience filtering, category ordering, and display naming in one place. Sections remain independently configurable; untouched ones keep their defaults. Documented in `docs/configuration.md`. Build clean; 194 tests passing (Core 158, Infrastructure 26, Cli 10), 17 new. Closes #25. (https://github.com/goldbarth/chartula/pull/65)

**Feature — Read chartula.yaml with sensible defaults**
Adds `AddChartulaYaml`, which loads `chartula.yaml`/`.yml` via YamlDotNet and flattens it into `Chartula:*` configuration keys, layered before environment variables (env overrides YAML). Covers all existing sections (`llm`, `github`, `labels`, `filter`, `factBase`, `faithfulness`, `review`); with no file and no env vars, every option falls back to its default. Ships a minimal, fully commented `chartula.example.yaml`; full option reference in `docs/configuration.md`. Configuration errors now surface as a clear `Configuration error: ...` message instead of an unhandled exception. Adds the `Chartula.Cli.Tests` project. Build clean; tests passing (Core 147, Infrastructure 26, Cli 5). Closes #24. (https://github.com/goldbarth/chartula/pull/64)

**Feature — Wire generate and preview commands to the pipeline**
`ReleasePipeline` orchestrates the full flow through ports only: read commit range and PRs, build the fact base, render all audiences, run faithfulness checks and review, then write outputs. `chartula generate` writes `changelog.json`, `CHANGELOG.md`, and GitHub release notes; `chartula preview` runs the identical flow but writes and publishes nothing. Both commands take `--tag` and `--repo <owner/name>`, with a usage screen and clear error handling for unknown commands, missing options, and pipeline failures. `--repo` is explicit for now; the interactive console reviewer is not yet wired in. Build clean; tests passing (Core 147, Infrastructure 26). Closes #23. (https://github.com/goldbarth/chartula/pull/63)

**Feature — Store all audience texts in changelog.json**
`ChangelogDocument` gains a `renderings` object keyed by audience (`technical`, `customer`, `product`) in a fixed order; `ChangelogJsonSerializer.Serialize` and `IChangelogJsonWriter` accept an optional renderings map, defaulting to an empty object when none is given. Change entries remain deterministic facts; only the renderings are LLM-produced text. No separate marketing files are written. `schemaVersion` stays at 1, since adding an optional field is non-breaking. Documented in `docs/changelog-json.md`. Build clean; 144 tests passing (Core 144, Infrastructure 26). Closes #22. (https://github.com/goldbarth/chartula/pull/62)

**Feature — Write generated text back to GitHub release notes**
Adds `IReleaseNotesWriter` and `GitHubReleaseNotesWriter`, which check for an existing release by tag (`GET /releases/tags/{tag}`) and either update it in place (`PATCH /releases/{id}`) or create a new one (`POST /releases`), returning the release's `html_url`. Built on plain `HttpClient` with source-generated JSON for AOT compatibility. API and network failures raise a clear `InvalidOperationException`. Since GitHub keys releases by tag, re-running for the same tag updates rather than duplicates. The GitHub `HttpClient` setup is now shared with the PR reader via `GitHubHttpClientFactory`. Build clean; tests passing (Core 141, Infrastructure 24). Closes #21. (https://github.com/goldbarth/chartula/pull/61)

**Feature — Write CHANGELOG.md, prepend and preserve history**
`ChangelogMarkdownComposer` prepends each new release section at the top of `CHANGELOG.md`, keeps existing sections verbatim, and replaces a re-run of the same tag's section in place rather than duplicating it; a new file gets a `# Changelog` title. `IChangelogMarkdownWriter`/`FileChangelogMarkdownWriter` handle the file I/O, following the same Core/Infrastructure split as `changelog.json`. Running the same release twice produces a byte-identical file. Build clean; tests passing (Core 141, Infrastructure 19). Closes #20. (https://github.com/goldbarth/chartula/pull/60)

**Feature — Opt-in review mode for human sign-off of flagged passages**
Adds `IReviewCoordinator`/`ReviewCoordinator`, gating each rendering on an opt-in toggle. With review off (default), text passes through unreviewed; with it on, an `IReviewer` approves as-is or returns an edited version via `ReviewDecision`. `ReviewPresentation` shows a maintainer the generated text alongside flagged passages from both faithfulness checks. `AutoApproveReviewer` is the non-interactive default; an interactive console reviewer ships separately with the CLI. Bound via the `Chartula:Review` configuration toggle. Build clean; tests passing (Core 134, Infrastructure 16). Closes #19. (https://github.com/goldbarth/chartula/pull/59)

**Feature — Thorough second-pass LLM check with a toggle**
Adds `IThoroughFaithfulnessChecker`/`ThoroughFaithfulnessChecker`, a second LLM pass that turns the fact base into grounded facts and flags unsupported claims, catching meaning-level hallucinations the rule-based check misses. Enabled by default via `ThoroughFaithfulnessOptions`, disabled with `Chartula:Faithfulness:Thorough`; when off, or when there's nothing to check, it returns a faithful report with no LLM call. The faithfulness prompt moves from an inline placeholder in `ChatModel` into `IChangelogPromptBuilder.BuildFaithfulnessPrompt`. Removing the toggle or adding finer-grained settings is deferred pending observability data. Build clean; tests passing (Core 128, Infrastructure 16). Closes #18. (https://github.com/goldbarth/chartula/pull/58)

**Feature — Rule-based check that catches obvious hallucinations**
Adds `IRuleBasedFaithfulnessChecker`/`RuleBasedFaithfulnessChecker`, which compares generated output against the fact base and flags numbers not present in the facts, quoted or backticked names absent from the facts, and breaking-change claims with no corresponding breaking fact. Findings are advisory, feeding review mode rather than failing the run. Has no `IChangelogModel` dependency, so it costs zero tokens and always runs. Uses source-generated regexes for AOT compatibility. Build clean; tests passing (Core 122, Infrastructure 16). Closes #17. (https://github.com/goldbarth/chartula/pull/57)

**Feature — Consistent formatting and tone per audience**
`IChangelogFormatter`/`ChangelogFormatter` normalizes model output deterministically — consistent line endings, a single bullet marker, trimmed trailing whitespace, collapsed blank-line runs — while leaving headings and prose intact, applied to every rendering. A new prompt rule instructs the model to write in one consistent voice and format, without carrying over an individual author's tone. Formatting is enforced in code for testability; tone normalization is handled via the prompt. Build clean; tests passing (Core 114, Infrastructure 16). Closes #16. (https://github.com/goldbarth/chartula/pull/56)

**Feature — Render technical, customer, and PM versions from one fact base**
`IReleaseRenderer`/`ReleaseRenderer` renders all three audiences from the same `FactBase`, one generator call per audience, so the renderings can never contradict each other; a failure in one audience doesn't affect the others. Audience selection is deterministic: customer omits non-user-visible changes and their links; technical keeps the pull request link and full change set; product sees the full set. Prompt guidance updated accordingly (technical keeps links, customer is benefit-focused, PM groups by theme). Build clean; tests passing (Core 105, Infrastructure 16). Closes #15. (https://github.com/goldbarth/chartula/pull/55)

**Feature — Prompt architecture that rephrases facts, never invents**
`IChangelogPromptBuilder`/`ChangelogPromptBuilder` produce a `ChangelogPrompt` (system + user). The system prompt pins the model to rephrasing only: never introduce a fact, number, or name absent from the list; treat each fact's category and breaking marker as established; stay brief on thin facts rather than padding or speculating; no preamble or conclusion — plus per-audience guidance. The user prompt carries only the facts. Categories and flags reach the model as text from deterministic curation and are presented verbatim, not decided by the model. `ChatModel` now delegates prompt construction to the builder. Build clean; tests passing (Core 100, Infrastructure 16). Closes #14. (https://github.com/goldbarth/chartula/pull/53)

**Feature — Generate a changelog through the provider interface**
`IReleaseChangelogGenerator`/`ReleaseChangelogGenerator` turn the fact base into grounded fact statements and make exactly one `IChangelogModel.RephraseAsync` call per release; an empty fact base makes no call at all. Provider failures are caught and returned as a failed `ChangelogGenerationResult` carrying the release tag and provider message; cancellation propagates rather than being swallowed. The generator depends only on `IChangelogModel`, with no provider-specific reference. Build clean; tests passing (Core 89, Infrastructure 16). Closes #13. (https://github.com/goldbarth/chartula/pull/52)

**Feature — Write the fact base to changelog.json**
`ChangelogDocument` defines the stable on-disk shape (`schemaVersion`, `tag`, `changes`), kept separate from the domain `FactBase` so the domain can evolve independently. `ChangelogJsonSerializer` converts `FactBase` to and from JSON deterministically, using source generation for AOT/trim safety, with categories written as names. `IChangelogJsonWriter`/`FileChangelogJsonWriter` handle the file I/O. `schemaVersion` (currently 1) is the stability contract: optional additions are non-breaking, while removals, renames, or re-meanings bump the version. Documented in `docs/changelog-json.md`. Build clean; tests passing (Core 84, Infrastructure 16). Closes #12. (https://github.com/goldbarth/chartula/pull/51)

**Feature — Make fact-base depth configurable**
Adds `FactBaseDepth` with three modes — `TitleOnly`, `TitleAndDescription` (the default), and `TitleDescriptionAndIssues` — plus `FactBaseDepthParser`. `FactBaseBuilder` honors the selected depth, including description from the middle mode up and linked issues only at the deepest mode. Set via `Chartula:FactBase:Depth`, with the parser accepting canonical names and aliases (`title`, `description`, `full`) and raising a clear error on an unknown value. Whether all three modes persist long-term is left for later, data-driven review. Build clean; tests passing (Core 79, Infrastructure 12). Closes #11. (https://github.com/goldbarth/chartula/pull/50)

**Feature — Transform curated changes into the release fact base**
`IFactBaseBuilder`/`FactBaseBuilder` assemble the `FactBase` container (tag plus one `ChangeFact` per included change), resolving changes via the missing-PR fallback, dropping filtered-out changes, and mapping each survivor to a `ChangeFact`. Category and breaking flag come from deterministic categorization, with label overrides taking precedence. `IsUserVisible` is derived from category and breaking status; `LinkedIssues` are parsed from GitHub closing keywords in title and body. The builder has no LLM dependency. Build clean; tests passing (Core 64, Infrastructure 12). Closes #10. (https://github.com/goldbarth/chartula/pull/49)

**Feature — Define the fact-base data model**
Defines `ChangeFact`, a structured, serializable object per change holding title, PR number, link, category, user-visible flag, breaking flag, linked issues, and an optional description populated per fact-base depth. Every field is derived deterministically; nothing in the model is LLM-generated. PR-only fields are nullable so commit-based changes fit the same shape. Build clean; tests passing (Core 58, Infrastructure 12). Closes #9. (https://github.com/goldbarth/chartula/pull/48)

**Feature — Drop internal/chore changes by default**
`IChangeFilter`/`ChangeFilter` and `ChangeFilterRules` combine label rules and deterministic categorization: an excluding label wins outright, a breaking change is never dropped, and otherwise a change is dropped when its effective category is in the excluded set (default: `Internal`, overridable via `Chartula:Filter:ExcludeCategories`). The breaking-change safeguard is deterministic, derived from the breaking flag rather than guesswork, and an explicit label exclusion still overrides it. Build clean; tests passing (Core 55, Infrastructure 12). Closes #8. (https://github.com/goldbarth/chartula/pull/47)

**Feature — Steer curation with label rules from config**
`LabelRules` (excluded labels, label-to-category overrides, only-include-labeled mode) and `ILabelRulePolicy`/`LabelRulePolicy` produce a `LabelDecision`, with precedence: exclusion first, then only-labeled filtering, then the first matching label's forced category. All behavior is optional — `LabelRules.None` disables label handling entirely — and matching is case-insensitive. Bound from `Chartula:Labels` via `LabelRules.From`, which rejects unknown category names with a clear error. Build clean; tests passing (Core 41, Infrastructure 12). Closes #7. (https://github.com/goldbarth/chartula/pull/46)

**Feature — Assign categories deterministically before the LLM**
`IChangeCategorizer`/`ConventionalCommitCategorizer` read Conventional Commit conventions from the change title to assign `ChangeCategory` (Feature, Fix, Performance, Documentation, Refactor, Internal, or Other as the default for unrecognized titles). Breaking status is tracked separately via `ChangeClassification.IsBreaking`, so a breaking feature keeps its category while still being flagged. Pure, deterministic, no LLM or I/O involved; uses a source-generated regex. Build clean; tests passing (Core 33, Infrastructure 12). Closes #6. (https://github.com/goldbarth/chartula/pull/45)

**Feature — Degrade gracefully when clean PRs are missing**
`IReleaseChangeResolver`/`ReleaseChangeResolver` turn a `CommitRange` and merged `PullRequestInfo` list into `ReleaseChange` values. When merged PRs exist, each becomes one change; with none, each commit becomes one change via its subject. Blank or uninformative PR titles fall back to the PR body's first informative line, then to a generic `PR #n`. An empty release yields an empty set rather than an exception. The uninformative-title heuristic is a small starter set, to be made configurable later. Build clean; tests passing (Core 13, Infrastructure 12). Closes #5. (https://github.com/goldbarth/chartula/pull/44)

**Feature — Fetch merged PRs for a release from the GitHub API**
`IReleasePullRequestReader`, `PullRequestInfo`, and `RepositoryCoordinates` define the domain seam; `GitHubPullRequestReader` queries GitHub's "pull requests associated with a commit" endpoint for each commit in a `CommitRange`, keeping merged PRs only and de-duplicating by number, via raw `HttpClient` and source-generated JSON rather than Octokit, for dependency-light native-AOT compatibility. The composition root configures the `HttpClient` and an optional bearer token by environment-variable name; API failures raise a clear `InvalidOperationException`. Build clean; tests passing (Core 5, Infrastructure 12). Fallback for missing clean PRs is handled separately. Closes #4. (https://github.com/goldbarth/chartula/pull/43)

**Feature — Read the commit range for a release from git**
`IReleaseCommitReader`, `CommitInfo`, and `CommitRange` (with `IsFirstRelease`) define the domain seam; `GitCliCommitReader` shells out to the `git` CLI to compute the range since the previous tag, or all history when there is none, in the new `Chartula.Infrastructure` layer. Chosen over LibGit2Sharp to avoid native dependencies that would conflict with the planned native-AOT goal. Tests run against real, throwaway git repositories, deterministic and offline. Build clean; tests passing (Core 5, Infrastructure 6). Closes #3. (https://github.com/goldbarth/chartula/pull/42)

**Feature — Abstract the LLM provider behind IChangelogModel**
`IChangelogModel` defines the pipeline-facing LLM operations (`RephraseAsync`, `CheckFaithfulnessAsync`), implemented by `ChatModel` over a provider-agnostic `Microsoft.Extensions.AI.IChatClient`, alongside domain types `Audience`, `GroundedFacts`, `RephraseRequest`, `FaithfulnessRequest`, and `FaithfulnessReport`. The composition root wires Anthropic as the first provider, with model and provider selectable via configuration and API keys read from environment/config, never hardcoded. Swapping providers is a composition-root-only change. Tests exercise the seam with a stub `IChatClient`, no live provider call. Build clean; 5/5 tests passing. Closes #2. (https://github.com/goldbarth/chartula/pull/41)

**Fix — Two release blockers found by dogfooding v0.1.0**
Found while running `chartula preview --tag v0.1.0` against this repository; neither bug was reachable by existing tests.

`ChatModel` sent calls without `ChatOptions`, so `MaxOutputTokens` was never set and the provider silently applied its own default of 1024, truncating all three audience texts mid-word — visible in the run metrics as 3 calls totaling 3,072 output tokens. The run reported success, and the thorough check spent 56,712 tokens flagging the severed sentence as an unsupported claim, a truncation bug read as a hallucination. The output ceiling is now always sent, configurable via `llm.maxOutputTokens`, defaulting to 16000.

`ConventionalCommitCategorizer`'s `MentionsBreakingChange` matched `BREAKING CHANGE` as a case-insensitive substring anywhere in the body, so prose discussing breaking changes was misread as declaring one — six of thirty-three v0.1.0 changes were mislabelled as breaking, none of which were. It now matches only the Conventional Commits footer format: uppercase, start of line, colon-terminated.

Verified against a real run: rephrasing output rose from 3,072 to 11,271 tokens with complete sentences instead of mid-word cuts; breaking changes reported dropped from 6 to 0; thorough-check claims dropped from 1 to 0. 265 tests passing, 9 new, including a regression test using the exact sentence that triggered the false positive.

A related issue remains open: `RuleBasedFaithfulnessChecker` still matches `\bbreaking\b` anywhere in the output and flags a breaking-change claim whenever the word appears, the same phrase-versus-assertion confusion, now visible since no fact is breaking. These flags are advisory and don't fail a run; distinguishing a claim from prose using the word needs more than a regex, and is filed separately. (https://github.com/goldbarth/chartula/pull/70)

**Documentation — Bring the docs up to what Chartula actually is**
With Phase 1 complete, the documentation still described a project still being planned. `Usage` called the commands "planned entry points" and omitted the required `--tag`/`--repo` flags; the `docs/` folder existed but was linked from nowhere; `chartula.example.yaml` showed 4 of the 8 supported sections, missing `github`, `labels`, `categories`, and `review`; the status badge read "early development" despite all 27 Phase 1 issues being closed; and `CONTRIBUTING` asked for an unspecified .NET SDK version (an older one cannot build `net10.0`) and documented four unused commit scopes while omitting the sixteen actually in use.

Adds a theme-aware wordmark to the README via `<picture>` and `prefers-color-scheme`; converts long, two-column tables (`Why Chartula`, `Core ideas`, `Roadmap`) to prose and headings for readability on narrow screens, keeping tables only for short facts like env vars and the doc index; adds `docs/architecture.md`, covering the layering, the inward-pointing dependency rule, why facts are established before an LLM sees them, and where each concern lives — previously undocumented, risking an unintentional reach for LibGit2Sharp or Octokit and a quiet loss of the native-AOT goal; and links all documentation from the README index and from CONTRIBUTING.

Verified: all 24 relative links across `README.md`, `CONTRIBUTING.md`, and `docs/*.md` resolve; both SVGs validated as external-reference-free, script-free XML and checked rendered on light and dark backgrounds; every section of `chartula.example.yaml` uncommented into a real `chartula.yaml` and run through the CLI, binding cleanly across all eight sections; every documented default checked against the code. Build clean; 256 tests passing. (https://github.com/goldbarth/chartula/pull/69)

**Refactor — Move prompt text into a partial class**
Splits `ChangelogPromptBuilder` into a partial class: `ChangelogPromptBuilder.Prompts.cs` holds the prompt strings only (system header, the four rules, per-audience guidance), while `ChangelogPromptBuilder.cs` holds the composition logic that references them, so prompt wording can be edited without navigating composition code. The prompt text is unchanged byte-for-byte; existing prompt-content assertions pass unmodified, confirming no behavior change. Build clean; tests passing and unchanged (Core 100, Infrastructure 16). (https://github.com/goldbarth/chartula/pull/54)

--- Customer ---

---
title: Release 0.1.0
description: This release introduces Chartula end to end — turning GitHub pull requests and commits into version-controlled, multi-audience release notes with built-in accuracy checks — and fixes two issues found while dogfooding it on its own first release.
publishedAt: 2026-07-17
---

### What needs action

- **LLM provider setup**: Generating or previewing a changelog calls out to your configured AI provider (Anthropic to start). You can rely on no credentials ever being hardcoded; provide your provider's API key through the environment variable named in your configuration, and choose the model and provider there as well.

### What's New

- **Category display settings**: The categories section of your chartula.yaml file now lets you set the order categories appear in, their display names, and whether breaking changes are called out prominently (on by default). An unrecognized category name there is rejected at startup with a clear error listing the valid options.
- **Config file support**: Chartula now reads settings from a chartula.yaml (or .yml) file in your project, with every option falling back to a sensible default when the file or a setting is missing. Copy the shipped chartula.example.yaml and uncomment what you need; environment variables still override anything set in the file, and an invalid value produces a clear configuration error instead of a crash.
- **Fact detail depth**: You can choose how much of each pull request feeds the changelog — title only, title and description (the default), or title, description, and linked issues. Set this as depth (title, description, or full) in the factBase section of your chartula.yaml.
- **Excluding categories from the changelog**: Internal and chore-type changes are left out of the changelog by default. Change which categories are excluded by setting excludeCategories in the filter section of chartula.yaml; breaking changes are never excluded, no matter what.
- **Label-based rules**: You can use GitHub labels to exclude specific pull requests, force one into a particular category, or restrict the changelog to only labeled pull requests. Set these rules in the labels section of chartula.yaml; matching is case-insensitive, and leaving the section out means labels are ignored entirely.
- **Thorough hallucination check toggle**: A second, AI-based check runs after generation to catch subtle wording that changes a fact's meaning (for example, "bug fixed" turned into "security hole closed"). It's on by default; turn it off with the thorough setting in the faithfulness section of chartula.yaml.
- **Review before publishing**: An optional review step shows you each generated passage together with anything the checks flagged, and lets you approve it as written or edit it first. Turn it on with the enabled setting in the review section of chartula.yaml; it's off by default, so nothing changes unless you opt in.
- **GitHub authentication**: Set the GITHUB_TOKEN environment variable to authenticate requests for pull request data. It's optional — public repositories work without it, subject to GitHub's standard rate limits.
- **Run metrics on every run**: Every preview and generate run now ends with a run metrics summary showing how many checks ran, how many findings and claims each produced, and the tokens spent by each step and overall. It also shows how many claims only the thorough check caught and at what token cost, so you can judge whether that check is worth keeping on.
- **Preview and generate commands**: Running `chartula preview --tag <tag> --repo <owner/name>` shows the changelog that would be produced without writing or publishing anything, while `chartula generate` with the same options writes it out for real. Running the tool with no arguments shows a usage screen, and a missing option, invalid repository, or unknown command produces a clear error message instead of a crash.
- **A durable changelog.json**: Every release now writes a changelog.json file recording each change's facts — title, pull request number, link, category, user-visible and breaking flags, and linked issues — as a versioned, machine-readable record. The format is documented and versioned, so later additions won't break anything already reading it.
- **All three audiences in one file**: changelog.json now also stores the customer-facing and product-manager text alongside the technical version, instead of those living as separate files in your repository. When a release has no such text yet, the field is simply present and empty.
- **Release notes updated automatically**: The generated changelog text is now written to the GitHub release's own notes. Running generate again for the same tag updates that release's notes in place rather than creating a duplicate release.
- **CHANGELOG.md kept up to date**: Each release is added as a new section at the top of CHANGELOG.md, with every earlier section preserved exactly as it was. Running generate again for a release you've already published replaces just that section in place, without duplicating or reordering anything.
- **Free hallucination check, always on**: Before anything is published, Chartula checks the generated text for numbers, quoted names, or breaking-change claims that don't appear anywhere in the source facts, and flags them for review. This check costs no tokens and always runs, with no setting to turn it off.
- **Consistent formatting and voice**: Regardless of how differently each pull request was written, every rendering now comes out in one consistent voice and formatting, with normalized bullets, line endings, and spacing. Headings and prose are left untouched.
- **One fact base, three consistent versions**: Technical, customer, and product-manager versions of a release are all generated from the same set of facts, so they can never contradict each other. The customer version leaves out changes that aren't user-visible and drops their links, the technical version keeps every link and the full set of changes, and the product-manager version groups everything by theme.
- **Rephrasing, not invention**: The generated text is instructed to only rephrase the facts it's given, never adding a number, name, or detail that isn't already there. When a change has little information behind it, the text stays brief instead of being padded out.
- **Automatic categorization**: Each change is assigned a category — feature, fix, performance, documentation, refactor, internal, or other — based on its Conventional Commit prefix, with no manual step and no AI guesswork involved. A change marked breaking (through a `!`, a `breaking` type, or a `BREAKING CHANGE` note) keeps its regular category but is still flagged as breaking.
- **Working with imperfect pull request hygiene**: When a release has no associated pull requests, Chartula falls back to the commit messages directly; when a pull request title is blank or unhelpful (like "WIP" or "update"), it falls back to the first informative line of the description, or a generic reference as a last resort. An empty release is handled cleanly rather than causing a failure.
- **Pull request details pulled in automatically**: For every commit in a release, Chartula looks up the merged pull request it belongs to and pulls in its title, description, labels, and link, removing duplicates when several commits share a pull request. A failure to reach GitHub's API produces a clear error message rather than a crash.
- **Also**: linked issues are picked up from closing keywords like "closes #12" in a pull request's title or body, the very first release is handled correctly by using the full commit history when there's no earlier tag, and a failed AI call or malformed API response is reported as a clear error instead of crashing the run.

### Bug Fixes

- **Complete, untruncated text**: Generated text could previously be cut off mid-word because no output length limit was sent, and the provider silently applied its own default of 1024 tokens. Chartula now always sends an explicit limit — 16,000 tokens by default — which you can change with the maxOutputTokens setting in the llm section of your configuration.
- **Accurate breaking-change flags**: A change could be marked as breaking just because its description mentioned the phrase "breaking change" in passing, even when nothing about it actually broke. Breaking changes are now only detected from the exact Conventional Commits footer format, so a change is flagged only when it genuinely declares one.

--- Product ---

## Changelog generation

- Chartula now builds each release's changelog from git history and merged GitHub pull requests, falling back to commit data when pull requests are missing or their titles aren't informative, so imperfect PR discipline never blocks a release.
- Every change is categorized automatically from its Conventional Commit type (feature, fix, performance, documentation, refactor, internal, or a sane default for anything unrecognized), with breaking changes flagged separately so they're never missed.
- GitHub labels can exclude a pull request, force its category, or restrict generation to only labeled pull requests - all optional and configured, never hardcoded.
- Internal and chore changes are left out of the changelog by default; breaking changes are never dropped by this filtering, and the excluded categories are configurable.
- How much source material feeds each change - title only, title and description, or title, description and linked issues - is configurable, with title and description as the default.
- Every established fact about a change (title, PR number, link, category, visibility, breaking flag, linked issues) is captured in one structured record - the only source the AI may draw from, and it may only rephrase it, never add to it.
- Generating a release makes exactly one AI call per release, and none at all when there's nothing to report; provider failures are caught and reported rather than crashing the run.
- A rewritten prompt design instructs the AI to rephrase established facts only - never invent a number, name, or claim - and to stay brief on thin material instead of padding it out.
- Technical, customer, and product-manager versions of a release are now all rendered from the same set of facts, so they can never contradict one another: technical keeps full detail and links, customer omits internal changes, product groups by theme.
- Formatting is now normalized consistently across every rendering, and individual pull request authors' tone no longer carries through into the final text - every release reads in one voice.

## Faithfulness & review

- A free, always-on check now catches obvious errors - invented numbers, invented names, and breaking-change claims not backed by any fact - before any AI involvement.
- An optional second AI pass checks generated text against the facts for subtler, meaning-level distortions. It's enabled by default and can be turned off with a single setting.
- An opt-in review mode lets a maintainer see flagged passages and approve or edit generated text before publishing. It's off by default and never required.

## Output & publishing

- Every release's underlying facts are now saved to `changelog.json` in a stable, documented, versioned format.
- Customer and product-manager texts are now stored in `changelog.json` alongside the technical version, rather than as separate marketing files.
- `CHANGELOG.md` is now updated automatically: each release is added to the top, all history is preserved, and re-running the same release updates its section in place instead of duplicating it.
- Generated release notes are now written directly to the GitHub release; re-running the same tag updates that release instead of creating a duplicate.

## CLI

- New `preview` and `generate` commands run the full pipeline: `preview` shows the result without writing or publishing anything, while `generate` writes and publishes everything.

## Configuration

- Chartula now reads settings from an optional `chartula.yaml` file, working with sensible defaults when no file is present; configuration errors are now reported clearly instead of crashing.
- A new `categories` configuration section controls category order, display names, and whether breaking changes are shown prominently.

## Observability & metrics

- Every run now reports how many checks ran, what they found, and their token cost - including whether the paid thorough check caught anything the free check missed - so checks can be tuned with data instead of guesswork.

## Fixes

- Fixed generated text being silently cut off mid-sentence because no output-length limit was set on AI calls; a limit is now always applied and is configurable.
- Fixed a false-positive breaking-change detector that matched the phrase "BREAKING CHANGE" anywhere in a pull request description - even when merely discussing the topic - instead of recognizing only a genuine breaking-change declaration.

## Documentation

- Documentation and the README were brought up to date with the tool's current state: runnable command examples, a discoverable docs folder, a complete example configuration file, an updated status badge, and corrected setup instructions for contributors.
