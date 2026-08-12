Preview changelog for v0.1.0

--- Technical ---
## Features

**Run metrics reporting** — every `preview` and `generate` run now ends with a run summary that reports check runs, findings, claims, and token usage per operation. The indented line pairs the claims caught *only* by the thorough check with the tokens spent catching them; claims found by both checks are excluded, since the thorough check adds nothing over the free one there. Details:
- `Chartula.Core/Observability/`: `IRunMetrics` with the `RunMetrics` sink, `NullRunMetrics`, `RunReport` and `RunReportFormatter`.
- `ChatModel` reports token usage, attributed per `LlmOperation`, so each check's cost is readable on its own; a provider reporting no usage still has its call counted.
- `ReleasePipeline` records both checks' findings in one call and returns the report on `ReleaseOutcome`.
- Measurement is a side channel: the sink is optional everywhere, and a run without one produces byte-identical output.
- `docs/run-metrics.md` explains how to read the summary and make the keep-or-drop call.

**Configuration sections for categories** — category presentation is now configurable alongside the existing `labels`, `factBase` and `faithfulness` sections. `CategorySettings` holds the category order, display names and breaking-change prominence, with `From(...)` parsing raw configuration values and rejecting unknown category names with a clear message. The new `categories` section in `chartula.yaml` supports `order`, `names` and `breakingProminent` (default `true`); sections remain independently editable and untouched sections keep their defaults. `GroundedFactsFactory` is extracted out of `ReleaseChangelogGenerator` to give audience filtering, category ordering and display naming a single home. Documented in `docs/configuration.md`.

**`chartula.yaml` support with sensible defaults** — `AddChartulaYaml` loads `chartula.yaml` (or `.yml`) via YamlDotNet and flattens it into `Chartula:*` configuration keys, layered before environment variables so env overrides YAML. All section options (`llm`, `github`, `labels`, `filter`, `factBase`, `faithfulness`, `review`) already existed; this adds the file as a source. With neither a file nor env vars, every option binds to its default. A minimal `chartula.example.yaml` ships at the repo root with everything commented out; the full option set is in `docs/configuration.md`. Configuration errors are now reported as a clear `Configuration error: ...` message instead of an unhandled exception. Adds the `Chartula.Cli.Tests` project as the home for CLI-level tests.

**`generate` and `preview` commands wired to the pipeline** — `ReleasePipeline` orchestrates the flow over ports only: read commit range and PRs, build the fact base, render all audiences, run the rule-based and thorough faithfulness checks plus review, then write outputs. The only difference between the two modes is the final write step. `generate` writes `changelog.json` (all audience texts), `CHANGELOG.md`, and the GitHub release notes from the technical rendering. `preview` runs the identical flow, including generation, but writes and publishes nothing. The CLI exposes `chartula preview` / `chartula generate`, each taking `--tag` and `--repo <owner/name>`, with a usage screen, clear errors for unknown commands and missing options, and a readable per-audience summary. Pipeline errors are reported rather than crashing. `--repo` is explicit for now; the interactive console reviewer is not wired here, so review mode still uses the auto-approve reviewer.

**All audience texts stored in `changelog.json`** — `ChangelogDocument` gains a `renderings` object keyed by audience (`technical` / `customer` / `product`), written in a fixed order. `ChangelogJsonSerializer.Serialize` and the `IChangelogJsonWriter` port take an optional renderings map; when none are provided, the object is present but empty. Change entries stay deterministic facts, and only the `renderings` are LLM-produced text. Customer and product-manager texts are kept in the one file rather than scattered as marketing files in the repo. `schemaVersion` stays **1**, since adding an optional field is non-breaking under the documented stability contract; old consumers ignore `renderings`. Documented in `docs/changelog-json.md`.

**Generated text written back to GitHub release notes** — adds the `IReleaseNotesWriter` port (reusing `RepositoryCoordinates`) and `GitHubReleaseNotesWriter` over the GitHub REST API using plain `HttpClient` and source-generated JSON, which is AOT-friendly. It issues `GET /releases/tags/{tag}`, then `PATCH /releases/{id}` to update in place when found or `POST /releases` to create with `tag_name` + `body` on a 404, returning the release's `html_url`. API and network failures become clear `InvalidOperationException`s. Because GitHub keys a release by its tag, re-running for the same tag updates that one release's notes rather than creating a second. The GitHub `HttpClient` setup is extracted into a shared `GitHubHttpClientFactory` used by both the PR reader and the release-notes writer.

**`CHANGELOG.md` output that prepends and preserves history** — `ChangelogMarkdownComposer` (pure logic) composes new content from the existing file and a release: the new section is prepended at the top, existing sections are kept verbatim, and re-running the same tag replaces that section in place rather than duplicating it, so history is never reordered. A brand-new file gets a `# Changelog` title. Running the same release twice yields a byte-identical file, and re-running an older release after a newer one does not move it above the newer one. The `IChangelogMarkdownWriter` port lives in Core with `FileChangelogMarkdownWriter` in `Chartula.Infrastructure` handling file I/O, matching the split used for `changelog.json`.

