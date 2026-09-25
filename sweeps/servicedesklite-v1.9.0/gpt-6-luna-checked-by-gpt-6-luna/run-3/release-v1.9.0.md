---
title: Release 1.9.0
description: This release brings together frontend updates to ticket workflows and assistant features, alongside improvements to assistant grounding and error reporting.
publishedAt: 2026-07-14
---

### What's New

- **Inline citation badges:** Citations can now appear as numbered badges beside cited passage titles in assistant Markdown answers, with hover and keyboard-focus previews. You can rely on the numbered Sources list matching the badges, while citations whose titles do not appear in the answer remain in the list.
- **Suggested ticket actions:** The first suggested ticket step now appears as a primary action in the ticket header, with other steps in an overflow menu. You can rely on suggested actions using the same handlers as manual ticket changes; steps without a mapped action remain non-clickable.
- **Command palette:** Press Ctrl+K or Cmd+K on any page to open a command palette with navigation and ticket search results. You can use the arrow keys and Enter to choose a result, and Esc to close the palette and return focus to where it was.
- **Optimistic status changes:** Board cards and ticket details now show a status change before the server responds. You can rely on rejected changes being rolled back and explained, and on the board reconciling successful changes with the server.
- **Inline ticket controls:** Status and assignee changes now open in popovers on the ticket header instead of dialogs. You can rely on the ticket staying on its current page, tab, and scroll position while changes are applied.
- **Inline assistant citations:** Citations can now appear as numbered badges beside matching titles in assistant answers, with previews on hover or keyboard focus. You can rely on the numbered Sources list as a fallback for citations that are not anchored in the answer.
- **Agent roster in assistant chats:** The assistant chat now identifies the active agent roster when discussing ticket assignments. You can rely on it to use roster names and list valid agents if the requested name is not on the roster.
- **Grounding checks:** After knowledge-base passages are retrieved, the assistant now performs a grounding check before streaming its answer unless it has already checked during that run. You can rely on a check being made at least once after retrieval, but not on every passage in a longer run being checked.
- **Consistent design tokens:** The app’s palette, spacing, radius, elevation, and semantic chip colors now use a shared design scale. You can rely on those styles drawing from the same tokens across the interface.

### What's Changed

- **v1.9.0 release:** The v1.9.0 release brings together the M9 frontend redesign and its related ticket and assistant updates.

### Bug Fixes

- **Board card title wrapping:** Long board-card titles now clamp to two lines with an ellipsis. You can rely on long titles staying within the card layout.
- **Assistant composer layout:** The assistant chat’s send button no longer sits against or beyond the panel’s edge. You can rely on the input and button staying aligned inside the panel, including at narrow widths.
- **Ticket queue Category header:** The Category header no longer overlaps the Due header in the ticket queue. You can rely on the headers and their columns staying aligned.
- **Assistant change confirmations:** The assistant no longer needs to ask again before carrying out a change the user already requested, and it must not claim a change succeeded without a successful tool result. You can rely on it to ask only when a genuine decision or missing information requires confirmation.
- **Summary timestamps:** Ticket summary timestamps now use the configured user timezone. You can rely on the summary times matching the timezone shown in the ticket details.
- **Knowledge-base search failures:** A failed knowledge-base search is now reported as an error, distinct from an unavailable search. You can rely on the dashboard error rate reflecting technical search failures.
- **Meaning-based grounding scores:** Grounding checks now compare answer sentences with retrieved passages by meaning, so supported paraphrases and translations can be recognized. If no Voyage key is available or embedding fails, you can still rely on the lexical evaluator as a fallback.
