--- Technical ---
# Release Notes

## Run metrics now reported

Every `preview` and `generate` run ends with a summary showing token usage and check effectiveness. The thorough check's cost is paired with the claims only it caught, answering whether the LLM pass earns its cost.
Measurement is optional and does not affect output byte-for-byte when disabled. See `docs/run-metrics.md` for interpretation guidance.

**New types:** `IRunMetrics`, `RunMetrics`, `NullRunMetrics`, `RunReport`, `RunReportFormatter` in `Chartula.Core/Observability/`.

## Category presentation is now configurable

The `categories` section in `chartula.yaml` controls order, display names, and breaking-change prominence via `order`, `names`, and `breakingProminent` (default `true`). Invalid category names are rejected at startu
p with a clear message.

**New types:** `CategorySettings` in the domain; `GroundedFactsFactory` extracted for unified audience filtering, ordering, and naming.

## Configuration file support

`chartula.yaml` (or `.yml`) refines behavior while the tool works with sensible defaults and no file. Environment variables override YAML values. Configuration errors report clearly instead of crashing. A minimal `c
hartula.example.yaml` ships in the repo root; full options are documented in `docs/configuration.md`.

**New:** `Chartula.Cli.Tests` project for CLI-level tests; `AddChartulaYaml` in composition; clear `Configuration error: ...` messages.

## CLI commands wired

`chartula preview` and `chartula generate` now work end-to-end. Both require `--tag` and `--repo <owner/name>`; both run the identical pipeline. `generate` writes `changelog.json`, `CHANGELOG.md`, and GitHub release
 notes; `preview` shows the result without writing or publishing. Pipeline errors are caught and reported; unknown commands and missing options show usage and exit cleanly.

## Outputs now written

- **`changelog.json`** stores the fact base as a durable, machine-readable record with schema version 1. The `renderings` object (keyed by `technical` / `customer` / `product`) holds audience-specific LLM-generated
text; all other fields are deterministic facts. Adding optional fields is non-breaking; see `docs/changelog-json.md`.
- **`CHANGELOG.md`** prepends each release at the top, preserving history verbatim. Re-running the same tag replaces that section in place (idempotent, never duplicates or reorders).
- **GitHub release notes** are created or updated via REST API (`POST` for new releases, `PATCH` for existing ones, keyed by tag).

## Faithfulness checks in place

**Rule-based check** (always on, zero cost): flags numbers not in the fact base, quoted/backticked names absent from facts, and breaking-change claims when no fact is marked breaking. Flags are advisory, surfaced fo
r review.

**Thorough check** (on by default, configurable via `Chartula:Faithfulness:Thorough`): a second LLM pass checks the output semantically against the fact base and flags unsupported claims. Makes no call when disabled
 or when there is nothing to check.

**New types:** `IRuleBasedFaithfulnessChecker`, `IThoroughFaithfulnessChecker`, `ThoroughFaithfulnessOptions`, `FaithfulnessReport`.

## Review mode for human sign-off

**Optional opt-in** via `Chartula:Review` (off by default). When enabled, each rendering is presented with flagged passages highlighted for a maintainer to approve as-is or edit. The edited text is what gets written
.

**New types:** `IReviewCoordinator`, `ReviewCoordinator`, `ReviewPresentation`, `ReviewDecision`, `AutoApproveReviewer`.

## Consistent formatting and tone per audience

`ChangelogFormatter` normalizes every rendering deterministically — normalized line endings, single `- ` bullet marker, trimmed trailing whitespace, collapsed blank-line runs — while preserving non-bullet lines. The
 prompt instructs the model to write in one consistent voice and not carry over an author's tone or phrasing.

**New type:** `IChangelogFormatter`, `ChangelogFormatter`.

## Three audience renderings from one fact base

`ReleaseRenderer` produces technical, customer, and product-manager versions from the same `FactBase`:
- **Technical**: full change set with PR links and precise breaking-change detail.
- **Customer**: benefit-focused, omits non-user-visible changes and their links.
- **Product**: full set, grouped by theme.

A failure in one audience does not fail the others. See `docs/audience-filtering.md`.

**New type:** `IReleaseRenderer`, `ReleaseRenderer`.

## Prompt architecture that prevents hallucination

