---
title: Release 0.1.0-preview.5
description: This release improves how the command line reads on a terminal, with cleaner summaries, aligned progress lines and narrow-window support, and fixes failure reporting, argument checks and number handling in the faithfulness check.
publishedAt: 2026-10-08
---

### What's New

- **Summary on a terminal:** The summary printed on a live terminal now shows each audience's rendering as readable text: bold group headings, bulleted entries wrapped to the window width, and no Markdown symbols or front matter line. You can read it directly in the terminal without mentally stripping Markdown. Redirected output, CI and --plain keep the Markdown as before, so copy it from the place docs/cli.md names.
- **Spinner and header alignment:** While a step ran, the spinner stood several columns away from its step label, and the header values sat one column left of the step labels. The spinner now sits right before the label, and Model:, GitHub: and Range: line up with the step labels, so the line reads as one unit. A script that reads those header keys still finds them, one space further right.

### Bug Fixes

- **Failed audience reporting:** When one audience failed to render, its step still showed as done, directly above the line reporting the failure. That step is now marked as failed, and a publishing run lists the release notes under Skipped with the reason, whether the technical rendering failed or --audience left it out. The step lines and the summary now agree, and you can see why no release notes were published.
- **Argument checks and run messages:** Mistakes in arguments were accepted or reported inconsistently: --audience with a trailing comma or a number such as 1 ran as a valid audience, and refused arguments printed different output. These are now refused, and every refused argument prints its error followed by a pointer to chartula --help. A blank line separates the Wrote: list from the failure count, and the rate limit message now explains the 60 versus 5000 requests an hour limit by itself, so you no longer have to look for an earlier warning.
- **Numbers with thousands separators:** The rule-based faithfulness check read a number such as 8,000 as two numbers, so a rendering that wrote 8000 was wrongly flagged while an invented 8 could pass. Numbers with thousands separators are now read as one number and compared without the commas, so flags on such numbers reflect real mismatches. Three-digit numbers listed with no space, like 100,200, are now read as one number.
- **Narrow terminal windows:** In a narrow terminal window, the line of a running step wrapped and left a new row behind with every frame, producing over a thousand lines in a two-minute step. The line now drops whole parts such as padding, time or count to fit in one row, and no frame is drawn below ten columns, so a narrow window stays readable. On a terminal, doctor also breaks long details between words and keeps their indent.
