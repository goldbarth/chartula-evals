---
title: Release 1.9.0
description: This release introduces a range of improvements including inline citation badges, primary action buttons, a keyboard command palette, optimistic updates, design tokens, and enhanced grounding evaluation, along with several bug fixes and system improvements.
publishedAt: 2026-07-14
---

### What's New

- **Inline citation badges in Markdown answers:** Inline citation badges now appear within the assistant's Markdown answers, ensuring each citation is anchored to the cited passage. This guarantees that every change is preserved even if the connection drops, eliminating the need for a local backup copy while working.
- **Primary action button for next step:** The most likely next action step for a ticket is now displayed as a primary button rather than a grey caption. This makes it more intuitive to take the next action without leaving the current page or opening a new dialog.
- **Command palette on Ctrl+K:** A keyboard-first command palette opens on `Ctrl+K`, accessible from any page. It allows quick navigation or searching for tickets directly from the keyboard, improving efficiency for power users.
- **Optimistic status updates with rollback:** Status changes on the Kanban board are now applied optimistically, with any server-side conflicts rolled back to the previous state. This improves responsiveness, with updates appearing instantly and corrections made automatically if needed.
- **Inline status and assignee edits:** Status and assignee changes are now made inline using popovers, rather than requiring the user to open a dialog. This keeps the ticket open and avoids unnecessary navigation, simplifying the user experience.
- **Inline citation badges with hover preview:** Inline citation badges with hover previews now appear in the assistant's chat, making it easier to see which sources support each claim. The badges appear directly after the passage they refer to, and hovering over them reveals the corresponding source details.
- **Agent roster in system prompt:** The agent roster is now injected into the model's system prompt, ensuring the assistant can correctly reference the valid agents. This prevents the assistant from making up nonexistent agents or picking an incorrect match.
- **Enforce grounding check via tool choice:** The assistant now enforces the grounding check via tool choice before any answer is streamed to the user. This ensures that every verified answer is backed by the relevant knowledge base content, preventing the model from skipping this safety step.
- **Centralized design tokens:** All styling is now controlled by a centralized design token scale that defines spacing, radius, elevation, and semantic color values. This eliminates inconsistent colors, spacing, and design elements across the application.

### What's Changed

- **Integrate M9 Frontend Redesign:** The complete M9 Frontend Redesign has been integrated into the main branch, ensuring that the full set of improvements and fixes from that milestone are available in a single consistent version of the code.

### Bug Fixes

- **Clamp board card title:** The title on a board card is now correctly wrapped with a line clamp to prevent it from extending beyond the card. This ensures cards maintain a consistent height and the two-line title is properly displayed.
- **Send button inside panel:** The send button in the assistant chat is now correctly placed within the panel, maintaining alignment with the input at all widths. This prevents the button from hanging outside the composer panel.
- **Fix Category header overlap:** The `Category` column header in the ticket queue is now properly spaced and rendered with the same styling as the `Due` column, preventing overlap and ensuring header alignment.
- **Write honesty and confirmation policy:** The assistant's system prompt now clearly defines policies for write honesty and confirmation. This ensures changes are only confirmed and executed when the user actually requests them, reducing unnecessary or misleading confirmations.
- **Summary timestamps in local timezone:** Summary timestamps now render in the user's local timezone rather than UTC, ensuring consistency between the ticket summary and the ticket detail view.
- **Report failed knowledge-base search as error:** Failed knowledge-base searches are now reported as errors rather than successful results. This allows the system to better distinguish between real knowledge failures and intentional unavailability.
- **Score grounding by meaning:** The grounding evaluation now scores answers based on semantic similarity rather than simple keyword matching, improving accuracy for paraphrased or translated responses.
