sonnet-5-place-out, rendered by Chartula from v0.1.0

--- Customer ---

---
title: Release 0.1.0
description: This release builds Chartula's full pipeline for turning pull requests and commits into fact-grounded, multi-audience release changelogs, adds configuration, review, and accuracy safeguards around that pipeline, and fixes two release-blocking bugs found while dogfooding v0.1.0.
publishedAt: 2026-07-17
---

### What needs action

- **LLM provider key:** Generating or previewing a changelog calls a language-model provider, so you can only run `generate` or `preview` once you supply that provider's API key. Set it as an environment variable or in the `llm` section of chartula.yaml.

### What's New

- **`preview` and `generate` commands:** Running `chartula preview --tag <tag> --repo <owner/name>` shows what a release's changelog would look like without writing or publishing anything, while `chartula generate --tag <tag> --repo <owner/name>` produces and writes it. Both commands print a usage screen and a clear error message for missing options or an unknown command instead of crashing.
- **Release scope:** Each run covers only the commits made since the previous tag, or your entire history when it's the first tagged release, so the changelog only ever reflects what's actually new.
- **Pull request details:** Changes are matched to the merged pull requests they came from, so each entry can carry that pull request's title, description, labels, and link instead of just a raw commit message. Set a `GITHUB_TOKEN` environment variable if you need authenticated access to a private repository or to avoid GitHub's rate limits.
- **Imperfect PR data:** When a commit isn't linked to a merged pull request, or a pull request has a blank or uninformative title such as "WIP" or "update", the change still shows up in the changelog, drawn instead from the commit message, the pull request's description, or a generic label. You can rely on every change appearing even when pull request discipline isn't perfect.
- **Automatic categorization:** Each change is assigned a category such as Feature, Fix, Performance, Documentation, Refactor, or Internal based on its title, with unrecognized titles falling back to a general "Other" category. Whether a change is breaking is tracked separately, so a breaking feature is still shown as a feature.
- **Label-based curation:** GitHub labels can exclude a pull request from the changelog, force it into a specific category, or, with an only-labeled mode turned on, require a label before it's included at all, and the tool works the same if you don't use labels at all. Set these rules in the `labels` section of chartula.yaml.
- **Filtering internal changes:** Internal and chore-type changes are left out of the changelog by default, though a change marked breaking is never left out. Adjust which categories are excluded in the `filter` section of chartula.yaml.
- **Fact-base depth:** You can choose how much of each pull request feeds the changelog - title only, title and description, or title, description, and linked issues - so you can match it to your team's pull request style. Title and description is the default; set your choice in the `factBase` section of chartula.yaml.
- **changelog.json facts:** changelog.json records the underlying facts for a release - title, pull request number, link, category, user-visible and breaking flags, and linked issues - giving you a durable, machine-readable record you can build other tools on.
- **Three audience versions:** Every release produces technical, customer, and product-manager versions from the same set of facts, so the three can never contradict each other. The customer version leaves out internal changes and their links, the technical version keeps links and the full set of changes, and the product version covers the full set grouped by theme.
- **Consistent formatting and voice:** Each version of the changelog uses normalized bullet markers, line endings, and spacing, and is written in one consistent voice, so it reads as one coherent document regardless of how individual pull requests were worded.
- **Text stays grounded in the facts:** Generated text only rephrases the facts it's given and treats each change's category and breaking marker as fixed, so you can trust it not to invent numbers, names, or claims. When there's little to say about a release, the output stays brief rather than padded out.
- **Rule-based accuracy check:** Every generated text is checked, at no extra token cost, for numbers, quoted or backticked names, and breaking-change claims not backed by the underlying facts. This check always runs, so obvious mismatches are caught automatically.
- **Thorough accuracy check:** A second check also looks for subtler mismatches between the generated text and the facts, such as a change's meaning being altered in rephrasing, and it runs automatically by default so issues the free check misses still get caught. Turn it off in the `faithfulness` section of chartula.yaml if you don't want the extra tokens it spends.
- **Review mode:** You can turn on a review step that shows the generated text together with any flagged passages, so a maintainer can approve it as-is or edit it before anything is written rather than publishing it unreviewed. It's off by default; enable it in the `review` section of chartula.yaml.
- **CHANGELOG.md history:** Each release is written as a new section at the top of CHANGELOG.md, with existing sections kept intact below it, so your history is preserved and never reordered. Running the same release again replaces just that section in place instead of duplicating it.
- **GitHub release notes:** The generated changelog text is written to the release's notes on GitHub, and running the same tag again updates that release's notes rather than creating a second one, so the notes always stay in sync with your latest run.
- **All audience texts in changelog.json:** The customer, technical, and product-manager texts for a release are stored together in changelog.json's renderings, so they're backed up in one file inst
