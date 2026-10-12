---
title: Release 0.1.0-preview.5
description: This release makes terminal output easier to read and improves how runs report progress, failures, and number checks.
publishedAt: 2026-10-08
---

### What's New

- **Terminal summaries:** On a live terminal, release summaries show readable headings and bullets, with labels and breaking markers emphasized, code styled, and links shown as their text. This gives you a summary you can read without interpreting Markdown; redirected output, CI, and `--plain` keep the Markdown form.
- **Progress display:** While a step runs in a terminal, its spinner appears next to its label, and the header values line up in a column. The step’s label, count, and time stay in place as its status changes.

### Bug Fixes

- **Failed audience reporting:** When an audience fails to render, its step is marked as failed, and a publishing run lists the release notes under `Skipped` with the reason. You can rely on the step status and summary to agree about what happened to the release notes.
- **Command-line errors:** Invalid command-line arguments are refused before a run header appears, and each error points to `chartula --help`; `chartula version` identifies `chartula --version` as the command for the installed version. You can rely on the same guidance for every refused argument.
- **Number checks:** The rule-based check reads numbers such as `8,000` as one number when comparing facts with a rendering. You can rely on the check not to flag a number supported by the facts solely because it uses thousands separators.
- **Terminal line wrapping:** Running-step lines now fit the terminal width, and `doctor` details wrap between words while keeping their indent. You can rely on terminal output staying within the available width when it can be read; if the width cannot be read, running-step lines keep their previous form.
