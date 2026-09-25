---
title: Release 1.9.0
description: This release brings together frontend changes for tickets and assistant answers with changes to assistant grounding, assignments, and summaries.
publishedAt: 2026-07-14
---

### What's New

- **Citations in Markdown answers:** When a cited passage title appears in an assistant Markdown answer, a numbered badge appears beside it with source details on hover or keyboard focus. The badge number matches the Sources list, where citations without a matching title remain available.
- **Suggested ticket actions:** A ticket’s first actionable suggestion now appears as a button or agent picker, with other suggestions in a menu. You can act on that suggestion while the usual ticket controls remain available, including on tickets with no suggestions.
- **Command palette:** Press Ctrl/Cmd+K on any page to open a command palette for navigation and ticket search. You can use arrow keys and Enter to open a result, or Esc to close the palette and return focus to where you were.
- **Ticket status changes:** A moved board card or changed ticket status now displays its new status before the server responds. If the change is rejected, the previous status returns with an error code, so the displayed status reflects the accepted change.
- **Inline ticket edits:** Changing a ticket’s status or assignee now happens from menus in its header rather than dialogs. You can keep the ticket open at the same scroll position and tab while the change takes effect.
- **Citation previews:** Cited passage titles in assistant answers can show numbered badges with source details on hover or keyboard focus. Citations without a matching title stay in the Sources list, so they remain available even when no badge appears.
- **Agent names in assignments:** The assistant now receives the active agent roster when you ask it to assign a ticket. It is instructed to use those names and list valid agents when a name is not on the roster, rather than invent or substitute one.
- **Grounding checks:** Answers drawing on knowledge-base passages now trigger a grounding check before the assistant starts streaming, unless a check has already run. You can count on at least one check after retrieval, though passages retrieved later in a long chain are not guaranteed to be covered.
- **Interface styling:** The queue, board, and ticket details now display status and priority chips using the same colors. You can read those chips consistently across the views, while spacing and corners follow shared scales throughout the interface.

### What's Changed

- **Frontend redesign:** Markdown answers and dark mode now ship alongside updated ticket controls in v1.9.0. You can read assistant replies as formatted text instead of raw Markdown markers.

### Bug Fixes

- **Board card titles:** Long board-card titles could extend beyond two lines and stretch the card. They now end with an ellipsis after two lines, so cards remain bounded even for long titles.
- **Assistant send button:** The assistant’s send button could sit against the panel edge while the message input lost its intended layout. The button now stays inside the panel, and the input and button remain aligned at narrow widths.
- **Ticket queue headers:** The Category header in the ticket queue could overlap Due and appear out of line with other headers. The headers now sit side by side with their columns aligned, so you can read both labels clearly.
- **Assistant change requests:** When you request a ticket change, the assistant may ask you to confirm it again or claim it succeeded without a successful result. It is now instructed to act without repeated confirmation and to report a change only after a successful result, while still asking when a decision is needed.
- **Ticket summary times:** Ticket summaries could show comment times in UTC rather than your timezone. Created, due, comment, and event times in summaries now use the same timezone as the ticket detail view.
- **Knowledge-base search failures:** A failed knowledge-base search could appear as a successful search in assistant records. Failures now count as errors in the dashboard, so its error rate distinguishes technical failures from an unavailable search.
- **Grounding by meaning:** Grounding checks could flag correct paraphrases or translations as unsupported when their words differed from a knowledge-base passage. When meaning-based scoring is available, the assistant can recognize them as supported; otherwise it falls back to word-based scoring.
