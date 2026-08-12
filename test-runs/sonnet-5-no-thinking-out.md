Preview changelog for v0.1.0

--- Technical ---
feat: report what a run does and what it costs

Every `preview` and `generate` run now ends with a metrics summary showing rule-based check runs/findings/claims, thorough check runs/findings/claims and token usage, and rephrasing token usage, with a total. The summary highlights claims caught only by the thorough check (excluding claims both checks find), paired with the tokens spent to catch them, so a keep-or-drop decision on the thorough check can be made from data rather than guesswork.

What changed:
- `Chartula.Core/Observability/`: added `IRunMetrics` with the `RunMetrics` sink, `NullRunMetrics`, `RunReport`, and `RunReportFormatter`.
- `ChatModel` now reports token usage, attributed per `LlmOperation`; a provider that reports no usage still has its call counted.
- `ReleasePipeline` records both checks' findings in a single call and returns the report on `ReleaseOutcome`.
- The sink is optional everywhere; a run without one produces byte-identical output.
- Added `docs/run-metrics.md` explaining how to read the summary.

Verification: `dotnet build` clean; `dotnet test` 215 passing (21 new), covering check-fire counts, per-operation token usage, thorough-only attribution, snapshot isolation, and concurrent recording. Verified end-to-end against the real DI graph and formatter output.

Closes #26 ([PR #66](https://github.com/goldbarth/chartula/pull/66))

---

feat: add configuration sections for categories

Adds a `categories` configuration section alongside the existing `labels`, `factBase`, and `faithfulness` sections, covering category order, display names, and breaking-change prominence.

What changed:
- Added `CategorySettings` in the domain, holding category order, display names, and breaking-change prominence; `From(...)` parses raw configuration values and rejects unknown category names with a clear error message.
- Extracted `GroundedFactsFactory` out of `ReleaseChangelogGenerator`, giving audience filtering, category ordering, and display naming a single home.
- Added the `categories` section to `chartula.yaml`: `order`, `names`, `breakingProminent` (default `true`). Sections remain independently editable; untouched sections keep their defaults.
- Documented the new section in `docs/configuration.md`.

Verification: `dotnet build` clean; `dotnet test` 194 passing (17 new). End-to-end: an invalid category name exits 1 with `Configuration error: Unknown category 'nonsense' in categories order. Valid categories: ...`; a valid `categories` section binds and reaches the pipeline.

Closes #25 ([PR #65](https://github.com/goldbarth/chartula/pull/65))

---

feat(config): read chartula.yaml with sensible defaults

Adds `chartula.yaml` as an optional configuration source; the tool continues to run with sensible defaults when no configuration is present.

What changed:
- `Chartula.Cli`: `AddChartulaYaml` loads `chartula.yaml` (or `.yml`) via YamlDotNet and flattens it into `Chartula:*` configuration keys, layered before environment variables (env overrides YAML). All existing section options (`llm`, `github`, `labels`, `filter`, `factBase`, `faithfulness`, `review`) are now readable from the file; with neither a file nor env vars, every option binds to its default.
- Added `chartula.example.yaml` at the repo root: minimal, everything commented out.
- Added `docs/configuration.md` documenting the full option set with defaults.
- Configuration errors (e.g. an invalid value in `chartula.yaml`) are now reported as a `Configuration error: ...` message instead of an unhandled exception.
- Added `Chartula.Cli.Tests` (new project, `InternalsVisibleTo` from the CLI) as the home for CLI-level tests.

Verification: build clean; tests green (Core 147, Infrastructure 26, Cli 5): YAML flattening to prefixed keys, no-config defaults, a present config refining `factBase.depth`/`faithfulness.thorough`, absent file as a no-op, and reading `chartula.yaml` from a directory. End-to-end: an invalid `depth` value prints a clear `Configuration error: ...`, and an environment variable overrides the YAML value.

Note: `chartula.example.yaml` is shipped rather than a live `chartula.yaml`, so it is not picked up when running Chartula in its own repo.

Closes #24 ([PR #64](https://github.com/goldbarth/chartula/pull/64))

---

feat(cli): generate and preview commands wired to the pipeline

Adds a CLI command surface and ties the pipeline together end to end.

What changed:
- `Chartula.Core`: added `ReleasePipeline`, orchestrating the flow over ports only — read commit range and PRs, build fact base, render all audiences, run rule-based and thorough faithfulness checks plus review, then write outputs. The only difference between the two modes is the final write step.
- `generate` writes `changelog.json` (all audience texts), `CHANGELOG.md`, and the GitHub release notes from the technical rendering.
- `preview` runs the identical flow, including generation, but writes and publishes nothing.
- `Chartula.Cli`: added `chartula preview` / `chartula generate`, each taking `--tag` and `--repo <owner/name>`; a usage screen; clear errors for unknown commands or missing options; a per-audience summary. Pipeline errors are caught and reported rather than crashing.

Verification: build clean; tests green (Core 147, Infrastructure 26): preview leaves all three writer spies uncalled and `WrittenOutputs` empty while still producing all three renderings; generate calls every writer and lists the outputs. End-to-end: usage on no args, exit-1 with a clear message for missing `--tag` / invalid `--repo` / unknown command, and `preview` failing gracefully rather than crashing.

Note: `--repo` is explicit for now; auto-detecting it from the git remote is a future consideration. The interactive console reviewer is not wired here — review mode still uses the auto-approve reviewer.

Closes #23 ([PR #63](https://github.com/goldbarth/chartula/pull/63))

---

feat(output): store all audience texts in changelog.json

Stores the customer and product-manager texts in `changelog.json` rather than as separate marketing files in the repo.

