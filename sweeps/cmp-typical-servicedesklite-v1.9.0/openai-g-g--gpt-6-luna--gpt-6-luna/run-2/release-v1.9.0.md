---
title: Release 1.9.0
description: This release brings together frontend updates to ticket workflows and assistant chat, alongside changes to assistant grounding and error handling.
publishedAt: 2026-07-14
---

### What's New

- **Inline citation badges:** Cited passage titles in assistant answers can now show numbered badges, with hover and keyboard-focus previews. When a citation title appears in the answer, its badge number matches its entry in the Sources list, and citations without a matching title remain in that list.
- **Suggested ticket actions:** The first suggested step now appears as a button or agent picker when it maps to an available ticket action. You can run the suggested action directly, while other steps remain available in the overflow menu and generic ticket controls stay available.
- **Command palette:** You can now open a command palette from any page with Ctrl+K or Cmd+K to search navigation links and tickets. Use the arrow keys to select a result, Enter to open it, and Escape to close the palette and return focus to where it was.
- **Optimistic status updates:** A ticket’s status now changes on the board or detail page as soon as you request a move, before the server responds. The view reconciles with the server after an accepted move, restores the previous status after a rejected move, and shows the rejection code.
- **Inline ticket controls:** You can now change a ticket’s status or assignee from menus in its header instead of opening a dialog. The ticket stays on its current page, tab, and scroll position, and errors appear in a snackbar.
- **Inline citation badges:** Citations can now appear as numbered badges beside matching passage titles in assistant answers, with previews available on hover or keyboard focus. Badges share their numbering with the Sources list, which remains available for citations that are not anchored in the answer.
- **Agent roster in assistant answers:** The assistant can now name the active agents when discussing ticket assignment. It uses the roster provided for each chat request, so it can list valid agents rather than guessing when a name is not on the roster.
- **Grounding checks:** After knowledge-base passages are retrieved, the assistant now runs a grounding check before streaming its first answer token, unless it has already checked during that run. This ensures at least one check after retrieval, but does not ensure that every passage retrieved later in a long chain is checked.
- **Consistent design tokens:** The interface now uses a shared scale for colors, spacing, corner radii, elevation, and chip colors across the theme and stylesheets. Status and priority chips use the same colors across the queue, board, and ticket detail views.

### What's Changed

- **v1.9.0 release:** This release brings together the M9 frontend redesign, including changes to ticket views, assistant chat, and interface styling.

### Bug Fixes

- **Board card titles:** Long ticket titles on board cards could extend the cards without being clamped. Titles now stop at two lines with an ellipsis, keeping cards within a bounded height.
- **Assistant chat layout:** The send button could sit flush with or beyond the edge of the assistant chat panel. The composer now stays inset within the panel, with its input and button aligned at narrow and wide widths.
- **Ticket queue headers:** The Category header could overlap the Due header in the ticket queue. The headers now sit side by side with their columns aligned, and Category uses uppercase styling.
- **Assistant confirmations and write honesty:** The assistant could ask for confirmation again after you had already requested a change, or claim a change without a successful tool result. It now acts on requested changes without re-asking and reports a change only after the tool call succeeds.
- **Summary timestamps:** Ticket summary timestamps could appear in UTC rather than the timezone used in the ticket details. Summaries now present creation, due, comment, and event times in the configured user timezone.
- **Knowledge-base search errors:** A failed knowledge-base search could be reported as a successful result, making technical failures indistinguishable from an unavailable search. Technical failures are now reported as errors, while the unavailable-search outcome remains distinct.
- **Grounding by meaning:** Correct paraphrases and translations could be marked as ungrounded because the check relied on word overlap. Grounding now uses semantic similarity when embeddings are available, with lexical scoring as a fallback when they are not.
