---
title: Release 1.9.0
description: Version 1.9.0 brings a redesigned support-desk interface alongside updates to ticket workflows and assistant responses.
publishedAt: 2026-07-14
---

### What's New

- **Inline citation badges:** Citations whose titles appear in the assistant’s Markdown answer now show numbered badges after the passage title, with previews on hover or keyboard focus. Badge numbers match the Sources list, and citations without a matching title remain in that list.
- **Suggested ticket actions:** When a ticket has suggested next steps, its first actionable step appears as a primary button or agent picker, with remaining steps in an overflow menu. You can run suggested status or assignment actions from the header, while unmapped steps stay non-clickable and tickets without suggestions keep the existing generic controls.
- **Command palette:** Press Ctrl+K or Cmd+K on any page to open a palette for finding navigation destinations and tickets. You can navigate it with the keyboard, and pressing Esc returns focus to where it was before the palette opened.
- **Immediate status updates:** A ticket’s status now changes on the board or detail page as soon as you choose a move, before the server responds. If the server rejects the change, the previous status is restored and the reason is shown, so a rejected or superseded move does not leave the interface showing an unaccepted status.
- **Inline ticket controls:** Choosing a status or assignee from the ticket header now opens an inline menu instead of a dialog. You stay on the ticket with your scroll position and current tab intact, and errors appear in a snackbar.
- **Assistant citation previews:** When the assistant’s answer includes citations, matching passage titles show numbered badges with previews on hover or keyboard focus. Citations without a matching title remain in the Sources list, and answers without citations are unchanged.
- **Agent names for assignments:** The assistant can now identify the active agents when you ask it to assign a ticket. For assignment requests, it is instructed to use only roster names and list valid agents instead of guessing when a requested name is absent.
- **Grounding checks:** After retrieving knowledge-base passages, the assistant now checks its draft against them before streaming an answer. The check runs at least once after retrieval for both chat and autonomous-worker runs, but is not guaranteed to cover every passage retrieved in a long run.
- **Consistent interface styling:** Status and priority chips now use the same colors across ticket queues, boards, and detail pages. Spacing and rounded corners follow a consistent scale across the interface.

### What's Changed

- **M9 frontend redesign:** The complete M9 frontend redesign is now brought together in the v1.9.0 release. The release notes cover this consolidated release.

### Bug Fixes

- **Board card titles:** Long ticket titles on board cards now clamp to two lines with an ellipsis. Cards stay a bounded height, so long titles no longer stretch their lane.
- **Assistant chat composer:** The assistant chat send button now sits inside its composer panel, including at narrow widths. The input and button stay aligned while messages scroll within the panel.
- **Ticket list Category column:** On the ticket list, the Category header now appears in uppercase beside Due instead of running into it. The header and column contents stay aligned, and Category remains a label rather than a sort control.
- **Assistant change confirmations:** The assistant no longer claims a ticket change succeeded unless a tool reports success in the conversation. When you have already requested a change, it proceeds without asking you to confirm again, while still asking when the ticket match or required details are unclear, intent is uncertain for a hard-to-reverse action, or a routing suggestion is uncertain.
- **Ticket summary times:** Ticket summaries now show created, due, comment, and event times in your configured timezone. Summary times match the timezone used in the ticket detail view.
- **Knowledge-base search errors:** When a knowledge-base search fails technically, it is now reported as an error instead of a successful search. The dashboard’s tool error rate reflects those failures, while an unavailable knowledge base remains a separate outcome.
- **Meaning-based grounding:** The assistant’s grounding check now compares answer sentences with retrieved passages by meaning, allowing correct paraphrases and translations to count as supported. When semantic scoring is unavailable or fails, the check falls back to word overlap, so paraphrases may not count as supported in those cases.