`ChangelogPromptBuilder` produces prompts with a system message that pins the model to rephrasing established facts — never introducing a fact, number, name, or detail not in the provided list. Categories and breaki
ng markers are presented verbatim and the model is instructed not to decide them. Thin fact bases are kept sparse rather than padded. The user prompt carries only facts, nothing our code adds.

**New type:** `IChangelogPromptBuilder`, `ChangelogPromptBuilder`.

## Generation through the provider interface

`ReleaseChangelogGenerator` makes exactly one `IChangelogModel.RephraseAsync` call per release, returning a `ChangelogGenerationResult`. Makes no call for an empty fact base. Provider failures are caught and returne
d as a failed result (not a crash); cancellation propagates.

**New type:** `IReleaseChangelogGenerator`, `ReleaseChangelogGenerator`, `ChangelogGenerationResult`.

## Fact base and grounding

`ChangeFact` represents one change as an index card: PR title, number, link, category, user-visible and breaking flags, linked issues, optional description. Every field is deterministic; nothing is LLM-generated.

`FactBaseBuilder` assembles the complete fact base for a release: resolves changes with the missing-PR fallback, drops filtered-out changes, and maps each survivor to a `ChangeFact`. Category and breaking flag come
from deterministic categorization (#6); a label can force the category (#7). Linked issues are parsed from GitHub closing keywords.

**New types:** `ChangeFact`, `IFactBaseBuilder`, `FactBaseBuilder`, `FactBase`.

## Fact-base depth configurable

Three modes control how much source material feeds the fact base via `Chartula:FactBase:Depth`:
- `title-only` — title only.
- `title-and-description` — **the default** (title + description, no issues).
- `title-description-and-issues` — title + description + linked issues.

Parser accepts canonical names and aliases (`title`, `description`, `full`); unknown values raise a clear error.

**New type:** `FactBaseDepth`, `FactBaseDepthParser`.

## Filtering keeps the changelog relevant

`ChangeFilter` drops internal/chore changes by default, combining deterministic categorization and label rules. Decision order: label exclusion wins outright → a breaking change is never dropped → otherwise dropped
when the effective category is in the excluded set. Default excluded set: `Internal`. Overridable via `Chartula:Filter:ExcludeCategories`. A breaking change is never filtered out unless an explicit label excludes it
.

**New types:** `IChangeFilter`, `ChangeFilter`, `ChangeFilterRules`.

## Label rules from configuration

`LabelRules` and `LabelRulePolicy` steer curation without code changes. Configuration keys (`Chartula:Labels`) control excluded labels, label → category overrides, and an only-include-labeled mode. All optional; the
 tool works with no labels. Matching is case-insensitive; unknown category names raise a clear error at startup.

**New types:** `LabelRules`, `ILabelRulePolicy`, `LabelRulePolicy`, `LabelDecision`.

## Deterministic categorization

`ConventionalCommitCategorizer` assigns categories from Conventional Commit conventions in the title (`type(scope)!: subject`). Categories: Feature, Fix, Performance, Documentation, Refactor, Internal, Other (defaul
t for unrecognized). Breaking is tracked separately via `!` marker, `breaking` type, or `BREAKING CHANGE` footer (now matched as a footer, uppercase, start-of-line, colon-terminated — not as a substring anywhere in
the body). **Breaking is never a category; a breaking feature stays a feature but is flagged.** Pure, deterministic, no LLM.

**New type:** `IChangeCategorizer`, `ConventionalCommitCategorizer`, `ChangeCategory`, `ChangeClassification`.

## Graceful degradation when PRs are missing

`ReleaseChangeResolver` turns a `CommitRange` and merged `PullRequestInfo` list into `ReleaseChange` values. With merged PRs present, one change per PR. With no PRs at all, one change per commit using the commit sub
ject. With blank/uninformative PR titles (`WIP`, `update`, `Merge ...`), falls back to the PR body's first informative line, then to a generic `PR #n`. Empty releases yield an empty set, never an exception.

**New types:** `IReleaseChangeResolver`, `ReleaseChangeResolver`, `ReleaseChange`, `ChangeSource`.

## Git history read via git CLI

`GitCliCommitReader` shells out to `git` to find the exact commits for a release — the range since the previous tag (`<prev>..<tag>`), or all history up to the tag when there is no previous. Clear errors for unknown
/blank tags. Avoids native dependencies to support planned native-AOT binaries.

**New types in Core:** `IReleaseCommitReader`, `CommitInfo`, `CommitRange`.
**New types in Infrastructure:** `GitCliCommitReader`.

## GitHub API for pull requests and releases

**`GitHubPullRequestReader`** queries GitHub's "pull requests associated with a commit" endpoint for commits in a range, keeps merged PRs only, de-duplicates by number. Returns `PullRequestInfo` (number, title, desc
ription, labels, url). Uses raw `HttpClient` + source-generated `System.Text.Json` (dependency-light, native-AOT friendly). Token optional, read from `GITHUB_TOKEN` env var.

