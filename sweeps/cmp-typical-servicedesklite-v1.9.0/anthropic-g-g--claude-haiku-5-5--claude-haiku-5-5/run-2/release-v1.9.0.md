---
title: Release 1.9.0
description: This release completes the M9 frontend redesign with inline citations, a next-step action button, a command palette, and immediate status updates, alongside assistant hardening for write honesty, grounding and summary timestamps.
publishedAt: 2026-07-14
---

### What's New

- **Inline citation badges:** Answers that cite a source now show a numbered badge right after the cited passage title, so a claim and its source sit together in the text. Hovering or focusing a badge shows the source title, its heading and a snippet, and the same number appears in the Sources list. Citations that never appear in the answer stay in the Sources list only.
- **Next-step action button:** The most likely next step for a ticket is now a button you can click to run it, instead of grey caption text. Other suggested steps sit in an overflow menu, and steps that have no action are shown as plain text. A ticket with no suggestions shows the usual controls and no empty button.
- **Command palette:** Pressing Ctrl+K (Cmd+K on Mac) opens a command palette on any page, even while a text field has focus. It lists the app's navigation pages and matching tickets as you type, and you can move through the results and open one with the keyboard alone. Esc closes it and returns focus to where you were.
- **Immediate status updates:** When you change a ticket's status, the new status appears immediately instead of after the server responds. If the change is rejected, the ticket returns to its previous status and a message shows the reason code. Rapid successive changes to the same ticket always end in a status the server has accepted.
- **Inline status and assignee editing:** Changing a ticket's status or assignee now happens in a menu anchored to the header buttons, not a separate dialog. The ticket stays open at the same scroll position and tab, and the change applies as soon as you pick an option.
- **Inline citations in chat:** In the assistant chat, citations appear as numbered badges where the model referenced a passage, with a hover or keyboard-focus tooltip showing the source, heading and snippet. Citations the model did not place inline are listed below the answer, and answers without citations look as they did before.
- **Agent names known to the assistant:** The assistant now knows the names of the active agents in every chat, so it can name valid assignees without first trying an assignment. It uses only those names and lists the valid ones instead of guessing when a name does not match.
- **Grounding check on every grounded answer:** When the assistant answers from the knowledge base, it now checks the grounding of its answer before the answer streams out, so every grounded answer gets a check rather than depending on the model remembering to ask for one.
- **Consistent design tokens:** Colours, spacing and corner radii across the app now come from one shared set of design tokens, so the same status or priority looks the same on every page. Some spacing and corner values shift by a few pixels to fit the shared scale.

### What's Changed

- **Frontend redesign integration:** Version 1.9.0 integrates the complete frontend redesign milestone into the main branch, so the release is built from a single consistent codebase.

### Bug Fixes

- **Board card titles:** Long ticket titles on the board are now cut off after two lines with an ellipsis, so cards in a column keep a consistent height.
- **Assistant send button placement:** The send button in the assistant composer now sits inside the chat panel, with the input and button aligned at narrow widths too.
- **Ticket queue column headers:** The Category column header in the ticket queue no longer overlaps the Due header, and it appears in uppercase like the other column headers.
- **Assistant write confirmations:** The assistant states a change as made only after the change has actually succeeded in the conversation, and it no longer asks for confirmation again once you have already asked for a change.
- **Summary timestamps:** Timestamps in ticket summaries now use your configured time zone, so a comment written at 12:07 local time no longer appears as 10:07.
- **Knowledge base search failures:** When the knowledge base search fails for a technical reason, it is now reported as an error rather than a successful empty search, so the dashboard's error rate reflects real failures.
- **Meaning-based grounding check:** Grounding is now judged by meaning, so a correct paraphrase, a correct answer in another language, or a hedged answer is no longer marked as ungrounded. If the meaning check is unavailable, the earlier word-matching check is used instead.
