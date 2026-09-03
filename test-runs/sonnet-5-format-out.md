sonnet-5-format-out, rendered by Chartula from v0.1.0

--- Technical ---

**Feature: report what a run does and what it costs**
- Adds a run-metrics summary printed after every `preview` and `generate` run, covering the rule-based check, thorough check, and rephrasing step, with token and call counts and a grand total.
- Isolates claims caught only by the thorough check (excluding claims both checks find) to make the keep-or-drop decision on that check data-driven rather than guesswork.
- Adds `IRunMetrics`/`RunMetrics`, `NullRunMetrics`, `RunReport`, and `RunReportFormatter` in `Chartula.Core/Observability`.
- `ChatModel` reports token usage per `LlmOperation`; `ReleasePipeline` records both checks' findings and exposes the report via `ReleaseOutcome`.
- Metrics collection is optional everywhere; a run without a sink produces byte-identical output.
- Documented in `docs/run-metrics.md`.
Closes #26 (https://github.com/goldbarth/chartula/pull/66)

**Feature: add configuration sections for categories**
- Adds a `categories` section to `chartula.yaml`: `order`, `names`, `breakingProminent` (default `true`).
- Adds `CategorySettings` with `From(...)` parsing, rejecting unknown category names with a clear error.
- Extracts `GroundedFactsFactory` from `ReleaseChangelogGenerator` to centralize audience filtering, category ordering, and display naming.
- Documented in `docs/configuration.md`.
Closes #25 (https://github.com/goldbarth/chartula/pull/65)

**Feature: read chartula.yaml with sensible defaults**
- Adds `AddChartulaYaml`, loading `chartula.yaml`/`.yml` via YamlDotNet and flattening it into `Chartula:*` keys, layered before environment variables (env overrides YAML).
- Ships `chartula.example.yaml` with all sections commented out.
- Adds `docs/configuration.md` documenting the full option set and defaults.
- Configuration errors now surface as a clear `Configuration error: ...` message instead of an unhandled exception.
- Adds the `Chartula.Cli.Tests` project for CLI-level tests.
Closes #24 (https://github.com/goldbarth/chartula/pull/64)

**Feature: generate and preview commands wired to the pipeline**
- Adds `ReleasePipeline`, orchestrating commit-range and PR reads, fact-base construction, per-audience rendering, faithfulness checks, review, and output writing.
- `generate` writes `changelog.json`, `CHANGELOG.md`, and GitHub release notes; `preview` runs the identical flow but writes and publishes nothing.
- Adds `chartula preview`/`chartula generate` commands with `--tag` and `--repo` options, a usage screen, and clear error handling for pipeline failures.
Closes #23 (https://github.com/goldbarth/chartula/pull/63)

**Feature: store all audience texts in changelog.json**
- Adds a `renderings` object to `ChangelogDocument`, keyed by audience (`technical`/`customer`/`product`); present but empty when no renderings are supplied.
- `schemaVersion` remains `1`; the addition is non-breaking.
Closes #22 (https://github.com/goldbarth/chartula/pull/62)

**Feature: write the generated text back to GitHub release notes**
- Adds the `IReleaseNotesWriter` port and `GitHubReleaseNotesWriter`, using the GitHub REST API over plain `HttpClient` with source-generated JSON.
- Updates an existing release's notes in place (`GET` then `PATCH`) or creates a release (`POST`) when none exists; re-running the same tag always updates rather than duplicating.
- Extracts shared GitHub `HttpClient` setup into `GitHubHttpClientFactory`.
Closes #21 (https://github.com/goldbarth/chartula/pull/61)

**Feature: write CHANGELOG.md, prepend and preserve history**
- Adds `ChangelogMarkdownComposer`, prepending each release as a new top section while keeping existing sections verbatim.
- Re-running the same tag replaces that section in place rather than duplicating it or reordering history.
- Adds the `IChangelogMarkdownWriter` port and `FileChangelogMarkdownWriter`.
Closes #20 (https://github.com/goldbarth/chartula/pull/60)

**Feature: opt-in review mode for human sign-off of flagged passages**
- Adds `IReviewCoordinator`/`ReviewCoordinator`, gating each rendering on an opt-in toggle.
- When enabled, an `IReviewer` approves or edits the text before it is written; `ReviewPresentation` shows flagged passages from both faithfulness checks alongside the generated text.
- Off by default; `AutoApproveReviewer` is the non-interactive default reviewer.
Closes #19 (https://github.com/goldbarth/chartula/pull/59)