What changed:
- `Chartula.Core`: `ChangelogDocument` gains a `renderings` object keyed by audience (`technical` / `customer` / `product`), written in a fixed order. `ChangelogJsonSerializer.Serialize` and the `IChangelogJsonWriter` port take an optional renderings map; the object is present but empty when none are provided.
- Change entries remain deterministic facts; only the `renderings` are LLM-produced text.
- Documented the new field in `docs/changelog-json.md`.

`schemaVersion` remains 1 — per the documented stability contract, adding an optional field is non-breaking, and old consumers ignore `renderings`.

Verification: build clean; tests green (Core 144, Infrastructure 26): customer/product texts stored and round-tripped, `renderings` empty when none given, and the writer produces only `changelog.json`.

Closes #22 ([PR #62](https://github.com/goldbarth/chartula/pull/62))

---

feat(releases): write the generated text back to GitHub release notes

Writes the generated technical text to the GitHub release notes.

What changed:
- `Chartula.Core`: added the `IReleaseNotesWriter` port (reuses `RepositoryCoordinates`).
- `Chartula.Infrastructure`: added `GitHubReleaseNotesWriter` over the GitHub REST API (plain `HttpClient`, source-generated JSON, AOT-friendly). `GET /releases/tags/{tag}` — if found, `PATCH /releases/{id}` updates in place; on 404, `POST /releases` creates the release. Returns the release's `html_url`; API/network failures become clear `InvalidOperationException`s.
- `Chartula.Cli`: registers the writer. Extracted the shared `GitHubHttpClientFactory`, now used by both the PR reader and the release-notes writer.

Re-running for the same tag hits the found path and updates that release's notes rather than creating a duplicate, since GitHub keys a release by its tag.

Verification: build clean; tests green (Core 141, Infrastructure 24): create when no release exists, update the found release without creating a second one, and the API-error / network-failure / blank-tag paths — all against a routing stub handler.

Closes #21 ([PR #61](https://github.com/goldbarth/chartula/pull/61))

---

feat(output): write CHANGELOG.md, prepend and preserve history

Writes each release as a new section at the top of `CHANGELOG.md`, preserving history and never overwriting it.

What changed:
- `Chartula.Core`: added `ChangelogMarkdownComposer` (pure logic), which composes new content from the existing file and a release. The new section is prepended at the top; existing sections are kept verbatim; re-running the same tag replaces that section in place rather than duplicating it, without reordering history. A brand-new file gets a `# Changelog` title.
- Added the `IChangelogMarkdownWriter` port in Core and `FileChangelogMarkdownWriter` in `Chartula.Infrastructure`, which reads the existing file and writes the composed result.
- `Chartula.Cli`: registers the writer alongside the JSON writer.

Re-running an older release after a newer one does not move it above the newer one; running the same release twice yields a byte-identical file.

Verification: build clean; tests green (Core 141, Infrastructure 19): new-file creation, prepend above existing history, verbatim preservation of earlier sections, idempotency on re-run, in-place replace without reordering, CRLF handling, and blank-tag rejection.

Closes #20 ([PR #60](https://github.com/goldbarth/chartula/pull/60))

---

feat(review): opt-in review mode for human sign-off of flagged passages

Adds an opt-in review mode letting a maintainer review generated texts before publishing.

What changed:
- `Chartula.Core`: added `IReviewCoordinator`/`ReviewCoordinator`, gating each rendering on an opt-in toggle. With review off (default), text passes straight through as approved and the reviewer is never consulted. With review on, the item goes to an `IReviewer`, which approves it as-is or returns an edited version; the coordinator returns the resulting `ReviewDecision`.
- Added `ReviewPresentation`, formatting an item for a maintainer — the generated text followed by highlighted flagged passages from the rule-based and thorough checks.
- Added `AutoApproveReviewer` as the non-interactive default; the interactive console reviewer ships with the CLI command surface.
- `Chartula.Cli`: binds the `Chartula:Review` toggle and registers the coordinator.

Verification: build clean; tests green (Core 134, Infrastructure 16): approve keeps the original, edit returns the corrected text, an off toggle skips the reviewer entirely, the option is off by default, and flagged passages are presented/highlighted. Config binding verified end-to-end via `Chartula__Review__Enabled=true`.

Closes #19 ([PR #59](https://github.com/goldbarth/chartula/pull/59))

---

feat(faithfulness): thorough second-pass LLM check with a toggle

Adds a second-pass LLM check that catches subtle, meaning-level hallucinations the rule-based check cannot see.

What changed:
- `Chartula.Core`: added `IThoroughFaithfulnessChecker`/`ThoroughFaithfulnessChecker`, running a second LLM pass via `CheckFaithfulnessAsync`, turning the fact base into grounded facts and flagging unsupported claims. When the toggle is off, or there is nothing to check, it returns a faithful report with no LLM call.
- Added a toggle, `ThoroughFaithfulnessOptions(Enabled = true)`, on by default and disabled via the `Chartula:Faithfulness:Thorough` config key.
- Moved the faithfulness prompt from an inline placeholder in `ChatModel` into `IChangelogPromptBuilder.BuildFaithfulnessPrompt`, consistent with the partial-class pattern, with an explicit meaning-level-distortion instruction.
- `Chartula.Cli`: binds the toggle and registers the checker.

Out of scope: removing the toggle or adding more granular check settings is deferred until observability data is available.

Verification: build clean; tests green (Core 128, Infrastructure 16): the second pass flags unsupported claims via a stubbed model, feeds output plus grounded facts, defaults on, and makes no call when disabled or when the output is empty. Toggle verified end-to-end via `Chartula__Faithfulness__Thorough=false`.

