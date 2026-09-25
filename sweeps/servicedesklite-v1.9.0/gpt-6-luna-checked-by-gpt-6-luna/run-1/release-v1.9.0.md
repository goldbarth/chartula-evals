---
title: Release 1.9.0
description: This release brings the M9 frontend redesign together with changes to ticket workflows and assistant behavior.
publishedAt: 2026-07-14
---

### What's New

- **Inline citation badges:** Citations can now appear as numbered badges beside matching passage titles in the assistant’s Markdown answer, with hover and focus previews. When a title is not quoted in the answer, its citation remains in the Sources list, so citations stay available even when they cannot be anchored inline.
- **Suggested ticket actions:** The ticket header can now show the first actionable suggested step as a button or agent picker, with other suggestions in an overflow menu. These controls use the same actions as the existing manual controls, so suggested actions do not trigger a separate automation path.
- **Command palette:** Press Ctrl+K or Cmd+K on any page to open a keyboard-operable command palette with navigation and ticket search. You can move through results with the arrow keys, open one with Enter, and close the palette with Esc.
- **Immediate status updates:** A ticket’s status now changes on the board or detail page as soon as you make a change, before the server responds. If the server rejects the change, the previous status is restored and you see the error reason.
- **Inline ticket actions:** Status and assignee choices now open in menus on the ticket header instead of dialogs. You can make either change while staying on the ticket, with its current tab and scroll position preserved.
- **Assistant citation badges:** Citations can now appear as numbered badges beside matching titles in assistant answers, with previews available on hover or keyboard focus. Citations that are not anchored in the answer remain in the numbered Sources list.
- **Assistant agent roster:** The assistant’s responses now have access to the active agent roster when handling assignment requests. It can use the listed names or show the valid agents when a requested name is not on the roster, rather than inventing an agent.
- **Grounding check enforcement:** After retrieving knowledge-base passages, the assistant and autonomous worker now perform a grounding check before streaming an answer, unless the assistant has already checked it. You can rely on at least one check after retrieval, though a single check does not guarantee that every passage retrieved later in a run is covered.
- **Consistent design tokens:** The interface’s colors, spacing, corner radii, elevation, and semantic chip colors now use shared design tokens. Status and priority chips use the same color definitions across the queue, board, and ticket detail views.

### What's Changed

- **v1.9.0 release:** Version 1.9.0 brings the M9 Frontend Redesign together with the web and assistant changes in this release.

### Bug Fixes

- **Board card titles:** Long board card titles now stop at two lines and end with an ellipsis. This keeps titles from extending a card without bound.
- **Assistant composer layout:** The assistant’s send button now sits inside its chat panel, with the input and button aligned at narrow and wide widths. The message area can scroll while the composer stays in place.
- **Ticket queue Category header:** The Category header now sits beside Due without overlapping it, and the column aligns with its header and body cells. Category remains a static label rather than a sort option.
- **Assistant confirmation policy:** The assistant no longer claims a change succeeded unless a tool call reports success in the conversation. When you have already requested a change, it proceeds without asking again unless the ticket match, required information, action, or intent needs clarification.
- **Summary timestamps:** Timestamps in ticket summaries now use the configured user timezone, including created and due dates, comments, and events. Summary times therefore match the timezone used in the ticket detail view.
- **Knowledge-base search errors:** A failed knowledge-base search is now reported as an error, while an unavailable search remains a separate outcome. Dashboard error rates can therefore reflect technical search failures.
- **Meaning-based grounding checks:** Grounding checks can now recognize supported paraphrases and translations by comparing sentence and passage meaning. If semantic evaluation is unavailable or embedding fails, the existing lexical check remains as a fallback.
