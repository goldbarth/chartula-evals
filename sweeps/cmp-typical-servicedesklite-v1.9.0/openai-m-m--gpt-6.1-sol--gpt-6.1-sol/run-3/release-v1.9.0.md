---
title: Release 1.9.0
description: This release brings together the frontend redesign and strengthens the assistant's handling of ticket changes and knowledge-base answers.
publishedAt: 2026-07-14
---

### What's New

- **Citations in Markdown:** Assistant Markdown answers now show numbered citation badges after passage titles when the model quotes those titles verbatim. Badge numbers match the Sources list, hover or keyboard focus shows source details, and citations without a matching title remain in the list.
- **Suggested ticket actions:** The ticket header now offers the first actionable suggestion as a status-change button or an agent picker, with remaining suggestions in an overflow menu. You can act on the recommendation while the usual Change Status, Assign and Edit controls remain available; advisory suggestions stay non-clickable.
- **Command palette:** You can now search for tickets and navigate between pages using a command palette available on every page, including while a text field has focus. Press Ctrl/Cmd+K to open it, use arrows and Enter to select a result, and press Esc to close it and return focus to where you were.
- **Immediate status changes:** Status changes previously waited for the server, and dragged board cards snapped back while waiting; the board and ticket detail now display the change immediately. You can count on rejected changes restoring the previous state with an error code, and rapid board changes reconciling with the status accepted by the server.
- **Inline ticket editing:** You can now change a ticket's status or assignee through menus in the ticket header instead of dialogs. The ticket stays open on its current tab and at its current scroll position while your selection is applied.
- **Citation previews:** Assistant chat answers now show inline citation badges where citation titles match the answer text, with source, heading and snippet previews on hover or keyboard focus. Citations that are not anchored in the answer remain available in the numbered Sources list, including turns without answer text.
- **Assistant agent names:** When asked to assign a ticket, the assistant could invent an agent name rather than use the active roster. It now receives the roster with every chat request and is instructed to use exact names and list valid agents when the requested name is absent, rather than choose a close match.
- **Required grounding check:** Knowledge-base answers could stream without a grounding check in assistant chat or the autonomous worker. A check now runs before answer streaming after passages are retrieved, but it runs only once and does not guarantee coverage of every passage retrieved later in a long chain.
- **Consistent interface styling:** The interface now uses shared spacing, corner shapes and colors, including matching status and priority chip colors across the queue, board and ticket detail. You can count on the same status and priority having consistent colors in those views.

### What's Changed

- **Frontend redesign release:** The complete Frontend Redesign is now brought together in v1.9.0. The combined release includes Markdown assistant answers, a composer contained within its panel and the dark-mode toggle.

### Bug Fixes

- **Long board titles:** Long ticket titles could make board cards grow without limit in older Chrome. Titles now stop at two lines with an ellipsis, keeping cards at a consistent height and preventing unbreakable titles from stretching a lane.
- **Assistant composer layout:** The assistant's send button sat at the panel border, hanging over it. The input and button now stay aligned inside the panel at narrow widths, while messages scroll internally and the composer stays pinned.
- **Ticket queue headers:** The Category header in the ticket queue overlapped Due, reading as “CategoryUE”. Header and body columns now stay aligned in both themes, and Category matches the neighboring uppercase labels while remaining a non-sortable heading.
- **Assistant change confirmations:** The assistant's policy did not explicitly prohibit claiming an unperformed change or asking again for a change you had already requested. It is now instructed to report a change only after a successful tool result and to ask for confirmation only when a genuine decision remains, such as an ambiguous ticket, missing information or uncertain intent.
- **Summary timestamps:** Ticket summaries showed UTC times that contradicted the local timestamps beside them in ticket detail. Created, due, comment and event timestamps now reach the summary model in the user's timezone with the UTC offset included, matching the ticket detail view.
- **Knowledge-base search failures:** Technical failures in knowledge-base searches were reported as successful invocations, understating the dashboard's error rate. The dashboard now counts those failures as errors, while an unavailable knowledge base remains a distinct result with a different message.
- **Grounding by meaning:** Correct paraphrases, translations and hedged answers could be marked ungrounded because their words did not overlap with the source. Grounding now assesses meaning when embeddings are available and falls back to word overlap when they are not; greetings, follow-up questions and ticket confirmations are still not distinguished from source claims.
