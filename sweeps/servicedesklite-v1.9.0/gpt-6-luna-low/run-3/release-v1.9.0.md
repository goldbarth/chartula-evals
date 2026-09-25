---
title: Release 1.9.0
description: This release brings the M9 frontend redesign together with updates to assistant behavior, ticket workflows, and knowledge-base grounding.
publishedAt: 2026-07-14
---

### What's New

- **Inline citation badges:** Citations appear as numbered badges after matching passage titles in the assistant’s sanitized Markdown answer, when a title appears in the answer. The badges and Sources list use the same numbering, and titles that do not appear remain in the list.
- **Suggested ticket actions:** The first actionable suggestion appears as a primary button or agent picker on tickets with actionable suggestions. You can run that suggested action directly, while other suggestions remain available in the overflow menu.
- **Command palette:** Pressing Ctrl/Cmd+K opens a command palette on any page, including when a text field has focus. You can search navigation and tickets, move through results with the arrow keys, open a selection with Enter, and close with Esc.
- **Ticket status updates:** A status change appears immediately on the board and ticket detail page while the server processes it. You can rely on the displayed status being reconciled with the server after success, or restored with an explanation if the change is rejected.
- **Inline ticket controls:** Status and assignee choices open in popovers on the ticket instead of in dialogs. You can make either change without leaving the ticket, and its current tab and scroll position stay in place.
- **Inline citation badges:** Citations appear as numbered badges beside matching titles in the assistant’s answer, when a title appears in the answer. You can view citation details on hover or keyboard focus, and use the numbered Sources list for citations without an inline match.
- **Assistant agent roster:** The assistant’s chat prompt includes the active agent roster for each request. It can name valid agents and, when your requested name is not listed, provide the available names instead of choosing a guessed match.
- **Grounding checks:** After knowledge-base passages are retrieved, the assistant is required to run a grounding check once before streaming its answer, unless it has already checked. You can rely on the answer having had that check after retrieval, though this does not guarantee that every passage retrieved during a longer exchange was checked.
- **Consistent design tokens:** Colors, spacing, radius, elevation, and semantic chip colors across the interface now come from shared design tokens. You can rely on those styles using the same defined values across the app.

### What's Changed

- **v1.9.0 release integration:** The M9 frontend redesign is integrated into the release, alongside assistant and ticket-interface updates. You can use these changes together in v1.9.0.

### Bug Fixes

- **Board card titles:** Long board-card titles are clamped to two lines with an ellipsis. You can scan cards without a long title expanding the card without bound.
- **Assistant composer layout:** The assistant composer’s send button no longer sits flush against or beyond the panel edge. You can use the input and button within the panel while they remain aligned at narrow widths.
- **Ticket queue category header:** The Category header no longer overlaps the Due column and appears in uppercase beside it. You can read the category and due columns with their headers aligned to the table.
- **Assistant change confirmations:** The assistant no longer claims a change succeeded unless a tool reports success, and it does not ask you to confirm a change you already requested. You can rely on its change claims being tied to a successful result in the conversation.
- **Summary timestamps:** Ticket summary timestamps are shown in the configured user timezone. You can compare summary times with the ticket detail view without the UTC wall time appearing in the prompt.
- **Knowledge-base search errors:** A failed knowledge-base search is reported as an error rather than as a successful search. You can distinguish a technical failure from an unavailable search, and the dashboard can count technical failures as errors.
- **Meaning-based grounding:** Grounding checks can recognize supported paraphrases and translations by comparing answer sentences with retrieved passages. When an embedding is unavailable or fails, the check falls back to lexical scoring rather than returning no verdict.
