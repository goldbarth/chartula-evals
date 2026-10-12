---
title: Release 0.1.0-preview.5
description: This release makes command-line output easier to read and clarifies validation and reporting of release results.
publishedAt: 2026-10-08
---

### What's New

- **Terminal summaries:** You can now read summaries in a live terminal as formatted text, with headings, bullets and a description above the entries rather than Markdown source. Redirected output, CI and `--plain` retain the original Markdown for copying or reading by a program.
- **Progress layout:** In a live terminal, the spinner now sits beside its step label, and header values align with step labels. Labels, counts and times stay in place when a step finishes or fails.

### Bug Fixes

- **Failed audience reporting:** An audience that failed to render could appear as a completed step, and missing technical output could leave release notes unaccounted for. You can now count on the step status to reflect the rendering failure and the summary to explain why release notes were skipped, including when the technical audience was excluded.
- **Command-line feedback:** Mistyped audience lists or numeric audience values could select an audience instead of being rejected, and argument errors gave inconsistent guidance. Invalid arguments now report an error and point to `chartula --help` before a run starts; version-command guidance, partial-failure spacing, colour help and GitHub rate-limit messages also make their meaning explicit.
- **Number checks:** Numbers written with thousands separators could trigger unsupported-number flags when rendered without commas, while fragments of those numbers could pass the check. You can now count on the check to compare those forms as one number, though comma-separated three-digit numbers without spaces, such as `100,200`, are also treated as one number.
- **Narrow terminal output:** Running steps could leave repeated rows in narrow terminals, and wrapped `doctor` details could lose their indentation. When the terminal width can be read, progress lines now fit as the window resizes; `doctor` details retain their indentation when wrapped between words, except when fewer than 20 columns are available.
