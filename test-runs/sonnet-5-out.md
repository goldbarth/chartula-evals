Preview changelog for v0.1.0

--- Technical ---
### Feature: Report what a run does and what it costs

- Every `preview` and `generate` run now ends with a run metrics summary covering the rule-based check (runs, findings, claims, token cost), the thorough check (runs, findings, claims, tokens in/out, and claims caught that the rule-based check missed), rephrasing (calls, tokens in/out), and a total token count.
- Adds `Chartula.Core/Observability/`: `IRunMetrics` with the `RunMetrics` sink, `NullRunMetrics`, `RunReport`, and `RunReportFormatter`.
- `ChatModel` now reports token usage per `LlmOperation`; a provider that reports no usage still has its call counted.
- `ReleasePipeline` records both checks' findings in one call and exposes the report via `ReleaseOutcome`.
- Metrics recording is optional throughout; a run without a sink produces byte-identical output.
- Documented in `docs/run-metrics.md`.
- Verification: build clean (0 warnings, 0 errors); 215 tests passing (Core 177, Infrastructure 26, Cli 12), 21 new, covering check-fire counts, per-operation token usage, thorough-only attribution, snapshot isolation, and concurrent recording; CLI end-to-end verified via the real DI graph and formatter output.

Closes #26 ([PR #66](https://github.com/goldbarth/chartula/pull/66))

### Feature: Add configuration sections for categories

- Adds a `categories` section to `chartula.yaml` (`order`, `names`, `breakingProminent`, default `true`), alongside the existing `labels`, `factBase`, and `faithfulness` sections. Sections remain independently editable, with defaults preserved when untouched.
- Adds `CategorySettings` in the domain, with `From(...)` parsing raw configuration values and rejecting unknown category names with a clear error message.
- Extracts `GroundedFactsFactory` from `ReleaseChangelogGenerator`, centralizing audience filtering, category ordering, and display naming.
- Documented in `docs/configuration.md`.
- Verification: build clean (0 warnings, 0 errors); 194 tests passing (Core 158, Infrastructure 26, Cli 10), 17 new; CLI end-to-end verified for both an invalid category (exits 1 with a clear error) and a valid `categories` section reaching the pipeline.

Closes #25 ([PR #65](https://github.com/goldbarth/chartula/pull/65))

### Feature: Read chartula.yaml with sensible defaults

- Adds `AddChartulaYaml`, which loads `chartula.yaml` (or `.yml`) via YamlDotNet and flattens it into `Chartula:*` configuration keys, layered before environment variables (env overrides YAML). Covers the existing `llm`, `github`, `labels`, `filter`, `factBase`, `faithfulness`, and `review` sections; with neither a file nor env vars, every option binds to its default.
- Adds `chartula.example.yaml` at the repo root: minimal, with everything commented out.
- Documented in `docs/configuration.md`, covering the full option set with defaults.
- Configuration errors are now reported as a clear `Configuration error: ...` message instead of an unhandled exception.
- Adds `Chartula.Cli.Tests` as a new project (`InternalsVisibleTo` from the CLI) for CLI-level tests.
- Verification: build clean (0 warnings, 0 errors); tests passing (Core 147, Infrastructure 26, Cli 5), covering YAML flattening, no-config defaults, config refining behavior, absent-file no-op, and reading from a directory; end-to-end verification of a clear error on invalid config and an env var overriding YAML.
- Note: `chartula.example.yaml` is shipped rather than a live `chartula.yaml`, so it is not picked up when running Chartula against its own repository.

Closes #24 ([PR #64](https://github.com/goldbarth/chartula/pull/64))

### Feature: Generate and preview commands wired to the pipeline

- Adds `ReleasePipeline`, orchestrating the full flow over ports only: read commit range and PRs, build fact base, render all audiences, run rule-based and thorough faithfulness checks plus review, then write outputs. The only difference between modes is the final write step.
- `generate` writes `changelog.json` (all audience texts), `CHANGELOG.md`, and GitHub release notes from the technical rendering.
- `preview` runs the identical flow, including generation, but writes and publishes nothing.
- Adds `chartula preview` / `chartula generate` CLI commands, each taking `--tag` and `--repo <owner/name>`, with a usage screen, clear errors for unknown commands or missing options, and a readable per-audience summary. Pipeline errors are caught and reported rather than causing a crash.
- Verification: build clean (0 warnings, 0 errors); tests passing (Core 147, Infrastructure 26), confirming preview leaves all writers uncalled with empty `WrittenOutputs` while still producing all three renderings, and generate calls every writer and lists the outputs; CLI end-to-end verified for usage output, exit-1 on missing/invalid options, and graceful failure on an unresolved tag.
- Note: `--repo` is explicit for now; the interactive console reviewer is not yet wired in, so review mode still uses the auto-approve reviewer.

Closes #23 ([PR #63](https://github.com/goldbarth/chartula/pull/63))

### Feature: Store all audience texts in changelog.json