**Opt-in review mode for human sign-off** — `IReviewCoordinator`/`ReviewCoordinator` gate each rendering on an opt-in toggle bound to `Chartula:Review`. With review off (the default) the text passes straight through, approved as-is, and the reviewer is never consulted. With review on, the item goes to an `IReviewer` that either approves it as-is or returns an edited version; the coordinator returns that `ReviewDecision`, whose `Text` is what gets written. `ReviewPresentation` formats an item for a maintainer, showing the generated text followed by the flagged passages from the rule-based and thorough checks. `AutoApproveReviewer` is the non-interactive default; the interactive console reviewer ships with the CLI command surface.

**Thorough second-pass LLM faithfulness check with a toggle** — `IThoroughFaithfulnessChecker`/`ThoroughFaithfulnessChecker` runs a second LLM pass via `CheckFaithfulnessAsync`, turning the fact base into grounded facts and flagging unsupported claims. This catches meaning-level hallucinations the rule-based check cannot see, such as "bug fixed" rendered as "security hole closed". When the toggle is off, or there is nothing to check, it returns a faithful report with no LLM call. `ThoroughFaithfulnessOptions(Enabled = true)` is on by default and can be disabled via the `Chartula:Faithfulness:Thorough` config key. Following the partial-class pattern, the faithfulness prompt moves from an inline placeholder in `ChatModel` into `IChangelogPromptBuilder.BuildFaithfulnessPrompt`, with its text in the Prompts partial and an explicit meaning-level-distortion instruction. Removing the toggle or adding more granular check settings is deferred until there is observability data.

**Rule-based faithfulness check for obvious hallucinations** — `IRuleBasedFaithfulnessChecker`/`RuleBasedFaithfulnessChecker` checks generated output against the fact base and returns a `FaithfulnessReport`, flagging a number in the output not present in the facts (allowed numbers include PR numbers, linked issues, and any number in titles, descriptions or the tag), a quoted or backticked name absent from the facts (the usual shape of an invented API, feature or option name), and a breaking-change claim when no fact is marked breaking. It has no `IChangelogModel` dependency, so there is structurally nothing to call and it costs zero tokens; it always runs, with no toggle. Flags are advisory, surfacing passages for review rather than failing a run. Uses source-generated regexes, which is AOT-friendly.

**Consistent formatting and tone per audience** — `IChangelogFormatter`/`ChangelogFormatter` normalizes model output with conservative, structure-preserving rules: normalized line endings, a single `- ` bullet marker, trimmed trailing whitespace and collapsed blank-line runs, while leaving non-bullet lines such as headings and prose intact. The generator applies it to every rendering, so formatting is consistent regardless of what the model returns. A new prompt rule tells the model to write in one consistent voice and format and not to carry over an individual author's tone or phrasing. Tone normalization comes from the prompt because it is a language judgment; formatting consistency is enforced deterministically in code, which also makes it testable with a stubbed model.

**Technical, customer and PM renderings from one fact base** — `IReleaseRenderer`/`ReleaseRenderer` renders all three audiences from the same `FactBase`, delegating to the generator with one call per audience and returning a result per `Audience`; a failure in one audience does not fail the others. Audience selection is deterministic in code rather than left to the LLM: customer omits non-user-visible changes and their links, technical keeps the pull request link and the full change set, and product sees the full set. Prompt guidance is extended so technical also asks to keep links, customer is benefit-focused, and PM groups by theme. Because every audience derives from the same established, deterministic facts, and each audience view is a selection over that one source, two renderings cannot disagree on what changed.

**Prompt architecture that rephrases facts and never invents** — `IChangelogPromptBuilder`/`ChangelogPromptBuilder` produces a `ChangelogPrompt` (system + user). The system prompt pins the model to rephrasing: never introduce a fact, number or name that is not in the list; treat each fact's category and `(breaking)` marker as established, using them as given without changing or inferring; on thin facts stay brief and do not pad, speculate or invent; and emit no preamble or conclusion, plus per-audience guidance. The user prompt carries only the facts, with nothing added by our code to pad them. `ChatModel` now delegates to the builder and simply wires the prompt into the `IChatClient`. Categories and flags reach the model as text embedded by the generator; the prompt presents them verbatim and instructs the model not to decide them.

**Changelog generation through the provider interface** — `IReleaseChangelogGenerator`/`ReleaseChangelogGenerator` and `ChangelogGenerationResult` turn the fact base into grounded fact statements and make exactly one `IChangelogModel.RephraseAsync` call per release; an empty fact base makes no call at all. Provider failures are caught and returned as a failed result carrying the release tag and the provider message, while cancellation propagates rather than being swallowed. The generator depends only on `IChangelogModel` and references no provider type.

