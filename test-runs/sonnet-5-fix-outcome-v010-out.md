sonnet-5-fix-outcome-v010-out, rendered by Chartula from v0.1.0

--- Customer ---

---
title: Release 0.1.0
description: This release delivers the full Chartula pipeline that turns a release's commits and pull requests into fact-checked, audience-specific release notes, publishes them to CHANGELOG.md and GitHub, and includes fixes for truncated text and mislabeled breaking changes found while dogfooding the first release.
publishedAt: 2026-07-17
---

### What's New

- **Preview and generate commands**: Two commands are now available: `chartula preview --tag <tag> --repo <owner/name>` shows the generated release notes without writing or publishing anything, while `chartula generate` runs the same process and writes the outputs. Both print a summary for each audience and report an unknown command or a missing/invalid option as a clear error instead of crashing.
- **CHANGELOG.md history**: Running `generate` adds each release as a new section at the top of CHANGELOG.md while leaving earlier sections untouched, and a first run creates the file with a title. Re-running `generate` for the same release tag replaces that section in place rather than duplicating it.
- **GitHub release notes**: Running `generate` also writes the generated text to the tag's release notes on GitHub, creating the release if it doesn't exist yet. Re-running `generate` for the same tag updates that release's notes instead of creating a second one.
- **Run metrics summary**: Every `preview` and `generate` run now ends with a summary of how many findings the rule-based and thorough checks made and how many tokens each step used, including the claims only the thorough check caught. Reading this across a few releases tells you whether the thorough check is catching anything the free check misses.
- **Rule-based faithfulness check**: Every generated release note is now checked for obvious mistakes at no extra cost: a number, a quoted or backticked name, or a breaking-change claim that isn't in your source facts is flagged for review. This check always runs and never makes a model call.
- **Thorough faithfulness check**: A second, model-based check now also compares the generated text against your source facts for meaning-level mistakes, such as a fix reworded into something it isn't. It's on by default; you can turn it off in the faithfulness section of chartula.yaml if you'd rather not spend the extra tokens.
- **Review mode**: An opt-in review step lets you see each generated text alongside its flagged passages and either approve it as written or edit it before anything is published. Review is off by default, so text passes straight through unless you turn it on in the review section of chartula.yaml.
- **Audience-specific renderings**: Each release is now rendered into three versions - technical, customer, and product-manager - all drawn from the same source facts, so they can't contradict each other. The customer version leaves out changes that aren't user-visible and their links, the technical version keeps every change and its pull request link, and the product-manager version is grouped by theme.
- **Fact-only generation**: Generated text only rephrases the facts you provide - titles, categories, and breaking markers - and never adds a number, name, or detail that isn't in them. When there's little to say about a change, the text stays short rather than being padded out.
- **Fact-base depth**: How much of a pull request feeds into the generated text is now a setting: title only, title and description (the default), or title, description, and linked issues. It's set in the factBase section of chartula.yaml.
- **Label rules**: A GitHub label can now exclude a pull request from the changelog, force it into a specific category, or, in an opt-in mode, restrict the changelog to only labeled pull requests. Label handling is optional and configured in the labels section of chartula.yaml; the tool behaves the same as before if you use no labels.
- **Filtering internal changes**: Internal and chore changes are left out of the changelog by default, though a breaking change is always kept even if its category would normally be excluded. Which categories are excluded can be changed in the filter section of chartula.yaml.
- **Change categorization**: Each change's category is now assigned automatically from its conventional-commit prefix rather than guessed, with an unrecognized prefix falling back to a sane default. Whether a change is breaking is tracked separately from its category, so a breaking feature is still shown as a feature but flagged as breaking.
- **Gathering commits and pull requests**: Chartula now determines the exact commits in a release from git and looks up the merged pull requests behind them on GitHub, including for a first release with no previous tag. When a pull request is missing or its title is blank or generic, it falls back to the pull request's description and then to the commit message instead of leaving the change out.
- **Configuration file**: Chartula now reads settings from a chartula.yaml (or .yml) file as well as environment variables, covering the LLM provider and model, GitHub access, labels, filtering, fact-base depth, faithfulness, and review. The file is optional - the tool runs on its existing defaults with none present - and a commented-out example file is shipped to copy from; an invalid value now shows a clear configuration error instead of crashing.
- **Category configuration**: How categories are ordered, displayed, and whether breaking changes are shown prominently is now configurable in a categories section of chartula.yaml, alongside the existing labels, factBase, and faithfulness sections. An unknown category name in that section is rejected with a clear error.

### Bug Fixes

- **Truncated release notes**: Generated text for all three audiences could be cut off mid-word because no output-length limit was set, letting the provider apply its own default and even causing the thorough check to flag the cut-off sentence as an unsupported claim. Output is no longer truncated by default, and you can raise or lower the limit yourself in the llm section of chartula.yaml.
- **Mislabeled breaking changes**: A change whose description merely discussed breaking changes in prose could be marked as breaking itself, mislabeling several changes in a real release even though none were breaking. Only an actual breaking-change footer now marks a change as breaking, so a mention in ordinary prose is no longer misread as one.
- Also: the rule-based faithfulness check still flags any mention of the word "breaking" anywhere in the generated text as a breaking-change claim; these flags are advisory and don't fail a run, so you may still see a flagged passage worth reviewing.
