---
title: Release 1.9.0
description: This release brings together the M9 frontend redesign and updates to assistant answers, ticket workflows, and knowledge-base checks.
publishedAt: 2026-07-14
---

### What's New

- **Markdown citation badges:** Citations appear as numbered badges beside matching passage titles in the assistant’s Markdown answer. The numbered Sources list stays consistent, and citations without a matching title remain in the list.
- **Suggested ticket actions:** The first actionable suggested step appears as a button or agent picker on tickets with an actionable suggestion. You can run the suggested action directly, while other suggestions remain available in the overflow menu.
- **Command palette:** Press Ctrl+K or Cmd+K on any page to open a keyboard-operated palette for navigation and ticket search. You can move through results with the arrow keys, open one with Enter, and close the palette with Esc.
- **Ticket status updates:** A status change appears immediately on the board and ticket detail page while the server processes it. You can rely on accepted changes being reconciled with the server, and rejected changes restore the previous status and show an explanation.
- **Inline ticket controls:** Status and assignee choices now open in menus on the ticket header. You can make either change while staying on the ticket, with your current tab and scroll position preserved.
- **Assistant citation previews:** Citations appear beside matching titles in the assistant’s answer, with a preview available on hover or keyboard focus. Sources remain available in the numbered list when a citation is not anchored in the answer.
- **Assistant agent roster:** The assistant can refer to the active agent roster when you ask it to assign a ticket. It uses listed names rather than guessing, and can show the valid agents if your requested name is not on the roster.
- **Grounding checks:** After knowledge-base passages are retrieved, the assistant and autonomous worker are required to run a grounding check before streaming an answer. You can rely on the check being run at least once after retrieval, though it does not check every passage retrieved later in a run.
- **Consistent design tokens:** Status and priority chips use the same color definitions across the queue, board, and ticket detail pages. You can rely on those chips presenting consistent colors in each view.

### What's Changed

- **Frontend redesign release:** This release brings the M9 frontend redesign together with updates to assistant citations, ticket actions, and navigation.

### Bug Fixes

- **Board title clipping:** Long board-card titles are clamped to two lines with an ellipsis. Cards in a lane stay bounded in height when titles are long.
- **Assistant message composer:** The send button now sits inside the assistant composer panel, with the input and button aligned at narrow widths. You can use the composer without the button extending beyond the panel.
- **Ticket category header:** The Category header no longer overlaps the Due column and now matches neighboring headers in uppercase. You can read the headers and their aligned columns without overlap.
- **Assistant confirmation policy:** The assistant no longer asks you to confirm a change you already requested, including after it corrects an earlier mistake. You can rely on it to report a change only after a tool call succeeds, while it can still ask when a genuine decision is needed.
- **Ticket summary timestamps:** Timestamps in ticket summaries are shown in the configured user timezone. You can rely on summary times matching that timezone rather than showing UTC times.
- **Knowledge-base search errors:** A failed knowledge-base search is now reported as an error, distinct from a search that is unavailable. You can distinguish a technical failure from the unavailable-search path.
- **Meaning-based grounding checks:** Grounding checks now compare answer sentences with retrieved passages by meaning, including paraphrases and translations, when semantic evaluation is available. If semantic evaluation is unavailable or embedding fails, the existing lexical check provides the fallback.
