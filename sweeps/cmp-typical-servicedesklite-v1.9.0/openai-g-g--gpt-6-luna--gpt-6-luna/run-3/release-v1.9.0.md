---
title: Release 1.9.0
description: Version 1.9.0 brings together the M9 frontend redesign and updates assistant interactions, citations, and grounding.
publishedAt: 2026-07-14
---

### What's New

- **Inline citation badges:** Cited passage titles in assistant Markdown answers can now show numbered citation badges, with source details available on hover or keyboard focus. Citations whose titles do not appear in the answer remain in the sources list, so every citation stays available there.
- **Suggested ticket actions:** The first suggested ticket step now appears as a button or agent picker when it maps to an action, while remaining steps are available from an overflow menu. You can rely on these controls to run the same ticket actions as the manual controls, and unmapped steps remain non-clickable.
- **Keyboard command palette:** Press Ctrl/Cmd+K on any page to open a keyboard-operable palette with navigation links and ticket search results. You can move through results with the arrow keys, open one with Enter, and close the palette with Esc, which restores your previous focus.
- **Optimistic status updates:** On the board and ticket detail page, a status change appears before the server responds. You can rely on the view to restore the previous status if the server rejects the change, and to show the reason in a snackbar.
- **Inline ticket controls:** Changing a ticket’s status or assignee now opens a menu in the ticket header instead of a dialog. You can rely on the ticket staying on its current page, tab, and scroll position while the change is applied.
- **Inline chat citations:** Assistant answers can now show numbered citation badges next to passage titles, with source details available on hover or keyboard focus. Citations that are not anchored in the answer remain in the numbered sources list, so the supporting sources are still available.
- **Assistant agent roster:** The assistant can now name the active agents when responding to assignment requests. You can rely on it to use roster names rather than infer or invent an agent, and to list valid agents if the requested name is not on the roster.
- **Grounding checks:** After knowledge-base passages are retrieved, the assistant now runs a grounding check before streaming its first answer token if it has not already checked during that run. You can rely on at least one check after retrieval, but not on every passage retrieved during a long chain being checked.
- **Consistent design system:** Spacing, corner radii, colors, and elevation now use a shared design scale across the interface. You can rely on these styles using the same tokens across components.

### What's Changed

- **Version 1.9.0 release:** Version 1.9.0 brings together the M9 frontend redesign, including updated ticket workflows and assistant citation presentation.

### Bug Fixes

- **Board card titles:** Long board card titles now stop at two lines and show an ellipsis. You can rely on cards in a lane keeping a bounded height.
- **Assistant composer layout:** The assistant chat composer and send button now sit inside the panel, including at narrow widths. You can rely on the input and button staying aligned within the panel.
- **Ticket queue headers:** The Category header no longer overlaps the Due header in the ticket queue. You can rely on the headers and their columns staying aligned.
- **Assistant confirmations:** The assistant now avoids claiming a change succeeded unless a tool call reports success, and does not ask for confirmation when you have already requested a change. You can rely on it to ask before a write only when there is a genuine decision to resolve, such as an ambiguous ticket match or missing required information.
- **Summary timestamps:** Ticket summary timestamps now appear in the configured user time zone. You can rely on them matching the time zone used in the ticket detail view.
- **Knowledge-base search errors:** A failed knowledge-base search is now reported as an error, distinct from a search that is unavailable. You can rely on the dashboard’s error rate reflecting technical search failures.
- **Meaning-based grounding:** The assistant’s grounding check now evaluates answer sentences against retrieved passages by meaning, including paraphrases and translations. If no Voyage key is available or embedding fails, it falls back to the lexical check, so a verdict is still produced.
