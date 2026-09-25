---
title: Release 1.9.0
description: This release brings frontend changes to ticket handling and assistant answers, alongside changes to assistant grounding and reliability.
publishedAt: 2026-07-14
---

### What's New

- **Citations in assistant answers:** Citation badges now appear beside cited passage titles in the assistant’s formatted answers, with previews on hover or keyboard focus. Their numbers match the Sources list, where citations without a matching title in the answer remain available.
- **Suggested ticket actions:** The first actionable suggestion on a ticket is now a control you can use to change its status or assign an agent. Other suggestions remain in a menu, and the usual ticket controls stay available when there are no suggestions.
- **Keyboard navigation:** Press Ctrl/Cmd+K from any page to open a palette for navigating the app and finding tickets. You can use the arrow keys and Enter to open a result, or Esc to close the palette and return focus to where it was.
- **Ticket status changes:** On the board and ticket detail page, a status change now appears before the server responds. You can count on a rejected change restoring the previous status and showing its error code, while the board keeps the server-accepted status when changes happen in quick succession.
- **Ticket header controls:** Changing a ticket’s status or assignee now happens from menus in its header instead of a dialog. The ticket stays open at the same scroll position and on the same tab while you make the change.
- **Citations beside answers:** Citation badges can appear beside passage titles in assistant answers, with source details shown on hover or keyboard focus. Citations that cannot be placed in the answer remain in the numbered Sources list.
- **Agent names in chat:** The assistant is now given the active agent roster during each chat request. It is told to use only those names for assignments and to list valid agents rather than guess when a name is not on the roster.
- **Grounding checks:** An assistant answer based on retrieved knowledge-base passages now receives a grounding check before it starts streaming, whether it comes from chat or the autonomous worker. You can count on at least one check after retrieval, though it is not guaranteed to cover passages retrieved later in a long run.
- **Consistent interface styling:** Status and priority chips now use the same colors across the queue, board, and ticket detail page. You can count on those views sharing the same spacing and corner styles.

### What's Changed

- **Frontend release integration:** The v1.9.0 frontend changes are now combined in one release. You can count on the assistant displaying formatted answers with citations in the Sources list.

### Bug Fixes

- **Board card titles:** Long board card titles could extend beyond two lines and make cards grow without bound. Titles now have a two-line limit with an ellipsis, so cards stay within a bounded height.
- **Assistant send button:** The assistant’s send button could sit against or over the edge of its panel. You can count on the button staying inside the panel and aligned with the input, including at narrow widths.
- **Ticket queue headers:** The Category header in the ticket queue could overlap Due. You can count on the headers appearing side by side, with Category aligned to its column and styled like its neighbors.
- **Assistant change confirmations:** The assistant is now told not to claim a requested change succeeded without a successful result, or ask you to confirm a change you already requested again. You can count on it being instructed to ask first only when a decision or required information is missing, a ticket match is ambiguous, or there is genuine doubt about the action.
- **Ticket summary times:** A ticket summary could show a comment time in UTC while the ticket detail page showed local time. You can count on summary timestamps using the same configured user time zone as chat.
- **Knowledge-base search failures:** A failed knowledge-base search could be reported as a successful result. You can now count on technical failures being recorded as errors, distinct from a knowledge base that is unavailable.
- **Grounding by meaning:** Grounding checks now compare an answer’s meaning with retrieved passages instead of relying only on shared words. Correct paraphrases and translations can be recognized as supported when the semantic check is available; if it is unavailable or fails, the earlier word-based check is used.
