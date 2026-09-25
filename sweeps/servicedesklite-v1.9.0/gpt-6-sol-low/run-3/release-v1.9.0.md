---
title: Release 1.9.0
description: This release brings together frontend changes and updates to how the assistant handles citations, ticket actions and knowledge-base answers.
publishedAt: 2026-07-14
---

### What's New

- **Citations in Markdown answers:** Citation badges now appear beside cited passage titles in the assistant’s Markdown answers, with a preview on hover or keyboard focus. Their numbers match the Sources list, where citations remain available if their titles do not appear in the answer.
- **Suggested ticket actions:** The first actionable suggestion on a ticket now appears as a status button or assignee picker, with other suggestions in a menu. The usual ticket controls remain available, and tickets without actionable suggestions show no empty button.
- **Command palette:** Press Ctrl+K or Cmd+K on any page to open a command palette for navigation and ticket search. You can use the arrow keys and Enter to open a result, or Esc to close it and return focus to where you were.
- **Ticket status changes:** A ticket’s status now changes immediately on the board or detail page while the request completes. If the change is rejected, the previous status returns and a message shows the error code; rapid board changes reconcile with the server’s status.
- **Inline ticket editing:** Changing a ticket’s status or assignee now uses menus in the ticket header instead of dialogs. The ticket stays open on the same tab and at the same scroll position while you make the change.
- **Assistant citation badges:** Citation badges now appear beside cited titles in assistant answers, with source details shown on hover or keyboard focus. Citations that cannot be placed in the answer remain available in a numbered Sources list.
- **Agent names in assistant chat:** The assistant now receives the active agent roster with each chat request when helping assign tickets. It is instructed to use only names on that roster and to list valid names rather than guess when a requested name is absent.
- **Grounding checks:** Assistant and worker answers based on retrieved knowledge-base passages now receive a grounding check before the answer starts streaming, unless the model has already made one. You can count on at least one check after retrieval, though passages retrieved later in a longer exchange are not necessarily checked.
- **Consistent interface styling:** Spacing, rounded corners, colours and status chips now follow shared scales across the interface. You can count on the same status and priority chip colours in the queue, board and ticket detail views.

### What's Changed

- **Frontend release:** The frontend redesign changes are now together in v1.9.0, including Markdown assistant answers and ticket-page changes. You can access them together in this release.

### Bug Fixes

- **Board card titles:** Long ticket titles on board cards could extend beyond two lines and enlarge their cards. Titles now stop at two lines with an ellipsis, so cards stay bounded even when a title is long.
- **Assistant send button:** The assistant’s send button could sit against or beyond the edge of its panel. It now stays inside the panel, with the input and button aligned even at narrow widths.
- **Ticket queue headings:** The Category heading in the ticket queue could overlap Due. The headings now sit side by side, with Category aligned to its column and styled like the neighbouring headings.
- **Assistant change confirmations:** The assistant’s chat instructions now distinguish between a requested change and a decision that needs your input. They tell it to report a change as complete only after a successful tool result, and not to ask you to confirm a change you already requested unless a genuine decision remains.
- **Ticket summary times:** Times in a streamed ticket summary could differ from those shown beside the ticket when you use a local timezone. Summary timestamps now use the configured user timezone, so they match the ticket detail view.
- **Knowledge-base search failures:** A failed knowledge-base search could be reported as a successful search. Technical failures are now reported as errors, so the dashboard’s tool error rate reflects them while an unavailable search remains a separate result.
- **Grounding by meaning:** Grounding checks could mark a correct paraphrase or translation as unsupported because its words differed from the source. When embeddings are available, checks now compare meaning with retrieved passages; without them, the previous word-based check remains the fallback.