**Feature: thorough second-pass LLM check with a toggle**
- Adds `IThoroughFaithfulnessChecker`/`ThoroughFaithfulnessChecker`, a second LLM pass flagging claims not supported by the grounded facts.
- On by default; disabled via `Chartula:Faithfulness:Thorough`. Makes no LLM call when disabled or when there is nothing to check.
- Moves the faithfulness prompt into `IChangelogPromptBuilder.BuildFaithfulnessPrompt`.
Closes #18 (https://github.com/goldbarth/chartula/pull/58)

**Feature: rule-based check that catches obvious hallucinations**
- Adds `IRuleBasedFaithfulnessChecker`/`RuleBasedFaithfulnessChecker`, flagging numbers, quoted/backticked names, and breaking-change claims absent from the fact base.
- No `IChangelogModel` dependency; zero token cost, always runs.
- Flags are advisory and feed review mode.
Closes #17 (https://github.com/goldbarth/chartula/pull/57)

**Feature: consistent formatting and tone per audience**
- Adds `IChangelogFormatter`/`ChangelogFormatter`, normalizing line endings, bullet markers, trailing whitespace, and blank-line runs on every rendering while leaving headings and prose intact.
- Adds a prompt rule directing the model to write in one consistent voice without carrying over an individual author's tone.
Closes #16 (https://github.com/goldbarth/chartula/pull/56)

**Feature: render technical, customer, and PM from one fact base**
- Adds `IReleaseRenderer`/`ReleaseRenderer`, producing technical, customer, and product-manager renderings from the same `FactBase`.
- Technical keeps links and the full change set, customer omits non-user-visible changes and their links, product sees the full set.
- A failure in one audience does not affect the others.
Closes #15 (https://github.com/goldbarth/chartula/pull/55)

**Feature: prompt architecture that rephrases facts, never invents**
- Adds `IChangelogPromptBuilder`/`ChangelogPromptBuilder`, producing a `ChangelogPrompt` (system + user).
- System prompt restricts the model to rephrasing: no new facts/numbers/names, categories and breaking markers used as established, no padding of thin facts, no preamble or conclusion, plus per-audience guidance.
- `ChatModel` now delegates prompt construction to the builder.
Closes #14 (https://github.com/goldbarth/chartula/pull/53)

**Feature: generate a changelog through the provider interface**
- Adds `IReleaseChangelogGenerator`/`ReleaseChangelogGenerator` and `ChangelogGenerationResult`, making exactly one `IChangelogModel.RephraseAsync` call per release and none for an empty fact base.
- Provider failures are caught and returned as a failed result; cancellation propagates.
Closes #13 (https://github.com/goldbarth/chartula/pull/52)

**Feature: write the fact base to changelog.json**
- Adds `ChangelogDocument` (`schemaVersion` + `tag` + `changes`) as the stable on-disk shape, kept separate from the domain `FactBase`.
- Adds `ChangelogJsonSerializer`, the `IChangelogJsonWriter` port, and `FileChangelogJsonWriter`.
- `schemaVersion` (currently `1`) is the stability contract; documented in `docs/changelog-json.md`.
Closes #12 (https://github.com/goldbarth/chartula/pull/51)

**Feature: make fact-base depth configurable**
- Adds `FactBaseDepth` (`TitleOnly`, `TitleAndDescription` default, `TitleDescriptionAndIssues`) and `FactBaseDepthParser`.
- `FactBaseBuilder` honours the selected depth; the parser accepts canonical names and aliases and raises a clear error on an unknown value.
- Configured via `Chartula:FactBase:Depth`.
Closes #11 (https://github.com/goldbarth/chartula/pull/50)

**Feature: transform curated changes into the release fact base**
- Adds `IFactBaseBuilder`/`FactBaseBuilder` and the `FactBase` container, mapping each curated change to a `ChangeFact`.
- Category and breaking flag come from deterministic categorization and label overrides, never from an LLM.
- `IsUserVisible` is derived from category; `LinkedIssues` are parsed from GitHub closing keywords in the title and body.
Closes #10 (https://github.com/goldbarth/chartula/pull/49)

**Feature: define the fact-base data model (index card per change)**
- Adds `ChangeFact` in `Chartula.Core`, capturing title, PR number, link, category, user-visible flag, breaking flag, linked issues, and an optional description.
- Every field is derived deterministically; nothing in the model is LLM-generated. PR-only fields are nullable so commit-based changes fit the same shape.
Closes #9 (https://github.com/goldbarth/chartula/pull/48)

**Feature: drop internal/chore changes by default**
- Adds `IChangeFilter`/`ChangeFilter` and `ChangeFilterRules`: label exclusion wins outright, a breaking change is never dropped, otherwise a change is dropped when its effective category is excluded.
- Default excluded category is `Internal`, overridable via `Chartula:Filter:ExcludeCategories`.
Closes #8 (https://github.com/goldbarth/chartula/pull/47)

