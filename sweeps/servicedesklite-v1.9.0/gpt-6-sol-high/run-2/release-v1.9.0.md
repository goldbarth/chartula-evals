---
title: Release 1.9.0
description: This release brings ticket and assistant interface changes together with updates to the assistant's grounding and assignment behavior.
publishedAt: 2026-07-14
---

### What's New

- **Citations in Markdown answers:** Numbered citation badges now appear beside passage titles quoted verbatim in assistant Markdown answers, with details on hover or keyboard focus. You can check the source, heading, and snippet beside the passage; citations without a matching title remain in the numbered Sources list.
- **Recommended ticket actions:** On tickets with an actionable suggested step, the first recommendation now appears as a status-change button or agent picker instead of a caption. You can act on it from the ticket header, while the usual controls remain available when there are no suggestions.
- **Keyboard command palette:** Ctrl/Cmd+K now opens a command palette from any page, including when a text field has focus, to find pages and tickets. You can open a result entirely by keyboard, and Esc closes the palette and returns focus to where it was.
- **Immediate status changes:** A ticket's status now changes immediately on the board or detail page instead of waiting for the server response. If a change is rejected, you can count on the previous status being restored and the error code appearing in a notification; rapid board changes reconcile with the server's accepted status.
- **Inline ticket edits:** Changing a ticket's status or assignee now happens from a menu in its header instead of a dialog. You can choose an allowed status, assign an agent, or unassign the ticket while keeping your scroll position and open tab.
- **Citation badges in chat:** When the assistant cites a passage by title in an answer, a numbered badge appears beside it with a preview on hover or keyboard focus. You can check the source, heading, and snippet there; citations without a matching title remain in the numbered Sources list.
- **Agent names in assistant chat:** The assistant can now name active agents when you ask about assigning a ticket, without first attempting an assignment. It is instructed to use only names from the active roster and to list valid agents rather than choose a close match when your requested name is not on it.
- **Grounding check before answers:** Knowledge-base answers now stream only after the assistant has run a grounding check, including in autonomous worker runs. The assistant receives the verdict before responding, though a check in a longer chain is not guaranteed to cover every passage retrieved later.
- **Ticket layout and colors:** Ticket views now share spacing, corner sizes, and the colors used for status and priority chips. You can use the same color cues in the queue, board, and ticket details; board card titles also no longer clip mid-character.

### What's Changed

- **Frontend redesign release:** In v1.9.0, Markdown assistant answers, dark mode, and saved views are available together. You can read formatted answers without raw Markdown markers, and grounding details stay out of the conversation.

### Bug Fixes

- **Board card titles:** Long titles on the ticket board could make cards grow without bound. You can count on a two-line title preview with an ellipsis and cards that keep a consistent height in their lane.
- **Assistant send button:** The assistant's send button could hang over its panel's right edge. You can count on the input and button staying aligned inside the panel at narrow widths, while messages scroll within the panel and the composer stays in place.
- **Ticket queue headers:** The Category header could overlap Due in the ticket queue. You can rely on both columns lining up with their ticket values, while Category remains a non-sortable label.
- **Assistant change confirmations:** When you ask for a ticket change, the assistant is now instructed not to report success before the action succeeds. It is also told to proceed without another confirmation unless it needs a decision, such as an ambiguous ticket match or missing required information.
- **Ticket summary times:** A ticket summary could show UTC times that differed from the local timestamps on the ticket detail page. You can now compare created, due, comment, and event times with the ticket detail view in your timezone, including the offset on due dates.
- **Knowledge-base search errors:** A failed knowledge-base search could look like a successful search or an unavailable service. You can now tell a technical failure from an unavailable search, and the dashboard's error rate includes those failures.
- **Meaning-based grounding checks:** A correct paraphrase or translation of a knowledge-base passage could be marked ungrounded because it used different words. With embeddings available, the assistant's check can recognize it by meaning; without them or if they fail, the check falls back to word matching.
