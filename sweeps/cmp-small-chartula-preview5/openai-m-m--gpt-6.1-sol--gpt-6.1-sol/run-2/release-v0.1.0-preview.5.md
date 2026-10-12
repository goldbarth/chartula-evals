---
title: Release 0.1.0-preview.5
description: This release improves how Chartula presents release summaries, progress and command feedback in the terminal, and how it checks numbers in generated notes.
publishedAt: 2026-10-08
---

### What's New

- **Terminal summaries:** You can now read summaries in a live terminal as formatted text rather than Markdown source, with headings, bullets and the release description above the entries. Redirected output, CI and `--plain` retain the original Markdown form for copying or reading by a program.
- **Progress layout:** The spinner now sits next to its step label, and header values align with the step labels. When a step finishes, its label, count and time stay in the same columns.

### Bug Fixes

- **Failed audience reporting:** An audience that failed to render could be marked done, and release notes could be missing from the skipped-output list when the technical audience failed or was excluded. You can now count on the step status to reflect whether that audience rendered and on the summary to explain why release notes were skipped, while rendering continues for the next audience.
- **Command-line feedback:** An empty place or a number in `--audience` could select an audience instead of being rejected, and invalid arguments produced inconsistent guidance. Invalid arguments now report an error and a help pointer before a run starts; version guidance, output spacing, colour help and GitHub rate-limit messages also make the command's results and limits explicit.
- **Number checks:** The rule-based check could flag `8000` when the facts said `8,000`, yet accept an unsupported `8` from those same facts. You can now count on numbers with thousands separators being checked as whole numbers, though a list such as `100,200` without a space is treated as one number.
- **Narrow terminal output:** Running steps could wrap in narrow terminals and leave rows behind, while wrapped `doctor` details lost their indent. When the terminal width can be read, progress lines now fit the available row and adapt to resizing; `doctor` details retain their indent when there is at least 20 columns of room, except that long words remain uncut.