- Adds a `renderings` object to `ChangelogDocument`, keyed by audience (`technical` / `customer` / `product`) in a fixed order, keeping customer and product-manager texts in `changelog.json` rather than as separate files.
- `ChangelogJsonSerializer.Serialize` and the `IChangelogJsonWriter` port take an optional renderings map; when none is provided, the object is present but empty.
- Change entries remain deterministic facts; only the `renderings` are LLM-produced text.
- Documented in `docs/changelog-json.md`.
- `schemaVersion` stays at `1`; per the documented stability contract, this optional field addition is non-breaking, and old consumers ignore `renderings`.
- Verification: build clean (0 warnings, 0 errors); 144 Core tests and 26 Infrastructure tests passing, confirming customer/product texts are stored and round-tripped, `renderings` is an empty object when none are given, and only `changelog.json` is written to the output directory.

Closes #22 ([PR #62](https://github.com/goldbarth/chartula/pull/62))

### Feature: Write generated text back to GitHub release notes

- Adds the `IReleaseNotesWriter` port, reusing `RepositoryCoordinates`.
- Adds `GitHubReleaseNotesWriter` in `Chartula.Infrastructure`, using the GitHub REST API over a plain `HttpClient` with source-generated JSON: checks `GET /releases/tags/{tag}`, updates via `PATCH /releases/{id}` when found, or creates via `POST /releases` on 404, returning the release's `html_url`. API and network failures surface as clear `InvalidOperationException`s.
- Extracts the shared GitHub `HttpClient` setup into `GitHubHttpClientFactory`, used by both the PR reader and the release-notes writer.
- Because GitHub keys a release by its tag, re-running for the same tag updates that release's notes rather than creating a duplicate.
- Verification: build clean (0 warnings, 0 errors); 141 Core tests and 24 Infrastructure tests passing, covering the create path, the update-not-duplicate path, and API-error/network-failure/blank-tag paths against a routing stub handler.

Closes #21 ([PR #61](https://github.com/goldbarth/chartula/pull/61))

### Feature: Write CHANGELOG.md, prepend and preserve history

- Adds `ChangelogMarkdownComposer`, composing new content from an existing file and a release: the new section is prepended at the top, existing sections are kept verbatim, re-running the same tag replaces that section in place rather than duplicating it (idempotent, without reordering history), and a brand-new file gets a `# Changelog` title.
- Adds the `IChangelogMarkdownWriter` port in Core and `FileChangelogMarkdownWriter` in `Chartula.Infrastructure`, which reads the existing file and writes the composed result.
- Re-running an older release after a newer one does not move it above the newer one; running the same release twice yields a byte-identical file.
- Verification: build clean (0 warnings, 0 errors); 141 Core tests and 19 Infrastructure tests passing, covering new-file creation, prepend behavior, verbatim preservation of earlier sections, idempotency, in-place replacement without reordering, CRLF handling, and blank-tag rejection.

Closes #20 ([PR #60](https://github.com/goldbarth/chartula/pull/60))

### Feature: Opt-in review mode for human sign-off of flagged passages

- Adds `IReviewCoordinator`/`ReviewCoordinator`, gating each rendering on an opt-in toggle: when off (the default), text passes straight through without consulting the reviewer; when on, an `IReviewer` approves the text as-is or returns an edited version, and the coordinator returns the resulting `ReviewDecision`.
- Adds `ReviewPresentation`, formatting a rendering for a maintainer alongside its flagged passages from the rule-based and thorough faithfulness checks.
- Adds `AutoApproveReviewer` as the non-interactive default; the interactive console reviewer ships with the CLI command surface separately.
- Binds the `Chartula:Review` toggle in the CLI and registers the coordinator.
- Verification: build clean (0 warnings, 0 errors); 134 Core tests and 16 Infrastructure tests passing, covering the approve path, the edit path, the off-by-default toggle skipping the reviewer, and flagged-passage presentation; config binding verified end-to-end via `Chartula__Review__Enabled=true`.

Closes #19 ([PR #59](https://github.com/goldbarth/chartula/pull/59))

### Feature: Thorough second-pass LLM check with a toggle

- Adds `IThoroughFaithfulnessChecker`/`ThoroughFaithfulnessChecker`, running a second LLM pass via `CheckFaithfulnessAsync` to catch subtle, meaning-level hallucinations that the rule-based check cannot see. When the toggle is off, or there is nothing to check, it returns a faithful report with no LLM call.
- Adds the `ThoroughFaithfulnessOptions(Enabled = true)` toggle, on by default and disabled via `Chartula:Faithfulness:Thorough`.
- Moves the faithfulness prompt from an inline placeholder in `ChatModel` into `IChangelogPromptBuilder.BuildFaithfulnessPrompt`, adding an explicit meaning-level-distortion instruction.
- Removing the toggle or adding more granular check settings is deferred until there is observability data.
- Verification: build clean (0 warnings, 0 errors); 128 Core tests and 16 Infrastructure tests passing, covering flagging of unsupported claims via a stubbed second pass, defaults-on behavior, no-call behavior when disabled or on empty output, and prompt content; toggle verified end-to-end via `Chartula__Faithfulness__Thorough=false`.

Closes #18 ([PR #58](https://github.com/goldbarth/chartula/pull/58))

### Feature: Rule-based check that catches obvious hallucinations

