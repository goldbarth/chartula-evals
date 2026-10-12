---
title: Release 1.9.0
description: This release completes the M9 frontend redesign, adding inline citations, direct ticket actions, a command palette and immediate status changes, along with the assistant fixes that came with them.
publishedAt: 2026-07-14
---

### What's New

- **Inline citation badges:** Answers now show numbered citation badges placed right after the passage they support. Hovering or focusing a badge shows the source, heading and snippet, so you can check each claim without leaving the answer.
- **Suggested next step button:** The most likely next step for a ticket now appears as a button you can press directly in the ticket header. Pressing it changes the status or assigns the owner, and the remaining suggested steps are in an overflow menu. When no step can be acted on, the header shows the suggestion as plain text.
- **Command palette:** Ctrl+K (Cmd+K on Mac) opens a command palette on every page, even while a text field has focus. It lists the main navigation pages and matching tickets, and you can move through the results and open one with the keyboard alone.
- **Immediate status changes:** A status change on the ticket board or the ticket detail page shows immediately, before the server replies. If the change is not allowed, the status returns to its previous value and a message gives the reason.
- **Inline status and assignee menus:** Changing a ticket's status or assignee no longer opens a dialog. The status and assignee menus open next to the header buttons, so the ticket stays open at the same scroll position and tab.
- **Citations in the assistant chat:** Citations from the assistant now appear next to the answer text they support, as numbered badges, and hovering or focusing one shows the source, heading and snippet. Citations the answer does not reference inline are still listed below it.
- **Agent names in the assistant:** The assistant now knows the names of the current agents when it answers, so it can name the valid agents directly. When a name you give does not match an agent, it lists the valid names instead of guessing.
- **Grounding check on every answer:** The assistant now checks each knowledge-base-grounded answer for support in the retrieved sources before it finishes. The check runs on every grounded answer, so you no longer depend on the model choosing to run it.
- **Shared design values:** Colours, spacing and corner radius now follow one shared set of design values across the app. The status and priority labels look the same wherever they appear.

### What's Changed

- **Release v1.9.0:** Release v1.9.0 combines the frontend redesign work into the main branch.

### Bug Fixes

- **Board card titles:** Long ticket titles on the board are now cut off after two lines with an ellipsis, so cards in a column keep a consistent height.
- **Assistant send button:** The send button in the assistant composer now sits inside the panel, and the input and button stay aligned when the window is narrow.
- **Ticket queue Category header:** The Category column header in the ticket queue no longer overlaps the Due header and reads in capitals like the other column headers. Category is a static label, not a sort control.
- **Assistant write confirmations:** The assistant no longer claims a change happened unless the change was made and reported as successful in the conversation. When you have already asked for a change, it makes the change without asking you to confirm again.
- **Summary timestamps:** Timestamps in AI ticket summaries are shown in your configured time zone, so they match the times shown in the ticket view.
- **Knowledge-base search errors:** A failed knowledge-base search is now reported as an error, separate from a search where the knowledge base is simply unavailable, so the dashboard error rate reflects real failures.
- **Grounding by meaning:** Grounding checks now recognise answers that restate the sources in other words or in another language. Answers that match the sources in meaning are no longer marked as ungrounded for using different wording.
