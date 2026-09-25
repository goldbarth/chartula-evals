---
title: Release 1.9.0
description: This release brings the redesigned web experience together with changes to ticket workflows and assistant responses.
publishedAt: 2026-07-14
---

### What's New

- **Inline citation badges:** Assistant answers now show numbered citation badges beside matching passage titles, with source details available on hover or keyboard focus. If a passage title is not in the answer, its citation remains in the Sources list, so the cited material is still available.
- **Suggested ticket actions:** For tickets with suggestions, the first actionable suggestion appears as the primary button or owner picker, with other suggestions in an overflow menu. Choosing it runs the suggested ticket action, while unmapped suggestions stay non-clickable and tickets without suggestions keep the existing generic controls.
- **Command palette:** Pressing Ctrl/Cmd+K opens a command palette on any page, where you can search navigation destinations and tickets and use arrow keys, Enter, and Esc. You can go straight to a page or ticket from the palette without switching to separate navigation or search controls.
- **Immediate status updates:** On the board, a dragged ticket changes columns immediately, and on a ticket detail page the selected status updates immediately. If the server rejects a change, the previous status is restored and the reason appears in a snackbar; rapid board changes do not leave a ticket showing a status the server did not accept.
- **Inline ticket editing:** The Change Status and Assign/Reassign controls now open menus on ticket details, so you can make either change without a modal or leaving the page. The ticket stays on its current tab and scroll position while the change is applied, and errors appear in a snackbar.
- **Inline citation previews:** Cited titles in assistant replies now have numbered badges beside them, and hovering or using keyboard focus shows the source, heading, and snippet. Citations that cannot be matched to the reply stay in the numbered Sources list, so the references remain available.
- **Agent roster awareness:** When you ask the assistant to assign a ticket, it can identify agents on the active roster rather than guessing names. If the person you name is not on the roster, it lists valid agents instead of choosing a close match.
- **Answer support checks:** After the assistant retrieves knowledge-base passages, it now checks its draft against them before streaming an answer, unless it has already made that check during the run. This means a retrieval run gets at least one support check, but later passages in a long run are not guaranteed to be checked.
- **Shared visual styling:** Colors, spacing, and corner radii across the web app now follow shared scales, including consistent status and priority chip colors in the queue, board, and ticket detail views. You can identify a status or priority by the same chip colors in each view.

### What's Changed

- **M9 frontend redesign:** The complete M9 frontend redesign is included in v1.9.0. You can get the milestone's frontend changes together in one release.

### Bug Fixes

- **Board title wrapping:** Long ticket titles on the board now wrap to a maximum of two lines and show an ellipsis when they continue. This keeps card height bounded for long titles.
- **Assistant composer layout:** The assistant composer and send button now sit within the chat panel, with the input and button aligned at narrow widths. Messages scroll within the panel while the composer stays pinned.
- **Ticket queue headers:** In the ticket queue, Category now appears as an uppercase header beside Due instead of running into it. The Category heading stays aligned with its column and remains a label rather than a sort control.
- **Assistant action confirmations:** For clear ticket-change requests, the assistant proceeds without asking again and reports a change only after it receives a successful result. You can rely on its success claims as confirmation that the action completed; it may still ask when the ticket match or required information is unclear or intent is uncertain.
- **Summary timestamps:** Ticket summaries now show creation, due, comment, and event times in the configured user timezone, matching ticket details. You can compare summary timestamps with ticket details without a timezone mismatch.
- **Knowledge search errors:** When a knowledge-base search hits a technical failure, it is now reported as an error rather than a successful search; an unavailable search remains a separate outcome. The dashboard's error rate now reflects technical search failures.
- **Meaning-based support checks:** When the assistant checks an answer against knowledge-base passages, it can now recognize a correct paraphrase or translation as supported even when the wording differs. If meaning-based comparison is unavailable or fails, it uses the existing word-overlap check instead, so a verdict can still be returned.