**Fact base serialization to `changelog.json`** — `ChangelogDocument` defines the stable on-disk shape (`schemaVersion` + `tag` + `changes`), kept separate from the domain `FactBase` so the domain can evolve without breaking the file format. `ChangelogJsonSerializer` converts `FactBase` to JSON and back, pure and deterministic with source-generated serialization for AOT and trim safety, writing category as its name for a stable, readable record. The `IChangelogJsonWriter` port lives in Core with `FileChangelogJsonWriter` in `Chartula.Infrastructure` handling directory writes. `schemaVersion` (currently `1`) is the contract: consumers read it and reject versions they do not understand; fields are always present, including `null` values; adding optional fields is non-breaking, while removing, renaming or re-meaning them bumps the version. Every field is a deterministic fact, with nothing in the file LLM-generated. Documented in `docs/changelog-json.md`.

**Configurable fact-base depth** — `FactBaseDepth` offers three modes with `FactBaseDepthParser`: `TitleOnly` (title only), `TitleAndDescription` (title plus description, no issues; the default), and `TitleDescriptionAndIssues` (title, description and linked issues). `FactBaseBuilder` honours the depth, taking the description from the middle mode up and linked issues only in the deepest mode. The CLI reads `Chartula:FactBase:Depth` and passes the parsed value into the builder; the parser accepts the canonical names plus the aliases `title`, `description` and `full`, and raises a clear error on an unknown value. Because a depth is a config value (an enum), it is passed into the builder via a factory rather than registered as its own DI service. Whether all three modes survive long-term is revisited with real data; the option set is not expanded here.

**Curated changes transformed into the release fact base** — `IFactBaseBuilder`/`FactBaseBuilder` and the `FactBase` container (tag plus one `ChangeFact` per included change) resolve changes with the missing-PR fallback, drop filtered-out changes, and map each survivor to a `ChangeFact`. Category and breaking flag come from deterministic categorization, and a label can force the category. `IsUserVisible` is derived from the category, covering outward-facing categories plus every breaking change. `LinkedIssues` are parsed from GitHub closing keywords (`closes/fixes/resolves #n`) in the title and body. Category and flags come from the deterministic curation steps, never from an LLM; the builder has no LLM dependency.

**Fact-base data model** — `ChangeFact` defines one structured object per change: the single source of truth the LLM may only rephrase from. It captures the title, PR number and link, category from deterministic categorization, user-visible and breaking flags, linked issues, and an optional description populated per the fact-base depth. Every field is derived deterministically and nothing in the model is LLM-generated. PR-only fields (number, link) are nullable so commit-based changes fit the same shape. This is the per-change "index card"; the release-level container is assembled when curated PRs are transformed into facts, and the whole base is serialized to `changelog.json`.

**Internal and chore changes dropped by default** — `IChangeFilter`/`ChangeFilter` and `ChangeFilterRules` combine deterministic categorization with label rules. The decision order is: a label that excludes the change wins outright; a breaking change is never dropped; otherwise the change is dropped when its effective category (a label-forced one, else the deterministic one) is in the excluded set. The default excluded set is `Internal`, overridable via `Chartula:Filter:ExcludeCategories`, where an explicit — possibly empty — list replaces the default. A breaking change is never dropped even if its category is excluded, a deterministic safeguard driven by the breaking flag rather than guesswork; an explicit label exclusion still wins over it.

**Label rules for steering curation from config** — `LabelRules` covers excluded labels, label-to-category overrides, and an only-include-labeled mode, with `ILabelRulePolicy`/`LabelRulePolicy` producing a `LabelDecision` (include plus an optional forced category). Precedence is: exclusion wins; then only-labeled drops unlabeled changes; otherwise the change is included, with the first matching label deciding a forced category. Everything is optional — `LabelRules.None` ignores labels entirely, so the tool works with no labels at all — and matching is case-insensitive. The CLI binds the `Chartula:Labels` section into `LabelRules` via `LabelRules.From`, parsing category names and raising a clear error on an unknown one, and registers the policy. This lets a maintainer steer curation with GitHub labels without touching code.

**Deterministic categorization before the LLM** — `IChangeCategorizer` and `ConventionalCommitCategorizer` read Conventional Commit conventions from the change title (`type(scope)!: subject`) so the model can never invent what kind of change something is. `ChangeCategory` covers Feature (`feat`), Fix (`fix`), Performance (`perf`), Documentation (`docs`), Refactor (`refactor`), Internal (`build`/`ci`/`chore`/`test`/`style`/`revert`), and `Other` as the default for unrecognized or prefix-less titles. Breaking is tracked separately via `ChangeClassification.IsBreaking`, detected from a `!` marker, a `breaking` type, or a `BREAKING CHANGE` body note, so a breaking feature stays a feature while still being flagged. Pure and deterministic, with no LLM and no I/O, using a source-generated regex that is AOT-friendly.

**Graceful degradation when clean PRs are missing** — `IReleaseChangeResolver` and `ReleaseChangeResolver` turn a `CommitRange` and the merged `PullRequestInfo` list into `ReleaseChange` values (title, description, number, url, labels, `ChangeSource`, commit sha) as pure domain logic with no I/O. When merged PRs are present, each PR yields one change with `Source = PullRequest`; with no PRs at all, each commit yields a change using the commit subject with `Source = Commit`. A blank or uninformative PR title such as `WIP`, `update` or `Merge ...` falls back to the PR body's first informative line, then to a generic `PR #n`. An empty release produces an empty set rather than an exception, so the tool never hard-fails solely because PR discipline is imperfect. The uninformative-title heuristic is a small starter set and becomes configurable with the config work.

