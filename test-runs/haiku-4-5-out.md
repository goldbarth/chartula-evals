--- Technical ---
## Run metrics reporting

Every `preview` and `generate` run now ends with a summary showing rule-based and thorough check execution counts, tokens consumed, and the claims caught only by the thorough check. This makes defaults measurable; t
he indented line pairs unique findings with their token cost, so you can decide whether the thorough check earns its cost across real releases.

New types in `Chartula.Core/Observability/`: `IRunMetrics` sink, `RunMetrics`, `NullRunMetrics`, `RunReport` and `RunReportFormatter`. `ChatModel` reports token usage per `LlmOperation`. `ReleasePipeline` records bo
th checks' findings and returns the report on `ReleaseOutcome`. Measurement is optional; runs without a sink produce identical output. Documented in `docs/run-metrics.md`.

## Category configuration

Category presentation is now configurable via the `categories` section in `chartula.yaml`: `order`, `names`, and `breakingProminent` (default `true`). `CategorySettings` parses configuration and rejects unknown cate
gory names. `GroundedFactsFactory` centralizes audience filtering, category ordering and display naming. Documented in `docs/configuration.md`.

## YAML configuration with sensible defaults

`chartula.yaml` (or `.yml`) now refines behavior via `AddChartulaYaml`, layered before environment variables so environment overrides YAML. All section options (`llm`, `github`, `labels`, `filter`, `factBase`, `fait
hfulness`, `review`, `categories`) already existed; this adds the file as a source. With neither file nor env vars, every option uses its default. `chartula.example.yaml` provides a minimal template; full options li
ve in `docs/configuration.md`. Configuration errors are reported as clear `Configuration error: ...` messages. New `Chartula.Cli.Tests` project covers no-config defaults and config-refines-behavior paths.

## CLI commands: preview and generate

`chartula preview` and `chartula generate` take `--tag` and `--repo <owner/name>`. `ReleasePipeline` orchestrates the flow: read commit range and PRs, build fact base, render all audiences, run rule-based and thorou
gh faithfulness checks, then review. `generate` writes `changelog.json`, `CHANGELOG.md`, and GitHub release notes; `preview` runs identically but writes and publishes nothing. Both give clear, readable per-audience
output. Pipeline errors are caught and reported. Documented in the usage screen; interactive console review still uses auto-approve until stdin review is built.

## Audience texts in changelog.json

`ChangelogDocument` now includes a `renderings` object keyed by audience (`technical`, `customer`, `product`), written in fixed order. Customer and product-manager texts are stored in the JSON alongside deterministi
c facts, backed up inside one file rather than scattered as marketing files. `schemaVersion` stays **1** — adding an optional field is non-breaking. Old consumers ignore `renderings`. Documented in `docs/changelog-j
son.md`.

## GitHub release notes writer

`IReleaseNotesWriter` port with `GitHubReleaseNotesWriter` implementation. For a given tag, `GET /releases/tags/{tag}` finds the release: found, `PATCH /releases/{id}` updates it; 404, `POST /releases` creates with
`tag_name` + `body`. Re-running for the same tag updates that one release without duplication. API/network failures raise clear `InvalidOperationException`s.

## CHANGELOG.md writer with history preservation

`ChangelogMarkdownComposer` composes new content from existing file and release. The new section is prepended at the top; existing sections are kept verbatim. Re-running the same tag replaces that section in place (
idempotent, preserves history order). Brand-new file gets a `# Changelog` title. `IChangelogMarkdownWriter` port with `FileChangelogMarkdownWriter` in Infrastructure.

## Human review mode (opt-in)

`ReviewCoordinator` gates each rendering on an opt-in toggle. Review **off** (default): text passes through approved as-is. Review **on**: item goes to `IReviewer` who approves it or returns an edited version. `Revi
ewPresentation` formats generated text with flagged passages highlighted for a maintainer. `AutoApproveReviewer` is the non-interactive default. Bound via `Chartula:Review` toggle.

## Thorough faithfulness check via second LLM pass

