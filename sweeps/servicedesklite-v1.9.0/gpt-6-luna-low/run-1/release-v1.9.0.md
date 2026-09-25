---
title: Release 1.9.0
description: Version 1.9.0 brings the M9 frontend redesign together with updates to ticket workflows and assistant behavior.
publishedAt: 2026-07-14
---

### What's New

- **Inline answer citations:** Cited passages in assistant Markdown answers can now show numbered badges beside their titles, with hover and keyboard-focus previews. When a title does not appear in the answer, its citation remains in the Sources list, so citations stay available and numbered consistently.
- **Suggested ticket actions:** Tickets with suggested actions can show the first actionable suggestion as a button or agent picker, with other suggestions in an overflow menu. You can rely on those controls to run the same ticket actions as the regular controls, which remain available.
- **Command palette:** Press Ctrl+K or Cmd+K on any page to open a command palette with navigation links and ticket search results. You can use the arrow keys, Enter, and Esc to navigate, open a result, and close the palette.
- **Status updates:** A status change now appears immediately on the board and ticket detail page while the server processes it. You can rely on accepted changes being reconciled with the server, and rejected changes restoring the previous status with an explanation.
- **Inline ticket editing:** Status and assignee changes on a ticket can now be made from menus in the header instead of dialogs. The ticket stays on its current page, tab, and scroll position while the change is applied.
- **Inline chat citations:** Assistant chat answers can show numbered citation badges beside matching passage titles, with source details available on hover or keyboard focus. Citations that are not anchored in the answer remain in the numbered Sources list.
- **Agent names for the assistant:** The assistant now receives the active agent roster when handling ticket assignments. You can rely on it to use roster names and list valid agents rather than inventing a name when the requested person is not on the roster.
- **Grounding checks:** After knowledge-base passages are retrieved, the assistant and autonomous worker are required to run a grounding check before answer text streams. The check is required once after retrieval, so you can rely on at least one check without assuming every passage in a longer retrieval chain is checked.
- **Consistent interface styling:** Status and priority chips now use one shared set of colors across the ticket queue, board, and detail page. You can rely on those chips using the same colors in each of those views.

### What's Changed

- **Frontend redesign release:** The M9 frontend redesign is integrated into v1.9.0. The redesign is available together in this release.

### Bug Fixes

- **Board card titles:** Long ticket titles on the board now end after two lines with an ellipsis. You can rely on long titles staying within a bounded card height.
- **Assistant composer layout:** The assistant composer’s send button now sits inside its panel, including at narrow widths. The input and button stay aligned in the same row.
- **Ticket queue headers:** The Category header in the ticket queue no longer overlaps Due and now appears in uppercase beside it. You can rely on the Category header and its column staying aligned with the table body.
- **Assistant confirmations:** The assistant no longer reports a change as complete unless a tool call succeeds, and it does not ask again when you have already requested a change. You can rely on it to ask for confirmation only when a decision is genuinely needed, such as an ambiguous ticket match or uncertain intent for a hard-to-reverse action.
- **Summary timestamps:** Timestamps in ticket summaries now use the configured user timezone. You can rely on summary times matching the timezone used in the ticket detail view.
- **Knowledge-base search errors:** A failed knowledge-base search is now reported as an error, distinct from a search that is unavailable. You can rely on technical failures being counted as errors rather than as healthy search results.
- **Grounding by meaning:** Grounding checks now compare the meaning of answer sentences with retrieved passages, so paraphrases and translations can be recognized as supported. If an embedding is unavailable or fails, the check falls back to lexical scoring.
