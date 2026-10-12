---
title: Release 1.9.0
description: This release brings together the frontend redesign and assistant changes focused on source checking, ticket actions, and accurate reporting.
publishedAt: 2026-07-14
---

### What's New

- **Citations in Markdown answers:** You can now see numbered citation badges beside cited passage titles in the assistant’s Markdown answers, with source details on hover or keyboard focus. When the model quotes a passage title verbatim, its badge matches the Sources numbering; citations without a matching title remain in Sources.
- **Suggested ticket actions:** You can now act on the first actionable suggestion directly from the ticket header, with remaining suggestions in an overflow menu. Suggestions can change status or open an agent picker, while the standard ticket controls remain available even when there are no suggestions.
- **Command palette:** You can now open navigation and ticket search from any page with Ctrl/Cmd+K, including while typing in a text field. Use arrow keys and Enter to open a result, or Esc to close the palette and return focus to where you were.
- **Immediate status updates:** Status changes now appear immediately on the board and ticket detail page, before the server responds. Accepted changes reconcile with the server; rejected changes restore the previous state and show an error code, and rapid board moves cannot leave an unaccepted status displayed.
- **Inline ticket editing:** You can now change status or assignee through menus in the ticket header instead of dialogs. Your ticket stays open at the same scroll position and tab, with allowed status changes, the agent roster, and Unassigned available in the menus.
- **Citation previews:** You can now hover over or keyboard-focus inline citation badges in assistant chat to see the source, heading, and snippet. Citations whose titles do not match the answer remain in the numbered Sources list, and sources are still shown for turns without answer text.
- **Assistant agent names:** The chat assistant now receives the active agent roster with every request, including an explicit notice when it is empty. For assignment requests, it is instructed to use exact roster names and list valid agents when a requested name is absent, rather than inventing a name or choosing a close match.
- **Required source checking:** Answers based on retrieved knowledge-base passages now undergo a grounding check before streaming begins, in both interactive chat and the autonomous worker. This guarantees one check after retrieval, not coverage of every passage retrieved later in a long chain, and the verdict is not displayed to users.
- **Consistent visual styling:** Spacing, rounded corners, and colors now follow shared scales throughout the interface. Status and priority chips use the same colors across the queue, board, and ticket detail views, so their appearance stays consistent between those views.

### What's Changed

- **Frontend redesign release:** v1.9.0 brings the complete Frontend Redesign milestone together in one release. The combined assistant page renders Markdown, keeps the send button inside its panel, and leaves grounding information out of the transcript.

### Bug Fixes

- **Board card titles:** Long ticket titles could grow board cards without bound in older Chrome versions. Titles now stop at two lines with an ellipsis, keeping card heights bounded and preventing unbroken titles from stretching lane columns.
- **Assistant composer layout:** The assistant’s send button could hang over the panel edge, and the intended scrolling layout was missing. The input and button now stay aligned inside the panel at narrow widths, while messages scroll internally and the composer stays pinned.
- **Ticket queue headers:** The Category header in the ticket queue overlapped Due. Headers and their column contents now stay aligned in both themes, with Category styled in uppercase like its neighbors and remaining a non-sortable label.
- **Assistant change confirmations:** The assistant had reported changes without executing them and asked for confirmation again after explicit requests. It is now instructed to claim completion only after a successful tool result in the conversation and to ask again only for genuine decisions, such as ambiguous tickets, missing information, uncertain routing, or doubtful intent for hard-to-reverse actions.
- **Summary timestamps:** Ticket summaries could show UTC times that contradicted the local timestamps beside them. Created, due, comment, and event timestamps now use the same user timezone as chat and the ticket detail view, with the UTC offset retained.
- **Knowledge-base search failures:** Technical knowledge-base search failures were counted as successful invocations and were indistinguishable from an unavailable service. The dashboard’s error rate now includes those failures, and failed searches have a distinct result and message from unavailable searches.
- **Meaning-based source checks:** Correct paraphrases and translations could be judged unsupported because grounding checks relied on matching words. When Voyage embeddings are available, checks now assess meaning against retrieved passages; without a key or when embeddings fail, word-overlap checking remains the fallback, and distinguishing source claims from other sentences remains unresolved.