`ThoroughFaithfulnessChecker` runs a second LLM pass, turning the fact base into grounded facts and flagging unsupported claims (e.g., "bug fixed" rendered as "security hole closed"). When disabled or with nothing t
o check, it returns a faithful report with no LLM call. Enabled by default via `Chartula:Faithfulness:Thorough`. The faithfulness prompt moved into `IChangelogPromptBuilder.BuildFaithfulnessPrompt` with explicit mea
ning-level-distortion instruction.

## Rule-based faithfulness check (zero token cost)

`RuleBasedFaithfulnessChecker` flags obvious hallucinations before any LLM check: numbers not in facts (except PR numbers, linked issues, and numbers in titles/descriptions/tags), quoted/backticked names absent from
 facts, and breaking-change claims without a breaking fact. No LLM dependency, no tokens, always on. Uses source-generated regexes (AOT-friendly). Flags are advisory, surfaced for review.

## Consistent formatting and tone per audience

`ChangelogFormatter` normalizes model output with conservative rules: normalized line endings, single `- ` bullets, trimmed trailing whitespace, collapsed blank lines. Applied to every rendering for consistency rega
rdless of model output. Prompt adds a tone rule: write in one consistent voice, not carrying over individual author tone. Formatting is deterministic (testable with stub model); tone comes from the prompt (language
judgment).

## Multi-audience rendering from one fact base

`ReleaseRenderer` produces technical, customer, and product-manager versions from one `FactBase`. Customer omits non-user-visible changes and links. Technical keeps PR links and full change set. Product sees the ful
l set. Audience selection is deterministic (in code, not the LLM). All three derive from the same source, so they can never contradict.

## Prompt architecture: rephrase facts, never invent

`IChangelogPromptBuilder` / `ChangelogPromptBuilder` produce a `ChangelogPrompt` (system + user). System prompt pins the model to rephrasing: never introduce facts/numbers/names not in the list; treat each fact's ca
tegory and `(breaking)` marker as established; on thin facts stay brief and do not pad, speculate, or invent; no preamble/conclusion. Plus per-audience guidance. User prompt carries only the facts. `ChatModel` deleg
ates to the builder. Categories and flags reach the model as text embedded by the generator; the prompt presents them verbatim and instructs the model not to decide them.

## Changelog generation through provider interface

`ReleasePipelineGenerator` / `ReleaseChangelogGenerator` turns the fact base into grounded fact statements and makes exactly one `IChangelogModel.RephraseAsync` call per release. Empty fact base makes no call. Provi
der failures are caught and returned as a failed result (carrying release tag and provider message); cancellation propagates. Generator depends only on `IChangelogModel` — no provider type is referenced.

## changelog.json serialization (stable, versioned)

`ChangelogDocument` defines the stable on-disk shape (`schemaVersion` + `tag` + `changes`), separate from domain `FactBase` so the domain can evolve without breaking the file format. `ChangelogJsonSerializer` (pure,
 deterministic, source-generated) serializes `FactBase` to JSON with category written as name for a stable, readable record. `IChangelogJsonWriter` port with `FileChangelogJsonWriter` in Infrastructure. `schemaVersi
on` (currently `1`) is the contract; adding optional fields is non-breaking, removing/renaming/re-meaning bumps the version. Every field is deterministic fact; nothing is LLM-generated. Documented in `docs/changelog
-json.md`.

## Configurable fact-base depth

`FactBaseDepth` offers three modes: `TitleOnly`, `TitleAndDescription` (default), `TitleDescriptionAndIssues`. `FactBaseBuilder` honours the depth; linked issues populate only in the deepest mode. Read from `Chartul
a:FactBase:Depth` config. Parser accepts canonical names plus aliases (`title`, `description`, `full`) and raises clear errors on unknown values. Passed to builder via factory rather than DI service.

## Fact-base assembly from curated changes

