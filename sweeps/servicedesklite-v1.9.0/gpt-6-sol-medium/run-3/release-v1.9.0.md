---
title: Release 1.9.0
description: This release updates ticket workflows and assistant answers while making the web interface more consistent.
publishedAt: 2026-07-14
---

### What's New

- **Citations in Markdown answers:** Citation badges now appear beside passage titles quoted in the assistant’s Markdown answers, with a preview on hover or focus. Each badge matches a numbered Sources entry; citations whose titles do not appear in the answer remain in Sources.
- **Suggested ticket actions:** An actionable suggested step now appears as a button or assignee picker in the ticket header, with other steps in a menu. You can act on the suggestion there while the usual ticket controls remain available; steps that cannot be acted on remain text.
- **Command palette:** You can open a command palette from any page with Ctrl+K or Cmd+K to find pages and tickets. You can navigate it with the keyboard, and closing it returns focus to where you were.
- **Ticket status updates:** A status change on the board or ticket detail page used to wait for the server before appearing. It now appears immediately; if the server rejects it, the previous status returns and a message shows the error code.
- **Editing ticket status and assignee:** You can change a ticket’s status or assignee from menus in its header instead of opening a dialog. The ticket stays on the same tab and at the same scroll position while you make the change.
- **Citations in assistant chat:** Citation badges can now appear beside cited titles in assistant answers, with a source preview on hover or keyboard focus. Citations that cannot be placed in the answer remain available in the numbered Sources list.
- **Agent names in assistant chat:** The assistant now receives the active agent roster when handling an assignment request. It is told to use only those names and to list valid agents rather than guess when a requested name is not on the roster.
- **Grounding checks:** After retrieving knowledge-base passages, the assistant must run a grounding check before streaming an answer unless it has already checked itself. You can count on at least one check after retrieval in a run, though passages retrieved later in that run are not guaranteed to be checked.
- **Consistent interface styling:** Spacing, corners, and colors now follow shared scales across the web interface. Status and priority chips use consistent styling in the ticket queue, board, and detail view.

### What's Changed

- **Frontend redesign release:** v1.9.0 brings the M9 frontend redesign together in one release. You can use Markdown answers, ticket controls, and the dark-mode toggle in that release.

### Bug Fixes

- **Board card titles:** Long ticket titles on the board could grow beyond two lines and expand their cards. Titles now end with an ellipsis after two lines, keeping cards bounded when titles are long.
- **Assistant send button:** The assistant’s send button sat against the edge of its panel. The input and button now stay aligned inside the panel, including at narrow widths.
- **Ticket queue headers:** The Category header overlapped Due in the ticket queue. The headers now sit side by side and align with their columns in both themes.
- **Assistant change confirmations:** The assistant could claim a ticket change had happened without a successful result or ask for confirmation again after you had already requested it. It is now told to report a change only after a successful tool result and not to ask again unless the ticket match is ambiguous, required information is missing, intent is in doubt for a hard-to-reverse action, or a routing suggestion is uncertain.
- **Ticket summary times:** A ticket summary could show comment times in UTC rather than the user time zone. Created, due, comment, and event times in summaries now use the configured user time zone, matching the ticket detail view.
- **Knowledge-base search errors:** A failed knowledge-base search could appear as a successful search. Technical failures now register as errors in the dashboard, while an unavailable search remains distinct.
- **Grounding by meaning:** Grounding checks could mark correct paraphrases and translations as unsupported because they used different words from the source. When embeddings are available, checks now compare meaning so those answers can be recognized as grounded; without embeddings, checks fall back to word matching.
