---
title: Release 1.9.0
description: The v1.9.0 release brings together the M9 frontend redesign, with changes to ticket workflows, assistant responses, and the interface.
publishedAt: 2026-07-14
---

### What's New

- **Inline citation badges:** Cited passage titles in assistant Markdown answers can show numbered badges, with a preview on hover or keyboard focus. The badges match the numbered source entries, and citations without a matching title remain in the source list.
- **Suggested ticket actions:** The first actionable suggested step appears as a button or agent picker on a ticket, while other steps remain in an overflow menu. You can use these controls to carry out suggested status changes or assignments through the same actions as the manual controls.
- **Command palette:** You can open a command palette from any page with Ctrl/Cmd+K, search navigation targets and tickets, and move through results with the keyboard. Esc closes it and returns focus to where it was before the palette opened.
- **Optimistic status updates:** A ticket’s status changes on the board or detail view as soon as you make the change. You can rely on the displayed status being reconciled with the server after success, or restored to its previous value with an explanation if the change is rejected.
- **Inline ticket controls:** Status and assignee choices open in menus on the ticket instead of dialogs. The ticket stays on its current page, tab, and scroll position, and errors appear in a snackbar.
- **Inline citation badges:** Citations can appear as numbered badges beside matching titles in assistant answers, with source details available on hover or keyboard focus. Unmatched citations remain in the numbered sources list.
- **Agent roster in assistant answers:** The assistant can name the active agents when responding to assignment requests. It is instructed to use only roster names and to list valid agents when the requested name is not present.
- **Grounding check:** After knowledge-base passages are retrieved, the assistant performs a grounding check before streaming its first answer token, unless it has already checked during that run. You can rely on at least one check after retrieval, but not on every passage in a longer retrieval chain being checked.
- **Consistent design tokens:** The interface uses shared design values for colors, spacing, corners, elevation, and semantic chip colors. Status and priority chips use the same colors across the queue, board, and ticket details.

### What's Changed

- **v1.9.0 release:** This release brings the M9 frontend redesign together in a single release, including updated ticket workflows and assistant features.

### Bug Fixes

- **Board card titles:** Long board card titles now stop at two lines with an ellipsis. Cards in a lane remain bounded in height.
- **Assistant chat layout:** The assistant’s send button now sits inside the composer panel, including at narrow widths. The input and button remain aligned in the panel.
- **Ticket queue columns:** The Category and Due headers now appear side by side without overlap, with the table columns aligned. Category is shown as a static label rather than a sort control.
- **Assistant confirmation policy:** The assistant no longer claims a change succeeded unless a tool reports success, and it carries out changes the user has already requested without asking again. It still asks for confirmation when the request involves a genuine decision, such as an ambiguous ticket match or uncertain intent.
- **Summary timestamps:** Timestamps in ticket summaries are shown in the configured user timezone. Summary times match the ticket detail view, so you can rely on the same local time in both.
- **Knowledge-base search failures:** A failed knowledge-base search is now reported as an error, distinct from a search that is unavailable. The dashboard’s error rate reflects technical failures.
- **Grounding by meaning:** Grounding checks now assess whether answer sentences are supported by retrieved passages, including when they paraphrase or translate them. If semantic evaluation is unavailable or embedding fails, the existing lexical check provides a fallback.
