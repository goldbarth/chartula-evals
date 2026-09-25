---
title: Release 1.9.0
description: This release brings the M9 frontend redesign together with updates to assistant guidance and knowledge-base grounding.
publishedAt: 2026-07-14
---

### What's New

- **Inline citations in answers:** When a cited passage title appears in an assistant Markdown answer, a numbered badge appears beside it; citations without a matching title remain in the Sources list. The inline badges and Sources entries use matching numbers.
- **Suggested ticket actions:** For tickets with an actionable suggested next step, the first step appears as a button or agent picker in the ticket header. Choosing it runs the suggested action, while steps that cannot be mapped to an action remain non-clickable.
- **Keyboard command palette:** Press Ctrl+K or Cmd+K on any page to open a palette with navigation destinations and ticket search results. You can move through results, open one, and close the palette using the keyboard.
- **Immediate status updates:** Status changes appear immediately on the board and ticket detail page. Accepted changes are reconciled with the server, and rejected changes restore the previous status and explain why.
- **Inline ticket edits:** Changing a ticket’s status or assignee no longer takes you away from the ticket into a modal. You can make the change while keeping your current tab and scroll position.
- **Inline citation previews:** When an assistant answer includes citations, numbered badges appear beside passage titles the model has anchored in the answer. You can reveal each badge’s source, heading, and snippet by hovering or moving keyboard focus, and citations without a match remain in the numbered Sources list.
- **Assistant agent roster:** When you ask the assistant to assign a ticket, it is instructed to use only the active agent names and not to invent one. If the name you provide is not on the roster, it is instructed to list the valid names instead of guessing.
- **Grounding checks:** When knowledge-base passages are retrieved, the assistant checks its draft before streaming an answer, at least once during the run. The check is not guaranteed to cover every passage retrieved across a longer chain.
- **Consistent ticket chip colors:** Status and priority chips use the same colors on the queue, board, and ticket detail pages. You can rely on a chip having a consistent color across those views.

### What's Changed

- **Frontend redesign release:** The v1.9.0 release brings the M9 frontend redesign together in one release.

### Bug Fixes

- **Board title clamping:** Long ticket titles on board cards could grow the card without a limit; they now clamp to two lines with an ellipsis. Cards in a lane keep a bounded height.
- **Assistant message composer:** The assistant’s send button could sit at the edge of its composer panel; it now sits inside the panel, with the input and button aligned at narrow widths. You can use the composer without the send button extending past the panel.
- **Ticket list column headers:** On the ticket list, the Category header could overlap Due; the columns now sit side by side, with Category in uppercase. You can read the headers without them running together.
- **Assistant change confirmations:** After you request a ticket change, the assistant proceeds without asking you to confirm again and reports it as done only after a successful result. It may still ask when the ticket match or required details are unclear, a hard-to-reverse action leaves genuine doubt about your intent, or a route suggestion is uncertain.
- **Ticket summary timestamps:** Ticket summary timestamps could appear in UTC instead of your configured timezone; they now use that timezone. You can compare summary times with the ticket detail view without adjusting for the timezone.
- **Knowledge-base search errors:** A failed knowledge-base search could appear successful; technical failures are now reported as errors, distinct from an unavailable search. Dashboard error rates now reflect technical failures.
- **Meaning-based grounding checks:** Grounding checks can now recognize supported paraphrases and translations against retrieved passages, even when the wording differs. If semantic embeddings are unavailable or fail, the existing lexical check still provides a verdict.
