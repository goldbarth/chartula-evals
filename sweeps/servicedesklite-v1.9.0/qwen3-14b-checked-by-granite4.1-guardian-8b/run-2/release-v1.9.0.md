---
title: Release 1.9.0
description: This release completes and integrates the M9 Frontend Redesign and includes significant improvements to the assistant's behavior, usability, and design consistency, alongside several fixes and performance improvements.
publishedAt: 2026-07-14
---

### What's New

- **Anchored citation badges:** Inline citation badges in assistant answers are now anchored to the exact passage they cite, ensuring citations stay with their reference rather than appearing in a separate list. This change allows you to see the source directly in the answer text, and the badge includes a hover tooltip with the source details.
- **Primary action for next steps:** The most likely next step in a ticket is now a primary button instead of a grey caption, making it easier to take action. This change applies to tickets that have suggested next steps, and you no longer need to manually click a separate button to proceed.
- **Command palette shortcut:** You can now use the `Ctrl+K` keyboard shortcut to open a command palette that lets you search and navigate the app from any page. This feature is especially useful for power users who prefer to work with the keyboard.
- **Optimistic status updates:** Status updates in the Kanban board and ticket detail views are now applied optimistically, instantly reflecting the new status without waiting for a server response. If the update fails, the board will revert to the previous state and show the reason for the error.
- **Inline status and assignee changes:** Changing a ticket's status or assigning it now happens inline using tooltip menus, without opening a modal dialog. This keeps you on the same page and avoids disrupting your workflow.
- **Inline citation badges with tooltip:** Citations in assistant answers are now rendered as inline badges with hover tooltips containing the source details, making it easier to reference the supporting information directly within the text.
- **Agent roster in system prompt:** The assistant now has access to the agent roster through the system prompt, ensuring it can only list valid agents and no longer invent names or misrepresent assignments.
- **Grounding check enforcement:** The assistant now enforces a grounding check using the `tool_choice` property, ensuring every answer is verified against its supporting content before being streamed out.
- **Design token system:** A unified design token system introduced a consistent set of spacing, radius, elevation, and color values for the application. This makes the UI look more cohesive and prevents inconsistencies across the app.

### What's Changed

- **Redesign integration:** M9 Frontend Redesign features integrated into `main` to deliver a complete and consistent look and feel with v1.9.0 release notes, and a single point of reference for tagging the release.

### Bug Fixes

- **Clamped board card titles:** The ticket board card title is now correctly limited to two lines with an ellipsis, ensuring a consistent card height and preventing lengthy titles from disrupting the layout.
- **Send button in composer panel:** The send button for the assistant composer is now positioned within the panel, ensuring that it is properly enclosed and aligned with the input field at any screen width.
- **Category header alignment:** The ticket queue now displays the `Category` and `Due` headers correctly side by side without overlapping, and with `Category` rendered in uppercase for consistency.
- **Write-honesty and confirmation policy:** The assistant now follows a write-honesty and confirmation policy in the system prompt, ensuring it only states changes that have been confirmed and avoids unnecessary user confirmations.
- **Timezone-aware summary timestamps:** Summary timestamps in the assistant are now rendered in the user's local timezone, aligning with the displayed ticket details.
- **Error flag on KB search failures:** Failing knowledge base search results are now reported as errors, making it easier to distinguish between failures and unavailable data for monitoring and debugging.
- **Semantic grounding check:** Grounding checks are now evaluated based on semantic similarity rather than word overlap, ensuring correct paraphrases, translations, and hedges are now recognized as grounded.