**`GitHubReleaseNotesWriter`** updates or creates a release's notes via REST API: `GET /releases/tags/{tag}` → found: `PATCH /releases/{id}` (update); 404: `POST /releases` (create with `tag_name` + body). Returns t
he release's `html_url`. API/network failures raise clear `InvalidOperationException`s.

**New types in Core:** `IReleasePullRequestReader`, `PullRequestInfo`, `RepositoryCoordinates`, `IReleaseNotesWriter`.
**New types in Infrastructure:** `GitHubPullRequestReader`, `GitHubReleaseNotesWriter`, `GitHubHttpClientFactory`.

## LLM provider abstraction

`IChangelogModel` is the provider-agnostic seam; `ChatModel` is the single implementation over `Microsoft.Extensions.AI.IChatClient`. Anthropic is the first provider, selectable via config. API key read from env var
 (never hardcoded). Domain types: `Audience`, `GroundedFacts`, `RephraseRequest`, `FaithfulnessRequest`, `FaithfulnessReport`.

**New types in Core:** `IChangelogModel`, `ChatModel`, `Audience`, `GroundedFacts`, `RephraseRequest`, `FaithfulnessRequest`, `FaithfulnessReport`.

## Architecture and organization

**`Chartula.Core`** — pure domain logic, no I/O or external dependencies beyond `Microsoft.Extensions.AI`.
**`Chartula.Infrastructure`** — concrete I/O adapters (git CLI, GitHub API, file writers).
**`Chartula.Cli`** — composition root, command surface, configuration binding.
**`Chartula.Core.Tests`**, **`Chartula.Infrastructure.Tests`**, **`Chartula.Cli.Tests`** — unit and integration tests; CLI tests exercise configuration and DI.

See `docs/architecture.md`.

## Documentation

- `docs/architecture.md` — layering, dependency choices, why facts are established before LLM input.
- `docs/changelog-json.md` — `changelog.json` schema, field types, stability contract.
- `docs/configuration.md` — all `chartula.yaml` options with defaults.
- `docs/run-metrics.md` — how to read the run summary and decide if a check earns its cost.
- `docs/audience-filtering.md` — how each audience view is derived and why contradictions are impossible.
- `chartula.example.yaml` — minimal template (repo root, never auto-loaded); uncomment what you need.

## Fix: truncation and false breaking changes

Output was truncated to 1024 tokens (the provider default) because `MaxOutputTokens` was never set. Re-runs now always send a ceiling (configurable via `llm.maxOutputTokens`, default 16000).

`ConventionalCommitCategorizer` matched `BREAKING CHANGE` as a substring anywhere in the PR body, so prose *discussing* breaking changes *declared* them. Now matches the Conventional Commits footer: uppercase, start
-of-line, colon-terminated.

Verified against real runs: rephrasing output grew from 3,072 to 11,271 tokens, text completeness restored, false breaking-change count dropped from 6 to 0.

---

**Build:** 0 warnings / 0 errors. **Tests:** 256 passing (Core 177, Infrastructure 26, Cli 12, 21 new test categories). **Architecture:** inward-pointing dependencies, facts established deterministically before LLM
input, provider-agnostic seams, all I/O abstracted behind ports.
  Flagged for review:
    ! 'docs/audience-filtering.md' is not supported by the facts.
    ! 'title-and-description' is not supported by the facts.
    ! 'title-description-and-issues' is not supported by the facts.
    ! 'Chartula.Infrastructure.Tests' is not supported by the facts.

