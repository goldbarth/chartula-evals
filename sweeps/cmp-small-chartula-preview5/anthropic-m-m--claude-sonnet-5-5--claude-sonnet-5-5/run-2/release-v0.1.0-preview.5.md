---
title: Release 0.1.0-preview.5
description: This release makes the command-line tool's terminal output easier to read and more consistent, and corrects how failed audiences, refused arguments and number checks are reported.
publishedAt: 2026-10-08
---

### What's New

- **Readable summary in the terminal:** On a terminal, the summary printed by the command-line tool now shows each audience's rendering as readable text: bold headings, bulleted entries, and links shown as their text, with no Markdown source or description line. You can read the summary directly, with entries wrapped to the window width; redirected output, CI and --plain still print the Markdown as before, so copy it from the file the docs name.
- **Spinner and header alignment:** While a step runs, its spinner now sits right next to the step's label, and the header values (Model, GitHub, Range) line up with the step labels. Nothing shifts when a step ends, and a script that reads Model: or Range: by its key still finds it, one space further right.

### Bug Fixes

- **Failed audience in a run:** A step for an audience that failed to render was shown as done, directly above the line reporting the failure. The step is now marked as failed, and a publishing run lists the release notes under Skipped with the reason, so the steps and the summary agree and you can see that nothing was published.
- **Refused arguments:** A slip in --audience, such as a trailing comma or a number, ran as a different audience instead of being refused. These are now refused, and every refused argument prints the same error followed by a pointer to chartula --help, so a wrong value no longer starts a run you did not ask for.
- **Numbers with thousands separators:** The rule-based faithfulness check read a number written with thousands separators, such as 8,000, as two numbers. It now reads it as one, so a rendering that writes 8000 is no longer flagged when the facts say 8,000, and an invented "8 retries" is no longer missed. Numbers written as 100,200 without a space are now read as one number.
- **Narrow terminal windows:** In a narrow terminal window, the line of a running step wrapped and left a new row behind on every redraw. The line now drops whole parts until it fits one row, so you can run in a narrow pane without the screen filling with lines. On a terminal, doctor also breaks long details between words and keeps their indent.
