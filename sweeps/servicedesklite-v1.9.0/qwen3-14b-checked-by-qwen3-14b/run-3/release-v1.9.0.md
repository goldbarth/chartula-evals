---
title: Release 1.9.0
description: This release integrates the complete M9 Frontend Redesign and includes several key improvements such as inline citation badges, optimistic status updates, a unified design token system, and enhanced grounding checks.
publishedAt: 2026-07-14
---

### What's New

- **Inline citation badges:** Inline citation badges now anchor to the assistant's Markdown answer. Changes are preserved even if the connection drops, so you no longer need a local backup copy while you work.
- **Primary action button:** The primary action button now appears for suggested steps, making it easier to take action directly from the ticket header.
- **Command palette:** A keyboard-first command palette now opens with Ctrl+K, accessible from any page and fully operable by keyboard.
- **Optimistic status updates:** Status changes on the board now update immediately with an optimistic preview and roll back if the server rejects the change.
- **Inline status and assignee edit:** Status and assignee changes are now made inline with popovers, keeping you on the same page without navigation or modals.
- **Inline citation badges with hover preview:** Inline citation badges with tooltips now appear in the assistant's chat, showing source details on hover or keyboard focus.
- **Agent roster in system prompt:** The agent roster is now injected into the system prompt, so the model can accurately name available agents without error.
- **Enforced grounding check:** Grounding checks are now enforced via tool_choice, guaranteeing at least one check after any retrieval.
- **Design tokens:** Design tokens now provide a unified scale for spacing, radius, elevation, and semantic color across the application.

### What's Changed

- **M9 Frontend Redesign integration:** The complete M9 Frontend Redesign is now merged into the main branch, including v1.9.0 release notes.

### Bug Fixes

- **Board card title wrapping:** Board card titles are now wrapped to ensure two-line clamping with ellipsis, preventing unbounded card growth.
- **Send button inside panel:** The assistant composer's send button is now inside its panel, keeping it aligned with the input field.
- **Category header alignment:** The Category header no longer overlaps with the Due column in the ticket queue, and both are now uppercase.
- **System prompt honesty policy:** The system prompt now enforces write-honesty and confirmation policy, ensuring changes are only made after user confirmation and avoiding unnecessary questions.
- **User timezone timestamps:** Summary timestamps are now rendered in the user's local timezone, matching the ticket detail view.
- **Error reporting for failed searches:** Failed knowledge-base searches now report as errors, allowing the dashboard to track technical failures.
- **Meaning-based grounding scoring:** Grounding is now scored by meaning instead of word overlap, correctly identifying paraphrased and translated answers.
