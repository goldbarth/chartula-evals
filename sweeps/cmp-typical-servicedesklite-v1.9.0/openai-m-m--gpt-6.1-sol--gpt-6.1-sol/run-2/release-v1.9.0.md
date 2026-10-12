---
title: Release 1.9.0
description: This release brings together the frontend redesign and changes to assistant grounding, assignment guidance, and change-confirmation behavior.
publishedAt: 2026-07-14
---

### What's New

- **Citations in Markdown answers:** Assistant Markdown answers now show numbered citation badges after passage titles quoted verbatim by the model, with previews on hover or keyboard focus. Badge numbers match the Sources list, and citations whose titles are absent from the answer remain in that list.
- **Suggested ticket actions:** Tickets with actionable suggestions now show the first suggested step as a primary header control, with remaining steps in an overflow menu. You can act on the recommendation while still using the existing Change Status, Assign, and Edit controls; suggestions without a supported action remain non-clickable.
- **Keyboard command palette:** You can now open a command palette from any page with Ctrl/Cmd+K to find tickets or navigate. Arrow keys and Enter let you select and open results, while Esc closes the palette and restores your previous focus.
- **Immediate status updates:** Status changes now appear immediately on the ticket board and detail page, rather than waiting for the server response. Rejected changes restore the previous state and show an error code, and rapid board changes reconcile with the status accepted by the server.
- **Inline ticket editing:** You can now change a ticket's status or assignee through header menus instead of dialogs. The ticket stays open on its current tab and at its current scroll position while the change is applied.
- **Citation previews:** Assistant chat now shows inline citation badges where citation titles match the answer text, with source, heading, and snippet previews on hover or keyboard focus. Citations without an inline match remain available in the numbered sources list, including turns with no answer text.
- **Assistant agent names:** The assistant could invent an agent name when asked to assign a ticket. Each chat request now supplies the active roster and tells the model to use those exact names, or list valid names when the requested name is absent rather than choose a close match.
- **Required grounding checks:** Knowledge-base answers could stream without a grounding check in assistant chats and autonomous worker runs. A check is now required before the answer starts streaming after retrieval, but this runs once and does not guarantee coverage of every passage retrieved later in a long chain.
- **Consistent interface styling:** The interface now uses a shared spacing, corner, and color scale. Status and priority chips use the same colors across the queue, board, and ticket detail views.

### What's Changed

- **Frontend redesign release:** The complete frontend redesign is now brought together in v1.9.0. The release includes Markdown assistant answers, a send button contained within its panel, and the dark-mode toggle.

### Bug Fixes

- **Long board titles:** Long ticket titles could grow board cards without bound in older Chrome browsers. Titles now stop at two lines with an ellipsis, keeping cards at a consistent height and preventing unbreakable titles from stretching the lane.
- **Assistant composer layout:** The assistant send button sat against the panel border and could hang over it. The input and button now stay aligned inside the panel at narrow widths, with messages scrolling internally and the composer pinned in place.
- **Ticket queue headers:** The Category header in the ticket queue overlapped Due. Header and body columns now stay aligned in both themes, and Category matches the neighboring uppercase labels while remaining a non-sortable heading.
- **Assistant change confirmations:** The assistant's chat policy now addresses claims of changes without successful results and unnecessary repeat confirmations. It tells the model to claim a change only after a successful tool result in the conversation, and to carry out explicit requests without asking again unless ambiguity, missing information, or genuine doubt about intent requires a decision.
- **Summary timestamps:** Ticket summaries showed UTC times that contradicted the local timestamps beside them. Created, due, comment, and event timestamps now reach the model in the user's timezone, with the zone and UTC offset included so summaries can match the ticket detail view.
- **Knowledge-base search failures:** Technical knowledge-base search failures were reported as successful invocations. The dashboard error rate now counts those failures, while an unavailable knowledge base remains a distinct result with a distinct message.
- **Grounding by meaning:** Correct paraphrases and translations could be judged ungrounded because their words differed from the source passages. With embeddings available, checks now assess meaning rather than word overlap; without a Voyage key or if embeddings fail, they fall back to word-overlap scoring, and distinguishing source claims from other sentences remains unresolved.