Closes #18 ([PR #58](https://github.com/goldbarth/chartula/pull/58))

---

feat(faithfulness): rule-based check that catches obvious hallucinations

Adds a zero-cost rule-based check that catches crude hallucinations before any LLM check.

What changed:
- `Chartula.Core`: added `IRuleBasedFaithfulnessChecker`/`RuleBasedFaithfulnessChecker`, checking generated output against the fact base and returning a `FaithfulnessReport`. It flags a number in the output not present in the facts (excluding PR numbers, linked issues, and numbers in titles/descriptions/tag), a quoted or backticked name absent from the facts, and a breaking-change claim when no fact is marked breaking.
- `Chartula.Cli`: registers the checker.

Flags are advisory, surfacing passages for review rather than causing hard failures. Uses source-generated regexes (AOT-friendly). The checker has no `IChangelogModel` dependency, so it costs zero tokens and always runs, with no toggle.

Verification: build clean; tests green (Core 122, Infrastructure 16): flags an invented number / quoted name / breaking claim; passes fully-supported output; does not flag supported numbers, names, or a genuine breaking change; deterministic with no model dependency; empty output passes.

Closes #17 ([PR #57](https://github.com/goldbarth/chartula/pull/57))

---

feat(formatting): consistent formatting and tone per audience

Makes each rendering read as one coherent document, regardless of how the source PRs were written.

What changed:
- `Chartula.Core`: added `IChangelogFormatter`/`ChangelogFormatter`, normalizing model output with conservative, structure-preserving rules — normalized line endings, a single `- ` bullet marker, trimmed trailing whitespace, and collapsed blank-line runs — while leaving non-bullet lines (headings, prose) intact. The generator applies it to every rendering.
- Added a prompt rule instructing the model to write in one consistent voice and format, without carrying over an individual author's tone or phrasing.
- `Chartula.Cli`: registers the formatter.

Tone normalization is handled via the prompt, since it is a language judgment; formatting consistency is enforced deterministically in code, which also makes it testable with a stubbed model.

Verification: build clean; tests green (Core 114, Infrastructure 16): bullet/spacing/whitespace/blank-line normalization, headings left intact, idempotency, the generator applying the formatter to model output, and the consistent-voice instruction present in the prompt.

Closes #16 ([PR #56](https://github.com/goldbarth/chartula/pull/56))

---

feat(rendering): render technical, customer, and PM from one fact base

Produces technical, customer, and product-manager versions of a release from one fact base, so they cannot contradict each other.

What changed:
- `Chartula.Core`: added `IReleaseRenderer`/`ReleaseRenderer`, rendering all three audiences from the same `FactBase`, delegating to the generator (one call per audience) and returning a result per `Audience`. A failure in one audience does not fail the others.
- Audience selection is deterministic, handled in code rather than by the LLM: customer omits non-user-visible changes and their links; technical keeps the pull request link and the full change set; product sees the full set.
- Updated prompt guidance: technical keeps links; customer is benefit-focused; PM groups by theme.
- `Chartula.Cli`: registers the renderer.

Because every audience is derived from the same `FactBase`, there is no way for two renderings to disagree on what changed.

Verification: build clean; tests green (Core 105, Infrastructure 16): all three derive from the same base, technical keeps links plus the full set, customer drops the internal change and carries no links, PM sees the full set, and one failed audience leaves the others intact — all via a stubbed model.

Closes #15 ([PR #55](https://github.com/goldbarth/chartula/pull/55))

---

feat(prompting): prompt architecture that rephrases facts, never invents

Replaces the placeholder prompt with a first-class, testable prompt architecture that keeps output trustworthy.

What changed:
- `Chartula.Core`: added `IChangelogPromptBuilder`/`ChangelogPromptBuilder`, producing a `ChangelogPrompt` (system + user). The system prompt pins the model to rephrasing: never introduce a fact, number, or name not in the list; treat each fact's category and `(breaking)` marker as established, using them as given rather than inferring or changing them; on thin facts stay brief without padding, speculating, or inventing detail; no preamble or conclusion — plus per-audience guidance. The user prompt carries only the facts.
- `ChatModel` now delegates to the builder and wires the prompt into the `IChatClient`.
- `Chartula.Cli`: registers the builder in the LLM composition.

Categories and flags reach the model as text embedded by the generator; the prompt presents them verbatim and instructs the model not to decide them.

Verification: build clean; tests green (Core 100, Infrastructure 16): facts and flags reach the prompt, the rephrase-only / category-established / stay-sparse instructions are present, a thin fact base is not padded, empty facts give an empty user prompt, and the prompt is tailored per audience. `ChatModel` tests updated for the new constructor, including a null-prompt-builder guard.

Closes #14 ([PR #53](https://github.com/goldbarth/chartula/pull/53))

---

feat(generation): generate a changelog through the provider interface

Makes generation work through the provider seam, while staying provider-agnostic.

What changed:
- `Chartula.Core`: added `IReleaseChangelogGenerator`/`ReleaseChangelogGenerator` and `ChangelogGenerationResult`. Turns the fact base into grounded fact statements and makes exactly one `IChangelogModel.RephraseAsync` call per release; an empty fact base makes no call at all. Provider failures are caught and returned as a failed result carrying the release tag and provider message; cancellation propagates rather than being swallowed.
- `Chartula.Cli`: registers the generator over the existing LLM services.

The generator depends only on `IChangelogModel`, with no provider type referenced.

Verification: build clean; tests green (Core 89, Infrastructure 16): the single successful call, grounded-facts feeding, the provider-failure path, the empty-fact-base no-call, and cancellation propagation — all via a fake `IChangelogModel`.

Closes #13 ([PR #52](https://github.com/goldbarth/chartula/pull/52))

