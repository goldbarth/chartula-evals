---
title: Release 1.9.0
description: Version 1.9.0 brings the M9 frontend redesign together, with updates to ticket workflows, the assistant, and the interface.
publishedAt: 2026-07-14
---

### What's New

- **Inline citation badges:** Citations can now appear as numbered badges in the assistant’s Markdown answer. When a citation title appears in the answer, its badge and Sources entry share a number; citations without a matching title remain in the Sources list, so the sources are still available.
- **Suggested ticket actions:** The ticket header can now show the first actionable suggested step as a button or agent picker, with other suggestions in an overflow menu. You can rely on these controls to run the same ticket actions as the manual controls; when there are no suggestions, the existing generic controls remain available.
- **Command palette:** Press Ctrl+K or Cmd+K on any page to open a command palette for navigation and ticket search. You can use the arrow keys and Enter to select a result, and Esc to close the palette and return focus to where you were.
- **Immediate status updates:** A ticket’s status now changes immediately when you move it on the board or update it on the detail page. You can rely on the displayed status being reconciled with the server, or restored to its previous value if the change is rejected, with the reason shown in a notification.
- **Inline ticket controls:** Changing a ticket’s status or assignee now happens from menus in the ticket header instead of a dialog. The ticket stays open on its current tab and scroll position, and any errors appear in a notification.
- **Inline citations in chat:** Citations can now appear as numbered badges alongside the assistant’s answer, with a preview available on hover or keyboard focus. Citations not matched to answer text remain in the numbered Sources list, and answers without citations keep their existing presentation.
- **Agent roster for the assistant:** The assistant can now name the active agents when responding to chat requests. You can rely on it to use names from the roster, or list the valid agents when the requested name is not present.
- **Grounding checks:** After knowledge-base passages are retrieved, the assistant now performs a grounding check before streaming its answer. You can rely on at least one check after retrieval, though this does not ensure that every passage retrieved during a longer chain is checked.
- **Consistent design tokens:** The interface now uses shared design tokens for colors, spacing, radius, elevation, and semantic chip colors. You can rely on these values being shared between the application theme and styles; the KPI card accent now uses a tone such as Info or Critical rather than a color name.

### What's Changed

- **M9 frontend release:** Version 1.9.0 brings the M9 frontend redesign together in one release, including changes to ticket workflows and the assistant experience.

### Bug Fixes

- **Board card titles:** Long board card titles now display at most two lines with an ellipsis. You can rely on titles staying within a bounded card height.
- **Assistant composer layout:** The assistant chat’s send button now sits inside its composer panel, with the input and button aligned at narrow widths. You can rely on the composer remaining contained and aligned across those widths.
- **Ticket queue headers:** The Category header no longer overlaps the Due header in the ticket queue. You can rely on the Category header and its column staying aligned with the table cells.
- **Assistant confirmations:** The assistant no longer claims a change was made unless a tool reports success, and it does not ask for confirmation when you have already requested a change. You can rely on it to ask only when a decision or missing information warrants confirmation.
- **Summary timestamps:** Ticket summary timestamps now appear in the configured user timezone. You can rely on the summary times matching the timezone used for the ticket detail view.
- **Knowledge-base search errors:** A failed knowledge-base search is now reported as an error, distinct from a search that is unavailable. You can rely on the dashboard’s error rate reflecting technical search failures.
- **Meaning-based grounding scores:** Correct paraphrases and translations can now count as grounded when their meaning matches retrieved passages. You can rely on the lexical evaluator as a fallback when an embedding is unavailable or fails; the semantic score is not deterministic.