**Feature: steer curation with label rules from config**
- Adds `LabelRules` (excluded labels, label-to-category overrides, only-include-labeled mode) and `ILabelRulePolicy`/`LabelRulePolicy`, producing a `LabelDecision`.
- Precedence: exclusion wins, then only-labeled mode, then a forced category from the first matching label.
- Bound from `Chartula:Labels`; entirely optional, with `LabelRules.None` as the no-labels default.
Closes #7 (https://github.com/goldbarth/chartula/pull/46)

**Feature: assign categories deterministically before the LLM**
- Adds `IChangeCategorizer`/`ConventionalCommitCategorizer`, parsing Conventional Commit prefixes into `ChangeCategory` (Feature, Fix, Performance, Documentation, Refactor, Internal, Other as default).
- Tracks breaking status separately via `ChangeClassification.IsBreaking`, detected via a `!` marker, a `breaking` type, or a `BREAKING CHANGE` body note.
- Pure and deterministic; no LLM call involved.
Closes #6 (https://github.com/goldbarth/chartula/pull/45)

**Feature: degrade gracefully when clean PRs are missing**
- Adds `IReleaseChangeResolver`/`ReleaseChangeResolver`, mapping a `CommitRange` and merged `PullRequestInfo` list into `ReleaseChange` values.
- Falls back to one change per commit when no PRs exist, and to the PR body's first informative line or a generic `PR #n` when a title is blank or uninformative.
- An empty release yields an empty set, never an exception.
Closes #5 (https://github.com/goldbarth/chartula/pull/44)

**Feature: fetch merged PRs for a release from the GitHub API**
- Adds the `IReleasePullRequestReader` port, `PullRequestInfo`, and `RepositoryCoordinates` in `Chartula.Core`.
- Adds `GitHubPullRequestReader` in `Chartula.Infrastructure`, querying GitHub's PR-associated-with-commit endpoint per commit in a `CommitRange`, keeping merged PRs only and de-duplicating by number.
- Uses raw `HttpClient` and source-generated `System.Text.Json` for native-AOT compatibility; token read by env-var name, optional for public repos.
Closes #4 (https://github.com/goldbarth/chartula/pull/43)

**Feature: read the commit range for a release from git**
- Adds the `IReleaseCommitReader` port, `CommitInfo`, and `CommitRange` (with `IsFirstRelease`) in `Chartula.Core`.
- Adds `GitCliCommitReader` in the new `Chartula.Infrastructure` layer, shelling out to `git` for the range since the previous tag or all history for a first release.
- Chosen over LibGit2Sharp to avoid native dependencies conflicting with the planned native-AOT binaries.
Closes #3 (https://github.com/goldbarth/chartula/pull/42)

**Feature: abstract the LLM provider behind IChangelogModel**
- Adds `IChangelogModel` (`RephraseAsync`, `CheckFaithfulnessAsync`), `ChatModel` backed by a provider-agnostic `Microsoft.Extensions.AI.IChatClient`, and domain types `Audience`, `GroundedFacts`, `RephraseRequest`, `FaithfulnessRequest`, `FaithfulnessReport` in the new `Chartula.Core`.
- Wires Anthropic as the first provider in the CLI composition root; model and provider are selectable via config, with the API key read by env-var name.
Closes #2 (https://github.com/goldbarth/chartula/pull/41)

