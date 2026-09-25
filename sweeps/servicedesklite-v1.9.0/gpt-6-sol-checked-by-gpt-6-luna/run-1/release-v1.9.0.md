---
title: Release 1.9.0
description: This release brings together frontend changes to ticket workflows and assistant answers, alongside changes to assistant grounding and error reporting.
publishedAt: 2026-07-14
---

### What's New

- **Citations in assistant answers:** Citation badges now appear beside cited passage titles in the assistant’s Markdown answers, with a preview on hover or keyboard focus. Badges and the Sources list use matching numbers, and citations whose titles do not appear in the answer remain in the list.
- **Suggested ticket actions:** The first suggested next step on a ticket appears as a button or agent picker when it can be acted on. You can use it to change status or assign an agent, while other suggestions remain available in a menu and the usual controls remain available.
- **Command palette:** You can open a command palette from any page with Ctrl/Cmd+K to find pages and tickets. Arrow keys and Enter let you open a result, and Esc closes the palette and returns focus to where it was.
- **Ticket status changes:** A ticket’s status now updates immediately when you move its card on the board or change it on the ticket page. If the server rejects the change, the previous status returns and a notification shows the error code; rapid changes on one ticket reconcile with the server’s accepted status.
- **Ticket status and assignee:** Changing a ticket’s status or assignee now happens from menus in its header instead of a dialog. The ticket stays open on the same tab and at the same scroll position after you make a selection.
- **Citations in assistant chat:** Citation badges appear beside matching passage titles in assistant answers, with source details available on hover or keyboard focus. Citations without a matching title remain in the numbered Sources list, and answers without citations remain unchanged.
- **Agent names in assistant chat:** The assistant is now given the active agent roster in each chat request. It is instructed to use those names exactly and list valid agents when a requested name is not on the roster, rather than inventing or guessing one.
- **Grounding checks:** Answers based on retrieved knowledge-base passages now receive at least one grounding check before the first answer text is streamed, in both assistant chat and the autonomous worker. You can count on a check after retrieval even when the model does not start one itself; this does not guarantee that every passage retrieved later in a long exchange is checked.
- **Consistent interface styles:** Spacing, corners, colors, and status and priority chips now follow a shared design scale across the web interface. Board card titles also no longer clip midway through a character.

### What's Changed

- **Frontend release:** Version v1.9.0 brings the frontend redesign changes together in one release. The combined interface includes Markdown assistant answers, a dark-mode toggle, and the updated ticket views.

### Bug Fixes

- **Board card titles:** Long ticket titles on the board could make cards grow without a limit. Titles are now limited to two lines with an ellipsis, keeping card height bounded.
- **Assistant send button:** The assistant’s send button could sit against or over the edge of its panel. It now stays inside the panel, aligned with the input even at narrow widths.
- **Ticket queue headers:** The Category header in the ticket queue could overlap Due. The headers now sit side by side, with Category aligned to its column and styled like the neighboring headers.
- **Assistant change confirmations:** The assistant is now instructed not to claim a ticket change succeeded unless the action ran and returned success in the conversation. It is also instructed to act on a change you have already requested without asking again, except when a genuine decision is still needed.
- **Ticket summary times:** Ticket summaries could show timestamps in UTC even when the ticket page showed local time. Created dates, due dates, comments, and events in summaries now use the same user time zone as assistant chat.
- **Knowledge-base search failures:** A failed knowledge-base search could be reported as a successful search. Technical failures are now reported as errors, so the dashboard’s error rate can reflect them while an unavailable search remains distinct.
- **Grounding by meaning:** The grounding check could mark a correct paraphrase or translation as unsupported because it matched words rather than meaning. It now compares the meaning of answer sentences with retrieved passages when embeddings are available, falling back to word matching when they are not; it can still count non-source claims in a whole answer.
