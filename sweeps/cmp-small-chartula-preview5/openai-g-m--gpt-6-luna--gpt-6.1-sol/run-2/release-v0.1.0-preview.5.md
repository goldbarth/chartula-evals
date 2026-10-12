---
title: Release 0.1.0-preview.5
description: This release improves the clarity of terminal output and the information shown during release runs.
publishedAt: 2026-10-08
---

### What's New

- **Terminal rendering:** On a live terminal, release summaries now show formatted headings, bullets, labels, code and links instead of Markdown source. This applies only to live terminal output, so copied, redirected and plain output remains unchanged; copy the Markdown from `CHANGELOG.md`.
- **Progress display:** While a step runs in a terminal, its spinner now appears beside its label, and header values line up with their labels. The step positions stay fixed when a step finishes, so you can read progress without the status changing the layout.

### Bug Fixes

- **Failed audience status:** A rendering step now shows as failed when its audience does not render, even if the run continues with another audience. The summary also lists release notes under `Skipped` when publishing is enabled and the technical rendering failed or was left out, so you can see why the notes were not published.
- **Command-line errors:** Invalid command-line arguments now receive the same help pointer, and a run header appears only after argument checks pass. You can rely on refused values being reported before a run starts, with guidance to `chartula --help`.
- **Numbers in checks:** The rule-based check now reads numbers with thousands separators as a single number, so values such as `8,000` are compared as one value. You can rely on matching facts not being split at those separators; lists such as `1, 2, 3` remain separate numbers.
- **Terminal line wrapping:** Running-step lines now fit within the terminal width, and long details in `doctor` wrap between words while keeping their indent. This applies to terminal output; plain `doctor` output remains unbroken, so pasted reports keep their existing form.
