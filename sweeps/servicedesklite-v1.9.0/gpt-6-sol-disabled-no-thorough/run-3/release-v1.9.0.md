---
title: Release 1.9.0
description: This release brings together frontend changes to tickets and assistant answers with updates to assistant checks and reporting.
publishedAt: 2026-07-14
---

### What's New

- **Citations in assistant answers:** Citation badges now appear beside cited passage titles in Markdown answers, with a preview on hover or keyboard focus. Their numbers match the Sources list, and citations without a matching title remain in that list.
- **Suggested ticket actions:** The first actionable suggestion on a ticket is now a button or agent picker, with other suggestions in a menu. You can act on a suggestion directly, while the usual ticket controls remain available.
- **Command palette:** Press Ctrl/Cmd+K on any page to open a command palette for navigation and ticket search. You can use the arrow keys and Enter to open a result, or Esc to close the palette and return to where you were typing.
- **Ticket status changes:** A status change now appears immediately on the board or ticket detail page. You can count on a rejected change restoring the previous status and showing an error code, while a successful board move is reconciled with the server.
- **Ticket status and assignment:** Changing a ticket’s status or assignee now uses menus in the ticket header instead of dialogs. The ticket stays open on the same tab and at the same scroll position when you make a selection.
- **Citations in assistant answers:** Citation badges now appear beside cited titles in assistant answers, with source details available on hover or keyboard focus. Citations that cannot be placed inline remain in the numbered Sources list.
- **Agent names in assistant chat:** The assistant now receives the active agent roster during each chat request. It is instructed to use those exact names and list valid agents rather than guess when a requested name is not on the roster.
- **Grounding checks:** The assistant now requires a grounding check before streaming an answer after retrieving knowledge-base passages, unless it has already checked that answer. You can count on at least one check after retrieval, though this does not guarantee that every passage retrieved later in a long exchange is checked.
- **Interface styles:** Spacing, corners, elevation and semantic colors now use shared design values across the interface. Status and priority chips on the queue, board and ticket detail pages can now count on the same color definitions.

### What's Changed

- **Frontend release integration:** The frontend redesign changes are now brought together for the v1.9.0 release. You can count on the combined release including Markdown assistant answers and a Sources list beneath them; inline citation badges are delivered separately.

### Bug Fixes

- **Board card titles:** Long board card titles could grow beyond two lines and stretch their cards. Titles now show an ellipsis after two lines, so cards in a lane retain a bounded height.
- **Assistant send button:** The assistant’s send button sat against the edge of its panel. It now stays inside the panel, with the input and button aligned at narrow widths.
- **Ticket queue headers:** The Category header overlapped Due in the ticket queue. Both headers now sit side by side, with the Category header and its column cells aligned.
- **Assistant change confirmations:** The assistant is now instructed not to claim a change happened without a successful result, and not to ask again when you have already requested the change. It can still ask when a ticket match is ambiguous, required information is missing, intent is genuinely uncertain for a hard-to-reverse action, or a routing suggestion is uncertain.
- **Ticket summary times:** Ticket summaries could show UTC times that differed from the local times beside them. Created dates, due dates, comments and events now use the configured user time zone, so summary times can match the ticket detail view.
- **Knowledge-base search failures:** A failed knowledge-base search could be reported as a successful search. Technical failures are now reported as errors, so the dashboard’s error rate reflects them while an unavailable search remains distinct.
- **Grounding assessment:** Grounding checks could mark correct paraphrases and translations as unsupported because they used different words from their sources. The assistant now compares meaning when embeddings are available, with word-based checking as a fallback; checks can still count non-source claims in a finished answer.