**Merged PRs fetched from the GitHub API** — the `IReleasePullRequestReader` port plus `PullRequestInfo` (number, title, description, labels, url) and `RepositoryCoordinates` live in Core as pure domain. `GitHubPullRequestReader` queries GitHub's "pull requests associated with a commit" endpoint for the commits in a `CommitRange`, keeps merged PRs only, and de-duplicates by number, with DTOs parsed via a source-generated `System.Text.Json` context. The composition root configures the `HttpClient` (base URL, GitHub headers, bearer token by env-var name) and registers the reader. Raw `HttpClient` plus `System.Text.Json` source generation was chosen over Octokit for being dependency-light and native-AOT friendly, consistent with the git-CLI choice, and a stub `HttpMessageHandler` makes it fully mockable without network. The token is read by env-var name (`GITHUB_TOKEN`) and is optional, since public repos work unauthenticated subject to rate limits. API status, network, and malformed-response paths all raise a clear `InvalidOperationException` instead of crashing.

**Commit range for a release read from git** — the `IReleaseCommitReader` port plus `CommitInfo` and `CommitRange` (with `IsFirstRelease`) live in Core as pure domain with no I/O. The new `Chartula.Infrastructure` layer adds `GitCliCommitReader`, which shells out to `git` for the range since the previous tag (`<prev>..<tag>`), or all history up to the tag when there is no previous tag (first release), with clear errors for unknown or blank tags. The composition root registers the git reader while the pipeline depends only on the port. The git CLI was chosen over LibGit2Sharp to avoid native dependencies that would fight the planned native-AOT binaries, and `git` is present in any repo Chartula runs on. `Chartula.Infrastructure` is the new home for concrete I/O adapters, keeping `Core` pure domain and `Cli` a thin composition root, and will host the GitHub API, file writers, and webhooks.

**LLM provider abstracted behind `IChangelogModel`** — the new `Chartula.Core` project holds the domain-focused seam: `IChangelogModel` (`RephraseAsync`, `CheckFaithfulnessAsync`) as the interface the pipeline depends on, `ChatModel` as the single implementation backed by a provider-agnostic `Microsoft.Extensions.AI.IChatClient`, and the domain types `Audience`, `GroundedFacts`, `RephraseRequest`, `FaithfulnessRequest` and `FaithfulnessReport`. The composition root wires Anthropic as the first provider via `AsIChatClient`, with model and provider selectable via config and the API key read by env-var name; this is the only provider-specific code, so swapping providers is a composition-root change only. The architecture is a hybrid: a domain interface over an agnostic `IChatClient`. `GroundedFacts` and the `ChatModel` prompts are intentionally minimal placeholders, since the fact base and prompt design are handled separately. Adds the `Chartula.Core.Tests` project, exercising the seam with a stub `IChatClient` and no live provider call.

## Fixes

**Two release blockers found by dogfooding v0.1.0** — both found by running `chartula preview --tag v0.1.0` against this repository, and neither reachable from the existing tests: the first needs a live API call, the second real pull request bodies.

*Truncation (`ChatModel`)* — calls went out without `ChatOptions`, so `MaxOutputTokens` was never set. The provider requires `max_tokens` and substitutes its own default of 1024 when absent, cutting all three audience texts off mid-word; the run metrics showed `3 calls, 3,072 out`, exactly 3 × 1024. It failed silently: the run reported success, and the thorough check spent 56,712 tokens flagging the severed sentence as an unsupported claim, so a real bug symptom was read as a hallucination. The ceiling is now always sent, configurable via `llm.maxOutputTokens` and defaulting to 16000.

*False breaking changes (`ConventionalCommitCategorizer`)* — `MentionsBreakingChange` searched the whole body for `BREAKING CHANGE` as a case-insensitive substring, so prose *discussing* breaking changes *declared* one. Six of the thirty-three changes in v0.1.0 were mislabelled and none were breaking; #65 described a setting called breaking-change prominence and was marked breaking for saying so, meaning the feature that renders breaking changes prominently became one. Matching now follows the Conventional Commits footer: uppercase, start of line, colon-terminated.

Confirmed against a real run rather than tests alone: rephrasing output went from 3,072 tokens (3 × 1024) to 11,271; text endings from mid-word to complete sentences; breaking changes reported from 6 to 0; thorough check claims from 1 (the truncation artifact) to 0.

Known and not fixed here: `RuleBasedFaithfulnessChecker` matches `\bbreaking\b` across the whole output and flags a breaking-change claim whenever the word appears — the same phrase-versus-assertion mistake, now visible because no fact is breaking anymore. The flags are advisory and do not fail a run, and separating a claim from prose that uses the word needs more than a regex, so it is filed separately rather than rushed in.

## Documentation