**Fix: two release blockers found by dogfooding v0.1.0**
- `ChatModel` calls omitted `ChatOptions`, so `MaxOutputTokens` was never set and the provider's default of 1024 tokens truncated all three audience texts mid-word; the thorough check then spent tokens flagging the truncation as an unsupported claim. The output ceiling is now always sent, configurable via `llm.maxOutputTokens`, defaulting to 16000.
- `ConventionalCommitCategorizer` matched `BREAKING CHANGE` as a case-insensitive substring anywhere in the body, so prose discussing breaking changes was mislabelled as declaring one; it now matches only the Conventional Commits footer format (uppercase, start of line, colon-terminated).
- Verified against a real v0.1.0 run: rephrasing output rose from 3,072 to 11,271 tokens with complete sentence endings, reported breaking changes dropped from 6 to 0, and thorough-check claims dropped from 1 to 0.
- Known, not fixed here: `RuleBasedFaithfulnessChecker` still matches `\bbreaking\b` anywhere in the output and flags a breaking-change claim on the word's mere presence; this is advisory and does not fail a run, and is filed separately.
(https://github.com/goldbarth/chartula/pull/70)

**Documentation: bring the docs up to what Chartula actually is**
- Fixes `Usage` examples to include the required `--tag` and `--repo` options, removing the "planned entry points" framing.
- Links the `docs/` folder from the README and `CONTRIBUTING`.
- Updates `chartula.example.yaml` to show all eight supported sections, previously only four (`github`, `labels`, `categories`, `review` were missing).
- Updates the status badge and `CONTRIBUTING`'s SDK requirement and commit-scope list to match current practice.
- Adds `docs/architecture.md`, covering the layering, dependency rationale, and the inward-pointing dependency rule.
(https://github.com/goldbarth/chartula/pull/69)

**Refactor: move prompt text into a partial class**
- Splits `ChangelogPromptBuilder` into a partial class: `ChangelogPromptBuilder.Prompts.cs` holding prompt strings only, `ChangelogPromptBuilder.cs` holding composition logic.
- Prompt text is unchanged; no behavior change.
(https://github.com/goldbarth/chartula/pull/54)

--- Customer ---

### What's New

- **Run metrics:** Every preview and generate run now ends with a summary of how many checks ran, how many findings they caught, and how many tokens were used. Reading this across a few releases tells you whether the thorough check is worth what it spends.
- **Category settings:** A new categories section in chartula.yaml lets you set the order categories appear in, their display names, and whether breaking changes are shown prominently. Leave it out and the existing defaults apply.
- **Configuration file:** You can now add a chartula.yaml file to a repository to customize Chartula's behavior; without one, the tool runs with sensible defaults. An example file with every option commented out is provided to copy and adjust, and an invalid setting now produces a clear configuration error message instead of a crash.
- **CLI commands:** Running chartula preview shows the changelog, release notes, and files that would be produced for a tag without writing or publishing anything, while chartula generate produces and writes them. Both take --tag and --repo options, print a per-audience summary, and report clear errors instead of crashing on an unknown command or a missing option.
- **Changelog JSON renderings:** changelog.json now stores the customer and product-manager text alongside the technical version, in a renderings section, keeping all generated texts in one file instead of separate files in the repository.
- **GitHub release notes:** The generated release text is now written to the GitHub release's own notes. Running the same tag again updates those notes in place rather than creating a second release.
- **CHANGELOG.md:** Each release is now added as a new section at the top of a CHANGELOG.md file, with all earlier sections kept intact below it. Running the same release again replaces its section in place instead of duplicating it.
- **Review mode:** An optional review mode lets you check generated text before it's published: it's shown alongside any flagged passages, and you can approve it as-is or edit it. Turn it on in the review section of chartula.yaml; it stays off by default.
- **Thorough faithfulness check:** A second check now compares the generated text against the source facts to catch subtler mistakes, such as a fix being rewritten as something more serious than it was. It runs by default and can be turned off in the faithfulness section of chartula.yaml.
- **Rule-based faithfulness check:** A free check now flags any number, quoted name, or breaking-change claim in the generated text that doesn't appear in the source facts, surfacing it for review. It always runs and needs no configuration.
- **Consistent formatting:** Generated changelog text now reads in one consistent voice and formatting style throughout, regardless of how the original pull requests were written.
- **Audience-specific renderings:** A release now produces three versions from the same facts: a technical version with links and the full set of changes, a customer-facing version focused on user-visible benefits, and a product-manager version grouped by theme. Because all three come from the same facts, they can't disagree with each other.
- **Fact-grounded generation:** Generated text is built only from the established facts of a release: it never adds a number, name, or detail that isn't already known, and it stays brief rather than padding out a change with little to say.
- **changelog.json fact record:** A changelog.json file is now written for every release, recording the release's facts in a stable, versioned format that isn't generated by AI.
- **Fact-base depth:** You can control how much detail feeds a release's changelog: title only, title and description (the default), or title, description, and linked issues. Set this in the factBase section of chartula.yaml.
- **Change filtering:** Internal and chore-type changes are now left out of the changelog by default, while breaking changes are always kept even if their category would otherwise be excluded. Adjust which categories are excluded in the filter section of chartula.yaml.
- **Label rules:** GitHub labels can now steer what appears in the changelog: a label can exclude a pull request, force it into a specific category, or restrict the changelog to only labeled pull requests. This is entirely optional and configured in the labels section of chartula.yaml.
- **Graceful fallback:** When a merge has no associated pull request, or the pull request has a blank or uninformative title, the changelog now falls back to the commit message or the pull request's description rather than leaving the change out or failing the run.

### Bug Fixes

- **Truncated text:** Generated text could previously be cut off mid-word because no maximum response length was set, letting the provider apply its own low default. Full text is now always generated, and the limit can be adjusted in the llm section of chartula.yaml if needed.
- **False breaking-change labels:** A pull request that merely discussed a breaking change in its description could previously be mislabeled as a breaking change itself. Only the standard Conventional Commits marker for a breaking change is now recognized, so labeling reflects the actual change.

--- Product ---

**Pipeline foundations**
- Feature: Added a provider-agnostic interface for the LLM, with Anthropic as the first backing provider; API keys are read from configuration or environment, never hardcoded.
- Feature: The commit range for a release is now read directly from git, covering ordinary releases and the first release with no prior tag.
- Feature: Changes are now summarized per merged pull request rather than per raw commit, pulling title, description, labels, and link from GitHub.
- Feature: When pull request discipline is imperfect, the tool now falls back gracefully — using commit data when no PRs exist, and the PR body when a title is blank or uninformative — so a release never fails purely because of messy PRs.
- Feature: Each change is now assigned a category deterministically (feature, fix, performance, docs, refactor, internal, other) from commit conventions, with breaking changes tracked separately, before the LLM is involved.

**Curation and the fact base**
- Feature: Maintainers can steer curation with GitHub labels — excluding a PR, forcing its category, or restricting the changelog to only labeled PRs — all configured without touching code.
- Feature: Internal and chore changes are excluded from the changelog by default; breaking changes are always kept even if their category is otherwise excluded, and the excluded set is configurable.
- Feature: Introduced a structured fact record for each change, capturing title, PR number, link, category, user-visible flag, breaking flag, and linked issues — all established deterministically, never generated by the LLM.
- Feature: Curated changes are now assembled into a complete, grounded fact base for each release, applying fallbacks, dropping filtered changes, and deriving user-visibility and linked issues.
- Feature: The amount of source material feeding the fact base is now configurable — title only, title and description (the default), or title, description, and linked issues.

**Generation and rendering**
- Feature: Generation now runs through the provider interface, making exactly one call per release (none for an empty fact base) and handling provider failures without crashing.
- Feature: Added a dedicated prompt design that instructs the model to rephrase established facts only, never invent numbers, names, or details, and stay brief when facts are thin.
- Feature: The changelog can now be rendered for three audiences — technical, customer, and product manager — all derived from the same fact base, so they can never contradict each other.
- Feature: Output formatting is now normalized consistently across every rendering, and the model is instructed to write each rendering in one coherent voice regardless of how the individual source material was written.

**Faithfulness checks and review**
- Feature: Added a free, always-on check that flags invented numbers, unsupported names, and unsupported breaking-change claims before any LLM check runs.
- Feature: Added an optional, on-by-default second LLM pass that catches meaning-level hallucinations the free check can't see, with a single toggle to disable it.
- Feature: Added an opt-in review mode that lets a maintainer approve or edit generated text before it is published, with flagged passages highlighted.

**Output and publishing**
- Feature: The release fact base is now written to `changelog.json` as a durable, versioned, machine-readable record.
- Feature: Each release now writes a new section to the top of `CHANGELOG.md`, preserving prior history and updating that release's section in place on re-runs rather than duplicating it.
- Feature: Generated release notes are now written back to the actual GitHub release, updating an existing release rather than duplicating it on repeat runs.
- Feature: Customer and product-manager texts are now stored alongside the technical rendering inside `changelog.json` rather than as separate files.

**CLI and configuration**
- Feature: Added `preview` and `generate` commands that run the full pipeline; `preview` shows the result without writing or publishing anything.
- Feature: The tool now reads an optional `chartula.yaml` configuration file with sensible defaults, so it works unconfigured and can be refined without code changes.
- Feature: Added a configuration section for category presentation — order, display names, and breaking-change prominence — completing the configuration surface.

**Observability**
- Feature: Every run now ends with a metrics summary reporting findings and token cost per check, including how many claims the thorough check caught that the free check missed — the basis for deciding whether that check earns its cost.

**Fixes**
- Fix: Fixed two release-blocking bugs found while dogfooding: generated text could be silently cut off because no output-token limit was set (now configurable, with a higher default), and prose merely discussing breaking changes could be mislabelled as one (now matches the precise breaking-change format).

**Documentation**
- Documentation: Overhauled the documentation to match the tool as it actually works — runnable usage examples, a linked documentation index, a complete example configuration file, an accurate development status, updated contribution requirements, and a new architecture guide.

**Internal**
- Refactor: Reorganized how prompt wording is stored internally, separating the prompt text from the logic that builds it, with no change in behavior.
