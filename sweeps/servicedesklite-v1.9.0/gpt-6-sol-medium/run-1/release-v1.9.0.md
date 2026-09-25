---
title: Release 1.9.0
description: This release updates ticket workflows, assistant answers, and the web interface.
publishedAt: 2026-07-14
---

### What's New

- **Assistant citations:** Citation badges now appear beside cited passages in the assistant’s Markdown answers. Their numbers match the Sources list, and citations that cannot be placed beside a passage remain available in that list.
- **Suggested ticket actions:** A ticket’s first actionable suggestion now appears as a button or agent picker, with other suggestions in a menu. You can act on a suggestion from the ticket header, while the regular controls remain available.
- **Command palette:** You can now open a command palette from any page with Ctrl+K or Cmd+K to find pages and tickets. Arrow keys and Enter let you choose a result, and Esc closes the palette and returns focus to where it was.
- **Ticket status changes:** A status change now appears immediately on the board or ticket detail page, rather than waiting for the server response. You can count on a rejected change restoring the previous status and showing an error code.
- **Editing a ticket:** You can now change a ticket’s status or assignee from menus in its header instead of opening a dialog. The ticket stays on the same tab and at the same scroll position while the change is applied.
- **Citations in chat:** Citation badges can appear beside matching passage titles in an assistant answer. You can inspect their source details by hovering or focusing on a badge, while citations without a match remain in the Sources list.
- **Agent names in chat:** The assistant now receives the active agent roster when you ask it to assign a ticket. It is instructed to use those exact names and list valid agents if the name you gave is not on the roster.
- **Grounding checks:** An assistant answer based on retrieved knowledge-base passages now undergoes a grounding check before its first words are streamed. You can count on at least one check after retrieval, though that does not guarantee a check for every passage retrieved later in a long exchange.
- **Interface styling:** Spacing, corners, and colors now draw from shared design scales. You can count on status and priority chips using the same colors across the ticket queue, board, and detail view.

### What's Changed

- **Frontend release:** The frontend redesign is now brought together in this release, including Markdown answers, a dark-mode toggle, and ticket-page changes. You can count on the assistant displaying formatted answers rather than raw Markdown.

### Bug Fixes

- **Board card titles:** Long ticket titles on board cards could extend beyond two lines and grow the card. Titles are now limited to two lines with an ellipsis, so cards with long titles stay within a bounded height.
- **Assistant message box:** The assistant’s send button could sit against or over the edge of its panel. You can count on the button staying inside the panel and aligned with the input, including at narrow widths.
- **Ticket queue headers:** The Category header in the ticket queue could overlap Due. You can now read both headers side by side, with Category aligned to its column and styled like the neighboring headers.
- **Assistant changes:** The assistant now receives clearer instructions about when to confirm a requested change and how to report its result. It is told not to claim a change succeeded without a successful tool result, or ask again for confirmation when you have already requested the change.
- **Summary timestamps:** A ticket summary could show UTC times that differed from the local times beside it. Summary timestamps now use the user time zone, so they can be read alongside the ticket detail view.
- **Knowledge-base search errors:** A technical failure during knowledge-base search could be recorded as a successful search. Failed searches are now reported as errors, so the dashboard’s error rate distinguishes them from an unavailable search.
- **Grounding scores:** Grounding checks could mark correct paraphrases or translations as unsupported because they did not share words with their sources. Checks now compare meaning when embeddings are available, so those answers can be recognized as supported; the earlier word-based check remains the fallback.