**Docs brought up to what Chartula actually is** — phase 1 is complete, but the docs still described a project that was being planned. `Usage` was not runnable: it called the commands "planned entry points" and showed `chartula preview` without the required `--tag` and `--repo`. The `docs/` folder was invisible, with all four documents existing and linked from nowhere. `chartula.example.yaml` showed 4 of 8 supported sections, missing `github`, `labels`, `categories` and `review`. The status badge said "early development" with 27 of 27 phase 1 issues closed. CONTRIBUTING asked for "the .NET SDK" — an older one cannot build `net10.0` — and documented four commit scopes (`collect`, `curate`, `render`, `check`) that were never used once, while the sixteen actually in use went unmentioned.

The wordmark now leads the README, switched via `<picture>` and `prefers-color-scheme` so it reads on either theme. Long-celled tables became prose, since two columns of paragraph text collapse on a phone, which is where a README often gets read: `Why Chartula`, `Core ideas` and `Roadmap` are now prose and headings, while the remaining tables (env vars, doc index) hold short facts and survive a narrow column. New `docs/architecture.md` captures the layering and the reasoning behind the dependency choices, which previously lived only in the code and in review comments, so nothing stopped a contributor from reaching for LibGit2Sharp or Octokit and quietly costing the native-AOT goal; it states the inward-pointing rule, why facts are established before an LLM sees them, and where each concern lives. Everything else now points somewhere, with a documentation index in the README and architecture and fixtures linked from CONTRIBUTING.

Verified: all 24 relative links in `README.md`, `CONTRIBUTING.md` and `docs/*.md` resolve to existing files; both SVGs are valid XML with no external references and no `<script>`, rendered to PNG and checked against dark and light backgrounds; every section of `chartula.example.yaml` was uncommented into a real `chartula.yaml` and run against the CLI, with all eight sections binding and no configuration error; every documented default was checked against the value in the code. The brand asset delivery note that came with the SVGs is deliberately excluded: it is in German, describes files that are not in the repo (`mark/`, `favicon/`), and states Chartula is "tiny charts for your terminal", which it is not.

## Refactors

**Prompt text moved into a partial class** — `ChangelogPromptBuilder` is now a `partial` class split across two files: `ChangelogPromptBuilder.Prompts.cs` holds the prompt strings only (system header, the four rules, per-audience guidance), and `ChangelogPromptBuilder.cs` holds the composition logic referencing those constants. This separates prompt text from build logic, so iterating on wording — which happens often — is text-only work in one file rather than navigating composition logic to find and change a string. The prompt text is byte-for-byte unchanged, and the existing prompt-content assertions pass without modification, which is the proof there is no behaviour change.

--- Customer ---
## Features

**Command-line interface**

- New `chartula preview` and `chartula generate` commands, each accepting `--tag` and `--repo <owner/name>`. Both run the full pipeline; `preview` shows you the real result without writing or publishing anything, while `generate` writes the outputs. Unknown commands and missing options produce clear messages, and pipeline errors are reported rather than crashing.

**Configuration**

- Chartula now reads settings from `chartula.yaml` (or `.yml`). A configuration file is never required — with no file and no environment variables, everything falls back to sensible defaults. Environment variables override file values. A minimal, fully commented `chartula.example.yaml` ships in the repository root; copy it and uncomment what you need. Invalid values are reported as a clear `Configuration error: ...` message instead of an unhandled exception. `docs/configuration.md` documents the full option set.
- New `categories` section controls how categories are presented: `order`, display `names`, and `breakingProminent` (default `true`). An unknown category name is rejected with a clear message. Sections remain independently editable — anything you leave untouched keeps its defaults.
- New `factBase.depth` setting chooses how much source material feeds the fact base: title only, title plus pull request description (the default), or title, description and linked issues. Unknown values raise a clear error.
- Label rules can steer curation from configuration, without code changes. A label can exclude a pull request from the changelog, force it into a given category, or you can switch to an "only include labeled pull requests" mode. All of this is optional — the tool works with no labels at all, and label matching is case-insensitive.
- Internal and chore changes are now excluded from the changelog by default, based on category and labels rather than guesswork. The excluded set is overridable in configuration. An explicit label exclusion always wins; otherwise a breaking change is never dropped, even if its category is excluded.

**Release inputs**

- Given a tag, Chartula determines the commit range since the previous tag, and falls back to the full history when there is no previous tag (a first release).
- Merged pull requests for that commit range are fetched from the GitHub API, giving each change a title, description, labels, number and link. Duplicates across commits are removed, and API, network or malformed-response failures produce a clear error rather than a crash. A token is read from the `GITHUB_TOKEN` environment variable and is optional — public repositories work unauthenticated, subject to rate limits.
- Imperfect pull request discipline no longer stops a release. With no associated pull requests, Chartula falls back to commit data. With a blank or uninformative title (for example `WIP`, `update`, `Merge ...`), it uses the pull request body's first informative line, then a generic `PR #n`. An empty release yields an empty set rather than an error.

**Curation and facts**

