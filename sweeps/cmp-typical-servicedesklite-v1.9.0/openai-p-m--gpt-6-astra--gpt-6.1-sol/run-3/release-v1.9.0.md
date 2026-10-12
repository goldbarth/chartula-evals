---
title: Release 1.9.0
description: This release brings together the frontend redesign and assistant hardening, with in-place ticket actions, keyboard navigation, source citations, and changes to how the assistant checks and reports its answers.
publishedAt: 2026-07-14
---

### What's New

- **Citations in Markdown:** Inline citation badges now appear in formatted assistant answers when the model quotes a passage title verbatim, with source previews on hover or keyboard focus. Badge numbers match the Sources list, where citations remain available even when their titles do not appear in the answer.
- **Suggested ticket actions:** The ticket header now presents an actionable suggested next step as its primary control, with remaining suggestions in an overflow menu. You can carry out suggested status changes or assignments there while the existing manual controls remain available; suggestions without an action stay non-clickable.
- **Command palette:** You can now find pages and search tickets from any page using a keyboard-operated command palette, including while typing in a text field. Open it with Ctrl/Cmd+K, use arrow keys and Enter to navigate, and press Esc to return focus to where you were.
- **Immediate status updates:** Ticket status changes now appear immediately on the board and ticket detail page, before the server responds. Rejected changes restore the previous state and show an error code, while rapid board changes reconcile with the status accepted by the server.
- **Inline ticket editing:** You can now change a ticket's status or assignee through menus in the ticket header rather than dialogs. Selecting an allowed status, agent, or Unassigned applies the change while preserving your current tab and scroll position.
- **Citation previews:** Assistant chat now places citation badges beside matching passage titles, with source, heading, and snippet previews on hover or keyboard focus. Citations without a matching title remain in the numbered Sources list, and sources are still shown for turns with no answer text.
- **Assistant agent names:** The chat assistant now receives the active agent roster with every request, including an explicit indication when it is empty. When assigning tickets, it is instructed to use exact roster names and list valid agents when a requested name is absent rather than inventing or choosing a similar name.
- **Required grounding check:** The interactive assistant and autonomous worker now check a draft against retrieved knowledge-base passages before streaming an answer. This guarantees at least one check after retrieval, not coverage of every passage retrieved later in a long chain, and the verdict is not displayed to users or on the dashboard.
- **Consistent visual styling:** Spacing, rounded corners, and colors now follow shared scales throughout the interface. Status and priority chips use the same colors across the queue, board, and ticket detail views.

### What's Changed

- **Frontend redesign release:** v1.9.0 brings the complete Frontend Redesign together in one release. Assistant answers retain Markdown formatting, the send button sits inside its panel, and grounding indicators are kept out of the conversation transcript.

### Bug Fixes

- **Board title layout:** Long ticket titles could expand board cards without bound in older Chrome versions. Titles now stop at two lines with an ellipsis, keeping card heights consistent and preventing unbroken titles from stretching lane columns.
- **Assistant composer layout:** The assistant's send button could hang over the edge of its panel. The input and button now stay aligned inside the panel at narrow widths, with messages scrolling internally while the composer stays pinned.
- **Queue column headers:** The Category header in the ticket queue overlapped Due. Headers and their column contents now remain aligned in both themes, with CATEGORY styled like neighboring headers while remaining a non-sortable label.
- **Assistant change confirmations:** The chat assistant could claim a requested change without executing it or ask again after the user had already requested it. It is now instructed to report completion only after a successful tool result in the conversation and to ask for confirmation only when a genuine user decision remains.
- **Summary timestamps:** Ticket summaries could show UTC times that contradicted the local times in ticket details. Summaries now receive created, due, comment, and event timestamps in the same user timezone as chat, including the UTC offset, so their times match the ticket detail view.
- **Knowledge-base search failures:** Technical knowledge-base search failures were reported as successful calls, understating dashboard errors and conflating failures with unavailability. The dashboard now counts those failures as errors, and search results distinguish a technical failure from an unavailable knowledge base.
- **Meaning-based grounding:** Grounding checks could mark correct paraphrases, translations, and hedged answers as unsupported because their words differed from the sources. Checks now assess meaning when Voyage is available, retaining word-overlap scoring as a fallback if no key is present or embedding fails; distinguishing source claims from greetings and other non-claims remains unresolved.
