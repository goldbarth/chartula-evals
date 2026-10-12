---
title: Release 1.9.0
description: This release brings together the frontend redesign with changes to ticket interactions, assistant citations, and checks on assistant answers.
publishedAt: 2026-07-14
---

### What's New

- **Citations in Markdown answers:** You can now see numbered citation badges beside cited passage titles in Markdown answers when the assistant quotes the title verbatim. Badge numbers match the Sources list, and citations without a matching title remain in that list so you can still find their evidence.
- **Suggested ticket actions:** You can now act on the first actionable suggestion from the ticket header, with remaining suggestions in the overflow menu. Status changes and assignments use the same actions as the manual controls, which remain available when suggestions are absent or cannot be acted on.
- **Keyboard navigation and search:** You can now open a command palette from any page with Ctrl/Cmd+K to find pages and tickets. Arrow keys and Enter let you navigate the results, while Esc closes the palette and returns focus to where you were.
- **Immediate status updates:** Ticket status changes now appear immediately on the board and detail page rather than waiting for the server response. You can count on rejected changes restoring the previous state with an error code explaining why, and rapid board changes reconciling with the status accepted by the server.
- **Inline ticket editing:** You can now change status or assignee through menus in the ticket header instead of dialogs. Your ticket stays open on the same tab and at the same scroll position while the change is applied.
- **Citation previews:** You can now hover over or focus numbered citation badges in assistant answers to see the source, heading, and snippet when a citation title matches the answer text. Citations without an inline match remain in the numbered Sources list, and even a turn without answer text retains its sources.
- **Assistant agent names:** The assistant could invent an agent name when asked to assign a ticket. Each chat request now gives it the active roster and instructs it to use those exact names or list valid agents when the requested name is absent, rather than choose the closest match.
- **Knowledge-base answer checks:** Answers based on retrieved knowledge-base passages now receive a grounding check before streaming begins, in both assistant chat and the autonomous worker. You can count on at least one check after retrieval, but not on every passage retrieved later in a long sequence being checked before the final answer.
- **Consistent interface styling:** Spacing, corner shapes, and colors now follow a shared scale across the interface. Status and priority chips use the same colors in the queue, board, and ticket detail views, so their meaning stays consistent between those views.

### What's Changed

- **Frontend redesign release:** The complete Frontend Redesign milestone is now brought together in v1.9.0. The combined release retains Markdown answers, the dark-mode toggle, and grounding information outside the assistant transcript.

### Bug Fixes

- **Long board titles:** Long ticket titles could grow board cards without limit in older Chrome versions. Titles now stop at two lines with an ellipsis, keeping card heights bounded and preventing unbreakable titles from stretching the lane.
- **Assistant message composer:** The assistant send button sat against the panel edge, hanging over its border. The input and button now stay aligned inside the panel at narrow widths, with messages scrolling internally while the composer stays pinned.
- **Ticket queue headers:** The Category header overlapped Due in the ticket queue. Header and body columns now stay aligned in both themes, with CATEGORY styled like the neighboring headers and remaining a static label rather than a sort control.
- **Assistant change confirmations:** The assistant could claim a ticket change without a successful result or ask again for a change you had already requested. Its chat instructions now require a successful tool result before claiming completion and direct it to proceed without repeat confirmation unless there is ambiguity, missing information, doubt about a hard-to-reverse action, or an uncertain routing suggestion.
- **Summary timestamps:** Ticket summaries could show UTC times that contradicted the local timestamps beside them. Created dates, due dates, comments, and events now reach the assistant in the user timezone, so summary times match the ticket detail view and retain the timezone offset.
- **Knowledge-base search failures:** A technical knowledge-base search failure could be reported as a successful invocation. Dashboard error rates now reflect those failures, while search failures and an unavailable knowledge base have distinct results and messages.
- **Grounding by meaning:** Correct paraphrases, translations, and cautious wording could be marked ungrounded because their words did not overlap with the source. When embeddings are available, checks now assess sentence meaning against retrieved passages; without an embedding service or when it fails, checks fall back to word overlap, and sentences that are not source claims can still affect the result.