---

feat(serialization): write the fact base to changelog.json

Writes the release fact base to `changelog.json` as a durable, machine-readable record and a source for later outputs.

What changed:
- `Chartula.Core`: added `ChangelogDocument`, the stable on-disk shape (`schemaVersion` + `tag` + `changes`), kept separate from the domain `FactBase` so the domain can evolve without breaking the file format. Added `ChangelogJsonSerializer` to convert `FactBase` to and from JSON — pure, deterministic, and source-generated (AOT/trim-safe), with category written as its name. Added the `IChangelogJsonWriter` port.
- `Chartula.Infrastructure`: added `FileChangelogJsonWriter`, writing `changelog.json` to a directory.
- Documented the schema, field types, and stability contract in `docs/changelog-json.md`.
- `Chartula.Cli`: registers the writer.

`schemaVersion` (currently 1) is the stability contract: fields are always present, including `null` values; adding optional fields is non-breaking, while removing, renaming, or re-meaning a field bumps the version. Every field is a deterministic fact.

Verification: build clean; tests green (Core 84, Infrastructure 16): serializer output is valid/parseable JSON matching the documented shape and round-trips; the file writer writes to a temp dir, the file parses and round-trips, and missing directories are created.

Closes #12 ([PR #51](https://github.com/goldbarth/chartula/pull/51))

---

feat(facts): make fact-base depth configurable

Lets a maintainer choose how much source material feeds the fact base.

What changed:
- `Chartula.Core`: added `FactBaseDepth` with three modes plus `FactBaseDepthParser`: `TitleOnly` (title only), `TitleAndDescription` (the default — title plus description, no issues), and `TitleDescriptionAndIssues` (title plus description plus linked issues). `FactBaseBuilder` honors the depth, including description from the middle mode up and linked issues only in the deepest mode.
- `Chartula.Cli`: reads `Chartula:FactBase:Depth` and passes the parsed value into the builder. The parser accepts canonical names plus aliases (`title`, `description`, `full`) and raises a clear error on an unknown value.

Out of scope: whether all three modes survive long-term is revisited with real data; the option set is not expanded here.

Verification: build clean; tests green (Core 79, Infrastructure 12): the three depth behaviors and the parser (names, aliases, default, unknown-value error). End-to-end: default and a `title-only` override both start cleanly, and an unknown depth fails at startup with a clear error.

Closes #11 ([PR #50](https://github.com/goldbarth/chartula/pull/50))

---

feat(facts): transform curated changes into the release fact base

Assembles the complete, grounded fact base for a release.

What changed:
- `Chartula.Core`: added `IFactBaseBuilder`/`FactBaseBuilder` and the `FactBase` container (tag plus one `ChangeFact` per included change). Resolves changes with the missing-PR fallback, drops filtered-out changes, and maps each survivor to a `ChangeFact`. Category and breaking flag come from deterministic categorization, with a label able to force the category. `IsUserVisible` is derived from the category (outward-facing categories, plus every breaking change). `LinkedIssues` are parsed from GitHub closing keywords (`closes/fixes/resolves #n`) in the title and body.
- `Chartula.Cli`: registers the builder.

Category and flags come from the deterministic curation steps, never from an LLM — the builder has no LLM dependency.

Verification: build clean; tests green (Core 64, Infrastructure 12): PR-to-fact mapping with curated category/flags and linked-issue extraction, exclusion of filtered changes, user-visible resolution including the breaking-change override, a label-forced category rescuing a chore, and the commit-data fallback.

Closes #10 ([PR #49](https://github.com/goldbarth/chartula/pull/49))

---

feat(facts): define the fact-base data model (index card per change)

Defines `ChangeFact` in `Chartula.Core` — one structured object per change, the single source of truth the LLM may only rephrase from.

What changed:
- Captures established facts: title, PR number, link, category (from deterministic categorization), user-visible flag, breaking flag, linked issues, and an optional description (populated per the fact-base depth). Every field is derived deterministically; nothing in the model is LLM-generated. PR-only fields (number, link) are nullable so commit-based changes fit the same shape.

This is the per-change "index card"; the release-level container is assembled separately, and the whole base is serialized to `changelog.json` elsewhere.

Verification: build clean; tests green (Core 58, Infrastructure 12): round-trip for a PR-based fact, a commit-based fact with no PR, and round-trip stability.

Closes #9 ([PR #48](https://github.com/goldbarth/chartula/pull/48))

---

feat(filtering): drop internal/chore changes by default

Keeps the changelog relevant by filtering out internal/chore changes, combining deterministic categorization and label rules.

What changed:
- `Chartula.Core`: added `IChangeFilter`/`ChangeFilter` and `ChangeFilterRules`. Decision order: a label that excludes the change wins outright; a breaking change is never dropped; otherwise the change is dropped when its effective category (a label-forced one, else the deterministic one) is in the excluded set. Default excluded set is `Internal`, overridable via config — an explicit (possibly empty) list replaces the default.
- `Chartula.Cli`: binds the `Chartula:Filter` section and registers the filter.

A breaking change is never dropped, even if its category is excluded, as a deterministic safeguard matching the intent to show breaking changes prominently; an explicit label exclusion still wins over it.

Verification: build clean; tests green (Core 55, Infrastructure 12): default internal/chore exclusion, user-facing categories kept, both config overrides, label exclusion, forced-category-into-excluded, only-labeled, the breaking safeguard, and label-exclusion precedence. Config validated end-to-end: an unknown `Chartula:Filter` category name fails at startup with a clear error.

Closes #8 ([PR #47](https://github.com/goldbarth/chartula/pull/47))

---

