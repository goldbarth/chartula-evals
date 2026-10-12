---
title: Release 0.1.0-preview.5
description: "This release makes the terminal output easier to read: summaries are formatted as text rather than raw Markdown, step and header lines line up, the run reports failed audiences accurately, and narrow windows no longer leave stray lines behind."
publishedAt: 2026-10-08
---

### What's New

- **Terminal summary:** Release summaries in a terminal now read as formatted text: group headings are bold without the Markdown marks, entries are bullets with a hanging indent, code is coloured without backticks, and links show their text, such as (#294). The description appears above the entries as a sentence. Entries wrap at the width of the window, and a word too long for the line, such as a URL, is kept whole. Redirected output, CI and --plain still print the Markdown source, so copy the rendering from CHANGELOG.md or from the file the run writes.
- **Spinner and header alignment:** While a step runs, its spinner now sits right beside its label, and the status marks that replace it when the step ends fill the same columns, so the label, count and time stay in place. The header values Model, GitHub and Range line up with the step labels, and their continuation lines are indented to match. Scripts that read these header keys still find them, one space further right.

### Bug Fixes

- **Failed audience reporting:** A step whose audience did not render is now marked as failed in the run output, so it no longer appears as done directly above a failed audience in the summary. The release notes are listed under Skipped with the reason when the technical rendering failed or was left out by --audience, and the summary no longer implies they were written. Without publishing, notes are listed under Skipped (--no-publish) as before, including when the technical rendering failed.
- **Argument and message fixes:** A refused --audience value now prints one error line and a pointer to chartula --help, the same as other refused arguments, and an unknown name or a number is rejected rather than silently accepted. Refused --repo values are checked before the run header is printed. chartula version now points to chartula --version. A blank line separates the list of written files from the failed-audience line, and the rate limit message without a token now states the 60-request limit and the 5000-request limit with GITHUB_TOKEN set.
- **Faithfulness number matching:** The rule-based faithfulness check now reads numbers with thousands separators as one number, so 8,000 in the facts matches 8000 in a rendering and the reverse. A finding quotes the number as the rendering wrote it, such as '9,000'. Three-digit numbers written without a space, like 100,200, are read as one number.
- **Narrow terminal output:** The line of a running step now fits the width of the terminal and is redrawn without wrapping, dropping parts such as the time or the count when the window is narrow. Below ten columns no frame is drawn and the step shows its finished line once. Resizing the window during a step takes effect from the next frame. In doctor output on a terminal, a long detail is broken between words with every row kept under its check's indent; plain output is not broken.