`FactBaseBuilder` assembles the complete fact base: resolves changes with missing-PR fallback, drops filtered-out changes, maps each survivor to a `ChangeFact`. Category and breaking flag come from deterministic cat
egorization; a label can force category. `IsUserVisible` derives from category (outward-facing categories plus breaking changes). `LinkedIssues` parse from GitHub closing keywords (`closes/fixes/resolves #n`) in tit
le and body. Category and flags never come from an LLM.

## Fact data model (per-change index card)

`ChangeFact` in Core captures established facts per change: title, PR number, link, category, user-visible flag, breaking flag, linked issues, optional description (per fact-base depth). Every field derives determin
istically; nothing is LLM-generated. PR-only fields (number, link) are nullable so commit-based changes fit the same shape.

## Internal/chore filtering with label rules

`ChangeFilter` / `ChangeFilterRules` drop internal/chore changes by default. Decision order: a label that excludes the change wins outright → breaking change is never dropped → otherwise dropped when effective categ
ory (label-forced or deterministic) is in excluded set. Default excludes `Internal`; overridable via `Chartula:Filter:ExcludeCategories`. Breaking safeguard is deterministic (from the breaking flag, not guesswork).

## Label-driven curation rules

`LabelRulePolicy` / `LabelRules` steer curation via GitHub labels from config. Excluded labels, label-to-category overrides, and only-include-labeled mode are all optional. Precedence: exclusion wins; then only-labe
led drops unlabeled; otherwise included with first matching label deciding forced category. `LabelRules.None` ignores labels; tool works with no labels at all. Matching is case-insensitive. Parsed from `Chartula:Lab
els` config with clear error on unknown category names.

## Deterministic categorization from Conventional Commits

`ConventionalCommitCategorizer` reads Conventional Commit conventions from change title (`type(scope)!: subject`). `ChangeCategory` includes Feature (`feat`), Fix (`fix`), Performance (`perf`), Documentation (`docs`
), Refactor (`refactor`), Internal (`build`/`ci`/`chore`/`test`/`style`/`revert`), and **Other** as default for unrecognized/prefix-less titles. Breaking tracked separately via `ChangeClassification.IsBreaking` (fro
m `!` marker, `breaking` type, or `BREAKING CHANGE` footer), so breaking feature stays feature but is flagged. Pure, deterministic, source-generated regex (AOT-friendly). No LLM involved.

## Graceful degradation when PRs are missing

`ReleaseChangeResolver` turns `CommitRange` and merged `PullRequestInfo` list into `ReleaseChange` values (title, description, number, url, labels, `ChangeSource`, commit sha). With merged PRs present, one change pe
r PR (`Source = PullRequest`). No PRs at all, one change per commit using commit subject (`Source = Commit`). Blank/uninformative PR title (e.g., `WIP`, `update`, `Merge ...`) falls back to PR body's first informati
ve line, then generic `PR #n`. Empty release yields empty set, never an exception. Pure domain logic, no I/O.

## GitHub pull request reader

`IReleaseCommitReader` port with `GitHubPullRequestReader` implementation. For commits in a `CommitRange`, queries GitHub's "pull requests associated with a commit" endpoint, keeps merged PRs only, de-duplicates by
number. Returns `PullRequestInfo` (number, title, description, labels, url). Uses raw `HttpClient` + source-generated `System.Text.Json` (dependency-light, native-AOT friendly). Token read from `GITHUB_TOKEN` env va
r (optional; public repos work unauthenticated). API/network failures and malformed responses raise clear `InvalidOperationException`s.

## Git commit reader

`IReleaseCommitReader` port with `GitCliCommitReader` implementation. Shells out to `git` for the range since previous tag (`<prev>..<tag>`), or all history to tag when no previous tag (first release). Returns `Comm
itRange` with `IsFirstRelease` flag. Uses git CLI (no native deps, supports native-AOT goal). Clear errors for unknown/blank tags.

## LLM provider abstraction

`IChangelogModel` port with `ChatModel` implementation, backed by provider-agnostic `Microsoft.Extensions.AI.IChatClient`. Domain types: `Audience`, `GroundedFacts`, `RephraseRequest`, `FaithfulnessRequest`, `Faithf
ulnessReport`. Composition root wires Anthropic as first provider; selectable via config. API key read from env var, never hardcoded. Tests exercise seam with stub `IChatClient` (no live call).

