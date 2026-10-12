---
title: Release 0.1.0-preview.5
description: This release makes terminal output easier to read and more consistent, and corrects how failed audiences, argument errors and numbers with thousands separators are reported.
publishedAt: 2026-10-08
---

### What's New

- **Readable summary in the terminal:** The summary printed on a live terminal showed the release text as raw Markdown, with heading marks, backticks and a front matter line. It now appears as readable text: bold headings, bulleted entries wrapped to the window width, and coloured code, so you can read it on screen without decoding the source. Redirected output, CI and `--plain` keep the Markdown as before, and the Markdown to copy now comes from the changelog file, as described in the CLI docs.
- **Spinner and header alignment:** While a step ran, its spinner stood six columns away from its label, and the header values sat one column left of the step labels. The spinner now sits right before the label and the header values line up with the labels, so the line reads as one unit and nothing shifts when a step ends. A script that reads `Model:` or `Range:` by its key still finds it, one space further right.

### Bug Fixes

- When one audience failed to render, its step was still shown as done, directly above the line reporting the failure, and a publishing run said nothing about the release notes. The step is now marked as failed, and the release notes are listed under Skipped with the reason: the technical rendering failed, or `--audience` left it out. You can now trust the step marks and the summary to agree, and see why nothing was published.
- **Argument checks and run messages:** A trailing comma or a number in `--audience` was accepted and run as a valid audience, and refused arguments printed inconsistent messages. Both are now refused, and every refused argument prints its error followed by a pointer to the help, with no run header before it. The rate limit message without a token now states the 60 requests an hour limit and the token that raises it to 5000, so you no longer need to look for an earlier warning. Smaller output fixes: `chartula version` now points to `chartula --version`, a blank line separates the Wrote list from the failure count, and the `--plain` help no longer reads as if `NO_COLOR` were a third plain case.
- **Numbers with thousands separators:** The rule-based faithfulness check read `8,000` as two numbers, `8` and `000`, so a rendering that wrote `8000` was flagged even though the facts backed it, and an invented `8 retries` went unflagged. Numbers with thousands separators are now read as one number and compared without the commas, so you no longer need to dismiss such flags. Lists like `1, 2, 3` stay separate numbers, but `100,200` written without a space is now read as one number.
- **Narrow terminal windows:** In a terminal narrower than the running step line, which is 53 to 60 columns wide, every redraw left a row behind, producing over a thousand lines for a two-minute step. The line now drops whole parts (padding, then time, then count, then the end of the label) to fit one row, and no frame is drawn below ten columns. On a terminal, `doctor` also wraps long details between words and keeps their indent, so narrow windows stay readable. Plain output is never wrapped.
