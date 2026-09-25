---
title: Release 1.9.0
description: This release brings changes to the web interface, assistant behavior, and error and timestamp reporting.
publishedAt: 2026-07-14
---

### What's New

- **Answer citations:** Citation badges now appear within the assistant's Markdown answers, anchored to the relevant text. You can see where a citation belongs as you read.
- **Suggested next steps:** Suggested next steps now have a primary action button. You can identify the main action from the suggestion.
- **Command palette:** You can open the command palette with Ctrl+K. The shortcut gives you access to the palette from the keyboard.
- **Status updates:** Status changes on the board and detail view now appear immediately. If an update fails, the previous status is restored.
- **Ticket editing:** You can edit status and assignee inline instead of opening a dialog. The fields can be changed where they appear.
- **Chat citations:** Citation badges in assistant chat now show a preview when you hover over them. You can inspect a citation while reading the answer.
- **Agent roster:** The assistant now receives the agent roster in its instructions. It can use that roster when responding.
- **Grounding checks:** The assistant is now required to run a grounding check. You can count on the check being part of its response process.
- **Interface styling:** Spacing, corner radius, elevation, and semantic colors now use shared design scales. These interface elements follow the same scales across the web app.

### What's Changed

- **Frontend release:** Version 1.9.0 includes the M9 Frontend Redesign. You can use the integrated redesign in this release.

### Bug Fixes

- **Board card titles:** Board card titles could fail to wrap as intended. They now wrap within the card.
- **Assistant send button:** The assistant's send button could extend outside the composer panel. You can count on the button staying inside the panel.
- **Ticket queue headers:** The Category header could overlap Due in the ticket queue. You can read both headers separately now.
- **Assistant confirmations:** The assistant's instructions now address honesty about writes and when to ask for confirmation. You can count on those instructions being part of its responses.
- **Summary timestamps:** Summary timestamps could appear outside your timezone. You can now read them in your timezone.
- **Knowledge-base search errors:** A failed knowledge-base search could go unreported as an error. You can now tell when the search fails.
- **Grounding assessment:** The assistant's grounding assessment could rely on overlapping words rather than meaning. You can now count on meaning being used to assess grounding.