- Each change's category is decided in code before any generation, so the model can never invent what kind of change something is. Conventional Commit prefixes are detected (`feat`, `fix`, `perf`, `docs`, `refactor`, and `build`/`ci`/`chore`/`test`/`style`/`revert` as internal), with `Other` as the default for unrecognized titles. Breaking status is tracked separately, so a breaking feature stays a feature while still being flagged.
- Every change is captured as one structured record holding its title, pull request number and link, category, user-visible and breaking flags, linked issues, and an optional description. Nothing in it is model-generated.
- Those records are assembled into a complete fact base for the release, resolving missing pull request data, dropping filtered-out changes, deriving user visibility from the category, and extracting linked issues from GitHub closing keywords (`closes`/`fixes`/`resolves #n`) in the title and body.

**Generation**

- Changelog generation now runs through a provider-agnostic interface, with Anthropic wired as the first provider. The model and provider are selectable in configuration and the API key is read from the environment, never hardcoded. Switching providers touches only the wiring.
- Generation makes exactly one model call per release, and no call at all for an empty fact base. Provider failures are returned as a failed result carrying the release tag and provider message rather than crashing.
- Prompts now instruct the model to rephrase the facts and nothing else: never introduce a fact, number or name that is not in the list; treat each fact's category and breaking marker as established; stay brief when the facts are thin rather than padding or speculating; no preamble or conclusion. Categories and flags are provided to the model, not decided by it.
- The technical, customer and product-manager versions of a release are all rendered from the same fact base, so they cannot contradict each other. Audience selection is deterministic: the customer version omits changes that are not user-visible along with their links, the technical version keeps the pull request link and the full change set, and the product version groups by theme. A failure rendering one audience does not affect the others.
- Each rendering now reads as one coherent document regardless of how individual pull requests were written. Formatting is normalized deterministically — consistent line endings and bullet markers, trimmed trailing whitespace, collapsed blank lines — while headings and prose are left intact. The prompt additionally asks for one consistent voice, with no individual author's tone carried over.

**Checks and review**

- A rule-based faithfulness check now runs on every release, at zero token cost and with no model call. It flags numbers, quoted or backticked names, and breaking-change claims that are not present in the fact base. Flags are advisory: they surface passages for review rather than failing a run.
- An optional thorough second pass asks the model to check the text against the fact base semantically, catching subtler distortions such as "bug fixed" rendered as "security hole closed". It is on by default and can be turned off with a single toggle; when off, or when there is nothing to check, no model call is made.
- New opt-in review mode presents each generated text along with its flagged passages so a maintainer can approve it as-is or supply an edited version before anything is written. Review is off by default, and when off the text passes straight through.

**Outputs**

- The fact base is written to `changelog.json` as a durable, machine-readable record. The format is versioned via `schemaVersion` (currently `1`) and documented in `docs/changelog-json.md`: fields are always present including `null` values, adding optional fields is non-breaking, and removing or re-meaning a field bumps the version. Every field is a deterministic fact — nothing in the file is model-generated.
- `changelog.json` also stores the customer and product-manager texts in a `renderings` object keyed by audience, so the marketing copy lives inside the one file instead of scattered across the repository. `schemaVersion` stays `1`; older consumers simply ignore the new field. The change entries themselves remain deterministic facts.
- Each release is written to `CHANGELOG.md` as a new section at the top. Existing sections are kept verbatim, a brand-new file gets a `# Changelog` title, and re-running the same tag replaces that section in place — so running twice produces a byte-identical file and never reorders history.
- The generated text is written back to the release's own GitHub release notes. Re-running for the same tag updates that one release rather than creating a duplicate, and the release URL is returned. API and network failures produce clear errors.

**Observability**

- Every `preview` and `generate` run now ends with a run metrics summary showing, per stage, how many times each check ran, how many findings and claims it produced, and how many tokens it spent, plus a total. An indented line pairs the claims that only the thorough check caught with the tokens it spent catching them — claims the free rule-based check also finds are excluded, so consistently zero there tells you the thorough check is not earning its cost. Token usage is attributed per operation, and a provider that reports no usage still has its call counted. Measurement is a side channel: a run without it produces byte-identical output. `docs/run-metrics.md` explains how to read the summary and make the keep-or-drop call.

## Fixes

- Generated text was being cut off mid-word. Calls went out without an output-token ceiling, so the provider substituted its own default of 1024 tokens, truncating all three audience texts while the run still reported success — and the thorough check then spent 56,712 tokens flagging the severed sentence as an unsupported claim. The ceiling is now always sent, configurable via `llm.maxOutputTokens` and defaulting to 16000.
- Changes were being wrongly marked as breaking. The check searched the whole pull request body for `BREAKING CHANGE` as a case-insensitive substring, so prose merely *discussing* breaking changes *declared* one — six of the thirty-three changes in v0.1.0 were mislabelled, none of them actually breaking. It now matches the Conventional Commits footer form: uppercase, at the start of a line, colon-terminated.