- Adds `IRuleBasedFaithfulnessChecker`/`RuleBasedFaithfulnessChecker`, checking generated output against the fact base and returning a `FaithfulnessReport`. Flags a number not present in the facts (excluding PR numbers, linked issues, and numbers in titles/descriptions/tag), a quoted or backticked name absent from the facts, and a breaking-change claim when no fact is marked breaking.
- The checker has no `IChangelogModel` dependency, is constructed with no arguments, always runs with no toggle, and costs zero tokens.
- Flags are advisory, surfacing passages for review rather than causing hard failures. Uses source-generated regexes.
- Verification: build clean (0 warnings, 0 errors); 122 Core tests and 16 Infrastructure tests passing, covering flagging of an invented number, quoted name, and breaking claim; passing fully-supported output; not flagging supported numbers, names, or a genuine breaking change; determinism with no model dependency; and empty output passing.

Closes #17 ([PR #57](https://github.com/goldbarth/chartula/pull/57))

### Feature: Consistent formatting and tone per audience

- Adds `IChangelogFormatter`/`ChangelogFormatter` in `Chartula.Core`, normalizing model output with conservative, structure-preserving rules: normalized line endings, a single `- ` bullet marker, trimmed trailing whitespace, and collapsed blank-line runs, while leaving non-bullet lines intact. Applied to every rendering, so formatting is consistent regardless of model output.
- Adds a prompt rule instructing the model to write in one consistent voice and format, without carrying over an individual author's tone or phrasing.
- Tone normalization is handled via the prompt; formatting consistency is enforced deterministically in code, making it testable with a stubbed model.
- Verification: build clean (0 warnings, 0 errors); 114 Core tests and 16 Infrastructure tests passing, covering bullet/spacing/whitespace/blank-line normalization, headings left intact, idempotency, the generator applying the formatter, and the consistent-voice instruction present in the prompt.

Closes #16 ([PR #56](https://github.com/goldbarth/chartula/pull/56))

### Feature: Render technical, customer, and PM audiences from one fact base

- Adds `IReleaseRenderer`/`ReleaseRenderer`, rendering all three audiences from the same `FactBase` via one generator call per audience, returning a result per `Audience`; a failure in one audience does not fail the others.
- Audience selection is deterministic, in code rather than the LLM: customer omits non-user-visible changes and their links; technical keeps the pull request link and the full change set; product sees the full set.
- Updates the prompt so technical guidance also asks to keep links, customer is benefit-focused, and PM groups by theme.
- Because every audience derives from the same `FactBase`, the same established facts, there is no way for two renderings to disagree on what changed.
- Verification: build clean (0 warnings, 0 errors); 105 Core tests and 16 Infrastructure tests passing, covering all three renderings deriving from the same base, technical keeping links and the full set, customer dropping the internal change with no links, PM seeing the full set, and one failed audience leaving others intact, all via a stubbed model.

Closes #15 ([PR #55](https://github.com/goldbarth/chartula/pull/55))

### Feature: Prompt architecture that rephrases facts, never invents

- Adds `IChangelogPromptBuilder`/`ChangelogPromptBuilder`, producing a `ChangelogPrompt` (system + user). The system prompt pins the model to rephrasing only: never introduce a fact, number, or name not in the list; treat each fact's category and `(breaking)` marker as established; on thin facts, stay brief without padding or inventing detail; no preamble or conclusion, plus per-audience guidance. The user prompt carries only the facts.
- `ChatModel` now delegates to the builder and wires the prompt into the `IChatClient`.
- Categories and flags reach the model as text embedded by the generator; the prompt presents them verbatim and instructs the model not to decide them.
- Verification: build clean (0 warnings, 0 errors); 100 Core tests and 16 Infrastructure tests passing, covering facts and flags reaching the prompt, presence of the rephrase-only/category-established/stay-sparse instructions, a thin fact base not being padded, empty facts producing an empty user prompt, and per-audience tailoring; `ChatModel` tests updated for the new constructor, including a null-prompt-builder guard.

Closes #14 ([PR #53](https://github.com/goldbarth/chartula/pull/53))

### Feature: Generate a changelog through the provider interface

- Adds `IReleaseChangelogGenerator`/`ReleaseChangelogGenerator` and `ChangelogGenerationResult`, turning the fact base into grounded fact statements and making exactly one `IChangelogModel.RephraseAsync` call per release. An empty fact base makes no call at all.
- Provider failures are caught and returned as a failed result carrying the release tag and provider message; cancellation propagates rather than being swallowed.
- The generator depends only on `IChangelogModel`, with no provider type referenced.
- Verification: build clean (0 warnings, 0 errors); 89 Core tests and 16 Infrastructure tests passing, covering the single successful call, grounded-facts feeding, the provider-failure path, the empty-fact-base no-call case, and cancellation propagation, all via a fake `IChangelogModel`.

Closes #13 ([PR #52](https://github.com/goldbarth/chartula/pull/52))

### Feature: Write the fact base to changelog.json

- Adds `ChangelogDocument`, the stable on-disk shape (`schemaVersion` + `tag` + `changes`), kept separate from the domain `FactBase` so the domain can evolve without breaking the file format.
- Adds `ChangelogJsonSerializer` for pure, deterministic, source-generated conversion between `FactBase` and JSON, writing category as its name, plus the `IChangelogJsonWriter` port.
- Adds `FileChangelogJsonWriter` in `Chartula.Infrastructure` for the file I/O.
- `schemaVersion` (currently `1`) is the stability contract: fields are always present (including `null` values), adding optional fields is non-breaking, and removing/renaming/re-meaning a field bumps the version. Every field is a deterministic fact; nothing in the file is LLM-generated.
- Documented in `docs/changelog-json.md`.
- Verification: build clean (0 warnings, 0 errors); 84 Core tests and 16 Infrastructure tests passing, covering valid/parseable JSON matching the documented shape, round-tripping, empty renderings handling, temp-directory writing, file parsing, and missing-directory creation.

