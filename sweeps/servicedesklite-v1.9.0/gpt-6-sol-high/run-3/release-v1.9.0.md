---
title: Release 1.9.0
description: This release brings ticket and assistant interface changes together with updates to how assistant answers are sourced and ticket changes are handled.
publishedAt: 2026-07-14
---

### What's New

- **Markdown citations:** In the assistant’s Markdown answers, numbered badges appear after matching passage titles and show a source preview on hover or focus. You can trace each badge to its matching Sources entry and still find citations whose titles do not appear in the answer.
- **Ticket recommendations:** The first actionable recommendation on a ticket appears as a status button or an agent picker, with other suggestions in a menu. You can act on it while the usual ticket controls remain available, even when there are no suggestions.
- **Quick navigation:** Press Ctrl/Cmd+K on any page to open a command palette for page navigation and ticket search. You can open a result with the arrow keys and Enter, then close the palette with Esc and return focus to where you were.
- **Immediate status changes:** When you move a ticket on the board or change its status on the detail page, its status updates before the server responds. Accepted board moves reflect the server’s status; if a change is rejected, the previous status returns with an error code.
- **In-place ticket editing:** You can now change a ticket’s status or assignee from menus in its header instead of opening a dialog. The ticket stays on its current tab at the same scroll position while the change is applied.
- **Answer source previews:** The assistant now places numbered citation badges alongside matching titles in its answers, with the source, heading, and snippet shown on hover or keyboard focus. Citations without a matching title remain in the Sources list, so you can still locate them.
- **Agent names in assignments:** When you ask the assistant to assign a ticket, it can refer to the active agent roster without first making a failed assignment attempt. It is told to use only those names and to list valid agents when the name you give is missing.
- **Knowledge-base answer checks:** When the assistant or autonomous worker retrieves knowledge-base passages, it checks a draft against them before answer text streams unless it has already checked. You can count on at least one check after retrieval, but not necessarily on every passage retrieved later in the same run.
- **Consistent visual cues:** Status and priority chips now use the same colors in the ticket queue, board, and detail view. You can recognize a ticket’s status or priority by the same color cue as you move between those views.

### What's Changed

- **Frontend redesign release:** The complete frontend redesign is available together in version 1.9.0. You can read Markdown-rendered assistant answers while using the dark-mode toggle in the same release.

### Bug Fixes

- **Board card titles:** A long ticket title on the board could grow beyond two lines and stretch its card. You can now see its first two lines with an ellipsis while the card stays a bounded height.
- **Assistant send control:** The send button could sit against the assistant chat panel’s edge or hang beyond it. You can count on the input and button staying aligned inside the panel, including at narrow widths.
- **Ticket queue columns:** In the ticket queue, the Category heading could overlap Due. You can now read them as separate headings with their values aligned beneath them.
- **Ticket change confirmations:** A clear request to change a ticket could lead to another confirmation question instead of an action. The assistant is now told to act without re-asking and to report completion only after a successful result, while still asking when a decision is genuinely uncertain.
- **Ticket summary times:** Times in ticket summaries could show UTC instead of the local times displayed beside them in the ticket view. Summaries now use the user’s timezone for created dates, due dates, comments, and events, so you can compare those times with the ticket detail view.
- **Knowledge-base search errors:** A failed knowledge-base search could look like a successful one. You can now distinguish a failure from an unavailable knowledge base, and the dashboard counts technical failures in its error rate.
- **Grounding by meaning:** Correct paraphrases or translations of knowledge-base passages could be flagged as unsupported when they used different words. When meaning-based scoring is available, they can be recognized as supported; otherwise, the existing word-matching check still provides a verdict.
