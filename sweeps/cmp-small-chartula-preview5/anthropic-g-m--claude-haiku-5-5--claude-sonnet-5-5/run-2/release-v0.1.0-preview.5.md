---
title: Release 0.1.0-preview.5
description: "This release makes the terminal summary and progress output read cleanly: rendered notes appear as formatted text, the spinner and header align, and narrow windows no longer break the progress display."
publishedAt: 2026-10-08
---

### What's New

- **Terminal summary:** Output shown in a live terminal now reads as formatted text rather than raw Markdown: headings lose their hash marks, bullets are indented, code appears coloured without backticks, and links show only their text, such as (#294). The description appears above the entries as a sentence, and long lines wrap at word boundaries to fit the window width. Redirected output, CI and --plain still print the Markdown and the description line unchanged, so copy the Markdown from CHANGELOG.md, as docs/cli.md explains.
- **Spinner and header alignment:** The spinner now sits next to its step label instead of six columns to the left. The status column stays put when a step ends, so the label, count and time do not move. The header values Model, GitHub and Range line up on the same column as the step labels. Plain output keeps the same lines, one space further right in the header.

### Bug Fixes

- **Failed audience step:** An audience that fails to render is now marked as failed in the step list instead of done, so the list agrees with the summary. A publishing run that does not produce a technical rendering lists the release notes under Skipped with the reason, instead of omitting them.
- **Argument errors:** A slip in --audience, such as a trailing comma or a bare number, is refused with a message naming the three valid audiences. Every refused argument now prints the same two lines, the error and a pointer to chartula --help, and a blank line separates the Wrote list from the failure count. The rate limit message without a token now states the 60-request hourly limit and the GITHUB_TOKEN raise to 5000 directly.
- **Number matching:** The rule-based faithfulness check now reads numbers with thousands separators as single numbers, so 8,000 in the facts matches 8000 in the rendering and the reverse. Numbers written without separators are unaffected.
- **Narrow terminal progress:** A running step's progress line now fits the terminal width and no longer wraps, which previously left a new row on every redraw in narrow windows. Doctor's detail lines wrap at word boundaries in a terminal and keep their indent; plain output is not wrapped.