Closes #12 ([PR #51](https://github.com/goldbarth/chartula/pull/51))

### Feature: Make fact-base depth configurable

- Adds `FactBaseDepth` with three modes and `FactBaseDepthParser`: `TitleOnly` (title only), `TitleAndDescription` (the default, title + description, no issues), and `TitleDescriptionAndIssues` (title + description + linked issues). `FactBaseBuilder` honors the depth, including description from the middle mode up and linked issues only in the deepest mode.
- The CLI reads `Chartula:FactBase:Depth` and passes the parsed value into the builder; the parser accepts canonical names plus aliases (`title`, `description`, `full`) and raises a clear error on an unknown value.
- Whether all three modes survive long-term is left for revisiting with real data; the option set is not expanded here.
- Verification: build clean (0 warnings, 0 errors); 79 Core tests and 12 Infrastructure tests passing, covering the three depth behaviors and the parser's names, aliases, default, and unknown-value error; end-to-end verified for the default, a `title-only` override, and a clear startup failure on an unknown depth.

Closes #11 ([PR #50](https://github.com/goldbarth/chartula/pull/50))

### Feature: Transform curated changes into the release fact base

- Adds `IFactBaseBuilder`/`FactBaseBuilder` and the `FactBase` container (tag + one `ChangeFact` per included change), resolving changes with the missing-PR fallback, dropping filtered-out changes, and mapping each survivor to a `ChangeFact`.
- Category and breaking flag come from deterministic categorization; a label can force the category. `IsUserVisible` is derived from the category (outward-facing categories, plus every breaking change). `LinkedIssues` are parsed from GitHub closing keywords (`closes/fixes/resolves #n`) in the title and body.
- The builder has no LLM dependency; category and flags come from deterministic curation steps only.
- Verification: build clean (0 warnings, 0 errors); 64 Core tests and 12 Infrastructure tests passing, covering PR-to-fact mapping with curated category/flags and linked-issue extraction, exclusion of filtered changes, user-visible resolution including the breaking-change override, a label-forced category rescuing a chore, and the commit-data fallback.

Closes #10 ([PR #49](https://github.com/goldbarth/chartula/pull/49))

### Feature: Define the fact-base data model (index card per change)

- Adds `ChangeFact` in `Chartula.Core`, one structured object per change and the single source of truth the LLM may only rephrase from, capturing title, PR number, link, category, user-visible flag, breaking flag, linked issues, and an optional description populated per the fact-base depth.
- Every field is derived deterministically; nothing in the model is LLM-generated. PR-only fields (number, link) are nullable so commit-based changes fit the same shape.
- This is the per-change index card; the release-level container is assembled separately, and the whole base is serialized to `changelog.json` elsewhere.
- Verification: build clean (0 warnings, 0 errors); 58 Core tests and 12 Infrastructure tests passing, covering round-trip for a PR-based fact, a commit-based fact with no PR, and round-trip stability.

Closes #9 ([PR #48](https://github.com/goldbarth/chartula/pull/48))

### Feature: Drop internal/chore changes by default

- Adds `IChangeFilter`/`ChangeFilter` and `ChangeFilterRules`, deciding in order: a label that excludes the change wins outright, a breaking change is never dropped, otherwise the change is dropped when its effective category (label-forced, else deterministic) is in the excluded set. Default excluded set is `Internal`, overridable via config with an explicit list replacing the default.
- Binds the `Chartula:Filter` section in the CLI and registers the filter.
- A breaking change is never dropped, even if its category is excluded, as a deterministic safeguard from the breaking flag; an explicit label exclusion still wins over it.
- Verification: build clean (0 warnings, 0 errors); 55 Core tests and 12 Infrastructure tests passing, covering default internal/chore exclusion, user-facing categories kept, both config overrides, label exclusion, forced-category-into-excluded, only-labeled, the breaking safeguard, and label-exclusion precedence; config validated end-to-end for an unknown filter category failing at startup with a clear error.

Closes #8 ([PR #47](https://github.com/goldbarth/chartula/pull/47))

### Feature: Steer curation with label rules from config

- Adds `LabelRules` (excluded labels, label-to-category overrides, only-include-labeled mode) plus `ILabelRulePolicy`/`LabelRulePolicy`, producing a `LabelDecision`. Precedence: exclusion wins, then only-labeled drops unlabeled changes, otherwise the change is included with the first matching label deciding a forced category. All optional: `LabelRules.None` ignores labels entirely, with case-insensitive matching.
- Binds the `Chartula:Labels` section into `LabelRules` via `LabelRules.From`, parsing category names with a clear error on an unknown one, and registers the policy.
- Verification: build clean (0 warnings, 0 errors); 41 Core tests and 12 Infrastructure tests passing; config binding verified end-to-end for a valid `Chartula:Labels` config starting cleanly and an unknown category name failing at startup with a clear error listing valid categories.

Closes #7 ([PR #46](https://github.com/goldbarth/chartula/pull/46))

### Feature: Assign categories deterministically before the LLM

