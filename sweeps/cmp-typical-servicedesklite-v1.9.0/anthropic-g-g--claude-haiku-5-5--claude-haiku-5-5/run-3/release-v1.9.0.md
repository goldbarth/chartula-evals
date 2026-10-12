---
title: Release 1.9.0
description: This release completes the frontend redesign milestone with inline citations, primary ticket actions and a command palette, and tightens the assistant's grounding and change reporting.
publishedAt: 2026-07-14
---

### What's New

- **Inline citation badges:** Answers now show numbered citation badges placed directly after the passage they support. Hovering or focusing a badge shows the source, its section and a snippet, so you can check each claim without leaving the answer.
- **Primary action from suggested next steps:** The most likely next step for a ticket now appears as a primary button that carries it out. Other suggested steps sit in an overflow menu, and steps that cannot be run directly are shown as plain text. Tickets with no suggestions keep the standard status and assignee controls.
- **Command palette:** Pressing Ctrl+K (Cmd+K on Mac) opens a command palette on any page. It lists navigation targets and matching tickets as you type, and you can move through it entirely by keyboard, with Esc returning focus to where you were.
- **Immediate status updates:** Changing a ticket's status on the board or in the detail view updates immediately, without waiting for the server. If the change is rejected, the ticket returns to its previous status and a message explains why.
- **Inline status and assignee changes:** Changing a ticket's status or assignee no longer opens a dialog. Both are set from a menu on the ticket itself, and the ticket stays open at the same scroll position and tab.
- **Citations in the assistant chat:** Citations in assistant answers appear as inline badges where the answer cites them, with a hover or keyboard-focus tooltip showing the source, heading and snippet. Answers without citations look as they did before.
- **Assistant knows the agent list:** The assistant now knows the list of active agents when it answers, so it can name valid assignees without first trying an assignment that fails. It uses only those names and lists the valid ones when your name does not match.
- **Grounding check always runs:** The assistant now always runs a grounding check on answers drawn from the knowledge base, before the answer is shown. You no longer depend on the model choosing to check.
- **Consistent visual design:** The interface uses one shared set of colours, spacing and corner radii. The status and priority labels look the same wherever they appear, and a dark mode is available.

### What's Changed

- **Frontend redesign release:** This release brings the M9 frontend redesign into the main branch as a single version.

### Bug Fixes

- **Board card titles:** Long ticket titles on the board are cut off after two lines with an ellipsis, so cards in a column keep a consistent height.
- **Assistant send button:** The send button in the assistant's message box sits inside the panel and stays aligned with the input at narrow widths.
- **Ticket list column headers:** The Category column header in the ticket list no longer overlaps the Due header and is shown in uppercase like its neighbours.
- **Assistant change confirmations:** The assistant states that a change was made only after the change has actually been carried out in the conversation, and it no longer asks again for confirmation when you have already asked for the change.
- **Summary timestamps:** Timestamps in the ticket summary are shown in your configured timezone, matching the ticket view, so a comment written at 12:07 local time no longer appears as 10:07.
- **Knowledge-base search failures:** When the knowledge-base search fails, it is reported as an error rather than a successful search, so failures show up in the dashboard's error rate. A knowledge base that is simply unavailable is still reported as unavailable.
- **Grounding check by meaning:** The grounding check now judges whether an answer's meaning matches its sources, so correct paraphrases, answers in another language and appropriately hedged answers are no longer marked as ungrounded. If the semantic check is unavailable, a word-overlap check is used instead.
