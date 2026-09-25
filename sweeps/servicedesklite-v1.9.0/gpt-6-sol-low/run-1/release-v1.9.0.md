---
title: Release 1.9.0
description: This release brings together interface changes and updates to how the assistant handles citations, grounding, and ticket information.
publishedAt: 2026-07-14
---

### What's New

- **Citations in Markdown answers:** Citation badges now appear beside cited titles in the assistant’s Markdown answers, with a preview on hover or keyboard focus. Their numbers match the Sources list, and citations without a matching title remain in that list.
- **Suggested ticket actions:** The first actionable suggestion on a ticket now appears as a control you can use, while other suggestions remain in a menu. The usual ticket controls stay available, and tickets without suggestions show no empty button.
- **Command palette:** Press Ctrl+K or Cmd+K on any page to open a palette for navigation and ticket search. You can use the arrow keys and Enter to open a result, or press Esc to close it and return focus to where you were.
- **Ticket status changes:** A status change now appears immediately on the board or ticket detail page while the server responds. If the change is rejected, the previous status returns and a notification shows the error code.
- **Inline ticket edits:** Changing a ticket’s status or assignee now happens from menus in the ticket header instead of dialogs. The ticket stays open on the same tab and at the same scroll position while you make the change.
- **Assistant citation badges:** Citations can now appear beside matching titles in the assistant’s answer, with source details shown on hover or keyboard focus. Citations that cannot be placed in the answer remain available in the numbered Sources list.
- **Agent names in assistant chat:** The assistant now receives the active agent roster in each chat request. It is instructed to use only those names and to list valid agents when a requested name is not on the roster.
- **Grounding checks:** The assistant now requires a grounding check after retrieving knowledge-base passages, before it starts streaming an answer. You can count on at least one check after retrieval, though this does not guarantee that every passage retrieved later in a long exchange is checked.
- **Consistent interface styling:** Spacing, corners, colors, and status and priority chips now use a shared design scale across the interface. You can count on the same chip styling in the queue, board, and ticket detail views.

### What's Changed

- **Frontend redesign release:** The frontend redesign changes are now combined in one release, including Markdown assistant answers and a dark-mode toggle. You can count on those changes being available together in v1.9.0.

### Bug Fixes

- **Board card titles:** Long ticket titles on board cards could make a card grow without bound. Titles now stop at two lines with an ellipsis, so cards keep a bounded height.
- **Assistant send button:** The assistant’s send button sat against the edge of its panel. It now stays inside the panel, with the input and button aligned even at narrow widths.
- **Ticket queue headers:** The Category header could overlap Due in the ticket queue. Both headers now sit side by side, with their columns aligned to the ticket rows.
- **Assistant change confirmations:** The assistant now receives instructions not to claim a change succeeded without a successful result, or ask you to confirm a change you already requested without a genuine decision to resolve. This is a prompt policy, so its effect depends on the model following those instructions.
- **Ticket summary times:** Times in a ticket summary could differ from the local times shown in the ticket view. Summary timestamps now use the configured user time zone, so they match the ticket detail view.
- **Knowledge-base search failures:** A failed knowledge-base search could appear as a successful search. Failures are now reported as errors, so the dashboard’s error rate can reflect them separately from an unavailable search.
- **Grounding by meaning:** Grounding checks now compare an answer’s meaning with retrieved passages rather than relying only on shared words. Correct paraphrases and translations can be recognized as supported; when the semantic check is unavailable, the word-based check remains the fallback.
