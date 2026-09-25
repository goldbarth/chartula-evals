---
title: Release 1.9.0
description: This release brings together frontend changes and updates how the assistant handles citations, grounding, and ticket-related requests.
publishedAt: 2026-07-14
---

### What's New

- **Citations in Markdown answers:** Citation badges appear beside cited passage titles in assistant Markdown answers, with source details on hover or focus. Their numbers match the Sources list, where citations without a matching title remain available.
- **Suggested ticket actions:** The first actionable suggestion appears as a control in the ticket header, with other suggestions in a menu. You can act on the recommendation while the usual ticket controls remain available.
- **Command palette:** Press Ctrl/Cmd+K on any page to open a palette for finding tickets or navigating the app. You can use the arrow keys and Enter to open a result, or Esc to close the palette and return focus to where it was.
- **Ticket status updates:** A status change on the board or ticket detail page now appears before the server responds. You can rely on a rejected change restoring the previous status and showing an error, while the board reconciles accepted changes with the server.
- **Ticket status and assignee:** Changing a ticket’s status or assignee now happens from menus in the ticket header rather than dialogs. Your ticket stays open on the same tab and at the same scroll position while you make the change.
- **Assistant citation badges:** Citation badges appear beside cited titles in assistant answers, with source details on hover or keyboard focus. Citations without a matching title remain in the numbered Sources list, so you can still find them.
- **Agent names in chat:** The assistant now receives the active agent roster when you ask it to assign a ticket. It is instructed to use those names and list valid agents rather than guess when a name is not on the roster.
- **Grounding checks:** Assistant answers based on retrieved knowledge-base passages now receive at least one grounding check before the answer starts streaming. You can count on that check after retrieval, though it does not guarantee that every passage retrieved later in a long exchange is checked.
- **Consistent interface styling:** Status and priority chips now use the same colors across the ticket queue, board, and detail pages. You can count on those indicators looking consistent between those views.

### What's Changed

- **Frontend redesign release:** The frontend redesign changes are brought together for v1.9.0. The release includes the combined interface changes in one version.

### Bug Fixes

- **Board card titles:** Long ticket titles on board cards could extend beyond two lines and make cards grow. Titles now display at most two lines with an ellipsis, so cards keep a bounded height.
- **Assistant send button:** The assistant’s send button sat against the edge of its panel. It now sits inside the panel, so the input and button stay aligned even at narrow widths.
- **Ticket queue headers:** The Category header in the ticket queue overlapped Due. The headers now sit side by side, so they remain readable and aligned with their columns.
- **Assistant change confirmations:** The assistant is now instructed not to claim a requested change succeeded without a successful result, or ask you to confirm a change you already requested. You can expect it to reserve questions before a change for ambiguous or missing information, genuine doubt about a hard-to-reverse action, or an uncertain routing suggestion.
- **Ticket summary times:** Times in streamed ticket summaries could differ from the local times shown in ticket details. Summary timestamps now use the user timezone, so the two views show times in the same zone.
- **Knowledge-base search failures:** A failed knowledge-base search could be reported as a successful tool result. Technical failures are now reported as errors, so the dashboard’s tool error rate reflects them while an unavailable search remains distinct.
- **Grounding scores:** Correct paraphrases and translations could be marked ungrounded when the assistant checked an answer against knowledge-base passages. The check now compares meaning when embeddings are available, so those answers can be recognized as supported; it falls back to word overlap without embeddings or when embedding fails.