## Output token limit fixed; breaking-change false positives eliminated

Two release blockers fixed. Calls went out without `ChatOptions`, so `MaxOutputTokens` was never set, defaulting to provider's 1024; all three audience texts were cut off mid-word. Ceiling now always sent, configura
ble via `llm.maxOutputTokens`, defaulting to 16000. `MentionsBreakingChange` searched whole body for `BREAKING CHANGE` as substring, so prose discussing breaking changes declared one; now matches Conventional Commit
s footer (uppercase, start of line, colon-terminated).

## Documentation refresh

README now leads with wordmark (responsive via `<picture>` + `prefers-color-scheme`). Long tables became prose for mobile readability; short-fact tables remain. New `docs/architecture.md` documents layering, inward-
pointing dependency rule, why facts are established before LLM, and where each concern lives. Documentation index in README. All relative links verified. Every documented default checked against code. CONTRIBUTING l
inks architecture and fixtures, lists actual commit scopes used.

## Prompt text separated into partial class

`ChangelogPromptBuilder` split across two files: `ChangelogPromptBuilder.Prompts.cs` holds prompt strings only (system header, four rules, per-audience guidance); `ChangelogPromptBuilder.cs` holds composition logic.
 Prompt text byte-for-byte unchanged; pure refactor so iterating on wording is text-only work.
  Flagged for review:
    ! 'ReleasePipelineGenerator' is not supported by the facts.
    ! Changelog generation through provider interface: `ReleasePipelineGenerator` / `ReleaseChangelogGenerator`
    ! Output token limit fixed: the feature now defaults to 16000 tokens
    ! Breaking-change false positives eliminated: now matches Conventional Commits footer (uppercase, start of line, colon-terminated)
    ! GitHub pull request reader: `IReleaseCommitReader` port with `GitHubPullRequestReader` implementation
    ! Git commit reader: `IReleaseCommitReader` port with `GitCliCommitReader` implementation

--- Customer ---
## Run metrics now show what each check costs and catches

Every `preview` and `generate` command now reports token usage and findings per check, so you can see whether the thorough LLM pass earns its cost. The summary pairs unsupported claims caught **only** by the thoroug
h check with the tokens spent finding them, answering the keep-or-drop question directly from real data.

## Categories are now configurable

You can set the order, display names, and breaking-change prominence of categories in `chartula.yaml` under a new `categories` section, without touching code.

## Configuration now reads from chartula.yaml

The tool reads `chartula.yaml` (or `.yml`) with sensible defaults and never requires a file. Environment variables still override YAML values. An example config ships in the repo; full options are documented.

## Commands are now wired: preview and generate

`chartula preview` shows what would be generated without writing or publishing anything. `chartula generate` produces and writes the outputs. Both take `--tag` and `--repo <owner/name>` and report progress per audie
nce.

## All audience texts are stored in changelog.json

Customer and product-manager renderings are now backed up in `changelog.json` alongside the technical one, under a `renderings` object keyed by audience.

## Generated text is written to GitHub release notes

The generated changelog text updates the GitHub release notes for the tag. Re-running the same tag updates that release in place instead of creating a duplicate.

## CHANGELOG.md is now prepended and preserved

New releases are added at the top of `CHANGELOG.md`, existing history stays intact, and re-running the same tag replaces that section in place without duplication.

## Human review is now optional

When enabled via `Chartula:Review`, flagged passages are presented for approval or editing before output is written. Review is off by default.

## Thorough faithfulness checking catches semantic hallucinations

A second LLM pass now checks generated text against the fact base for meaning-level distortions (e.g., "bug fixed" rendered as "security hole closed"). On by default; disable via config if needed.

## Rule-based faithfulness checking flags obvious hallucinations for free

Numbers, quoted names, and breaking-change claims not present in the facts are flagged before any LLM call, catching crude hallucinations with zero token cost.

