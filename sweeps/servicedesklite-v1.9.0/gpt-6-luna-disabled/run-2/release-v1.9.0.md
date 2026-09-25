---
title: Release 1.9.0
description: This release brings the M9 frontend redesign together with updates to ticket workflows and assistant behavior.
publishedAt: 2026-07-14
---

### What's New

- **Inline citation badges:** Cited passage titles in assistant answers can now show numbered badges with a hover or keyboard-focus preview. This applies when a citation’s title appears in the answer, so you can match the badge number to the Sources list and rely on citations that do not appear in the answer remaining in that list. The title must be quoted verbatim for a badge to be anchored.
- **Suggested ticket actions:** The first suggested next step now appears as a primary button or assignee picker when it maps to an action. This applies to tickets with an actionable suggestion, so you can run that step directly from the ticket header; unmapped suggestions remain non-clickable, and tickets without suggestions keep the existing generic controls.
- **Command palette:** Press Ctrl+K or Cmd+K to open a command palette from any page and search navigation targets and tickets. You can use the arrow keys and Enter to choose a result, and Esc to close the palette and return focus to where you were.
- **Immediate status updates:** A ticket’s status now changes on the board or detail view before the server responds. This applies when changing status, so you can see the requested status immediately and rely on rejected changes being restored with an explanation.
- **Inline ticket actions:** Status and assignee choices now open in popovers in the ticket header instead of dialogs. This applies when changing a ticket’s status or assignee, so the ticket stays on its current page, tab, and scroll position while the change is applied.
- **Inline assistant citations:** Citations in assistant answers can now appear as numbered badges beside matching passage titles, with source details available on hover or keyboard focus. When a title is not matched, its citation remains in the numbered Sources list, so citations are still available; answers without citations remain unchanged.
- **Agent roster in assistant:** The assistant can now name the active agents when asked to assign a ticket. This applies to each chat request, so you can rely on the assistant to use roster names and list the valid agents when your requested name is not on the roster.
- **Grounding checks:** After retrieving knowledge-base passages, the assistant now performs a grounding check before it streams its answer, unless it has already checked during that run. You can rely on at least one check after retrieval in both chat and worker runs, though the check does not guarantee that every passage retrieved in a longer run was grounded.
- **Consistent design tokens:** Colors, spacing, corner radii, elevation, and semantic chip colors now follow shared design tokens across the interface. You can rely on those styles using the same token values across the app, and KPI cards now use tone names such as Info or Critical instead of color names.

### What's Changed

- **v1.9.0 release:** This release brings the M9 frontend redesign together in a single release, including Markdown assistant answers, inline citations, and interface updates across ticket workflows.

### Bug Fixes

- **Board card titles:** Long board card titles now stop at two lines with an ellipsis instead of growing without bound. You can rely on cards keeping a bounded height when a title is long.
- **Assistant composer layout:** The assistant composer’s send button no longer sits flush against or beyond the panel edge. The input and button stay aligned inside the panel, including at narrow widths.
- **Ticket queue headers:** The Category header no longer overlaps Due in the ticket queue. You can read the headers side by side and rely on Category and Due staying aligned with their columns.
- **Assistant change confirmations:** The assistant no longer asks for confirmation after you have already requested a change, including after correcting an earlier mistake. You can rely on it to report a change only after a tool call succeeds; it still asks when a genuine decision is needed, such as an ambiguous ticket match or missing required information.
- **Summary timestamps:** Ticket summary timestamps now use the configured user timezone instead of UTC. This applies to creation, due dates, comments, and events, so you can rely on the summary times matching the timezone used in the ticket detail view.
- **Knowledge-base search errors:** A failed knowledge-base search is now reported as an error rather than a successful search result. This applies to technical failures, so you can distinguish them from searches that are unavailable by design.
- **Grounding by meaning:** Correct paraphrases and translations can now be recognized as grounded in retrieved passages. This applies when an embedding service is available, so you can rely on meaning-based checks; if embeddings are unavailable or fail, the existing lexical check is used instead.
