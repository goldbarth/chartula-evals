---
title: Release 1.9.0
description: Version 1.9.0 combines the M9 frontend redesign with updates to ticket handling and assistant answers.
publishedAt: 2026-07-14
---

### What's New

- **Inline citations:** When an assistant Markdown answer includes a passage title verbatim, a numbered citation badge appears beside it, with source details on hover or keyboard focus. The badge number matches the Sources list, and citations without a matching title remain listed there.
- **Suggested ticket actions:** When a ticket has an actionable suggestion, its first suggested step appears as a primary button or owner picker, with other steps in an overflow menu. You can run mapped suggestions there; unmapped steps remain non-clickable, and tickets without suggestions keep their existing controls.
- **Command palette:** Press Ctrl+K or Cmd+K from any page to open a command palette with navigation and ticket search results. Use the arrow keys to move through results, Enter to open one, and Esc to close the palette and return focus to where you were.
- **Status updates:** On the board, a dragged ticket could snap back while its status change awaited the server; status changes now appear immediately on the board and ticket detail. If a change is rejected, the previous status is restored and you see the reason; rapid changes do not leave the board showing a status the server rejected.
- **Inline ticket actions:** Changing a ticket's status or assignee now opens an inline menu instead of a dialog. The ticket stays on its current tab and scroll position as the change is applied, and errors appear in a notification.
- **Citation previews:** In assistant answers, numbered citation badges appear beside quoted titles, and hovering over or focusing a badge shows its source, heading, and snippet. Citations without a matching title remain in the numbered Sources list, and answers without citations have no empty list.
- **Agent roster:** When you ask the assistant to assign a ticket, it can tell you the active agents and list valid names if the one you request isn't on the roster. You no longer have to make a failed assignment attempt to get those options.
- **Grounding checks:** After knowledge-base passages are retrieved, the product now tells the assistant and autonomous worker to check a draft against them before streaming an answer. If a run retrieves passages more than once, this does not guarantee that every passage is checked.
- **Consistent interface styling:** Spacing, corner rounding, and status and priority chip colors now follow shared design rules across the interface. You can rely on status and priority chips using the same colors in the queue, board, and ticket detail.

### What's Changed

- **M9 frontend redesign:** The M9 frontend redesign is brought together in v1.9.0, with release notes for the release. You can follow the redesign as one complete release rather than separate partial updates.

### Bug Fixes

- **Board card titles:** Long board-card titles could stretch cards beyond two lines; they now clamp to two lines with an ellipsis. Card heights stay bounded within a lane.
- **Assistant composer:** The assistant chat's send button could sit at the panel edge; it now appears inset within the panel. The input and button stay aligned in the same row at narrow widths.
- **Ticket list headers:** On the ticket list, the Category heading could run into Due; the headers now sit side by side, with Category uppercase. The header and body cells line up across those columns.
- **Assistant confirmations:** When you ask the assistant to make a ticket change, it proceeds without asking again unless the ticket match or required details are unclear, your intent is in doubt for a hard-to-reverse action, or a route suggestion is uncertain. It reports a change only after the action succeeds.
- **Summary time zones:** Ticket summaries could show UTC times even when ticket details showed local times. Summary timestamps now use the same user time zone as ticket details, so you can compare them directly.
- **Knowledge-base search errors:** A failed knowledge-base search could be treated as a successful search. Technical failures are now reported as errors, distinct from searches that are unavailable by design, so you can tell a service failure from an unavailable search.
- **Meaning-based grounding:** For answers checked against retrieved knowledge-base passages, a correct paraphrase or translation could be marked ungrounded because its wording differed from the source. When meaning-based checking is available, supported paraphrases and translations can count as grounded; if that check is unavailable or fails, the earlier text-matching method remains the fallback.
