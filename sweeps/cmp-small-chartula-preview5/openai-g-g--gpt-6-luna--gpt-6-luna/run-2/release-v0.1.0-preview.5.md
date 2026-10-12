---
title: Release 0.1.0-preview.5
description: Terminal output and progress reporting are easier to read, while release summaries and command-line checks report failures and invalid input more clearly.
publishedAt: 2026-10-08
---

### What's New

- **Terminal summaries:** On a live terminal, release summaries show headings, labels, code and links in a readable layout instead of Markdown source. This applies only to live terminal output, so redirected output, CI and `--plain` keep their existing Markdown form; the link text identifies the pull request, and its URL remains in `CHANGELOG.md`.
- **Progress display:** While a step runs, its spinner appears immediately before its label, and header values line up in a column. This applies to the terminal progress display; the finished status, label, count and time keep their positions, so you can follow each step without the spinner sitting apart from its label.

### Bug Fixes

- **Failed audience reporting:** When an audience fails to render, its step is marked as failed, and a publishing run lists the release notes under `Skipped` with the reason. This applies when an audience fails or is omitted, so the progress display and summary agree about what rendered and what happened to the notes.
- **Command-line errors:** Refused command-line arguments now show an error followed by a pointer to `chartula --help`, and an invalid `--repo` value is rejected before the run header appears. You can rely on the header appearing only for a run that started; use `chartula --version` to see the installed version.
- **Number checks:** The rule-based check now reads numbers such as `8,000` as a single number when comparing facts with a rendering. You can rely on thousands-separated numbers being compared without their commas, while versions such as `10.0.1` keep their existing comparison.
- **Terminal line wrapping:** Running-step lines now fit within the terminal width, and `doctor` details wrap between words while keeping their indent. On terminals narrower than ten columns, no running-step frame is drawn; when the terminal width cannot be read, the running-step line keeps its previous form, and plain `doctor` output remains unwrapped.
