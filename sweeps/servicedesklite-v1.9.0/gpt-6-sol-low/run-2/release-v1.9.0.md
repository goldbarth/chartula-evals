---
title: Release 1.9.0
description: This release brings frontend changes together with updates to assistant responses, ticket workflows, and error reporting.
publishedAt: 2026-07-14
---

### What's New

- **Citations in Markdown answers:** Citation badges appear beside cited passage titles in the assistant’s Markdown answers. Their numbers match the Sources list, and citations without a matching title remain in that list.
- **Suggested ticket actions:** A suggested next step appears as the primary action on a ticket when it can be carried out there. You can use it to change status or assign an agent, while the usual ticket controls remain available.
- **Command palette:** Press Ctrl+K or Cmd+K on any page to open a command palette for navigation and ticket search. You can use the arrow keys and Enter to open a result, or Esc to close it and return to your previous field.
- **Ticket status changes:** A ticket’s status now updates immediately when you change it on the board or ticket page. If the change is rejected, the previous status returns and a notification shows the error; rapid changes on the board reconcile with the server’s status.
- **Inline ticket controls:** Changing a ticket’s status or assignee now happens from menus in the ticket header instead of a dialog. The ticket stays open on the same tab and at the same scroll position.
- **Citation previews:** Citation badges appear beside matching titles in the assistant’s answer text. You can hover over or focus a badge to see its source, heading, and snippet; unmatched citations remain in the Sources list.
- **Agent names in assistant chat:** The assistant is now given the active agent roster in each chat request. It is instructed to use those exact names when assigning tickets and to list valid agents instead of guessing when a name is not on the roster.
- **Grounding checks:** Answers that use retrieved knowledge-base passages now trigger a grounding check before the assistant starts streaming its response, unless it has already checked. You can count on at least one check after retrieval, though this does not guarantee a check of every passage retrieved later in a long exchange.
- **Consistent interface styling:** Spacing, corners, elevation, and colors now use shared design values across the interface. Status and priority chips on the queue, board, and ticket page can now count on the same colors.

### What's Changed

- **Frontend redesign release:** The frontend redesign changes are brought together in v1.9.0. The release can be tagged from one integrated version.

### Bug Fixes

- **Board card titles:** Long board-card titles could extend beyond two lines and grow the card. They now end with an ellipsis after two lines, so cards remain bounded in their lanes.
- **Assistant send button:** The assistant’s send button sat against the edge of its panel. It now stays inside the panel, with the input and button aligned even at narrow widths.
- **Ticket queue headers:** The Category header in the ticket queue overlapped Due. The headers now sit side by side, with Category aligned to its column and styled like the other headers.
- **Assistant change confirmations:** The assistant is now instructed not to claim a change succeeded without a successful result, or ask you to confirm a change you already requested. You can rely on it being told to ask before a change only when a user decision is genuinely needed.
- **Ticket summary times:** Ticket summaries could show timestamps in UTC even when the ticket page showed local times. Created dates, due dates, comments, and events now use the configured user timezone, so summary times match the ticket view.
- **Knowledge-base search errors:** A failed knowledge-base search could be reported as a successful tool result. Technical failures are now reported separately from an unavailable search, so the dashboard’s error rate reflects those failures.
- **Grounding by meaning:** Grounding checks now compare an answer’s meaning with retrieved passages rather than relying only on shared words. Correct paraphrases and translations can be recognized as supported; when semantic scoring is unavailable, the earlier word-based check is used.
