---
title: Release 1.9.0
description: v1.9.0 brings together the frontend redesign with updates to ticket actions and assistant answers.
publishedAt: 2026-07-14
---

### What's New

- **Inline citation badges:** When an assistant answer includes a cited passage title verbatim, a numbered badge appears beside it with a preview on hover or keyboard focus; citations without a matching title stay in Sources. The inline numbers match the numbered source entries, so you can connect each badge to its source.
- **Suggested ticket actions:** On tickets with suggested next steps, the first actionable suggestion appears in the header as a button or assignee picker, while other suggestions appear in an overflow menu and unmapped suggestions stay non-clickable; tickets without suggestions keep the existing generic controls. You can run suggested actions through the same handlers as the regular ticket controls.
- **Keyboard command palette:** Press Ctrl/Cmd+K from any page to open a palette with navigation destinations and ticket search results. You can move through results with the arrow keys, open one with Enter, and close the palette with Esc to return focus to where it was.
- **Immediate status updates:** On the board and ticket detail, a status change appears immediately and returns to its previous status if rejected, with an error snackbar. The displayed status settles on the server's accepted state, and the snackbar includes the problem code.
- **Inline ticket controls:** On ticket details, choosing a status or assignee from the header popover applies the change without opening a dialog or leaving the ticket. Your tab and scroll position stay in place, and errors appear in a snackbar.
- **Citation previews:** When an assistant answer contains a citation title, a numbered badge appears beside it, and hovering over or focusing the badge shows the source, heading, and snippet. Citations that aren't anchored in the answer remain in the numbered Sources list, so the source is still available.
- **Available ticket assignees:** When you ask the chat assistant to assign a ticket, it is told which agents are active and to use only those names; if the requested name isn't listed, it should give you the valid names instead of guessing. You can check available assignees without first getting a failed assignment.
- **Grounding check before answers:** After knowledge-base passages are retrieved, the assistant runs a grounding check before streaming its answer unless it has already checked during that run. You can rely on at least one check after retrieval, but not on every passage gathered later in a long retrieval chain being checked.
- **Consistent visual styling:** Spacing, corner rounding, and semantic chip colors now follow shared scales across the interface. Status and priority chips use the same color definitions wherever they appear, so their styling stays consistent between the queue, board, and ticket details.

### What's Changed

- **v1.9.0 release:** The complete M9 frontend redesign is included in v1.9.0. You can read the release notes for the integrated milestone.

### Bug Fixes

- **Board card titles:** Long board-card titles now stop at two lines with an ellipsis. This keeps card heights bounded within each lane.
- **Assistant composer layout:** The assistant chat's send button now sits inside its composer panel, including at narrow widths. The input and button stay aligned in the same row.
- **Ticket queue headings:** In the ticket queue, the Category heading no longer runs into Due and now matches neighboring headings in uppercase. Category and its body cells stay aligned, and the heading remains a label rather than a sort control.
- **Ticket change confirmations:** When you ask the assistant to change a ticket, it is instructed to act without asking you to confirm again and not to report success unless the tool result succeeds. Completion claims are tied to successful tool results in the conversation; the assistant may still ask about an ambiguous ticket, missing information, uncertain intent for a hard-to-reverse action, or an uncertain routing suggestion.
- **Summary timestamps:** Ticket summaries now express timestamps in the configured user time zone, matching the ticket detail view. You can compare times in a summary and ticket details without accounting for a difference between their time zones.
- **Knowledge-base search errors:** When knowledge-base search encounters a technical failure, it now returns an error distinct from the unavailable-search result. The dashboard can count the failure in its error rate, so an unavailable search and a failed search are not conflated.
- **Meaning-based grounding checks:** When semantic embeddings are available, grounding checks can recognize correct paraphrases and translations against retrieved passages instead of relying on word overlap. If embeddings are unavailable or fail, the lexical check remains the fallback, and the check still does not separate source claims from other answer content.