**Known limitation, not fixed here:** the rule-based check matches the word "breaking" anywhere in the output and flags a breaking-change claim whenever it appears — the same phrase-versus-assertion confusion, now more visible since no fact is breaking. The flags are advisory and do not fail a run, and reliably separating a claim from prose that merely uses the word needs more than a regex, so this is tracked separately.
  Flagged for review:
    ! 'only include labeled pull requests' is not supported by the facts.

--- Product ---
## LLM provider and generation

Chartula now talks to language models through a single provider-agnostic seam. `IChangelogModel` defines the operations the pipeline needs, backed by one implementation over an agnostic chat client. Anthropic is wired as the first provider, with model and provider selectable in configuration and API keys read from the environment rather than hardcoded. Swapping providers is a configuration-root change only.

Generation runs through that seam end to end. Each release makes exactly one model call; an empty fact base makes no call at all. Provider failures come back as a failed result carrying the release tag and the provider message instead of crashing.

The prompt layer is now first-class. A dedicated prompt builder produces a system and user prompt: the system prompt pins the model to rephrasing only — never introducing a fact, number or name that is not in the list, treating each fact's category and breaking marker as established, and staying brief when the facts are thin instead of padding or speculating. Categories and flags are handed to the model as text, never decided by it. Prompt text now lives in its own file separate from the composition logic, so wording changes are text-only work; the text itself is unchanged.

## Reading history and pull requests

Chartula reads the commits belonging to a release from git. Given a tag, it determines the range since the previous tag, and falls back to all history when there is no previous tag — the first release. Unknown and blank tags produce clear errors.

For that commit range, it retrieves the associated merged pull requests from the GitHub API, yielding each one's title, description, labels, number and link. Merged pull requests only, de-duplicated across commits. API failures, network problems and malformed responses all surface as clear errors rather than a crash.

When pull request discipline is imperfect, the tool degrades instead of failing. With no associated pull requests it falls back to commit data. With a blank or uninformative title such as `WIP` or `update`, it uses the pull request body's first informative line, then a generic reference. An empty release yields an empty set, never an exception.

## Deterministic curation

Categories are assigned in code before any model sees a change. Conventional-commit prefixes are detected from the title and mapped to Feature, Fix, Performance, Documentation, Refactor and Internal, with Other as the default for unrecognised titles. Breaking is tracked separately from category, so a breaking feature stays a feature while still being flagged.

Labels can steer curation from configuration, without code changes: a label can exclude a pull request, force it into a given category, or an "only include labeled pull requests" mode can be enabled. All of it is optional — the tool works with no labels at all.

Internal and chore changes are excluded by default, and the excluded set is overridable in configuration. Filtering rests on category and labels rather than guesswork. A breaking change is never dropped for being in an excluded category, though an explicit label exclusion still wins.

## The fact base

A per-change data model captures the established facts for one change: title, pull request number and link, category, user-visible and breaking flags, linked issues, and an optional description. Every field is derived deterministically; nothing in the model is generated by a language model. Pull-request-only fields are optional so commit-based changes fit the same shape.

Curated changes are assembled into a complete release fact base — one fact object per included change, with categories and flags coming from the deterministic curation steps. Linked issues are parsed from GitHub closing keywords in the title and body, and user visibility is derived from the category, with every breaking change counted as visible.

How much source material feeds the fact base is configurable in three depths: title only, title plus pull request description, or title, description and linked issues. The middle mode is the default.

## Rendering for three audiences

Technical, customer and product-manager versions of a release are all rendered from the same fact base, so they cannot contradict each other. Audience selection is deterministic rather than left to the model: the customer version omits non-user-visible changes and their links, the technical version keeps pull request links and the full change set, and the product version sees the full set. A failure rendering one audience does not fail the others.

Each rendering also reads as one coherent document regardless of how individual pull requests were written. A deterministic formatter normalises line endings, bullet markers, trailing whitespace and blank-line runs on every rendering, while leaving headings and prose intact. A prompt rule asks for one consistent voice, with no individual author's tone carried over.

## Faithfulness checks and review

A rule-based check runs on every release at zero token cost, with no model dependency at all. It flags a number in the output that is not present in the facts, a quoted or backticked name that does not appear in them, and a breaking-change claim when no fact is marked breaking. Flags are advisory: they surface passages for review rather than failing a run.

A thorough second pass catches subtler, meaning-level problems the rule-based check cannot see — a bug fix rendered as a closed security hole, for example. It checks the text semantically against the fact base and flags unsupported claims. It is on by default and can be disabled with a single toggle; when off, or when there is nothing to check, it makes no model call.

An opt-in review mode lets a maintainer sign off before anything is published. It presents each generated text with the flagged passages from both checks highlighted, and the reviewer can approve it as-is or return an edited version, which is then what gets written. Review is off by default; when off, the reviewer is never consulted.

## Outputs

The fact base is written to `changelog.json` as a durable, machine-readable record. The file has a documented, versioned schema kept deliberately separate from the internal domain model, so the domain can evolve without breaking the format. Every field in it is a deterministic fact — nothing in the file is model-generated.

That same file also stores the customer and product-manager texts, keyed by audience, so marketing copy lives inside the one file rather than scattered across the repository. The schema version stays at 1, since adding an optional field is non-breaking and older consumers simply ignore it.

