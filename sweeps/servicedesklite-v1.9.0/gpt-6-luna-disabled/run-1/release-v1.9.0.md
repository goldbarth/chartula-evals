---
title: Release 1.9.0
description: Version 1.9.0 brings together the M9 frontend redesign, with changes to ticket workflows, assistant responses, and the shared interface.
publishedAt: 2026-07-14
---

### What's New

- **Inline citation badges:** Citations can now appear as numbered badges beside matching passage titles in assistant answers, with hover and keyboard-focus previews. When a title appears in the answer, its badge number matches the Sources list, and citations without a matching title remain in that list; the answer must quote the passage title verbatim for a badge to be anchored.
- **Suggested ticket actions:** The first actionable suggestion now appears as a button or agent picker in the ticket header, with other suggestions in an overflow menu. For tickets with suggestions, you can run supported actions directly and rely on the same handlers as the manual controls; unmapped suggestions remain non-clickable, and tickets without suggestions keep the existing generic controls.
- **Keyboard command palette:** Press Ctrl+K or Cmd+K on any page to open a command palette with navigation links and ticket search results. You can navigate the results with the arrow keys, open a selection with Enter, and close the palette with Esc, which restores your previous focus.
- **Immediate status updates:** A ticket's status now changes on the board or detail page before the server responds. You can rely on the displayed status being reconciled after success or restored with an error message if the server rejects the change.
- **Inline ticket controls:** Changing a ticket's status or assignee now opens a menu beside the header action instead of a dialog. The ticket stays on its current page, tab, and scroll position, and errors appear in a snackbar.
- **Inline assistant citations:** Assistant answers can show numbered citation badges beside matching passage titles, with source details on hover or keyboard focus. Citations that do not match a title remain in the numbered Sources list, so the source references are still available.
- **Agent roster in assistant replies:** The assistant now has the active agent roster in its instructions for every chat request. When asked to assign a ticket, it can name valid agents and should list them rather than inventing a name or choosing a closest match.
- **Required grounding check:** After knowledge-base passages are retrieved, the assistant now checks grounding before streaming its first answer token, unless it has already checked during that run. You can rely on at least one grounding check after retrieval, though this does not ensure every passage in a long retrieval chain is checked.
- **Consistent design tokens:** The app's colors, spacing, radius, elevation, and semantic chip colors now come from shared design tokens. You can rely on the same token values across the app's styles and theme.

### What's Changed

- **v1.9.0 release:** Version 1.9.0 brings together the M9 frontend redesign and its related assistant and ticket-interface updates.

### Bug Fixes

- **Board card title clamping:** Long board-card titles now stop at two lines and end with an ellipsis. You can rely on titles staying within a bounded card height.
- **Assistant composer layout:** The assistant's send button could sit flush against or beyond the composer panel edge. The composer is now inset within the panel, so its input and button stay aligned at narrow and wide widths.
- **Ticket queue Category header:** The Category header could overlap the Due header in the ticket queue. The headers now sit side by side with aligned columns, and Category is displayed in uppercase.
- **Assistant confirmation policy:** The assistant could claim a ticket change without a successful tool result or ask you to confirm a change you had already requested. It now reports a change only after a tool call succeeds and proceeds with requested changes without asking again, while still asking when a genuine decision or missing information requires it.
- **Summary timestamps:** Ticket summary timestamps could differ from the local times shown in the ticket detail view. Summary timestamps are now converted to the configured user timezone, so you can rely on both views showing times in the same zone.
- **Knowledge-base search errors:** A failed knowledge-base search could be reported as a successful result. Technical failures are now reported as errors, so they are distinguishable from a search that is unavailable by design.
- **Meaning-based grounding scores:** Correct paraphrases and translations could be scored as ungrounded when their wording differed from the source passages. Grounding now uses semantic similarity when available, so you can rely on those answers being assessed by meaning; if embeddings are unavailable or fail, the existing lexical evaluator remains the fallback.
