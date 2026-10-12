---
title: Release 0.1.0-preview.5
description: This release improves how command-line output presents release summaries, run progress, errors, and checks.
publishedAt: 2026-10-08
---

### What's New

- **Terminal summaries:** On a live terminal, release summaries show formatted headings, bullets, labels, code, and link text instead of Markdown source. You can read the description above the entries and rely on redirected output, CI, and `--plain` to keep the existing Markdown form.
- **Run progress layout:** While a step runs, its spinner appears beside its label, and the header values line up in a column. The step labels keep their existing indent, and scripts can still find header values by their keys.

### Bug Fixes

- **Failed audience reporting:** When an audience fails to render, its step is marked as failed, and publishing runs list release notes under `Skipped` with the reason. You can rely on the step status and summary to agree, including when the technical audience is omitted.
- **Command-line errors:** Invalid `--audience` values, including empty list entries and numbers, are refused before a run header appears, and refused arguments point to `chartula --help`. You can rely on invalid audience values not being accepted as a different audience.
- **Number checks:** The rule-based check can flag an unsupported number as it appears in the rendering, including numbers written with thousands separators. You can rely on numbers such as `8,000` in the facts and `8000` in the rendering being compared as the same number.
- **Terminal-width output:** On a terminal, running-step lines fit the available width, and `doctor` details wrap between words while keeping their indent. You can rely on long words remaining uncut and on plain output keeping `doctor` details unbroken.
