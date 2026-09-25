---
title: Release 1.9.0
description: This release brings together frontend changes and updates how the assistant handles citations, grounding, ticket changes and knowledge-base failures.
publishedAt: 2026-07-14
---

### What's New

- **Citations in Markdown answers:** Citation badges now appear beside cited passage titles in the assistant’s Markdown answers, with source details on hover or keyboard focus. Their numbers match the Sources list, where citations without a matching title in the answer remain available.
- **Suggested ticket actions:** The first actionable suggestion on a ticket is now a control you can use to change its status or assign an agent. Other suggestions remain in the menu, and the usual ticket controls remain available when there are no suggestions.
- **Command palette:** Press Ctrl+K or Cmd+K from any page to open a palette for navigation and ticket search. You can use the arrow keys and Enter to open a result, or Esc to close the palette and return to where you were typing.
- **Ticket status changes:** A ticket’s status now changes on screen as soon as you move its board card or select a status on its detail page. If the change is rejected, the previous status returns and a notification shows the error code.
- **Editing ticket status and assignee:** Changing a ticket’s status or assignee used to open a dialog. You can now choose from menus in the ticket header while staying on the same ticket, at the same scroll position and tab.
- **Assistant citation badges:** Citations now appear as numbered badges beside matching titles in assistant answers, instead of only in a separate Sources list. You can hover over or focus a badge to see its source, heading and snippet; citations without a matching title stay in the list.
- **Agent names in assistant chat:** The assistant now receives the active agent roster during each chat request. It is instructed to use those names for ticket assignments and list valid agents rather than choose a close match when a requested name is not on the roster.
- **Grounding checks:** Assistant answers based on retrieved knowledge-base passages now receive a grounding check before the answer starts streaming. This applies to chat and the autonomous worker; you can count on at least one check after retrieval, though not on a check for every passage retrieved later in the same run.
- **Consistent interface styling:** Spacing, corners, elevation and colors now use shared design values across the interface. Status and priority chips on the queue, board and ticket detail pages can now rely on the same color definitions.

### What's Changed

- **Frontend release integration:** The frontend redesign is now brought together in v1.9.0. The release includes Markdown assistant answers and a dark-mode toggle, with citation badges for Markdown answers delivered separately.

### Bug Fixes

- **Board card titles:** Long ticket titles on board cards could keep growing past two lines. Titles now end with an ellipsis after two lines, so long titles do not keep stretching their cards or lane columns.
- **Assistant send button:** The assistant’s send button could sit against the edge of its panel. It now stays inside the panel, with the input and button aligned even at narrow widths.
- **Ticket queue headers:** The Category header in the ticket queue could overlap Due. The headers now sit side by side, with Category aligned to its column and styled like the other headers.
- **Assistant change confirmations:** The assistant is now instructed not to claim a ticket change succeeded unless a tool reports success in the conversation. It is also instructed to act on a requested change without asking again, except when a genuine decision or missing information requires your input.
- **Ticket summary times:** Ticket summaries could show comment times in UTC rather than the time shown on the ticket. Created, due, comment and event times in summaries now use the same user time zone as the ticket detail view.
- **Knowledge-base search failures:** A failed knowledge-base search could be reported as a successful tool result. Technical failures are now reported as errors, so the dashboard’s error rate reflects them while an unavailable search remains a distinct result.
- **Grounding by meaning:** Grounding checks could mark correct paraphrases and translations as unsupported when their wording differed from the source. With embeddings available, the check now compares meaning against retrieved passages; without them, it falls back to the existing word-based check.
