---
title: Release 0.1.0-preview.5
description: This release focuses on readable terminal output and clearer feedback about release generation and checks.
publishedAt: 2026-10-08
---

### What's New

- **Terminal summaries:** You can now read release summaries in a live terminal as formatted text, with headings, bullets and a description above the entries rather than Markdown source. Redirected output, CI and `--plain` retain the original Markdown for copying or reading with a program.
- **Progress layout:** The spinner now sits next to its step label in terminal output, and header values align with the step labels. When a step finishes, its label, count and time stay in the same columns.

### Bug Fixes

- **Failed audience reporting:** An audience that failed to render could show a completed step, and missing technical output could leave release notes unaccounted for. You can now distinguish failed rendering steps from completed ones and see why release notes were skipped when the technical rendering failed or was excluded.
- **Command feedback:** Invalid `--audience` values could select an unintended audience, and rejected arguments gave inconsistent guidance. Invalid values are now rejected before a run header appears, with an error and a pointer to `chartula --help`; version guidance, failure summaries, colour help and GitHub rate-limit messages also explain their cases directly.
- **Number checks:** The rule-based check could flag `8000` when the facts said `8,000`, yet accept an unsupported “8 retries.” It now compares numbers with and without thousands separators together, while treating comma-separated three-digit numbers without spaces, such as `100,200`, as one number.
- **Narrow terminal output:** Running steps could wrap in narrow terminals and leave rows behind, while wrapped `doctor` details lost their indentation. When terminal width is available, progress lines fit as the window changes, and `doctor` details retain their indentation when there is enough room to wrap them.