--- Customer ---
## Release 0.2.0

**Run metrics and observability**

Every `preview` and `generate` run now ends with a metrics summary showing rule-based check runs, thorough check runs with findings, rephrasing calls, and total token usage. The thorough check's cost is paired with
the claims it caught that the rule-based check missed, so you can see whether the second pass earns its tokens. Measurement is optional and does not affect output when disabled.

**Configuration from `chartula.yaml`**

The tool now reads `chartula.yaml` (or `.yml`) with sensible defaults for all options. Configuration layers before environment variables, so env vars override the file. A minimal example file ships in the repo; full
 options are documented. All settings remain optional—the tool works with no configuration file at all. Configuration errors report clearly instead of crashing.

**Configurable category display**

Category ordering, display names, and breaking-change prominence are now configurable via the `categories` section alongside existing `labels`, `factBase`, and `faithfulness` sections.

**Configurable fact-base depth**

Three modes control how much source material feeds the fact base: title only, title and PR description (the default), or title, description, and linked issues. Set via `Chartula:FactBase:Depth` in configuration.

**Two-pass faithfulness checking**

A rule-based check runs first and catches obvious hallucinations for free: invented numbers, quoted names not in the facts, and breaking-change claims without a breaking fact. A second LLM pass (on by default, confi
gurable via `Chartula:Faithfulness:Thorough`) catches subtle semantic distortions the rules cannot see. Both checks are reported in the run metrics so you can measure their value over time.

**Consistent formatting and voice**

Generated text is normalized deterministically—line endings, bullet markers, whitespace, blank lines—while preserving structure. A prompt rule asks the model to write in one consistent voice and not carry over indiv
idual author tones, so each audience rendering reads as a coherent document.

**Three audience renderings from one fact base**

The technical, customer, and product-manager versions of a release are all rendered from the same underlying fact base, so they can never contradict each other. Customer text omits internal changes and links; techni
cal keeps the full set with links; product sees the full set grouped by theme.

**Changelog outputs**

The fact base is written to `changelog.json` with a stable, versioned schema. Customer and PM audience texts are stored in the same file. `CHANGELOG.md` is prepended with each new release while preserving history—re
-running the same tag replaces that section in place without duplication or reordering. Generated text is also written to the GitHub release notes, creating or updating as needed.

**Human review mode**

An optional review mode (off by default) presents each generated rendering with flagged passages highlighted, letting a maintainer approve or edit before output is written.

**Label-driven curation**

GitHub labels can exclude a PR, force it into a category, or enable an "only include labeled PRs" mode. All optional—the tool works with no labels. Rules are read from configuration.

**Graceful degradation when PRs are missing**

When a clean PR title is blank or uninformative, the tool falls back to the PR body or commit subject. When no associated PRs exist, it uses commit data. The tool never fails solely because PR discipline is imperfec
t.

**Commands and CLI**

`chartula preview` and `chartula generate` commands now wire the full pipeline. `preview` runs the identical flow (including generation, so you see the real result) without writing or publishing. `generate` writes o
utputs. Both commands take `--tag` and `--repo <owner/name>`, display usage on missing options, and report errors clearly.

**Bug fixes**

Fixed output truncation by setting `max_tokens` on LLM calls. Previously omitted, it defaulted to 1024 per provider, cutting off all three audience texts mid-word. Now configurable via `llm.maxOutputTokens`, default
ing to 16000.

Fixed false breaking-change detection. The categorizer was matching `BREAKING CHANGE` as a case-insensitive substring anywhere in the PR body, so prose discussing breaking changes declared one. Now matches the Conve
ntional Commits footer format: uppercase, start of line, colon-terminated.
  Flagged for review:
    ! The number '0.2.0' is not supported by the facts.

--- Product ---
## Release Metrics

Measurement is now built in. Every `preview` and `generate` run ends with a summary of what operations ran and what they cost—rule-based checks, thorough checks, rephrasing, and total tokens—so defaults can be decid
ed by data instead of guesswork.

## Configuration

