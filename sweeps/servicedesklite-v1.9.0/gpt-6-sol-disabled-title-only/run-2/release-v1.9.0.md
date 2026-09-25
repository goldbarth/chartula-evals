---
title: Release 1.9.0
description: This release updates the web interface and assistant behavior, alongside fixes to ticket views, summaries, and knowledge-base search.
publishedAt: 2026-07-14
---

### What's New

- **Citations in answers:** Citation badges now appear inline in the assistant’s Markdown answers. You can see where a citation belongs in the answer.
- **Suggested next steps:** Suggested next steps now include a primary action button. You can use it to take the suggested action.
- **Command palette:** You can now open the command palette with Ctrl+K. The shortcut gives you access to the palette.
- **Status updates:** Status changes appear immediately on the board and detail view. If an update fails, the status returns to its previous value.
- **Editing ticket details:** You can now edit status and assignee inline instead of in dialogs. Both fields can be changed where they appear.
- **Citation previews:** Citation badges now appear inline in assistant chat, with previews on hover. You can inspect a citation from the chat.
- **Agent roster:** The assistant now receives the agent roster in its instructions. It can refer to that roster when responding.
- **Grounding check:** The assistant now runs the grounding check through a required tool choice. You can count on that check being invoked.
- **Visual consistency:** Spacing, corner radius, elevation, and semantic colors now use shared design scales in the web interface. You can expect those values to follow the same scales across the interface.

### What's Changed

- **Frontend redesign:** Version 1.9.0 includes the M9 Frontend Redesign in the main release. You can use the redesign in this version.

### Bug Fixes

- **Board card titles:** Board card titles could fail to wrap as intended. They now wrap within the card.
- **Assistant send button:** The assistant composer’s send button could extend outside its panel. You can count on it staying inside the panel.
- **Ticket queue headings:** The Category heading could overlap Due in the ticket queue. You can read both headings separately.
- **Assistant confirmations:** The assistant’s instructions now include a write-honesty and confirmation policy. You can expect it to follow that policy when responding.
- **Summary timestamps:** Summary timestamps could appear in a timezone other than yours. You can read them in your timezone.
- **Knowledge-base search errors:** A failed knowledge-base search was not reported as an error. You can now tell when the search fails.
- **Grounding assessment:** The assistant’s grounding check could score responses by word overlap rather than meaning. You can count on the score reflecting meaning instead.
