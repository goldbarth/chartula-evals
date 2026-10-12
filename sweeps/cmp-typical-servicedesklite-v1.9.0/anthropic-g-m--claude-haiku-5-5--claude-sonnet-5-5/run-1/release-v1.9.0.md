---
title: Release 1.9.0
description: This release completes the Frontend Redesign milestone, adding inline citations, status and assignee controls, a command palette, and a set of assistant reliability fixes.
publishedAt: 2026-07-14
---

### What's New

- **Inline citation badges:** Answers that cite a source can now show a numbered badge right after the cited passage title, with the source, heading and a snippet in a hover or focus tooltip. The sources list uses the same numbers, so you can match a badge to its entry directly.
- **Suggested next step as a button:** The most likely next step for a ticket now appears as a primary button that carries out the action when clicked. Other suggested steps sit behind an overflow menu, and steps that cannot be run from the header are shown as text only.
- **Command palette on Ctrl+K:** Pressing Ctrl+K (Cmd+K on macOS) opens a command palette from any page. It lists the navigation destinations and matches tickets as you type, and you can move through the results and open one using only the keyboard.
- **Immediate status updates:** A status change on the ticket board or detail view now shows immediately. If the server rejects the change, the ticket returns to its previous status and a message gives the reason code.
- **Status and assignee changes in place:** Changing a ticket's status or assignee is done from a menu in the ticket header. The ticket stays open and keeps its scroll position and current tab, so you no longer get pulled into a separate dialog.
- **Citations in assistant answers:** Assistant answers now show citations as badges placed where the answer uses them, and hovering or focusing a badge shows the source, heading and snippet. Citations the answer does not reference are listed below it, and answers without citations look as before.
- **Agent names known to the assistant:** The assistant now knows the names of the active agents when it answers, so it can name valid agents directly. If a requested name is not on the roster, it lists the valid names rather than guessing a close match.
- **Grounding check always runs:** When the assistant has retrieved knowledge-base passages, it now checks its answer against them before responding, so the check no longer depends on the model choosing to run it.
- **Consistent visual styling:** The interface uses one set of colours, spacing and corner radii across all pages, and the status and priority tags look the same wherever they appear.

### What's Changed

- **Frontend Redesign release:** The release v1.9.0 brings the Frontend Redesign milestone into the main branch.

### Bug Fixes

- **Board card titles clipped:** Long ticket titles on the board are now cut off after two lines with an ellipsis, so cards in a column keep a consistent height.
- **Assistant send button placement:** The send button in the assistant's message box now stays inside the panel, and the text field and button stay aligned at narrow widths.
- **Ticket queue column header:** The Category column in the ticket queue no longer overlaps the Due column, and its header matches the other column headers in uppercase.
- **Assistant change confirmations:** The assistant no longer states that a change was made unless the change was actually carried out and reported as successful, and it makes a requested change without asking again.
- **Summary timestamps in your timezone:** Timestamps in the streamed ticket summary now match the times shown in the ticket detail view in your timezone.
- **Failed knowledge-base searches reported:** A failed knowledge-base search is now reported as an error, distinct from a search that found nothing, so the dashboard's error rate reflects real failures.
- **Grounding check by meaning:** The grounding check now compares the meaning of answer sentences with the retrieved passages, so a correct paraphrase or a translation is no longer marked as ungrounded.
