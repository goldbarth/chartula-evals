---
title: Release 1.9.0
description: This release brings together the v1.9.0 frontend redesign, with updates to assistant responses, ticket workflows, and the interface.
publishedAt: 2026-07-14
---

### What's New

- **Inline citation badges:** Citations can now appear as numbered badges beside matching passage titles in the assistant’s Markdown answer, with a tooltip showing the title, source, heading, and snippet. The numbered Sources list stays consistent, and citations whose titles do not appear in the answer remain listed there.
- **Suggested ticket actions:** The first suggested step now appears as a primary button or agent picker when it maps to an available action. You can rely on it to run through the same action path as the corresponding manual control; suggestions without an actionable step remain non-clickable, and tickets with no suggestions keep the existing generic controls.
- **Command palette:** Press Ctrl+K or Cmd+K on any page to open a command palette with navigation and ticket search. You can use the arrow keys, Enter, and Esc to navigate, open results, and close the palette, which returns focus to where it was before.
- **Immediate status updates:** A ticket’s status now changes on the board or detail view before the server responds. You can rely on successful changes being reconciled with the server and rejected changes restoring the previous status with an explanatory notification.
- **Inline ticket controls:** Changing a ticket’s status or assignee now opens an inline menu instead of a dialog. The ticket stays on its current page, tab, and scroll position, and the same status and assignment actions remain available.
- **Inline assistant citations:** Matching citation titles in an assistant answer now have numbered badges, with source details available on hover or keyboard focus. Unmatched citations remain in the numbered Sources list, and answers without citations have no empty sources section.
- **Agent roster in assistant replies:** The assistant now receives the active agent roster with each chat request. When assigning a ticket, it can rely on the roster to use valid agent names and list them if the requested name is not present.
- **Grounding checks:** After knowledge-base passages are retrieved, the assistant now runs a grounding check before streaming its first answer token if it has not already checked. This ensures at least one check after retrieval, while leaving the assistant free to respond after that check.
- **Consistent design tokens:** The interface’s colors, spacing, radii, elevation, and semantic chip colors now come from a shared design system. Status and priority chips use the same definitions across the queue, board, and ticket detail views.

### What's Changed

- **v1.9.0 release:** This release brings together the M9 frontend redesign, including assistant Markdown rendering, inline citation badges, keyboard navigation, and ticket workflow controls.

### Bug Fixes

- **Board card titles:** Long board card titles now truncate after two lines with an ellipsis. This keeps cards from growing without bound when a title is long.
- **Assistant composer layout:** The assistant chat’s send button now sits inside its panel, with the input and button aligned at narrow and wide widths. The message area can scroll while the composer stays in place.
- **Ticket queue category header:** The Category header in the ticket queue now appears beside Due without overlapping it, and matches the uppercase style of the other headers. Category remains a static label rather than a sort control.
- **Assistant confirmation policy:** The assistant now makes a requested change without asking for confirmation again, including after correcting an earlier mistake. You can rely on it to report a change only after the tool reports success; it still asks when a genuine decision is needed.
- **Summary timestamps:** Timestamps in ticket summaries now use the configured user timezone. They match the times shown in the ticket detail view.
- **Knowledge-base search errors:** A failed knowledge-base search is now reported as an error, distinct from a search that is unavailable. The dashboard’s error rate reflects technical search failures.
- **Meaning-based grounding checks:** Grounding checks now compare answer sentences with retrieved passages by meaning, so supported paraphrases and translations can be recognized. If semantic scoring is unavailable or embedding fails, the existing lexical check provides the fallback.
