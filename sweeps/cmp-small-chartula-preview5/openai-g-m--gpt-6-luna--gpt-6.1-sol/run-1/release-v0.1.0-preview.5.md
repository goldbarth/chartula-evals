---
title: Release 0.1.0-preview.5
description: This release improves terminal output and reporting, and makes the rule-based check read thousands-separated numbers as single values.
publishedAt: 2026-10-08
---

### What's New

- **Terminal summaries:** Release summaries in a live terminal display headings and entries as formatted text, with labels, code, and links shown in readable form. You can rely on redirected output, CI, and `--plain` to keep the Markdown source unchanged.
- **Progress display:** A running step's spinner now sits beside its label, and the header values line up in a column. You can rely on the step label, count, and time staying in place when the step ends.

### Bug Fixes

- **Failed audience reporting:** When an audience fails to render, its step is marked as failed and the run continues with the next audience. You can rely on publishing summaries to list release notes as skipped when the technical rendering fails or the technical audience is excluded.
- **Argument errors:** Invalid argument values are rejected before the run header appears, and each refusal points to `chartula --help`; `chartula version` identifies `chartula --version` as the command for the installed version. You can rely on a run header appearing only when a run has started.
- **Thousands-separated numbers:** The rule-based check now reads numbers such as `8,000` as a single number when checking a rendering against the facts. You can rely on supported numbers with thousands separators no longer being treated as separate values.
- **Terminal-width output:** Running-step lines now fit the terminal width, and `doctor` details wrap while keeping their indent. On terminals narrower than ten columns, running steps show only their finished line; when the width cannot be read, the running line keeps its previous form.
