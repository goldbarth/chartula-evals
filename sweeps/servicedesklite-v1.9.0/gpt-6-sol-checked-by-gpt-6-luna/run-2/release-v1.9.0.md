---
title: Release 1.9.0
description: This release brings together ticket and assistant interface changes with checks and fixes for assistant responses.
publishedAt: 2026-07-14
---

### What's New

- **Citations in Markdown answers:** Citation badges now appear beside cited titles in the assistant's Markdown answers, with a preview on hover or keyboard focus. Their numbers match the sources list, and citations without a matching title remain in that list.
- **Suggested ticket actions:** The first actionable suggestion on a ticket is now a button or agent picker, with other suggestions in a menu. The usual ticket controls remain available, so you can still use them when there is no actionable suggestion.
- **Command palette:** You can open a command palette from any page with Ctrl+K or Cmd+K to find pages and tickets. Arrow keys and Enter let you open a result, and Esc closes the palette and returns focus to where it was.
- **Ticket status changes:** A ticket's status now changes on the board or detail page before the server responds. If the change is rejected, the previous status returns with an error message, and rapid changes keep the display aligned with the status the server accepted.
- **Ticket status and assignee:** Changing a ticket's status or assignee now happens in menus on the ticket page rather than in dialogs. Your scroll position and open tab stay in place while you make the change.
- **Citations in assistant answers:** Citation badges now appear beside cited titles in assistant answers, with source details on hover or keyboard focus. Citations that cannot be placed in the answer remain available in the numbered sources list.
- **Agent names in chat:** The assistant now receives the current agent roster during each chat request. It is instructed to use only those names when assigning a ticket and to list valid agents rather than guess when a name is not on the roster.
- **Grounding checks:** The assistant and autonomous worker now run a grounding check before streaming an answer after retrieving knowledge-base passages, unless a check has already run. You can count on at least one check after retrieval, though this does not guarantee that every passage retrieved later in a long exchange is checked.
- **Consistent interface styles:** Spacing, corners, colors, and status and priority chips now use a shared design scale across the interface. You can count on the same chip colors in the queue, board, and ticket detail views.

### What's Changed

- **Frontend redesign release:** Version 1.9.0 brings the frontend redesign together in one release. Markdown answers, dark mode, and the updated ticket controls are available together.

### Bug Fixes

- **Long board card titles:** Long titles on board cards could extend beyond two lines and make cards grow. Titles now stop at two lines with an ellipsis, keeping cards bounded.
- **Assistant send button:** The assistant's send button could sit against or over the edge of its panel. It now stays inside the panel, aligned with the input even at narrow widths.
- **Ticket queue headers:** The Category header in the ticket queue could overlap Due. Both headers now sit side by side, with their columns aligned.
- **Assistant change confirmations:** The assistant now receives instructions not to claim a change succeeded without a successful result and not to ask you again before making a change you requested. It is instructed to ask only when a genuine decision is still needed.
- **Ticket summary times:** Times in a ticket summary could differ from those shown on the ticket detail page. Created, due, comment, and event times now use the same user timezone as the ticket detail view.
- **Knowledge-base search failures:** A technical failure during a knowledge-base search could be reported as a successful search. Failures now count as errors in the dashboard, while an unavailable search remains a separate result.
- **Grounding by meaning:** Grounding checks could mark a correct paraphrase or translation as unsupported when its words differed from the source. Checks now compare meaning when embeddings are available, so those answers can be recognized as supported; without embeddings or if embedding fails, the earlier word-based check remains the fallback.
