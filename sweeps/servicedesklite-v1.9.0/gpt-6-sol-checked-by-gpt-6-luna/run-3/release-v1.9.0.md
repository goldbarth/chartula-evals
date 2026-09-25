---
title: Release 1.9.0
description: This release brings together ticket and assistant interface changes with updates to assistant grounding and ticket summaries.
publishedAt: 2026-07-14
---

### What's New

- **Citations in assistant answers:** Citation badges now appear beside cited passage titles in the assistant’s Markdown answers, with source details on hover or keyboard focus. Their numbers match the sources list, where citations without a matching title in the answer remain available.
- **Suggested ticket actions:** The first actionable suggestion on a ticket now appears as a button or agent picker, with other suggestions in a menu. You can act on a suggestion directly, while the usual ticket controls remain available.
- **Command palette:** Press Ctrl+K or Cmd+K on any page to open a palette for navigation and ticket search. You can select a result with the arrow keys and Enter, or press Esc to close it and return focus to where you were.
- **Ticket status changes:** A ticket’s status now changes on screen immediately when you move its board card or change it on the ticket page. If the server rejects the change, the previous status returns and a notification shows the error code.
- **Editing ticket status and assignee:** Changing a ticket’s status or assignee now happens in a menu on the ticket page instead of a dialog. The ticket stays open at the same scroll position and on the same tab while you make the change.
- **Citations in assistant chat:** Citation badges now appear beside matching passage titles in assistant answers, and hovering over or focusing a badge shows its source details. Citations that cannot be placed in the answer remain in a numbered sources list.
- **Agent names in assistant chat:** The assistant now has the current agent roster when you ask it to assign a ticket. It is instructed to use only names on that roster and to list valid names if the one you give is not there.
- **Grounding checks:** Answers based on retrieved knowledge-base passages now receive a grounding check before the assistant begins streaming its reply. You can count on at least one check after retrieval, though it does not guarantee a separate check for every passage retrieved later.
- **Consistent interface styling:** Spacing, corners, colours and status chips now use shared styles across the interface. You can count on the same status and priority chip styling in the queue, board and ticket details.

### What's Changed

- **Frontend redesign release:** The frontend redesign is included together in v1.9.0, with Markdown answers and a sources list in the assistant. You can count on those changes being part of the same release.

### Bug Fixes

- **Board card titles:** Long ticket titles could stretch board cards beyond their intended height. Titles now stop at two lines with an ellipsis, so cards stay bounded.
- **Assistant send button:** The assistant’s send button could sit against or beyond the edge of its panel. It now stays inside the panel, with the input and button aligned at narrow widths.
- **Ticket queue headers:** The Category header could overlap Due in the ticket queue. The two headers now sit side by side, with their columns aligned to the ticket rows.
- **Assistant change confirmations:** The assistant is now instructed not to claim a ticket change happened unless a tool reports success. When you have already asked for a change, it is also instructed not to ask for confirmation again unless a genuine decision remains.
- **Ticket summary times:** Ticket summaries could show UTC times that disagreed with the local times on the ticket page. Created dates, due dates, comments and events now use the user timezone in summaries, so their times match the ticket view.
- **Knowledge-base search failures:** A technical failure in knowledge-base search could appear as a successful search. It now counts as an error, so the dashboard’s tool error rate includes it while an unavailable search remains distinct.
- **Grounding by meaning:** Correct paraphrases and translations could be marked ungrounded when the assistant checked an answer against knowledge-base passages. Grounding now compares meaning, so those answers can be recognised as supported; if that comparison is unavailable, the previous word-based check is used.
