---
title: Release 1.9.0
description: Version 1.9.0 brings together the frontend redesign, with updates to ticket workflows, assistant chat, and the interface.
publishedAt: 2026-07-14
---

### What's New

- **Inline citation badges:** Citations can appear as numbered badges beside the passages they cite in the assistant’s Markdown answer. When a passage title appears in the answer, its badge and Sources entry share a number; citations without a matching title remain in the Sources list, so you can still find every citation.
- **Suggested ticket actions:** A ticket’s first actionable suggested step appears as a button or agent picker, with other suggestions in an overflow menu. You can use these controls to carry out the suggested status change or assignment through the same actions as before.
- **Command palette:** Press Ctrl/Cmd+K on any page to open a keyboard-operated palette with navigation destinations and ticket search results. You can move through results with the arrow keys, open one with Enter, and close the palette with Esc, which restores your previous focus.
- **Optimistic status changes:** A ticket’s status updates immediately when you change it on the board or detail page. You can rely on the status being reconciled with the server, or restored if the change is rejected; rejected changes also show the error code in a snackbar.
- **Inline ticket controls:** You can change a ticket’s status or assignee from menus in its header without opening a dialog or leaving the ticket. The ticket stays on its current tab and at its current scroll position, and errors appear in a snackbar.
- **Inline chat citations:** Citations can appear as numbered badges beside matching passage titles in assistant chat answers, with a preview on hover or keyboard focus. Citations without a matching title remain in the numbered Sources list, so you can still find them.
- **Agent roster in assistant chat:** The assistant can name the active agents when discussing ticket assignment. If your requested name is not on the roster, it can list the valid agents rather than choosing a close match.
- **Grounding check:** After knowledge-base passages are retrieved, the assistant is required to run a grounding check before streaming its first answer token. You can rely on the answer having been checked at least once after retrieval, though not necessarily against every passage retrieved during a longer chain.
- **Consistent design tokens:** The interface now uses shared design scales for colors, spacing, corner radii, elevation, and semantic chip colors. Ticket status and priority chips use the same colors across the queue, board, and detail views, so their appearance stays consistent.

### What's Changed

- The v1.9.0 release brings the M9 Frontend Redesign together in one release, including refreshed ticket and assistant interfaces.

### Bug Fixes

- **Board card titles:** Long ticket titles on board cards are now limited to two lines with an ellipsis. Cards in a lane stay bounded in height when a title is long.
- **Assistant composer layout:** The assistant chat’s send button now sits inside the composer panel, with the input and button aligned at narrow widths. You can use the composer without the button extending beyond the panel.
- **Ticket queue headers:** The Category header now sits beside Due without overlapping, and the columns stay aligned. You can read the headers in both themes without them running together.
- **Assistant change confirmations:** The assistant no longer asks for confirmation after you have already requested a change, including after correcting an earlier mistake. It reports a change as completed only after a tool call succeeds in the conversation.
- **Summary timestamps:** Ticket summary timestamps are now shown in the configured user timezone. You can rely on the times in summaries matching the timezone used by the ticket detail view.
- **Knowledge-base search errors:** A failed knowledge-base search is now reported as an error, distinct from a search that is unavailable. The dashboard can count technical failures in its error rate.
- **Meaning-based grounding scores:** Correct paraphrases and translations can now be recognized as grounded against retrieved passages. If embeddings are unavailable or fail, grounding falls back to lexical scoring, so a verdict can still be returned.
