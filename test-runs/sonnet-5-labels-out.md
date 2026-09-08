sonnet-5-labels-out, rendered by Chartula from v0.1.0

--- Customer ---

### What needs action

- **API key required**: Every `preview` and `generate` run now calls a language model (Anthropic to start) to write the changelog text you see. Provide an API key for that provider through an environment variable before running either command.

### What's New

- **New commands**: `chartula preview --tag <tag> --repo <owner/name>` shows exactly what a release's changelog text, `CHANGELOG.md` update, and GitHub release notes would look like, without writing or publishing anything. `chartula generate` with the same flags writes `changelog.json`, updates `CHANGELOG.md`, and updates the GitHub release notes, and both commands report a clear error instead of crashing on a missing option or an unknown command.
- **GitHub rate limits**: Chartula reads merged pull requests from GitHub to build each release's changelog, which works unauthenticated on public repositories but is subject to GitHub's rate limits. Set the `GITHUB_TOKEN` environment variable if you hit them.
- **Configuration file**: Chartula now reads settings from a `chartula.yaml` (or `.yml`) file in your project, layered under any environment variables you set, and a run with neither a file nor environment variables still uses the built-in defaults. Copy the shipped `chartula.example.yaml`, uncomment what you need, and save it as `chartula.yaml`.
- **Category settings**: A `categories` section in `chartula.yaml` now controls how categories are presented - their `order`, their display `names`, and whether breaking changes stand out via `breakingProminent` (on by default). Set any of these in the `categories` section; an unrecognized category name in `order` fails with a clear error naming the valid categories.
- **Fact base depth**: A `depth` setting in the `factBase` section of `chartula.yaml` controls how much of each pull request feeds the changelog - title only, title plus description (the default), or title plus description plus linked issues. Set it to `title`, `description`, or `full` to change it.
- **Default filtering**: Internal and chore-type changes are now left out of the changelog by default, though a breaking change is always kept even if its category would otherwise be excluded. Override the excluded categories in the `filter` section of `chartula.yaml` if you want a different set.
- **Label rules**: A GitHub label can now drop a pull request from the changelog, force it into a specific category, or - in "only labeled" mode - be required before a change is included at all; with no labels configured, nothing changes. Configure these rules in the `labels` section of `chartula.yaml`.
- **Review mode**: An opt-in review mode lets you see each generated text alongside its flagged passages and approve it as-is or edit it before anything is written, and it stays off by default so nothing is held up unless you turn it on. Enable it in the `review` section of `chartula.yaml`, or set `Chartula__Review__Enabled=true`.
- **Thorough check toggle**: A second, LLM-based check now re-reads each generated text against the release facts and flags claims the wording doesn't support, catching meaning-level mistakes a simple word search would miss, and it runs by default. Turn it off in the `faithfulness` section of `chartula.yaml`, or set `Chartula__Faithfulness__Thorough=false`, if the extra tokens aren't worth it to you.
- **Rule-based check**: A free, always-on check now scans each generated text for numbers, quoted names, or breaking-change claims that aren't in the release facts, flagging them for your attention before anything ships. It runs on every release with no language-model call and no toggle.
- **Audience-specific text**: Each release now produces three versions of the changelog - technical, customer, and product-manager - from the same set of facts, so they can't contradict each other. The customer version leaves out internal-only changes and their links unless a change is breaking, in which case it always appears; the technical version keeps links and the full set of changes, and the product-manager version is grouped by theme.
- **Run metrics**: Every `preview` and `generate` run now ends with a metrics summary showing how many runs and tokens each check and the rephrasing step used, including how many claims the LLM-based check caught that the free check missed and at what token cost. This lets you judge for yourself whether the LLM-based check is worth keeping on.
- **GitHub release notes**: Publishing a release again for the same tag updates that release's existing GitHub notes in place rather than creating a duplicate release.
- **CHANGELOG.md**: Each release is now added as a new section at the top of `CHANGELOG.md`, with earlier sections kept exactly as they were. Running the same release again replaces just that section in place rather than duplicating it or moving it out of order.
- **Automatic categorization**: Each change's category (feature, fix, performance, documentation, refactor, or internal, with a default "other" for anything unrecognized) is now assigned automatically from its conventional-commit-style title. Breaking is tracked separately, so a breaking feature still shows as a feature but is also flagged as breaking.
- **Linked issues**: Closing keywords such as `closes #12`, `fixes #34`, or `resolves #56` in a pull request's title or body are now automatically linked to that change in the changelog.
- **Fallback for missing PR data**: When a release has no associated pull requests, or a pull request's title is blank or uninformative (like `WIP` or `update`), the changelog now falls back to the commit message or the pull request's description instead of leaving that change out.
- **Grouped by pull request**: Changes are now summarized per merged pull request rather than per raw commit, using each pull request's title, description, and labels.
- **Rephrase-only output**: The generated text now only rephrases the facts it's given - it won't introduce a number, name, or detail that isn't in your commit and pull-request data - and stays brief instead of padding out a short list of changes.
- Also: a release with no changes now produces an empty changelog instead of an error, and no language-model call is made in that case.

### What's Changed

- **Configuration errors**: A mistake in `chartula.yaml` now stops the run with a plain `Configuration error: ...` message instead of an unhandled exception.

### Bug Fixes

- **Truncated output**: Generated changelog text no longer gets cut off mid-word - every `preview` and `generate` run now sends an explicit output-length limit to the model instead of relying on the provider's own default, so the text renders in full and won't be mistakenly flagged by the LLM-based check as an unsupported claim. The limit defaults to 16,000 tokens and can be changed via `llm.maxOutputTokens`.
- **False breaking-change labels**: A change is no longer marked breaking just because its description discusses breaking changes in passing text - only a proper Conventional Commits `BREAKING CHANGE:` footer now counts. Previously, prose merely mentioning the phrase was enough to mislabel a change as breaking.