feat(labels): steer curation with label rules from config

Lets a maintainer steer curation with GitHub labels, controlled from configuration.

What changed:
- `Chartula.Core`: added `LabelRules` (excluded labels, label-to-category overrides, only-include-labeled mode) plus `ILabelRulePolicy`/`LabelRulePolicy`, producing a `LabelDecision` (include plus optional forced category). Precedence: exclusion wins; then only-labeled drops unlabeled changes; otherwise included, with the first matching label deciding a forced category. All optional — `LabelRules.None` ignores labels entirely. Matching is case-insensitive.
- `Chartula.Cli`: binds the `Chartula:Labels` section into `LabelRules` via `LabelRules.From` (parses category names, with a clear error on an unknown one) and registers the policy.

Verification: build clean; tests green (Core 41, Infrastructure 12). Config binding verified end-to-end: a valid `Chartula:Labels` config starts cleanly, and an unknown category name fails at startup with a clear error listing valid categories.

Closes #7 ([PR #46](https://github.com/goldbarth/chartula/pull/46))

---

feat(categorization): assign categories deterministically before the LLM

Decides the kind of each change in code, before any generation.

What changed:
- `Chartula.Core`: added `IChangeCategorizer` and `ConventionalCommitCategorizer`, reading Conventional Commit conventions from the change title (`type(scope)!: subject`). `ChangeCategory` covers Feature (`feat`), Fix (`fix`), Performance (`perf`), Documentation (`docs`), Refactor (`refactor`), Internal (`build`/`ci`/`chore`/`test`/`style`/`revert`), and Other as the default for unrecognized or prefix-less titles. Breaking is tracked separately via `ChangeClassification.IsBreaking`, detected by a `!` marker, a `breaking` type, or a `BREAKING CHANGE` body note, so a breaking feature stays a feature but is still flagged.
- `Chartula.Cli`: registers the categorizer alongside the resolver.

Pure and deterministic — no LLM, no I/O. Uses a source-generated regex (AOT-friendly).

Verification: build clean; tests green (Core 33, Infrastructure 12): per-type prefix detection, scopes, case-insensitivity, all three breaking markers, the `Other` default, and determinism.

Closes #6 ([PR #45](https://github.com/goldbarth/chartula/pull/45))

---

feat(curation): degrade gracefully when clean PRs are missing

Makes the pipeline still produce something useful when PR discipline is imperfect.

What changed:
- `Chartula.Core`: added `IReleaseChangeResolver`/`ReleaseChangeResolver`, turning a `CommitRange` and the merged `PullRequestInfo` list into `ReleaseChange` values (title, description, number, url, labels, `ChangeSource`, commit sha). Pure domain logic, no I/O.
- `Chartula.Cli`: registers the resolver (dependency-free singleton).

Behavior: merged PRs present produces one change per PR; no PRs at all falls back to one change per commit using the commit subject; a blank or uninformative PR title falls back to the PR body's first informative line, then to a generic `PR #n`; an empty release yields an empty set, never an exception. The uninformative-title heuristic is a small starter set, to become configurable later.

Verification: build clean; tests green (Core 13, Infrastructure 12): PR-preferred path, commit fallback, blank-title-to-body, uninformative-title-to-body (theory), number fallback, and the empty-release no-op.

Closes #5 ([PR #44](https://github.com/goldbarth/chartula/pull/44))

---

feat(pull-requests): fetch merged PRs for a release from the GitHub API

Summarizes changes per merged PR instead of per raw commit.

What changed:
- `Chartula.Core`: added the `IReleasePullRequestReader` port plus `PullRequestInfo` (number, title, description, labels, url) and `RepositoryCoordinates`.
- `Chartula.Infrastructure`: added `GitHubPullRequestReader`, which for the commits in a `CommitRange` queries GitHub's "pull requests associated with a commit" endpoint, keeps merged PRs only, and de-duplicates by number. DTOs are parsed via a source-generated `System.Text.Json` context.
- `Chartula.Cli`: composition root configures the `HttpClient` (base URL, GitHub headers, bearer token by env-var name) and registers the reader.

Raw `HttpClient` plus `System.Text.Json` source generation was chosen over Octokit for dependency-light, native-AOT-friendly behavior, consistent with the earlier git-CLI choice. A stub `HttpMessageHandler` makes it fully mockable without network access. The token is read by env-var name (`GITHUB_TOKEN`) and is optional — public repos work unauthenticated, subject to rate limits.

Verification: build clean; tests green (Core 5, Infrastructure 12): field mapping, merged-only filtering, de-duplication across commits, empty-range no-op, and the API/network/malformed error paths, which all raise a clear `InvalidOperationException`.

Out of scope (separate issue): fallback when clean PRs are missing.

Closes #4 ([PR #43](https://github.com/goldbarth/chartula/pull/43))

---

feat(history): read the commit range for a release from git

Finds exactly the commits belonging to a release.

What changed:
- `Chartula.Core`: added the `IReleaseCommitReader` port plus `CommitInfo` and `CommitRange` (with `IsFirstRelease`). Pure domain, no I/O.
- `Chartula.Infrastructure` (new layer): added `GitCliCommitReader`, shelling out to `git` for the range since the previous tag (`<prev>..<tag>`), or all history up to the tag when there is no previous tag (first release). Clear errors for unknown or blank tags.
- `Chartula.Cli`: composition root registers the git reader; the pipeline depends only on the port.

The git CLI was chosen over LibGit2Sharp to avoid native dependencies that would conflict with the planned native-AOT binaries; `git` is present in any repo Chartula runs on. `Chartula.Infrastructure` is a new layer for concrete I/O adapters, keeping `Core` pure domain and `Cli` a thin composition root, and will house the GitHub API, file writers, and webhooks going forward.