## Formatting and tone are now consistent per audience

Formatting is deterministically normalized (bullet markers, spacing, blank lines) on every rendering. A new prompt instruction tells the model to write in one consistent voice and not carry over individual author to
nes.

## Three renderings come from one fact base

Technical, customer, and product-manager versions are all generated from the same facts, so they can never contradict each other. Technical keeps links and the full changeset; customer is benefit-focused and omits n
on-user-visible changes; product sees the full set grouped by theme.

## Prompts are now first-class and testable

The system prompt pins the model to rephrasing established facts only, never inventing details, categories, or flags. Categories and facts reach the model as text; the model is instructed to use them as given, not d
ecide them.

## Generation now runs through the provider interface

A single LLM call per release turns the fact base into a grounded summary. Empty fact bases make no call at all.

## Fact base is now durable and documented

The release facts are written to `changelog.json` as a stable, machine-readable record separate from LLM-generated text. The format is versioned and documented.

## Fact-base depth is now configurable

Choose how much PR data feeds the fact base: title only, title and description (the default), or title, description, and linked issues. Set via `Chartula:FactBase:Depth` in config.

## Facts are now assembled from curated changes

The fact base is built by mapping filtered, categorized, label-steered PRs to structured fact objects. Category and breaking flag come from deterministic code, never from the LLM.

## Facts are now defined with a structured model

Each change is captured as a `ChangeFact` with title, PR number, link, category, flags, and linked issues. Everything in the model is derived deterministically.

## Internal and chore changes are now filtered by default

Changes in the `Internal` category are excluded by default. Exclude other categories or customize the list via `Chartula:Filter:ExcludeCategories`. Breaking changes are never dropped.

## Labels now steer curation without code changes

GitHub labels can exclude PRs, force them into a category, or switch on "only include labeled" mode. Rules are read from `Chartula:Labels` in config.

## Changes are now categorized by Conventional Commits before generation

Titles are parsed for Conventional Commit prefixes (`feat`, `fix`, `perf`, `docs`, `refactor`, chore-like types) and assigned deterministically. Unrecognized changes default to `Other`. Breaking is tracked separatel
y via a `!` marker, type, or footer, so a breaking feature stays a feature but is flagged.

## Missing PRs no longer block the pipeline

When PR discipline is imperfect, the tool falls back: no PRs at all uses commit subjects; blank or uninformative PR titles fall back to the body's first informative line or a generic fallback. The pipeline still pro
duces useful output.

## Merged PRs are now read from the GitHub API

Associated merged PRs are fetched for the commit range from GitHub, providing title, description, labels, number, and link per change instead of raw commits.

## Commit ranges are now read from git

The tool finds commits since the previous tag (`<prev>..<tag>`), or all history when there is no previous tag (first release). Unknown or blank tags produce clear errors.

## An LLM provider interface is now the seam

`IChangelogModel` abstracts the LLM provider. Anthropic is wired as the first provider; swapping providers is a composition-root change only. API keys are read from environment variables, never hardcoded.

## Output truncation is now bounded and configurable

Calls now always send `MaxOutputTokens` to prevent silent truncation when the provider's default is too low. The ceiling is configurable via `llm.maxOutputTokens` in config, defaulting to 16,000.

## False breaking-change detection is now precise

The breaking-change footer is now matched only when it appears at line start and is colon-terminated, per Conventional Commits. Previously, any mention of the word triggered a false positive.
  Flagged for review:
    ! The number '000' is not supported by the facts.
    ! All audience texts are stored in changelog.json
    ! The breaking-change footer is now matched only when it appears at line start and is colon-terminated, per Conventional Commits. Previously, any mention of the word triggered a false positive.

--- Product ---
## Run metrics and cost visibility

Every `preview` and `generate` run now reports what it did and what it cost — rule-based and thorough faithfulness checks, rephrasing, and total token usage — so defaults can be decided by data instead of guesswork.
 The thorough check's cost is paired with the claims it caught that the rule-based check missed, making it clear whether the tokens buy anything.

