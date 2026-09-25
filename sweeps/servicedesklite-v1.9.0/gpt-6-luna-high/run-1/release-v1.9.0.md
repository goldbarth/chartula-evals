---
title: Release 1.9.0
description: This release brings the M9 frontend redesign together with updates to ticket workflows and assistant responses.
publishedAt: 2026-07-14
---

### What's New

- **Citation badges:** Numbered badges appear beside cited passage titles in assistant answers, matching the numbers in the Sources list. You can inspect a badge’s source, heading, and snippet on hover or keyboard focus; citations without a matching title remain in the list.
- **Suggested ticket actions:** The ticket header shows the first suggested action as its primary control, with remaining suggestions in an overflow menu; suggestions that cannot be mapped to an action are not clickable. You can run supported suggestions from the header, and tickets without suggestions keep their existing generic controls.
- **Command palette:** Pressing Ctrl+K or Command+K opens a command palette on any page, with navigation destinations and ticket search results. You can search and navigate using the keyboard, and closing the palette returns focus to where it was before opening.
- **Status updates:** On the board and ticket detail page, a status change appears before the server response arrives. The display is then reconciled with the accepted status; if the change is rejected, the previous status is restored and an error message appears.
- **Inline ticket edits:** Status and assignee choices now open in menus on the ticket header instead of dialogs. You can apply either change without leaving the ticket, and your scroll position and open tab stay in place.
- **Citation previews:** Citation badges in assistant answers show a preview of the source, heading, and snippet on hover or keyboard focus. Citations without an inline match remain available in the numbered Sources list.
- **Agent roster:** When you ask the assistant to assign a ticket, it can tell you which agents are available. If the requested name is not listed, it gives you the valid names instead of guessing.
- **Grounding checks:** When the assistant retrieves knowledge-base passages, it runs a grounding check before sending its first answer token, at least once in that run. The verdict is not shown, and this does not ensure that every passage retrieved later in a long chain is checked.
- **Interface design consistency:** Status and priority chips use consistent colors across the ticket queue, board, and detail pages. Their appearance no longer varies between those views.

### What's Changed

- **Release integration:** The complete M9 frontend redesign is included in v1.9.0.

### Bug Fixes

- **Board card titles:** Long board-card titles now wrap to two lines and end with an ellipsis. Card height stays bounded instead of growing with the title.
- **Assistant composer:** The assistant’s send button now sits inside its composer panel. The input and button remain aligned at narrow widths.
- **Ticket queue columns:** In the ticket queue, Category and Due appear as separate uppercase headers, with Category aligned to its column. Category remains a label rather than a sort control.
- **Assistant change confirmations:** When you request a clear change that needs no further decision, the assistant proceeds without asking you to confirm again, including after correcting a mistake. It reports the change as complete only after a tool call succeeds, so you can rely on its account of the result.
- **Summary timestamps:** Ticket summaries show created, due, comment, and event times in the same time zone as ticket details. You can compare those times without converting them from UTC.
- **Knowledge-base search errors:** A technical knowledge-base search failure could appear as a successful invocation in the dashboard. The dashboard now counts it as an error, while an unavailable knowledge base remains a separate outcome.
- **Grounding by meaning:** Answers that paraphrase or translate retrieved passages can now pass the grounding check even when their wording differs. If semantic scoring is unavailable or an embedding fails, the existing word-based check remains the fallback.