Verification: tests run the real `git` CLI against throwaway repositories (deterministic, offline): between-tags range, first-release fallback, sha/subject mapping, unknown-tag and blank-tag errors. Build clean; tests green (Core 5, Infrastructure 6).

Closes #3 ([PR #42](https://github.com/goldbarth/chartula/pull/42))

---

feat(llm): abstract the LLM provider behind IChangelogModel

Adds the provider-agnostic LLM seam the pipeline builds on.

What changed:
- `Chartula.Core` (new): added `IChangelogModel`, the interface the pipeline depends on (`RephraseAsync`, `CheckFaithfulnessAsync`), and `ChatModel`, the single implementation, backed by a provider-agnostic `Microsoft.Extensions.AI.IChatClient`. Added domain types `Audience`, `GroundedFacts`, `RephraseRequest`, `FaithfulnessRequest`, `FaithfulnessReport`.
- `Chartula.Cli`: composition root wires Anthropic as the first provider (`AsIChatClient`), with model and provider selectable via config and the API key read by env-var name. This is the only provider-specific code.
- Added `Chartula.Core.Tests` (new), with 5 tests exercising the seam via a stub `IChatClient`, no live provider call.

Architecture chosen after discussion: a hybrid, domain interface over an agnostic `IChatClient`; swapping providers is a composition-root change only. `GroundedFacts` and the `ChatModel` prompts are intentionally minimal placeholders; the fact base and prompt design are handled separately.

Verification: build clean; `dotnet test` 5/5 green.

Closes #2 ([PR #41](https://github.com/goldbarth/chartula/pull/41))

---

fix: two release blockers found by dogfooding v0.1.0

Found by running `chartula preview --tag v0.1.0` against this repository. Neither bug was reachable from the existing tests — one needed a live API call, the other needed real pull request bodies.

Truncation (`ChatModel`): calls went out without `ChatOptions`, so `MaxOutputTokens` was never set, and the provider substituted its own default of 1024 when absent. All three audience texts were cut off mid-word; run metrics showed 3 calls, 3,072 output tokens — exactly 3 × 1024. The failure was silent: the run reported success, and the thorough check spent 56,712 tokens flagging the severed sentence as an unsupported claim, a bug symptom read as a hallucination. The ceiling is now always sent, configurable via `llm.maxOutputTokens`, defaulting to 16000.

False breaking changes (`ConventionalCommitCategorizer`): `MentionsBreakingChange` searched the whole body for `BREAKING CHANGE` as a case-insensitive substring, so prose discussing breaking changes was read as declaring one. Six of the thirty-three changes in v0.1.0 were mislabelled; none were actually breaking. Now matches the Conventional Commits footer: uppercase, start of line, colon-terminated.

Verification (against a real run, not just tests):

| | Before | After |
|---|---|---|
| Rephrasing output | 3,072 tokens (3 × 1024) | 11,271 tokens |
| Text endings | mid-word | complete sentences |
| Breaking changes reported | 6 | 0 |
| Thorough check claims | 1 (the truncation artifact) | 0 |

265 tests pass, 9 new; the categorizer regression test uses a real prose sentence as a fixture.