- Adds `IChangeCategorizer` and `ConventionalCommitCategorizer`, reading Conventional Commit conventions from the change title (`type(scope)!: subject`) to assign `ChangeCategory`: Feature (`feat`), Fix (`fix`), Performance (`perf`), Documentation (`docs`), Refactor (`refactor`), Internal (`build`/`ci`/`chore`/`test`/`style`/`revert`), and Other as the default for unrecognized/prefix-less titles.
- Breaking is tracked separately via `ChangeClassification.IsBreaking`, detected via a `!` marker, a `breaking` type, or a `BREAKING CHANGE` body note, so a breaking feature stays a feature but is still flagged.
- Pure and deterministic, with no LLM call or I/O involved; uses a source-generated regex.
- Verification: build clean (0 warnings, 0 errors); 33 Core tests and 12 Infrastructure tests passing, covering per-type prefix detection, scopes, case-insensitivity, all three breaking markers, the `Other` default, and determinism.

Closes #6 ([PR #45](https://github.com/goldbarth/chartula/pull/45))

### Feature: Degrade gracefully when clean PRs are missing

- Adds `IReleaseChangeResolver`/`ReleaseChangeResolver`, turning a `CommitRange` and merged `PullRequestInfo` list into `ReleaseChange` values (title, description, number, url, labels, `ChangeSource`, commit sha) as pure domain logic with no I/O.
- Behavior: merged PRs present yield one change per PR; no PRs at all falls back to one change per commit using the commit subject; a blank or uninformative PR title falls back to the PR body's first informative line, then to a generic `PR #n`; an empty release yields an empty set, never an exception.
- The uninformative-title heuristic is a small starter set, to become configurable separately.
- Verification: build clean (0 warnings, 0 errors); 13 Core tests and 12 Infrastructure tests passing, covering the PR-preferred path, commit fallback, blank-title fallback to body, uninformative-title fallback to body, number fallback, and the empty-release no-op.

Closes #5 ([PR #44](https://github.com/goldbarth/chartula/pull/44))

### Feature: Fetch merged PRs for a release from the GitHub API

- Adds the `IReleasePullRequestReader` port plus `PullRequestInfo` (number, title, description, labels, url) and `RepositoryCoordinates` as pure domain types.
- Adds `GitHubPullRequestReader` in `Chartula.Infrastructure`, querying GitHub's "pull requests associated with a commit" endpoint for each commit in a `CommitRange`, keeping merged PRs only and de-duplicating by number, with DTOs parsed via a source-generated `System.Text.Json` context.
- Configures the `HttpClient` (base URL, GitHub headers, bearer token by env-var name) in the CLI composition root and registers the reader.
- Uses raw `HttpClient` and `System.Text.Json` source generation over Octokit for a dependency-light, native-AOT-friendly approach, consistent with the git-CLI choice used elsewhere. The token is read by env-var name (`GITHUB_TOKEN`) and is optional, with public repos working unauthenticated subject to rate limits.
- API failures, including status, network, and malformed-response cases, all raise a clear `InvalidOperationException` rather than crashing.
- Verification: build clean (0 warnings, 0 errors); 5 Core tests and 12 Infrastructure tests passing, covering field mapping, merged-only filtering, de-duplication across commits, empty-range no-op, and the API/network/malformed error paths.
- Fallback behavior when clean PRs are missing is out of scope here, tracked separately.

Closes #4 ([PR #43](https://github.com/goldbarth/chartula/pull/43))

### Feature: Read the commit range for a release from git

- Adds the `IReleaseCommitReader` port plus `CommitInfo` and `CommitRange` (with `IsFirstRelease`) as pure domain types with no I/O.
- Adds `Chartula.Infrastructure` as a new layer, with `GitCliCommitReader` shelling out to `git` for the range since the previous tag, or all history up to the tag when there is no previous tag (first release), with clear errors for unknown or blank tags.
- Registers the git reader in the CLI composition root; the pipeline depends only on the port.
- Chooses the git CLI over LibGit2Sharp to avoid native dependencies that would conflict with the planned native-AOT binaries; `git` is present in any repo Chartula runs on.
- The new `Chartula.Infrastructure` layer keeps `Core` pure domain and `Cli` a thin composition root, and becomes the future home for the GitHub API, file writers, and webhooks.
- Verification: tests run the real `git` CLI against throwaway repositories, deterministic and offline, covering the between-tags range, first-release fallback, sha/subject mapping, and unknown-tag/blank-tag errors. Build clean (0 warnings, 0 errors); tests passing (Core 5, Infrastructure 6).

Closes #3 ([PR #42](https://github.com/goldbarth/chartula/pull/42))

### Feature: Abstract the LLM provider behind IChangelogModel

- Adds `Chartula.Core` as a new project, containing the domain-focused seam: `IChangelogModel` (the interface the pipeline depends on, with `RephraseAsync` and `CheckFaithfulnessAsync`), `ChatModel` as the single implementation backed by a provider-agnostic `Microsoft.Extensions.AI.IChatClient`, and domain types `Audience`, `GroundedFacts`, `RephraseRequest`, `FaithfulnessRequest`, `FaithfulnessReport`.
- Wires Anthropic as the first provider (`AsIChatClient`) in the CLI composition root, with model and provider selectable via config and API key read by env-var name; this is the only provider-specific code.
- Adds `Chartula.Core.Tests` as a new project, with 5 tests exercising the seam via a stub `IChatClient`, without a live provider call.
- Chosen architecture is a hybrid: a domain interface over an agnostic `IChatClient`, so swapping providers is a composition-root-only change. `GroundedFacts` and the `ChatModel` prompts are intentionally minimal placeholders, with fact-base and prompt design handled separately.
- Verification: build clean (0 warnings, 0 errors); `dotnet test`: 5/5 passing.

