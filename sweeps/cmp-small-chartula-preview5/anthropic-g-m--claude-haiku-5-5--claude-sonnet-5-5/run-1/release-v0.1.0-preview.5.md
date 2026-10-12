---
title: Release 0.1.0-preview.5
description: "This release makes the terminal output easier to read: renderings display as text, step lines fit narrow windows, and a few misleading statuses and argument checks are corrected."
publishedAt: 2026-10-08
---

### What's New

- **Readable rendering on a terminal:** Terminal output now shows each audience's rendering as readable text: headings without their Markdown markers, bold labels, code without backticks, links shown as their text such as (#294), and the description as a plain sentence above the entries. Output redirected to a file or run in CI keeps the Markdown source, so a copied rendering reads the same as before.
- **Spinner and header alignment:** The spinner that marks a running step now sits directly before its label instead of six columns away, and the header values line up with the step labels. Finished steps keep their label, count and time in place.

### Bug Fixes

- **Failed audience step and skipped notes:** An audience whose rendering failed is now marked as failed in the step list instead of done, and the release notes are listed as skipped with the reason when no technical rendering exists to publish.
- **Refused arguments:** A misspelled or malformed --audience value is now refused rather than silently accepted, and every refused argument prints the same error and help pointer. chartula version reports an unknown command and points to chartula --version.
- **Numbers with separators in the check:** A number with thousands separators, such as 8,000, is now matched against the source facts as one number, so a rendering that writes 8000 is no longer flagged as unsupported.
- **Narrow terminal output:** The line of a running step now fits the terminal's width, so it no longer wraps and piles up rows in a narrow window. The doctor details also break between words and keep their indent on a terminal.