Known, not fixed here: `RuleBasedFaithfulnessChecker` matches `\bbreaking\b` across the whole output and flags a breaking-change claim whenever the word appears — the same phrase-versus-assertion mistake, now visible because no fact is breaking anymore. The flags are advisory and do not fail a run; separating a claim from prose using the word needs more than a regex, and is filed separately. ([PR #70](https://github.com/goldbarth/chartula/pull/70))

---

docs: bring the docs up to what Chartula actually is

Updates documentation to reflect the completed phase 1, which the docs previously did not describe accurately.

What was wrong: `Usage` was not runnable, calling the commands "planned entry points" and showing `chartula preview` without the required `--tag` and `--repo`. The `docs/` folder existed but was linked from nowhere. `chartula.example.yaml` showed 4 of 8 supported sections, missing `github`, `labels`, `categories`, and `review`. The status badge said "early development" despite 27 of 27 phase 1 issues being closed. CONTRIBUTING asked for "the .NET SDK" generically, though an older SDK cannot build `net10.0`, and documented four commit scopes (`collect`, `curate`, `render`, `check`) that were never used, while the sixteen actually in use went unmentioned.

What changed:
- The wordmark now leads the README, switched via `<picture>` + `prefers-color-scheme` so it reads on either theme.
- Long-celled tables became prose; `Why Chartula`, `Core ideas`, and `Roadmap` are now prose and headings, since two columns of paragraph text collapse on a narrow screen. Tables that remain hold short facts and survive a narrow column.
- Added `docs/architecture.md`, covering the layering and the reasoning behind the dependency choices, including the inward-pointing rule, why facts are established before an LLM sees them, and where each concern lives.
- Everything else now points somewhere: a documentation index in the README, with architecture and fixtures linked from CONTRIBUTING.

Verification: all 24 relative links in `README.md`, `CONTRIBUTING.md`, and `docs/*.md` resolve to existing files. Both SVGs are valid XML with no external references and no `<script>`, rendered to PNG and checked against a dark and a light background. Uncommented every section of `chartula.example.yaml` into a real `chartula.yaml` and ran the CLI against it: all eight sections bind, no configuration error. Every documented default checked against the value in the code. Build clean; 256 tests passing.

Note: the brand asset delivery note that came with the SVGs is deliberately not included in this change; it is in German, describes files not in the repo, and states a description of Chartula that is inaccurate. ([PR #69](https://github.com/goldbarth/chartula/pull/69))

---

refactor(prompting): move prompt text into a partial class

Separates prompt text from prompt build logic, so prompt strings live in one place.

What changed: `ChangelogPromptBuilder` is now a `partial` class split across two files — `ChangelogPromptBuilder.Prompts.cs` holds the prompt strings only (system header, the four rules, per-audience guidance), and `ChangelogPromptBuilder.cs` holds the composition logic referencing those constants. Iterating on prompt wording is now text-only work, without navigating composition logic to find and change a string.

This is a pure refactor: the prompt text is byte-for-byte unchanged, and the prompt-content assertions pass without modification, confirming no behavior change.

Verification: build clean; tests green and unchanged (Core 100, Infrastructure 16). ([PR #54](https://github.com/goldbarth/chartula/pull/54))

--- Customer ---
Fix: two release-blocking bugs found while testing v0.1.0 against this repository.

- Generated text could be cut off mid-sentence. Requests to the language model didn't set an output length limit, so the provider silently applied its own default and truncated all three audience texts. This failed quietly — the run reported success, and the thorough check spent tens of thousands of tokens flagging the cut-off text as an unsupported claim, when the real problem was truncation. The output limit is now always set explicitly, configurable via `llm.maxOutputTokens`, defaulting to 16000.
- Changes could be wrongly marked as breaking. The check for breaking changes matched the phrase "BREAKING CHANGE" anywhere in a pull request's text, so simply discussing breaking changes caused a change to be mislabelled as one. In the v0.1.0 release, six changes were incorrectly flagged this way. The check now only matches the standard breaking-change marker format, not incidental mentions.

Verified against a real run: rephrased text now ends in complete sentences instead of mid-word, and breaking changes dropped from 6 false positives to 0.

A related issue remains open: the free, rule-based check can still flag the word "breaking" appearing anywhere in generated text, even in ordinary prose. This is advisory only and doesn't fail a run, so it's being addressed separately.

--- Product ---
**Feature: Run metrics report token cost per check**

Every `preview` and `generate` run now ends with a summary of token usage and cost, so defaults can be set from data rather than guesswork. The report breaks out the rule-based check, the thorough check, and rephrasing separately, and highlights specifically what the thorough check caught that the rule-based check missed against the tokens it spent doing so — making it possible to judge, release over release, whether that check is earning its keep. Measurement is optional throughout; a run with no metrics sink produces identical output to one with it.

**Feature: Configurable category presentation**

A new `categories` configuration section sets category order, display names, and whether breaking changes are shown prominently, joining the existing `labels`, `factBase`, and `faithfulness` sections. Unknown category names are rejected with a clear error, and any section left untouched keeps its default.

**Feature: `chartula.yaml` configuration file**

Chartula now reads a `chartula.yaml` (or `.yml`) file to refine its behavior, layered so that environment variables still take precedence. All existing configuration sections (`llm`, `github`, `labels`, `filter`, `factBase`, `faithfulness`, `review`) can be set this way. With no file and no environment variables, every option falls back to a sensible default. A minimal example file is included, with the full option set documented separately. Configuration errors now surface as a clear message instead of a crash.

**Feature: `preview` and `generate` commands**

The CLI now exposes two commands: `generate`, which runs the full pipeline and writes `changelog.json`, `CHANGELOG.md`, and the GitHub release notes; and `preview`, which runs the identical pipeline but writes and publishes nothing, so you can see the real result before committing to it. Both commands take `--tag` and `--repo`, include a usage screen, give clear errors for missing options or unknown commands, and report a readable per-audience summary. Pipeline errors are caught and reported rather than causing a crash.

**Feature: All audience texts stored in `changelog.json`**

`changelog.json` now includes the customer- and product-manager-facing texts alongside the technical rendering, keyed by audience, so they live in the one file rather than as separate marketing files in the repository. The change data itself remains deterministic; only the renderings are LLM-produced. This is a non-breaking, optional addition to the existing schema.

**Feature: Release notes written to GitHub**

Generated release text is now written directly to the GitHub release notes: created if the release doesn't exist yet, updated in place if it does. Re-running for the same tag updates that release rather than creating a duplicate.

**Feature: `CHANGELOG.md` writing with history preservation**

Each release is now written as a new section prepended to the top of `CHANGELOG.md`. Existing sections are preserved verbatim, and re-running the same tag replaces that section in place rather than duplicating it or reordering history.

**Feature: Optional human review before publishing**

An opt-in review mode lets a maintainer see each generated text alongside its flagged passages and either approve it as-is or edit it before it's written. Review is off by default, in which case text passes through untouched and no reviewer is consulted.

**Feature: Thorough LLM-based faithfulness check**

A second LLM pass checks generated text against the fact base for subtle, meaning-level hallucinations that a rule-based check can't catch (for example, a rephrasing that quietly changes what actually happened). It's on by default and can be disabled with a single toggle; when disabled, or when there's nothing to check, no LLM call is made.

**Feature: Rule-based faithfulness check**

A zero-cost, no-LLM check now runs on every release, flagging numbers, quoted or backticked names, and breaking-change claims that don't appear in the fact base. It always runs, requires no model call, and surfaces flagged passages for review rather than failing the run outright.

**Feature: Consistent formatting and tone across renderings**

Each rendering is now normalized to a single consistent format — bullet style, line endings, whitespace — regardless of how individual pull requests were written, and the prompt instructs the model to write in one consistent voice rather than carrying over any individual author's tone.

**Feature: Technical, customer, and product-manager renderings from one fact base**

All three audience-specific versions of a release are now rendered from the same underlying fact base, so they can never contradict each other. The technical version keeps full detail and links; the customer version omits internal-only changes and their links, focusing on benefits; the product-manager version covers everything, grouped by theme. A failure rendering one audience doesn't affect the others.

**Feature: Prompt architecture built around rephrasing only**

The prompt sent to the model now firmly constrains it to rephrasing the given facts: it may never introduce a fact, number, or name that isn't in the list; category and breaking-change status are treated as already established; thin facts are rendered briefly rather than padded out; and output has no added preamble or conclusion. Categories and flags are passed to the model as given text, not decided by it.

**Feature: Changelog generation through the provider interface**

Generation now runs through the provider-agnostic model interface established earlier, making exactly one call per release (and none at all when the fact base is empty). Provider failures are caught and returned as a failed result rather than crashing.

**Feature: Fact base written to `changelog.json`**

The release fact base is now written to `changelog.json` as a stable, versioned, machine-readable record, kept intentionally separate from the internal domain model so the format can stay stable as the domain evolves. Every field is a deterministic fact — nothing in this file is LLM-generated.

**Feature: Configurable fact-base depth**

A maintainer can now choose how much source material feeds the fact base: title only, title and description (the default), or title, description, and linked issues — accommodating different team PR styles.

**Feature: Release fact base assembled from curated changes**

Curated changes are now transformed into the complete fact base for a release, combining each change's category and flags (already decided deterministically, never by the model) with a resolved user-visible flag and any linked issues parsed from GitHub closing keywords.

**Feature: Fact-base data model defined**

A structured `ChangeFact` model now captures, per change, the title, PR number and link, category, user-visible and breaking flags, linked issues, and an optional description — the single source of truth the model is later allowed to rephrase from. Every field is deterministic; nothing here is LLM-generated.

**Feature: Internal and chore changes excluded by default**

Changes categorized as internal are now excluded from the changelog by default, combining deterministic categorization with label rules. A breaking change is never dropped, even if its category would otherwise be excluded, unless a label explicitly excludes it. The excluded category list is configurable.

**Feature: Label-driven curation rules**

GitHub labels can now steer curation via configuration: a label can exclude a change entirely, force it into a specific category, or (in "only labeled" mode) require a label for inclusion at all. All of this is optional — the tool works the same with no labels in use.

**Feature: Deterministic categorization before the model sees anything**

Each change is now assigned a category based on Conventional Commit conventions in its title, before any generation happens, so the kind of change is never left to the model to infer. Breaking-change status is tracked separately from category, so a breaking feature is still categorized as a feature but flagged as breaking. Unrecognized changes fall back to a sane default category.

**Feature: Graceful fallback when PR discipline is imperfect**

The tool now degrades gracefully rather than failing when pull request data is missing or unhelpful: it falls back to commit data when there are no associated PRs, and to the PR body or a generic label when a PR title is blank or uninformative. An empty release simply produces an empty result.

**Feature: Merged pull requests fetched from GitHub**

Changes are now summarized per merged pull request rather than per raw commit, fetched from the GitHub API for the commits in a release's range. API failures produce a clear error rather than a crash.

**Feature: Commit range resolved from git history**

The tool can now determine exactly which commits belong to a release: everything since the previous tag, or, for a first release with no previous tag, the full history up to that tag. Unknown or blank tags produce a clear error.

**Feature: LLM provider abstracted behind a stable interface**

The pipeline now depends on a single provider-agnostic interface for all language-model operations, with Anthropic wired in as the first concrete provider. Swapping providers going forward is a configuration-only change. API keys are read from environment or configuration and are never hardcoded.

**Fix: Two release-blocking bugs found by dogfooding**

Generated text could be silently truncated mid-sentence: output token limits were never sent to the provider, so its own low default applied. The token ceiling is now always sent and is configurable, with a much higher default.

Six changes in a real release were incorrectly flagged as breaking changes because the categorizer matched the phrase "BREAKING CHANGE" anywhere in a commit body, including in ordinary prose discussing breaking changes. It now only matches the specific footer format Conventional Commits defines, at the start of a line.

A related, narrower issue remains open: the rule-based faithfulness check can still flag the word "breaking" appearing in ordinary text as a breaking-change claim. It doesn't fail a run and is filed separately for a proper fix.

**Documentation: Docs brought up to date with the current state of the tool**

Documentation is updated to reflect that core development is complete, rather than still describing a planned project. Usage instructions are now runnable as written, all documentation is linked from the README and cross-referenced from CONTRIBUTING, the example configuration file shows all supported sections, and a new architecture document explains the layering and dependency choices behind the codebase. Setup instructions and commit conventions in CONTRIBUTING are corrected to match actual practice.

**Refactor: Prompt text separated from prompt-building logic**

Prompt strings now live in their own file, separate from the logic that assembles them, so wording changes no longer require navigating composition code. This is a pure refactor with no change in behavior or output.
  Flagged for review:
    ! 'only labeled' is not supported by the facts.
    ! Documentation section: 'Documentation is updated to reflect that core development is complete' — the facts state 'Phase 1 is complete', not that 'core development is complete'; these are not clearly equivalent claims and the changelog overstates/generalizes the fact.
    ! Run metrics feature: 'a summary of token usage and cost' — the facts describe token usage counts (in/out tokens, calls), but do not mention 'cost' in terms of money or pricing; presenting it as 'cost' overstates what the metrics report.

Preview only - nothing was written or published.

Run metrics
  Rule-based check: 3 runs, 1 with findings, 1 claim, no tokens
  Thorough check:   3 runs, 1 with findings, 2 claims, 73,656 in / 237 out
    caught 2 claims the rule-based check missed, for 73,893 tokens in 3 calls
  Rephrasing:       3 calls, 54,874 in / 17,636 out
  Total:            146,403 tokens