Closes #2 ([PR #41](https://github.com/goldbarth/chartula/pull/41))

### Fix: Two release blockers found by dogfooding v0.1.0

Both bugs were found by running `chartula preview --tag v0.1.0` against this repository and were not reachable from existing tests: one requires a live API call, the other requires real pull request bodies.

- **Truncation (`ChatModel`)**: calls went out without `ChatOptions`, so `MaxOutputTokens` was never set; the provider substituted its own default of 1024, cutting off all three audience texts mid-word (confirmed by run metrics showing 3 calls and 3,072 output tokens, exactly 3 × 1024). The run reported success, and the thorough check spent 56,712 tokens flagging the severed sentence as an unsupported claim, a bug symptom misread as a hallucination. The output ceiling is now always sent, configurable via `llm.maxOutputTokens`, defaulting to 16000.
- **False breaking changes (`ConventionalCommitCategorizer`)**: `MentionsBreakingChange` searched the whole body for `BREAKING CHANGE` as a case-insensitive substring, so prose discussing breaking changes was read as declaring one; six of thirty-three changes in v0.1.0 were mislabelled as breaking when none were. Now matches the Conventional Commits footer format: uppercase, start of line, colon-terminated.
- Verification: both fixes confirmed against a real run rather than tests alone. Rephrasing output went from 3,072 tokens (3 × 1024, mid-word endings) to 11,271 tokens (complete sentences); reported breaking changes went from 6 to 0; thorough-check claims went from 1 (the truncation artifact) to 0. 265 tests passing, 9 new, including a categorizer regression test using the sentence from the earlier PR verbatim as a fixture.
- Known, not fixed here: `RuleBasedFaithfulnessChecker` matches `\bbreaking\b` across the whole output and flags a breaking-change claim whenever the word appears, the same phrase-versus-assertion issue, now visible because no fact is breaking anymore. These flags are advisory and do not fail a run; separating a claim from prose using the word needs more than a regex, and is filed separately.

