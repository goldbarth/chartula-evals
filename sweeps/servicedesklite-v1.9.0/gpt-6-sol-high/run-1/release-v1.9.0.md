---
title: Release 1.9.0
description: This release brings together ticket and assistant interface changes with updates to how the assistant checks and presents information.
publishedAt: 2026-07-14
---

### What's New

- **Citations in Markdown answers:** When the assistant quotes a passage title in a Markdown answer, a numbered citation badge appears beside it. You can match the badge to its Sources entry and inspect the source, heading, and snippet on hover or keyboard focus; citations without a matching title remain in Sources.
- **Suggested ticket actions:** Tickets with actionable suggestions show the first as a status-change button or assignment picker, with other suggestions in a menu. You can act on that suggestion from the ticket header, while the usual controls remain available.
- **Command palette:** Press Ctrl/Cmd+K on any page to open a palette for navigation and ticket search. You can open a result with the arrow keys and Enter, or close the palette with Esc and return focus to where you were.
- **Ticket status updates:** A status change on the ticket board or detail page now appears before the server responds. You can count on the displayed status being reconciled after a successful change or restored after a rejection, with a message explaining the rejection.
- **Inline ticket edits:** Changing a ticket's status or assignee now opens a menu in the ticket header instead of a dialog. You can make the change without leaving the ticket or losing your scroll position or current tab.
- **Assistant citation previews:** When an assistant answer includes a citation's title, a numbered badge appears beside the cited passage. You can inspect its source, heading, and snippet by hovering or focusing on it, while citations that cannot be placed remain in Sources.
- **Agent names in assistant chat:** When you ask the assistant to assign a ticket, it now has the active agent roster before attempting an assignment. It is instructed to use exact roster names and list valid agents rather than guess when the name you give is not on the roster.
- **Grounding checks before answers:** Knowledge-base answers no longer stream before an initial grounding check after passages have been retrieved. You can count on the model receiving a verdict before the first streamed answer text, though passages retrieved later in a long chain are not guaranteed to be covered.
- **Consistent interface styles:** Spacing, corners, and chip colors now follow shared design scales across the web app. You can rely on the same visual cue for a ticket status or priority as you move between the queue, board, and detail page.

### What's Changed

- **Frontend redesign release:** The v1.9.0 web app displays formatted assistant answers and offers a dark-mode toggle. You can read those answers without grounding details appearing in the transcript, with both interface changes available in this release.

### Bug Fixes

- **Board card titles:** Long ticket titles on the board could grow a card beyond its usual height. You can count on titles ending with an ellipsis after two lines and on long unbroken titles not stretching the lane.
- **Assistant send button:** The assistant's send button could sit over the edge of its panel. You can count on the input and button staying aligned within the panel, including at narrow widths.
- **Ticket queue headers:** In the ticket queue, the Category header could overlap Due and appear in a different case from nearby headers. You can count on the headers and their columns staying aligned, with Category shown in uppercase like its neighbours.
- **Assistant change confirmations:** For a clear ticket-change request, the assistant is now instructed to act without asking for another confirmation. It is also told not to claim a change succeeded without a successful result, and to ask first when the ticket match, required information, intent for a hard-to-reverse action, or a routing suggestion is uncertain.
- **Ticket summary times:** A ticket summary could show comment times in UTC while the ticket page showed local times. You can now compare created, due, comment, and event times in the summary against the ticket page in the same user timezone.
- **Knowledge-base search failures:** A failed knowledge-base search could be recorded as successful. You can count on the dashboard's error rate including technical failures, while an unavailable search remains identified separately.
- **Grounding verdicts:** Correct paraphrases and translations of retrieved passages could be marked ungrounded. Grounding verdicts now consider meaning instead of just shared words when semantic checking is available; otherwise, the earlier word-based check applies.
