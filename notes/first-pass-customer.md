# First pass over the customer rendering

Impressions, not labels.
Written in one sitting across six of the seven runs in `test-runs/`, before the rubric was applied to anything.
The second Haiku 4.5 run was not part of this pass.
They are kept because the rubric came out of them, not because they are evidence.

Proper labelling against C1 to C3 is still open, see issue #1.

Only the customer rendering was looked at.
It is where the differences between the runs are most obvious.

## Across all runs

No fixed output format.
Structure is whatever the model chose, which is tracked as goldbarth/chartula#96.

## Haiku 4.5

- Line breaks inside words.
- Language too technical for the audience in places.

This run was picked as the reference case for the rubric, because it is the clearest failure.
Measuring against a run that is merely so-so makes the criteria harder to see.

Output:

> Fixed output truncation by setting max_tokens on LLM calls. Previously omitted, it defaulted to 1024 per provider, cutting off all three audience texts mid-word. Now configurable via llm.maxOutputTokens, defaulting to 16000.
>
> Fixed false breaking-change detection. The categorizer was matching BREAKING CHANGE as a case-insensitive substring anywhere in the PR body, so prose discussing breaking changes declared one. Now matches the Conventional Commits footer format: uppercase, start of line, colon-terminated.

Desirable output, written by hand:

> Generated text could be cut off mid-sentence in some runs because no output length limit was set; there's now a configurable ceiling with a higher default, so text completes properly.
> Separately, changes that merely discussed "breaking changes" in their description were sometimes incorrectly labeled as breaking themselves; the detection now only matches an actual breaking-change declaration, so release notes no longer warn about breaking changes that aren't there.

## Sonnet 5, thinking off

- Technical rendering: pull requests summarised by their PR title. No format.
- Customer rendering: only two fixes generated, no feature list at all.
- Technical heading kept as-is (*"Fix: two release-blocking bugs found while testing v0.1.0 against this repository"*), no customer-facing heading produced.
- Bug descriptions too detailed and largely irrelevant to a customer. The fix is not stated clearly enough in terms of what the customer gets out of it.

Description 1:

> Generated text could be cut off mid-sentence. Requests to the language model didn't set an output length limit, so the provider silently applied its own default and truncated all three audience texts. This failed quietly - the run reported success, and the thorough check spent tens of thousands of tokens flagging the cut-off text as an unsupported claim, when the real problem was truncation. The output limit is now always set explicitly, configurable via llm.maxOutputTokens, defaulting to 16000.

Fix 1:

> Verified against a real run: rephrased text now ends in complete sentences instead of mid-word, and breaking changes dropped from 6 false positives to 0.

Description 2:

> Changes could be wrongly marked as breaking. The check for breaking changes matched the phrase "BREAKING CHANGE" anywhere in a pull request's text, so simply discussing breaking changes caused a change to be mislabelled as one. In the v0.1.0 release, six changes were incorrectly flagged this way. The check now only matches the standard breaking-change marker format, not incidental mentions.

Fix 2:

> A related issue remains open: the free, rule-based check can still flag the word "breaking" appearing anywhere in generated text, even in ordinary prose. This is advisory only and doesn't fail a run, so it's being addressed separately.

## Sonnet 5, thinking on

Readable and well aimed at the audience.
Each feature or fix description ends on the benefit to the user.

## Opus 4.8, thinking on

Understandable, partly aimed at the audience.
More technical than Sonnet 5 with thinking on, and frequently carries source references.
Does not read fluently.
Carries more information than a customer needs.
No explicit benefit at the end.

## Opus 5, thinking off

Understandable, partly aimed at the audience.
More technical than Sonnet 5 with thinking on, frequently with source references.
Reads somewhat more fluently than Opus 4.8.
More information than a customer needs.
No explicit benefit at the end.

## Opus 5, thinking on

Understandable, partly aimed at the audience.
More technical than Sonnet 5 with thinking on, frequently with source references.
Reads more fluently than Opus 4.8.
More information than a customer needs.
No explicit benefit at the end.
