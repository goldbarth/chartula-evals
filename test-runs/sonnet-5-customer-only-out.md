sonnet-5-customer-only-out, rendered by Chartula from v0.1.0

--- Customer ---

---
title: Release 0.1.0
description: This release delivers Chartula's full changelog pipeline — from reading commit and pull-request history to generating and publishing audience-specific release notes — along with the configuration options to steer it, and fixes two issues found while dogfooding it on its own v0.1.0 release.
publishedAt: 2026-07-17
---

### What's New

- **Commands:** Two commands, `chartula preview` and `chartula generate`, each take `--tag` and `--repo owner/name`. Preview runs the full process and shows what would be produced without writing or publishing anything, while generate writes `changelog.json`, updates `CHANGELOG.md`, and publishes the GitHub release notes; both report errors clearly instead of crashing.
- **Run metrics:** Every preview and generate run now ends with a run metrics summary showing how many rule-based and thorough checks ran, how many findings each produced, and how many tokens the thorough check and the rephrasing step used. You can use this to judge whether the thorough check is worth the tokens it costs.
- **changelog.json text:** `changelog.json` stores the generated customer and product-manager text alongside the technical text, instead of leaving them as separate marketing files in your repository.
- **changelog.json facts:** `changelog.json` also records the full list of facts behind a release — title, category, breaking flag, linked issues, and more — in a documented, versioned format you can parse.
- **GitHub release notes:** Running generate writes the release notes directly onto the matching GitHub release, and re-running it for the same tag updates that release's notes rather than creating a duplicate.
- **CHANGELOG.md:** Running generate adds each release as a new section at the top of `CHANGELOG.md`, leaving earlier releases untouched, and re-running it for the same release replaces that section in place instead of duplicating it.
- **Review mode:** An optional review mode, turned on in the review section of `chartula.yaml`, shows you the generated text with flagged passages highlighted and lets you approve it as-is or edit it before it's written; it stays off by default, so generation runs unattended unless you turn it on.
- **Thorough check:** A second, AI-based check compares the generated text against the source facts to catch subtle wording that changes a claim's meaning. It runs by default and can be turned off with the thorough option in the faithfulness section of `chartula.yaml`.
- **Rule-based check:** A free, always-on check flags any number, quoted or backticked name, or breaking-change claim in the generated text that isn't backed by the source facts, surfacing as highlighted passages when review mode is on.
- **Formatting:** Generated changelog text is now consistently formatted — uniform bullet markers, spacing, and blank lines — and written in one voice regardless of how the underlying pull requests were worded.
- **Multiple audiences:** Customer, technical, and product-manager versions of a release are generated from the same set of facts, so they can't disagree with each other: technical keeps links and the full list of changes, customer leaves out changes with no user-visible effect along with their links, and product-manager sees the full list grouped by theme.
- **Grounded text:** Generated changelog text only rephrases the established facts about a release and never introduces a number, name, or detail that isn't in them; when the source facts are thin, the text stays brief instead of being padded out.
- **Category settings:** A categories section in `chartula.yaml` lets you set the order categories appear in, give them display names, and control whether breaking changes are shown prominently; an unrecognized category name there produces a clear error listing the valid ones.
- **Configuration file:** A `chartula.yaml` (or `.yml`) file can refine Chartula's behavior across its llm, github, labels, filter, factBase, faithfulness, review, and categories settings, while Chartula still runs on sensible defaults with no file at all; a commented-out `chartula.example.yaml` ships in the repository root to copy and adjust, and an invalid value in the file produces a clear configuration error instead of a crash.
- **Fact detail depth:** How much source detail feeds each release's facts is configurable with the depth option in the factBase section of `chartula.yaml`: title only, title and description (the default), or title, description, and linked issues.
- **Filtering:** Internal and maintenance-only changes are left out of the changelog by default, though a breaking change is never left out even when its category is normally excluded; which categories are excluded can be changed with the excludeCategories option in the filter section of `chartula.yaml`.
- **Label rules:** GitHub labels can exclude a pull request from the changelog, force it into a specific category, or, with an only-labeled mode, require a label before a pull request is included at all; these rules are set in the labels section of `chartula.yaml`, and Chartula works the same with no labels at all.
- **LLM provider:** The LLM provider and model are set in the llm section of `chartula.yaml` (Anthropic is the available provider), and the API key is read from an environment variable rather than stored in the file.
- **Categorization:** Each change is placed into a category — feature, fix, performance, documentation, refactor, internal, or other — based on a conventional-commit-style prefix such as `feat:` or `fix:` in its title, with breaking changes tracked separately using a `!` marker, a breaking type, or a `BREAKING CHANGE` footer.
- **Missing PR data:** When a change has no linked pull request, or an uninformative title like "WIP" or "update", Chartula falls back to the commit message, then the pull request's description, then a generic label, so the changelog is still produced.
- **Pull request grouping:** Changes are grouped by merged pull request rather than by individual commit, pulling in each pull request's title, description, labels, and link; if GitHub's API can't be reached, you get a clear error instead of a crash.
- **GitHub token:** An optional `GITHUB_TOKEN` environment variable can be set for higher API rate limits; public repositories still work without one, subject to the standard limits.
- **Commit range:** The commits included in a release are determined automatically from the tag you pass in — everything since the previous tag, or the entire history for a first release — and an unknown or blank tag produces a clear error.

### Bug Fixes

- **Truncated text:** Generated changelog text no longer gets cut off partway through a sentence, which previously happened silently and could even trigger a false unsupported-claim warning from the thorough check. The output limit now defaults to 16,000 tokens and can be adjusted with the maxOutputTokens option in the llm section of `chartula.yaml`.
- **False breaking labels:** Changes are no longer marked as breaking just because the words "breaking change" appear somewhere in a pull request's description; only an actual `!` marker, breaking type, or `BREAKING CHANGE` footer now triggers the flag, so breaking-change prominence and review highlights reflect genuine breaking changes only.
