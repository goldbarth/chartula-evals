---
title: Release 1.9.0
description: The v1.9.0 release brings together the M9 frontend redesign and updates to the assistant’s ticket actions, citations, and grounding checks.
publishedAt: 2026-07-14
---

### What's New

- **Inline citation badges:** Cited passage titles in assistant answers can now show numbered badges in the rendered Markdown, with matching numbers in the sources list. Citations whose titles do not appear in the answer remain available in the sources list, so no citation is lost.
- **Suggested ticket actions:** The first suggested next step appears as a button for status changes or an agent picker for assignments, when the ticket has an actionable suggestion. You can rely on these controls to run the same actions as the existing manual controls; other suggestions remain non-clickable text or appear in the overflow menu.
- **Command palette:** Press Ctrl+K or Cmd+K on any page to open a keyboard-operable palette with navigation links and ticket search results. You can use the arrow keys, Enter, and Esc to move through results, open a selection, and close the palette.
- **Ticket status updates:** A ticket’s status changes immediately on the board or detail page when you select a new status. You can rely on the displayed status being reconciled with the server, with rejected changes restored and an explanation shown.
- **Inline ticket controls:** Status and assignee choices open in menus on the ticket page instead of in dialogs. Choosing an option applies the change in place, so the ticket stays on its current page and tab.
- **Inline citations in assistant chat:** Assistant answers can show numbered citation badges beside passages whose titles appear in the answer, with a preview on hover or keyboard focus. Citations without a matching title remain in the numbered sources list.
- **Assistant agent roster:** The assistant can now name the active agents when responding to assignment requests. It is instructed to use only roster names and to list valid agents when the requested name is not on the roster.
- **Grounding checks:** After knowledge-base passages are retrieved, the assistant is required to run a grounding check before streaming its draft. You can rely on at least one check after retrieval, though this does not guarantee that every passage retrieved later in a long chain is checked.
- **Consistent design tokens:** The interface’s colors, spacing, corner radii, elevation, and semantic chip colors now use shared design tokens. Status and priority chips use the same token set across the queue, board, and ticket detail views.

### What's Changed

- **v1.9.0 release:** This release brings together the M9 frontend redesign, including interface updates to ticket workflows and the assistant experience.

### Bug Fixes

- **Board card titles:** Long board-card titles now stop at two lines with an ellipsis. Cards in a lane stay within a bounded height.
- **Assistant composer layout:** The assistant chat composer’s send button now sits inside its panel, with the input and button aligned at narrow widths. You can rely on the composer staying within the panel bounds.
- **Ticket queue headers:** The Category and Due headers now appear side by side without overlapping, and the header columns stay aligned with the table cells. Category is displayed in uppercase.
- **Assistant confirmations:** The assistant now reports a change only after its tool call succeeds, and carries out changes users have already requested without asking again. It still asks for confirmation when a genuine decision is needed, such as an ambiguous ticket match or missing required information.
- **Summary timestamps:** Ticket summary timestamps now use the configured user timezone, including created, due, comment, and event times. You can rely on the summary’s times matching the ticket detail view.
- **Knowledge-base search errors:** A technical failure during a knowledge-base search is now reported as an error, while an unavailable search remains a distinct outcome. The dashboard’s error rate can therefore reflect technical search failures.
- **Meaning-based grounding:** Grounding checks now assess answer sentences against retrieved passages by meaning, so paraphrases and translations can be recognized as supported. If no Voyage key is available or embedding fails, the check falls back to lexical scoring.
