---
title: Release 1.9.0
description: This release brings changes to ticket workflows, assistant answers, search, and interface styling, alongside fixes to summaries and knowledge-base handling.
publishedAt: 2026-07-14
---

### What's New

- **Citations in Markdown answers:** Citation badges now appear after cited passage titles in the assistant’s Markdown answers, with a source preview on hover or keyboard focus. Their numbers match the Sources list, where citations without a matching title in the answer remain available.
- **Suggested ticket actions:** The first actionable suggestion on a ticket now appears as a control you can use, while other suggestions remain in a menu. The usual ticket controls stay available, and tickets without suggestions show no empty suggested-action control.
- **Command palette:** Press Ctrl+K or Cmd+K on any page to open a command palette for navigation and ticket search. You can use the arrow keys and Enter to open a result, or Esc to close the palette and return focus to where it was.
- **Ticket status updates:** A status change now appears immediately on the board or ticket detail page, before the server responds. If the change is rejected, the previous status returns and a message shows the error code; rapid changes reconcile with the status the server accepted.
- **Ticket status and assignee:** You can now change a ticket’s status or assignee from menus in its header instead of opening a dialog. The ticket stays open on the same tab and at the same scroll position while the change is applied.
- **Citations in assistant answers:** Citation badges now appear beside passage titles in assistant answers when those titles can be matched, with source details on hover or keyboard focus. Citations without a match remain in the numbered Sources list, and answers without citations show no empty list.
- **Agent names in assistant chat:** The assistant now receives the active agent roster for each chat request. It is instructed to use only those names when assigning tickets and to list valid agents rather than choose a near match when a requested name is absent.
- **Grounding checks:** A knowledge-base-backed answer now receives a grounding check before the assistant starts streaming it, unless the assistant has already made that check. You can count on at least one check after retrieval, though passages retrieved later in a long exchange are not guaranteed to be checked.
- **Consistent interface styling:** Status and priority chips now use the same colors across the ticket queue, board, and detail page. The interface also uses shared spacing and corner-radius scales, so those elements follow the same styling across pages.

### What's Changed

- **Frontend release integration:** The frontend redesign changes are now together in v1.9.0. Assistant answers retain Markdown and a Sources list; inline citation badges are not included in this integration.

### Bug Fixes

- **Board card titles:** Long board card titles could grow beyond two lines and stretch their cards. Titles now end with an ellipsis after two lines, keeping card height bounded.
- **Assistant send button:** The assistant’s send button could sit against the edge of its panel. It now sits inside the panel, with the input and button aligned even at narrow widths.
- **Ticket queue headers:** The Category header could overlap Due in the ticket queue. The headers now sit side by side, with Category aligned to its column and styled like its neighboring headers.
- **Assistant change confirmations:** The assistant is now instructed not to claim a ticket change succeeded without a successful result, or ask you to confirm a change you already requested. It may still ask when the ticket is ambiguous, required information is missing, intent is genuinely uncertain for a hard-to-reverse action, or a routing suggestion is uncertain.
- **Ticket summary times:** Ticket summaries could show UTC times that differed from the local times beside them in the ticket view. Created, due, comment, and event times now use the configured user time zone, so the summary matches the ticket detail view.
- **Knowledge-base search failures:** A failed knowledge-base search could be reported as a successful result. Technical failures are now reported as errors, so they count toward the dashboard’s tool error rate and remain distinct from an unavailable search.
- **Grounding by meaning:** Grounding checks could mark correct paraphrases or translations as unsupported when their words differed from the source. With the semantic check available, those answers can be assessed by meaning; the word-based check remains the fallback when it is unavailable.