The tool now reads `chartula.yaml` with sensible defaults. All existing options (`llm`, `github`, `labels`, `factBase`, `faithfulness`, `review`, `categories`, `filter`) are configurable via file or environment vari
ables, with environment taking precedence. A new `categories` section controls category order, display names, and breaking-change prominence. An example `chartula.yaml` ships in the repo; full documentation is in `d
ocs/configuration.md`.

## Commands

`chartula preview` and `chartula generate` are now wired end-to-end. Both run the complete pipeline—reading commits and PRs, building the fact base, rendering all three audiences, running rule-based and thorough fai
thfulness checks, and applying review—then either preview the results (writing nothing) or write outputs to disk and GitHub.

## Outputs

Releases are now written to three destinations:

- **`changelog.json`** stores the fact base and all three audience renderings (technical, customer, product), backed up in one durable, machine-readable file.
- **`CHANGELOG.md`** prepends each release at the top, preserving history and replacing prior versions in place on re-run for idempotency.
- **GitHub release notes** are created or updated via the REST API, never duplicated.

## Generation & Reasoning

The pipeline generates changelog text by rephrasing a fact base, never inventing. A system prompt establishes the rules: rephrase only, treat categories and breaking flags as given, keep output sparse on thin facts,
 no preamble or conclusion. Each audience (technical, customer, product) is rendered from the same facts with deterministic filtering per audience, so renderings can never contradict each other.

## Faithfulness

Two passes check the output for hallucinations:

- **Rule-based check** (always on, zero tokens): flags numbers, feature names, or breaking claims not present in the facts.
- **Thorough check** (on by default, toggleable): runs a second LLM pass to catch subtle meaning-level distortions like "bug fixed" rendered as "security hole closed."

A report pairs each claim caught only by the thorough check with its token cost, answering directly whether it earns its cost.

## Curation

Changes are curated deterministically before the LLM sees them:

- **Categorization** reads Conventional Commit prefixes (feat, fix, docs, perf, refactor, internal, etc.) with a sane `Other` default. Breaking is tracked separately via `!` marker, `breaking` type, or `BREAKING CHA
NGE` footer.
- **Label rules** (from config) can exclude changes, force a category, or require all changes to be labeled—all optional, all case-insensitive.
- **Filtering** drops internal and chore changes by default (overridable), but never drops a breaking change.
- **Fact-base depth** (from config) controls what source material is included: title-only, title + PR description (default), or + linked issues.
- **Graceful degradation**: when clean PRs are missing, the tool falls back to commit data; when PR titles are blank or uninformative, it uses the PR body or a generic fallback.

## Review

An opt-in review mode lets a maintainer approve or edit generated text before publishing. The reviewer sees the text with flagged passages (findings from both checks) highlighted, and can approve as-is or return an
edited version.

## Consistency

Formatting is normalized per audience—bullet markers, spacing, blank lines, and trailing whitespace—while keeping structure intact. A tone rule in the system prompt ensures one consistent voice throughout, with no i
ndividual author's style carried over.

## Fixes

Two release blockers found by dogfooding v0.1.0 are now fixed:

- **Truncation**: `ChatModel` now always sends `maxOutputTokens` (configurable, default 16000) so output is never silently cut off.
- **False breaking changes**: `ConventionalCommitCategorizer` now matches the `BREAKING CHANGE` footer rule strictly—uppercase, start of line, colon-terminated—instead of flagging any prose that mentions breaking ch
anges.

## Documentation

`docs/` is now visible and complete: `architecture.md` covers the layering and dependency choices, `changelog-json.md` documents the output schema and stability contract, `configuration.md` covers all configuration
options, and `run-metrics.md` explains how to read the metrics summary. The README links to all of them, and `CONTRIBUTING.md` documents the architecture and commit scope conventions actually in use.
  Flagged for review:
    ! 'security hole closed.' is not supported by the facts.

Preview only - nothing was written or published.

Run metrics
  Rule-based check: 3 runs, 3 with findings, 6 claims, no tokens
  Thorough check:   3 runs, 0 with findings, 0 claims, 45,721 in / 66 out
    caught 0 claims the rule-based check missed, for 45,787 tokens in 3 calls
  Rephrasing:       3 calls, 39,476 in / 5,419 out
  Total:            90,682 tokens
❯ tmux capture-pane -pS - > /home/goldbarth/repos/chartula-notes/sonnet-5-out.md