([PR #70](https://github.com/goldbarth/chartula/pull/70))

### Documentation: Bring the docs up to what Chartula actually is

Phase 1 was complete, but the docs still described a project still being planned.

- Prior issues: `Usage` was not runnable, calling the commands "planned entry points" and omitting the required `--tag` and `--repo` options; the `docs/` folder was linked from nowhere; `chartula.example.yaml` showed 4 of 8 supported sections, missing `github`, `labels`, `categories`, and `review`; the status badge said "early development" despite all 27 phase 1 issues being closed; CONTRIBUTING asked for "the .NET SDK" without specifying that an older one cannot build `net10.0`, and documented four commit scopes never actually used while the sixteen in real use went unmentioned.
- The wordmark now leads the README, switched via `<picture>` and `prefers-color-scheme` so it reads on either theme.
- Long-celled tables became prose: `Why Chartula`, `Core ideas`, and `Roadmap` are now prose and headings, since two columns of paragraph text collapse on a narrow screen. Tables with short facts (env vars, doc index) remain.
- Adds `docs/architecture.md`, documenting the layering and the reasoning behind dependency choices, previously living only in code and review comments, stating the inward-pointing rule, why facts are established before an LLM sees them, and where each concern lives.
- The documentation index in the README, and architecture/fixtures links from CONTRIBUTING, now point to existing files.
- Verification: all 24 relative links in `README.md`, `CONTRIBUTING.md`, and `docs/*.md` resolve to existing files; both SVGs are valid XML with no external references or `<script>`, rendered to PNG and checked against dark and light backgrounds; every section of `chartula.example.yaml` uncommented into a real `chartula.yaml` and run through the CLI, with all eight sections binding without a configuration error; every documented default checked against the value in code; build clean (0 warnings); 256 tests passing.
- Note: a brand asset delivery note that accompanied the SVGs is deliberately excluded, as it is in German, describes files not in the repo, and inaccurately describes Chartula.

([PR #69](https://github.com/goldbarth/chartula/pull/69))

### Refactor: Move prompt text into a partial class

- Splits `ChangelogPromptBuilder` into a `partial` class across two files: `ChangelogPromptBuilder.Prompts.cs` holding only the prompt strings (system header, the four rules, per-audience guidance), and `ChangelogPromptBuilder.cs` holding the composition logic referencing those constants.
- Separates prompt text from prompt build logic, so all prompt strings live in one place and wording iteration becomes text-only work, without navigating composition logic to find a string.
- The prompt text is byte-for-byte unchanged; the prompt-content assertions pass without modification, confirming no behavior change.
- Verification: build clean (0 warnings, 0 errors); tests passing and unchanged (Core 100, Infrastructure 16).

([PR #54](https://github.com/goldbarth/chartula/pull/54))

--- Customer ---
- **Run metrics summary**: Every `preview` and `generate` run now ends with a metrics report showing how many checks ran, how many issues each found, and how many tokens were spent — including whether the deeper (thorough) check caught anything the free check missed. Use this to decide whether the thorough check is worth keeping on.
- **Configurable category display**: Added a `categories` section to `chartula.yaml` to control the order categories appear in, their display names, and whether breaking changes are shown prominently.
- **`chartula.yaml` configuration file**: Chartula now reads settings from a `chartula.yaml` file (or `.yml`), letting you customize behavior without touching code. The tool still works with no configuration file at all, using sensible defaults. A minimal example file is included; full documentation covers every option. Configuration mistakes now show a clear error message instead of crashing.
- **`preview` and `generate` commands**: The CLI now has working `preview` and `generate` commands. `generate` produces and writes the changelog files and updates the GitHub release notes. `preview` runs the same process but writes and publishes nothing, so you can see the result first. Both give clear feedback, including helpful errors for missing or invalid options.
- **All audience texts saved in `changelog.json`**: The customer-facing and product-manager texts are now stored alongside the technical version inside `changelog.json`, instead of being written as separate files in your repository.
- **GitHub release notes are updated automatically**: Generated release text is now written directly to the GitHub release notes. Running it again for the same tag updates the existing release notes instead of creating a duplicate.
- **`CHANGELOG.md` is maintained automatically**: Each release now adds a new section to the top of `CHANGELOG.md`, keeping all previous history intact. Running the same release again updates that section in place rather than duplicating it.
- **Optional review mode**: You can now enable a review step where generated text is shown for approval before publishing, along with any passages flagged by the checks. You can approve as-is or edit the text. This is off by default.
- **Deeper hallucination check**: Added an optional second-pass check that catches subtler mistakes than a plain fact check can, such as text that changes the meaning of a change (for example, describing a bug fix as something more severe). It's on by default and can be turned off.
- **Basic hallucination check, always on and free**: Added a lightweight check that catches obvious mistakes — made-up numbers, invented feature names, or breaking-change claims not backed by facts — with no added cost, since it doesn't use the AI model at all.
- **Consistent formatting across releases**: Generated text is now automatically cleaned up for consistent formatting (bullet style, spacing, line breaks) and written in one consistent voice, regardless of how the original pull requests were written.
- **Three versions of every release, always consistent**: Chartula now generates technical, customer-facing, and product-manager versions of each release from the same set of facts, so they can never contradict one another. Technical notes keep links and full detail; customer notes focus on benefits and skip internal-only changes; product notes are grouped by theme.
- **More reliable, fact-grounded text generation**: Reworked how instructions are sent to the AI model so it only rephrases the given facts and never invents details, numbers, or names. When there's little information to work with, the output stays brief instead of being padded out.
- **Real changelog generation**: Chartula now actually generates changelog text through the connected AI model for each release, making exactly one request per release (and none if there's nothing to report). Errors from the AI provider are handled gracefully instead of crashing the tool.
- **Fact base saved to `changelog.json`**: Each release's underlying facts are now saved to a `changelog.json` file, giving you a durable, machine-readable record that can also feed future outputs. The file format is documented and versioned for stability.
- **Adjustable level of detail for source material**: You can now configure how much information feeds into each release's facts — title only, title plus description, or title, description, and linked issues. The default is title plus description.
- **Complete fact base per release**: Chartula now assembles a full set of facts for each release, combining pull request data, categorization, and any label overrides, ready to feed into generation.
- **Structured per-change data**: Each change is now captured as a structured record — title, PR link, category, visibility, breaking flag, and linked issues — ensuring nothing in the generated text is made up.
- **Internal changes hidden by default**: Internal and maintenance-only changes are now excluded from the changelog by default. This can be customized, and breaking changes are never hidden even if their category would otherwise be excluded.
- **Label-based control over what gets included**: You can now use GitHub labels to exclude specific pull requests, force them into a particular category, or restrict the changelog to only labeled pull requests — all configurable, and with no effect if you don't use labels.
- **Automatic categorization**: Changes are now automatically categorized (feature, fix, performance, docs, refactor, internal, or other) based on standard commit conventions, before any AI involvement, so the kind of change is never guessed by the model. Breaking changes are flagged separately and always retain their original category.
- **Graceful handling of messy pull requests**: When a release has no linked pull requests, or when PR titles are missing or unhelpful, Chartula now falls back to commit messages or PR descriptions rather than failing.
- **Pull request data fetched from GitHub**: Chartula now looks up the merged pull requests behind each release directly from GitHub, using their titles, descriptions, and labels, instead of relying only on raw commits.
- **Accurate commit range per release**: Chartula now correctly determines which commits belong to each release, including correctly handling your very first release when there's no previous tag to compare against.
- **Foundation for AI-generated text**: Added the underlying support for generating changelog text through an AI model, with the first supported provider connected. API keys are read from your environment, never hardcoded.
- **Fixed: cut-off changelog text and mislabeled breaking changes**: Generated text could be cut off mid-sentence in some runs because no output length limit was set; there's now a configurable ceiling with a higher default, so text completes properly. Separately, changes that merely discussed "breaking changes" in their description were sometimes incorrectly labeled as breaking themselves; the detection now only matches an actual breaking-change declaration, not any mention of the phrase.

--- Product ---
## Run Metrics & Cost Visibility
- Feature: Every preview and generate run now ends with a metrics summary showing how many checks ran, what each found, and the tokens spent — including a line isolating what the thorough check caught that the free check missed, so its cost-effectiveness can be judged from real data instead of guesswork.

## Configuration
- Feature: A new `categories` section in `chartula.yaml` sets category order, display names, and whether breaking changes are shown prominently, rounding out the configuration surface alongside the existing `labels`, `factBase`, and `faithfulness` sections.
- Feature: `chartula.yaml` is now read for configuration, with environment variables able to override it. The tool still runs with sensible defaults when no file is present, and a minimal example file ships alongside full documentation of every option.
- Feature: The amount of source material used to build the fact base is now configurable, with three modes — title only, title and description, or title, description, and linked issues — defaulting to title and description.
- Feature: GitHub labels can now steer curation from configuration: excluding a change, forcing it into a category, or restricting the changelog to only labeled changes. The tool still works normally with no labels at all.
- Feature: Internal and chore changes are excluded from the changelog by default, with the excluded categories overridable in configuration. Breaking changes are never dropped, regardless of category.

## Command Line Interface
- Feature: `chartula preview` and `chartula generate` commands are now available, each taking `--tag` and `--repo`. Both run the full pipeline; `generate` writes and publishes the results, while `preview` shows the same result without writing or publishing anything.

## Release Outputs
- Feature: Generated technical, customer, and product-manager texts are now stored in `changelog.json` alongside the deterministic change facts, keeping everything in one file rather than scattered as separate marketing files.
- Feature: Each release is now written as a new section at the top of `CHANGELOG.md`, preserving existing history; re-running the same release updates its section in place instead of duplicating it.
- Feature: Generated release notes are now written directly to the GitHub release, updating the existing release rather than creating a duplicate when run again for the same tag.
- Feature: The release fact base is now written to `changelog.json` as a stable, versioned, machine-readable record, with a documented stability contract for future consumers.

## Review Mode
- Feature: An optional review mode lets a maintainer inspect generated text with flagged passages highlighted before it's published, approving it as-is or editing it. Review is off by default and can be turned on with a single toggle.

## Faithfulness Checking
- Feature: A free, always-on check now flags obvious hallucinations — invented numbers, invented quoted names, or breaking-change claims not backed by a fact — before any LLM check runs.
- Feature: A second, LLM-based check now catches subtler hallucinations the first check can't see, such as meaning-level distortions in the generated text. It's on by default and can be disabled with a single toggle.

## Generation & Rendering
- Feature: Generation now makes a real call through the LLM provider interface — exactly one call per release, and none for an empty fact base — with provider failures handled gracefully instead of crashing.
- Feature: A first-class prompt architecture now instructs the model to only rephrase established facts, never invent or pad them, with categories and flags supplied as given rather than decided by the model.
- Feature: Technical, customer, and product-manager versions of a release are now all rendered from the same fact base, so they can never contradict each other. Customer text omits non-user-visible changes, technical keeps full detail and links, and product-manager groups by theme.
- Feature: Formatting is now normalized consistently across every rendering, and the model is instructed to write in one consistent voice regardless of how the individual source material was written.

## Fact Base
- Feature: A new structured fact object captures the established details of each change — title, PR number, link, category, visibility, breaking flag, and linked issues — none of it LLM-generated.
- Feature: Curated changes are now assembled into a complete fact base for a release, with category and flags coming from deterministic curation rather than the LLM.

## Source Data Collection
- Feature: The tool can now determine the exact commit range belonging to a release, including the first-release case with no prior tag.
- Feature: Merged pull requests associated with a release's commits are now fetched from GitHub, providing title, description, labels, and link for each.
- Feature: When pull request discipline is imperfect, the tool now degrades gracefully — falling back to commit data when there are no PRs, and to the PR body or a generic label when a title is blank or uninformative.
- Feature: Each change is now assigned a category deterministically from its conventional-commit prefix, with breaking changes tracked separately so a breaking feature is still recognized as a feature.

## LLM Provider Abstraction
- Feature: LLM operations are now abstracted behind a provider-agnostic interface, with a single implementation currently backed by Anthropic. API keys are read from configuration or environment, never hardcoded.

## Fixes
- Fix: Two release-blocking bugs found by dogfooding the first release have been fixed. Generated text was being silently truncated because no output-token ceiling was sent to the provider; a ceiling is now always sent and is configurable. Separately, prose merely discussing breaking changes was being mislabelled as an actual breaking change; the check now matches only the proper marker.

## Documentation
- Documentation: Documentation has been brought up to date with what the tool actually does: usage instructions are now runnable as written, the docs folder is linked from the README, the example configuration file shows all supported sections, the project status reflects completion of phase one, and contributor build instructions match reality.

## Internal Refactor
- Refactor: Prompt wording was moved into its own file, separate from the logic that assembles the prompt, with no change in behavior.

Preview only - nothing was written or published.

Run metrics
  Rule-based check: 3 runs, 0 with findings, 0 claims, no tokens
  Thorough check:   3 runs, 0 with findings, 0 claims, 72,699 in / 6,982 out
    caught 0 claims the rule-based check missed, for 79,681 tokens in 3 calls
  Rephrasing:       3 calls, 54,874 in / 22,151 out
  Total:            156,706 tokens
