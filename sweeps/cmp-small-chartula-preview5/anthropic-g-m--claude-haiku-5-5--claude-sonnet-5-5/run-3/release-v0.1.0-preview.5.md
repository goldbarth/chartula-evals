---
title: Release 0.1.0-preview.5
description: "This release makes the terminal output easier to read: summaries show text instead of Markdown source, step lines fit the window and line up with the header, and refused arguments and failed audiences are reported more clearly."
publishedAt: 2026-10-08
---

### What's New

- **Readable terminal summary:** Terminal output shows a rendering as readable text instead of Markdown source. Headings no longer carry their hash marks, entries are bullets with a hanging indent, and links show their text with the pull request number, so you no longer have to strip Markdown syntax before reading or copying it. Plain output, output redirected to a file, CI runs and --plain keep the Markdown and the description line as before, and docs/cli.md says where to copy the Markdown from.
- **Spinner and header alignment:** While a step runs, its spinner now sits next to its label instead of several columns to the left. The header values Model, GitHub and Range start on the same column as the step labels, and their continuation lines are indented to match.

### Bug Fixes

- **Failed audience and release notes:** A step whose audience did not render now shows as failed in the run output, so it no longer appears as done directly above a failed audience. A publishing run lists the release notes as skipped with the reason, instead of omitting them when the technical rendering failed or was left out with --audience.
- **Refused arguments and run messages:** A mistyped --audience value is refused, including an empty place in a list and a number. Every refused argument now prints the same two lines, and chartula version points to chartula --version. The output has a blank line before the failed-audience count, and the rate limit message no longer refers to a warning that doctor does not print.
- **Numbers with thousands separators:** The rule-based faithfulness check reads numbers with thousands separators as one number, so 8,000 in the facts matches 8000 in a rendering and the reverse. Numbers without separators, lists of numbers and version strings are compared as before.
- **Progress line fits the terminal:** The progress line of a running step fits the width of the terminal and is redrawn to fit when the window is resized, so it no longer wraps and leaves rows behind. On a narrow window the line drops its least important parts first. doctor breaks long details between words on a terminal and keeps their indent; plain output is not broken.
