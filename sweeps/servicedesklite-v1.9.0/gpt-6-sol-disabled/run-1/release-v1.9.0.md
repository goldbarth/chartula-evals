---
title: Release 1.9.0
description: This release brings together changes to ticket workflows, assistant answers, and the web interface.
publishedAt: 2026-07-14
---

### What's New

- **Citations in Markdown answers:** Citation badges now appear beside matching passage titles in the assistant’s Markdown answers, with source details on hover or keyboard focus. Their numbers match the Sources list, where citations without a matching title remain available.
- **Suggested ticket actions:** The first actionable suggestion on a ticket is now a button or agent picker, with other suggestions in a menu. You can act on a suggestion directly, while the usual ticket controls remain available.
- **Command palette:** Press Ctrl+K or Cmd+K from any page to open a palette for navigation and ticket search. You can use the arrow keys and Enter to open a result, or Esc to close the palette and return to your previous focus.
- **Ticket status updates:** A status change on the board or ticket details now appears before the server responds. You can count on a rejected change restoring the previous status and showing an error, while an accepted board move is reconciled with the server.
- **Ticket status and assignee:** Status and assignee changes now open menus in the ticket header instead of dialogs. You can make either change without leaving the ticket or losing your scroll position or open tab.
- **Inline citations:** Citations now appear as numbered badges beside matching titles in assistant answers, with source details available on hover or keyboard focus. Citations without a matching title remain in the Sources list, so you can still find them.
- **Agent names in assistant chat:** The assistant now receives the active agent roster in each chat request. It is instructed to use those names for assignments and list valid names rather than guess when a requested name is absent.
- **Grounding checks:** When the assistant retrieves knowledge-base passages, it now requires a grounding check before streaming its answer. You can count on at least one check after retrieval, though this does not guarantee that every passage retrieved later in a long exchange is checked.
- **Consistent interface styling:** Status and priority chips that differed across the queue, board, and ticket details now use the same colors. You can count on those indicators having a consistent appearance across the three views.

### What's Changed

- **Frontend redesign release:** The frontend redesign changes are now brought together for v1.9.0. You can use the combined release with Markdown assistant answers and a Sources list below them.

### Bug Fixes

- **Board card titles:** Long ticket titles on board cards could grow beyond two lines and stretch the card. Titles now stop at two lines with an ellipsis, so you can count on cards staying bounded.
- **Assistant send button:** The assistant’s send button could sit against the panel edge. It now sits inside the panel, so you can count on the input and button staying aligned at narrow widths.
- **Ticket queue headings:** The Category heading in the ticket queue could overlap Due. The headings now sit side by side in both themes, with their columns aligned to the ticket rows.
- **Assistant change confirmations:** The assistant now receives instructions not to claim a ticket change succeeded without a successful result, or ask again for confirmation when you have already requested the change. You can count on it being instructed to reserve pre-change questions for ambiguous matches, missing information, uncertain routing suggestions, or hard-to-reverse actions where your intent is unclear.
- **Ticket summary times:** Times in streamed ticket summaries could differ from the local times shown on the ticket. Summaries now use the user timezone, so you can count on their timestamps matching the ticket detail view.
- **Knowledge-base search failures:** A failed knowledge-base search could appear as a successful search. Technical failures are now reported as errors, so you can distinguish them from a search that is unavailable.
- **Grounding by meaning:** Grounding checks could mark correct paraphrases and translations as unsupported when their words differed from the source. When semantic scoring is available, the check now compares meaning, so you can count on those answers being assessed against the retrieved passages; if it is unavailable or fails, the check falls back to word overlap.