`CHANGELOG.md` is written with each release added as a new section at the top. Existing sections are kept verbatim, and re-running the same release replaces its section in place rather than duplicating it or reordering history — running the same release twice produces an identical file.

The generated text is also written back to the GitHub release notes, where the release actually lives. Because a release is keyed by its tag, re-running for the same tag updates that release's notes rather than creating a second one.

## Command line and configuration

Two commands make up the surface: `chartula preview` and `chartula generate`, each taking a tag and a repository. `generate` writes `changelog.json`, `CHANGELOG.md` and the GitHub release notes. `preview` runs the identical flow, including generation so the real result is visible, but writes and publishes nothing. Both print a readable per-audience summary, and pipeline errors are reported rather than crashing. A usage screen and clear messages for unknown commands and missing options round it out.

Configuration comes from `chartula.yaml`, which refines behaviour but is never required — with no file and no environment variables at all, every option binds to a sensible default. Environment variables override the file. A shipped example file keeps everything commented out, and configuration errors are reported as a clear message instead of an unhandled exception.

Category presentation is configurable too, alongside the existing sections: category order, display names, and whether breaking changes are shown prominently, which is on by default. Unknown category names are rejected with a clear message, and every section stays independently editable — untouched sections keep their defaults.

## Run metrics

Every `preview` and `generate` run now ends with a metrics summary reporting what the run did and what it cost: how often each check ran, how many produced findings, how many claims were raised, and tokens in and out per operation, with a total.

The key line pairs the claims that only the thorough check caught with the tokens it spent catching them. Claims both checks find are excluded, because on those the thorough check adds nothing over the free one. Read across a few real releases, that line answers whether the thorough check earns its cost — consistently zero claims caught means the tokens buy nothing.

Measurement is a side channel: the metrics sink is optional everywhere, and a run without one produces byte-identical output. A document explains how to read the summary and make the keep-or-drop call.

## Fixes

Two release blockers surfaced from running Chartula against its own repository.

Model calls went out without a maximum output token setting, so the provider substituted its own default of 1024 and all three audience texts were cut off mid-word. It failed silently: the run reported success, and the thorough check then spent 56,712 tokens flagging the severed sentence as an unsupported claim — a real bug read as a hallucination. The ceiling is now always sent, configurable and defaulting to 16000.

Breaking-change detection searched the whole body for `BREAKING CHANGE` as a case-insensitive substring, so prose merely discussing breaking changes declared one. Six of the thirty-three changes in v0.1.0 were mislabelled and none were breaking — including the change describing breaking-change prominence, which was marked breaking for saying so. Detection now matches the Conventional Commits footer: uppercase, at the start of a line, colon-terminated.

One related issue is known and deliberately not fixed here: the rule-based check still flags a breaking-change claim whenever the word "breaking" appears anywhere in the output. The flags are advisory and do not fail a run, and telling an assertion apart from prose that uses the word needs more than a regular expression, so it is filed separately rather than rushed.

## Documentation

The documentation now describes what Chartula actually is rather than what was being planned. The usage section is runnable, with the options the commands actually require. The `docs/` folder is reachable through an index in the README, and the wordmark leads it, switching between light and dark themes.

Long-celled tables became prose and headings, since two columns of paragraph text collapse on a phone — where a README is often read. The tables that remain hold short facts and survive a narrow column.

A new architecture document states the inward-pointing dependency rule, why facts are established before a model sees them, and where each concern lives. That reasoning previously lived only in the code and in review comments, so nothing stopped a contributor from reaching for a dependency that would quietly cost the native-AOT goal.

The example configuration file now shows all eight supported sections rather than four, the status badge reflects that phase 1 is complete, and the contributing guide names the required SDK version and the commit scopes actually in use.
  Flagged for review:
    ! 'only include labeled pull requests' is not supported by the facts.
    ! "Swapping providers is a configuration-root change only." — the facts state it is a composition-root change; "configuration-root" misstates the mechanism, implying a config change rather than a code composition change.
    ! "A rule-based check runs on every release at zero token cost" — the facts say it always runs (no toggle) as part of the pipeline; "on every release" is an extrapolation, though minor.
    ! "the status badge reflects that phase 1 is complete" — the facts state the badge said "early development" with 27 of 27 phase 1 issues closed as a problem, but do not state what the badge was changed to.
    ! "the contributing guide names the required SDK version and the commit scopes actually in use" — the facts identify these as problems (asked for "the .NET SDK", documented four unused scopes while sixteen went unmentioned) but do not state that the guide was changed to name the SDK version or list the scopes in use.

Preview only - nothing was written or published.

Run metrics
  Rule-based check: 3 runs, 2 with findings, 2 claims, no tokens
  Thorough check:   3 runs, 1 with findings, 4 claims, 71,538 in / 377 out
    caught 4 claims the rule-based check missed, for 71,915 tokens in 3 calls
  Rephrasing:       3 calls, 54,874 in / 15,516 out
  Total:            142,305 tokens
