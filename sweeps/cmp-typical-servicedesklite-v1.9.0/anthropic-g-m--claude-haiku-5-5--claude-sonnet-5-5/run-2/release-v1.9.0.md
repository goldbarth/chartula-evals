---
title: Release 1.9.0
description: This release completes the frontend redesign, adding inline citations, direct action buttons, a command palette, immediate status updates and a shared design system, alongside assistant hardening fixes.
publishedAt: 2026-07-14
---

### What's New

- **Inline citation badges:** Answers in the assistant now show numbered citation badges placed right after the passage title they support. Hovering or focusing a badge shows the source, heading and snippet, and the sources list shares the same numbers, so you no longer have to match a claim to its source by hand.
- **Next-step action button:** The most likely next step for a ticket is now a button in the ticket header that runs it directly, such as changing the status or assigning an owner. Other suggested steps are in an overflow menu, and steps that cannot be run appear as plain text, so you can act on a suggestion without leaving the ticket.
- **Command palette:** Ctrl+K (Cmd+K on macOS) opens a command palette from any page, even while typing in a text field. It lists navigation targets and matching tickets as you type, and you can move through the results and open one using only the keyboard.
- **Immediate status updates:** A status change on the board or in the ticket detail view appears immediately, without waiting for the server. If the change is rejected, the ticket returns to its previous status and a message shows the reason code, so the screen always reflects what the server holds.
- **Inline status and assignee changes:** Changing a ticket's status or assignee happens in a small menu next to the header action instead of a separate dialog. The ticket stays open at the same scroll position and tab, so you do not lose your place.
- **Assistant citations:** Citations in the assistant's answers are linked to the passages they support, and a sources list appears under the answer for any citation not placed inline. Hovering a citation shows its source, heading and snippet, and answers without citations look as they did before.
- **Agent names in the assistant:** The assistant now knows the names of the active agents in every chat, so it can name valid agents when assigning a ticket without first trying a failed assignment. If a name you give is not on the roster, it lists the valid names instead of guessing.
- **Grounding check enforced:** The assistant now checks its own answers against the knowledge base whenever it has retrieved passages, before the answer streams to you. You get a verified answer in every such case, not one that depends on whether the model chose to check.
- **Consistent design tokens:** Colors, spacing and corner radii across the interface now come from one shared set of design tokens, so the screens look consistent with each other. Status and priority chips also match across the queue, board and ticket detail views.

### What's Changed

- **Category header in the queue:** The ticket queue's Category column header no longer overlaps the Due header, and it is uppercase like the other column headers.

### Bug Fixes

- **Board card titles:** Long ticket titles on the board are cut off after two lines with an ellipsis, so cards in a column keep a consistent height.
- **Assistant send button:** The send button in the assistant's message box now sits inside the panel, with the input and button aligned at narrow widths.
- **Queue column headers:** The Category column no longer overlaps the Due column in the ticket queue, and its header matches the other column headers.
- **Assistant change reporting:** The assistant no longer claims a change was made unless it actually made the change and received a successful result. It also no longer asks you to confirm a change you have already requested.
- **Summary timestamps:** Timestamps in the streamed ticket summary now use your configured timezone, so the times match those shown next to the summary.
- **Knowledge-base search errors:** A failed knowledge-base search is now reported as an error, distinct from a search that found nothing or was unavailable, so the dashboard's error rate reflects real failures.
- **Grounding check by meaning:** The grounding check now recognizes correct answers that are paraphrased or written in another language than the source, instead of marking them as ungrounded because the words differ.
