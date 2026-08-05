# Rubric: the customer rendering

What makes a customer-facing changelog entry shippable.
Written for the customer audience only.
The technical and product renderings are not covered here.

Each criterion is one axis.
An entry can fail one and pass the others, and the criteria are written so that it is visible which one failed.

Status: first version, not yet calibrated against a judge.
It was derived from labelling the customer sections of the runs in `test-runs/`.

## C1 - No knowledge of the codebase required

A customer entry must be fully understandable to someone who uses the product but has never seen its source code.

**Allowed (product surface):** user-facing settings, features, commands, and outputs, meaning things a user encounters by using the tool.
Refer to settings in prose form ("max output tokens", "a configurable limit").

**Not allowed (internals):** code-style identifiers (`llm.maxOutputTokens`, `Chartula:Faithfulness:Thorough`); concrete configuration values (1024, 16000); internal component or stage names ("the categorizer", "the second LLM pass"); file, class, or module references; format specifications ("uppercase, start of line, colon-terminated").

**Decision procedure**

1. Could a user who has only ever used the product know what this refers to? If no, fail.
2. If unsure: could the expression be pasted into a configuration file or source file as written? If yes, fail.
3. Describing what changed in plain language is not an internal reference. "No output length limit was set" passes. "`max_tokens` was omitted" fails.

## C2 - Symptom before cause

The entry opens with what the user could observe, not with what was changed in the code.
The cause follows, in everyday language.

**Pass:** "Generated text could be cut off mid-sentence in some runs because no output length limit was set."

**Fail:** to be written.
The example must pass C1 and C3 and fail only on the order, so that a failure on this axis is unambiguous.

## C3 - Explicit user benefit

Each entry ends with the outcome for the user, not with the technical change.
The benefit must be stated, not merely inferable.

**Pass:** "...so release notes no longer warn about breaking changes that aren't there."

**Fail:** "...the detection now only matches an actual breaking-change declaration."

## Reference case

The case the rubric was written from: the fix section of the v0.1.0 customer rendering.

**Labelled not shippable** (Haiku 4.5, `test-runs/haiku-4-5-out.md`):

> Fixed output truncation by setting max_tokens on LLM calls. Previously omitted, it defaulted to 1024 per provider, cutting off all three audience texts mid-word. Now configurable via llm.maxOutputTokens, defaulting to 16000.
>
> Fixed false breaking-change detection. The categorizer was matching BREAKING CHANGE as a case-insensitive substring anywhere in the PR body, so prose discussing breaking changes declared one. Now matches the Conventional Commits footer format: uppercase, start of line, colon-terminated.

Fails C1 (`max_tokens`, `llm.maxOutputTokens`, 1024, 16000, "the categorizer", the footer format spec), C2 (opens with the code change) and C3 (ends on the mechanism).

**Labelled shippable** (written by hand, not produced by a run):

> Generated text could be cut off mid-sentence in some runs because no output length limit was set; there's now a configurable ceiling with a higher default, so text completes properly.
> Separately, changes that merely discussed "breaking changes" in their description were sometimes incorrectly labeled as breaking themselves; the detection now only matches an actual breaking-change declaration, so release notes no longer warn about breaking changes that aren't there.

## Open

- C2 needs a fail example that isolates the axis.
- The remaining five runs in `test-runs/` are not labelled yet. Disagreements found there are the input for the next revision.
