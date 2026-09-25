---
title: Release 1.9.0
description: Version 1.9.0 brings together the M9 frontend redesign and changes to ticket workflows and assistant behavior.
publishedAt: 2026-07-14
---

### What's New

- **Inline citation badges:** Citations can now appear as numbered badges beside their cited passage titles in assistant Markdown answers, with hover and keyboard-focus previews. When a title appears in the answer, its badge and Sources entry use the same number; citations whose titles do not appear remain in the Sources list, so you can still find them.
- **Suggested ticket actions:** The first actionable suggested step now appears as a primary control in the ticket header, with other steps available in an overflow menu. For tickets with an actionable suggestion, you can run it directly through the same action path as the manual controls; when no suggestion is available, the generic controls remain available.
- **Command palette:** Press Ctrl+K or Cmd+K on any page to open a command palette with navigation links and ticket search results. You can use the arrow keys, Enter, and Esc to navigate, open a result, and close the palette, with focus returning to where it was before.
- **Immediate status updates:** A ticket’s status now changes on the board or detail page as soon as you select or move it, before the server responds. You can count on a rejected change restoring the previous status and showing the error, while rapid successive board changes do not leave the displayed status out of step with the server.
- **Inline ticket actions:** Changing a ticket’s status or assignee now opens a menu in the ticket header instead of a dialog. The ticket stays on its current page, tab, and scroll position while the change is applied, and errors appear in a notification.
- **Inline assistant citations:** Citations can now appear as numbered badges beside matching titles in assistant answers, with previews on hover or keyboard focus. If a citation title is not found in the answer, it remains in the numbered Sources list, so you can still access it.
- **Assistant agent roster:** The assistant’s replies now have access to the current agent roster, including when it is empty. When assigning a ticket, you can rely on the assistant to use roster names and list valid agents instead of inventing a name or choosing a closest match.
- **Grounding checks:** After knowledge-base passages are retrieved, the assistant now performs a grounding check before streaming its answer if one has not already run. This applies to both assistant chat and the autonomous worker, so you can rely on a check being made after retrieval without the model having to choose to call it.
- **Consistent design styling:** Colors, spacing, corner rounding, elevation, and semantic chip colors now use shared design tokens across the interface. You can rely on status and priority chips using the same color definitions in the queue, board, and ticket detail views.

### What's Changed

- Version 1.9.0 brings the M9 frontend redesign together with updates to ticket workflows, assistant responses, and interface styling.

### Bug Fixes

- **Board card titles:** Long board card titles now wrap and are clamped to two lines with an ellipsis. You can scan board lanes without long titles growing cards without limit.
- **Assistant composer layout:** The assistant’s send button now sits inside the composer panel, with the input and button aligned at narrow as well as wide widths. You can rely on the composer controls staying within the panel.
- **Ticket queue headers:** The Category header now appears beside Due without overlapping it, and uses the same uppercase styling as the other headers. You can read the queue’s column labels and match them to their cells.
- **Assistant change confirmations:** The assistant now follows explicit rules for reporting changes and asking for confirmation. You can rely on it to claim a change only after a successful tool result, and to make requested changes without asking again unless a genuine decision or missing information requires clarification.
- **Summary timestamps:** Ticket summary timestamps now use the configured user timezone. You can rely on the summary’s times matching the timezone used for the ticket detail view.
- **Knowledge-base search errors:** A failed knowledge-base search now reports an error instead of appearing as a successful search with no results. You can distinguish a technical failure from the normal unavailable state, and the dashboard’s error rate reflects failed searches.
- **Meaning-based grounding:** Correct paraphrases and translations can now be recognized as grounded against retrieved passages, rather than being judged only by word overlap. When semantic evaluation is unavailable or embedding fails, you can still rely on the existing lexical check to provide a verdict.
