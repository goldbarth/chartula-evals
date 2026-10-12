---
title: Release 0.1.0-preview.5
description: This release improves terminal output and run reporting, and corrects number handling in the rule-based check.
publishedAt: 2026-10-08
---

### What's New

- **Terminal summaries:** Release summaries on a live terminal display headings, labels, code, and links as readable text instead of Markdown source. You can rely on the summary fitting the window without cutting long words; use `CHANGELOG.md` to copy Markdown, or use `--plain` for Markdown output.
- **Run progress layout:** While a step runs in a terminal, its spinner appears beside its label, and the header values line up in a column. You can rely on the step’s label, count, and time staying in place when it finishes.

### Bug Fixes

- **Failed audience status:** When an audience fails to render, its step is now marked as failed while later audiences can still render. You can rely on the summary to list release notes under `Skipped` when publishing is enabled and technical rendering failed or the technical audience was left out.
- **Command-line errors:** Invalid command-line arguments now show an error and a help hint before a run header is printed. You can rely on `--audience` accepting only the three audience names, and on the GitHub rate-limit message stating the request limits with and without a token.
- **Number checks:** The rule-based check no longer splits numbers such as `8,000` into separate numbers. You can rely on thousands-separated numbers being compared as a whole, while lists and version numbers keep their existing interpretation.
- **Terminal line fitting:** Running-step lines now fit within the terminal width, and long `doctor` details wrap while retaining their indent. You can rely on the line width being read again for each frame, so resizing the window changes the next frame; plain output remains unwrapped.
