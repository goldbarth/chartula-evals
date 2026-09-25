---
title: Release 1.9.0
description: This release updates the web interface and assistant behavior, including citations, ticket controls, and grounding checks.
publishedAt: 2026-07-14
---

### What's New

- **Answer citations:** Citation badges now appear within the assistant’s answer. You can see which part of the answer each citation belongs to.
- **Suggested next steps:** Suggested next steps now include a primary action button. You can identify the main action from the suggestion.
- **Command palette:** You can now open the command palette with Ctrl+K. The shortcut gives you access to the palette.
- **Status updates:** Status changes on the board and detail view now appear immediately. If an update fails, the previous status is restored.
- **Ticket edits:** You can now edit status and assignee directly instead of opening dialogs. Both fields can be changed in place.
- **Citation previews:** Citation badges in assistant chat now show a preview when you hover over them. You can inspect a citation from the chat.
- **Agent roster:** The assistant now receives the agent roster in its instructions. It can use that roster when responding.
- **Grounding checks:** The assistant now runs the grounding check as a required tool step. Its responses can be checked for grounding.
- **Interface styling:** Spacing, corner radius, elevation, and colors now use shared design scales. Interface elements use those scales consistently.

### What's Changed

- **Version 1.9.0:** Version 1.9.0 includes the M9 frontend redesign.

### Bug Fixes

- **Board card titles:** Board card titles could fail to wrap as intended. Titles now follow the card’s line limit.
- **Assistant send button:** The assistant’s send button could extend outside its panel. You can count on it staying inside the panel.
- **Ticket queue headers:** The Category header could overlap Due in the ticket queue. You can now read both column headers.
- **Assistant confirmations:** The assistant’s instructions now cover honesty about write actions and confirmation. You can expect it to follow those instructions when responding.
- **Summary timestamps:** Summary timestamps could appear outside your timezone. You can now read them in your timezone.
- **Knowledge-base search errors:** A failed knowledge-base search was not reported as an error. You can now tell when the search failed.
- **Grounding scores:** Grounding scores previously relied on word overlap. They now account for meaning when scoring grounding.
