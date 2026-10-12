---
title: Release 0.1.0-preview.5
description: This release makes the terminal output easier to read, with formatted summaries, aligned progress and header values, and clearer handling of failures and refused arguments.
publishedAt: 2026-10-08
---

### What's New

- **Readable summary in the terminal:** Release summaries in a terminal now read as formatted text rather than raw Markdown: headings appear without their markers, entries are bulleted with a hanging indent, and the breaking-change marker and code are styled. Links show their text, such as the pull request number, and the URL is in the changelog file. Output redirected to a file, run in CI, or using --plain still prints the Markdown source as before, so copy the text from CHANGELOG.md when you need the original.
- **Spinner and header alignment:** While a step runs, its spinner now sits next to the step's label instead of several columns to the left, and the header values line up with the step labels. Scripts that read the header by its key still find it, one space further right.

### Bug Fixes

- **Failed audience in progress and summary:** A step whose audience failed to render is now marked as failed, and the run continues to the next audience. The release notes section of the summary lists them as skipped with the reason: the technical rendering failed, or --audience left it out.
- **Refused arguments:** A misspelled or malformed --audience value, such as a trailing comma or a number, is now refused with a clear message instead of running as a different audience. Every refused argument prints its error followed by a pointer to chartula --help, and chartula version now points to chartula --version.
- **Numbers with separators in the faithfulness check:** The rule-based faithfulness check now reads numbers with thousands separators as one number, so 8,000 in the facts matches 8000 in a rendering and is no longer flagged. Findings quote the number as the rendering wrote it.
- **Progress line fits the terminal:** The running step line now fits the width of the terminal, so narrow windows no longer leave a trail of wrapped lines during a step. The line is redrawn at the current width on each frame, and doctor's details are broken between words under their check on a terminal.