## Configuration from `chartula.yaml`

The tool now reads `chartula.yaml` (or `.yml`) with sensible defaults; configuration is never required. The file is layered before environment variables, so env overrides YAML. New `categories` section configures ca
tegory order, display names, and breaking-change prominence. All sections (`llm`, `github`, `labels`, `factBase`, `faithfulness`, `review`, `filter`, `categories`) are independently editable; untouched sections keep
 their defaults.

## End-to-end pipeline: preview and generate

`chartula preview` and `chartula generate` commands now wire the entire pipeline together. Both run the identical flow — reading commits, building the fact base, rendering all three audiences, running both faithfuln
ess checks, and optionally reviewing — but preview writes and publishes nothing while generate produces `changelog.json`, `CHANGELOG.md`, and GitHub release notes. Errors are caught and reported clearly rather than
crashing.

## Outputs: JSON, Markdown, and GitHub

- **`changelog.json`**: durable, machine-readable record of the release fact base (tag, changes with categories/flags/linked issues) plus all three audience renderings (technical, customer, product).
- **`CHANGELOG.md`**: new release section prepended at the top, existing content preserved intact and idempotent on re-run (same tag replaces in place rather than duplicating).
- **GitHub release notes**: generated text written to or updated on the GitHub release, never duplicated.

## Fact base and filtering

The fact base is built from merged PRs (with commit fallback when PRs are missing), with each change mapped to a `ChangeFact` holding title, category, PR number/link, user-visible and breaking flags, and linked issu
es. Deterministic Conventional Commit categorization happens before any LLM sees the data. Filtering combines category and label rules to drop internal/chore changes by default (overridable via config), but breaking
 changes are never dropped. Fact-base depth is configurable (title-only, title + description, or + linked issues; default is middle).

## Label rules and category control

GitHub labels now steer curation: exclude a PR, force it into a category, or enable "only include labeled PRs" mode. All label rules are optional and case-insensitive; the tool works with no labels. Unknown categori
es in configuration fail at startup with a clear error.

## Formatting and tone per audience

Each rendering is normalized with conservative, structure-preserving rules — consistent line endings, single bullet markers, trimmed whitespace, collapsed blank lines — while leaving headings and prose intact. The p
rompt instructs the model to write in one consistent voice and format without carrying over individual author tone. All three audiences (technical with links and full detail, customer focused on benefits with non-us
er-visible changes omitted, product grouped by theme) derive from the same fact base so they can never contradict each other.

## Faithfulness: rule-based then thorough

A rule-based check catches obvious hallucinations for free — invented numbers, quoted names that don't appear in the facts, breaking-change claims without supporting facts — before any LLM call. A second LLM pass th
en checks the text semantically against the fact base, flagging unsupported claims. Both checks are toggleable (thorough on by default, rule-based always runs). Flagged passages feed an opt-in review mode where a ma
intainer approves or edits before output is written.

## Documentation

- **`docs/architecture.md`**: layering, dependency choices, and why facts are established before an LLM.
- **`docs/configuration.md`**: full option set with defaults.
- **`docs/changelog-json.md`**: schema, field types, and stability contract.
- **`docs/run-metrics.md`**: how to read the summary and decide whether the thorough check is worth its cost.

## Fixes

Two release blockers found by dogfooding: output truncation (missing `max_tokens` in chat options, now configurable with a 16000-token default) and false breaking-change detection (substring match on "BREAKING CHANG
E" in PR bodies now correctly matches the footer format only).

Preview only - nothing was written or published.

Run metrics
  Rule-based check: 3 runs, 2 with findings, 2 claims, no tokens
  Thorough check:   3 runs, 2 with findings, 7 claims, 46,368 in / 238 out
    caught 7 claims the rule-based check missed, for 46,606 tokens in 3 calls
  Rephrasing:       3 calls, 39,476 in / 6,066 out
  Total:            92,148 tokens
❯ tmux capture-pane -pS - > /home/goldbarth/repos/chartula-notes/haiku-4-5-out.txt



