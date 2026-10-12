---
title: Release 1.9.0
description: This release completes the frontend redesign and makes the assistant more reliable and honest.
publishedAt: 2026-07-14
---

### What's New

- **Inline citation badges:** Citations in an assistant answer now appear as numbered badges right after the cited passage title, with a tooltip on hover or focus showing the title, source, heading and snippet. Each badge shares its number with the matching entry in the Sources list, and a citation the answer does not quote by title still appears in that list, so no source is dropped.
- **Suggested next step button:** The ticket header now shows the most likely next step as a button that carries it out, such as moving the ticket to a new status or picking an agent to assign, with the other suggested steps in an overflow menu. Suggestions that cannot be run appear as plain text, and the usual status and assign controls stay available, so you can act on the recommendation in one click or ignore it.
- **Command palette:** Pressing Ctrl+K (Cmd+K on Mac) on any page opens a command palette to jump to a page or search for a ticket, even while a text field has focus. You can move through results with the arrow keys, open one with Enter and close with Esc, which returns you to where you were.
- **Instant status changes:** Changing a ticket's status on the board or the detail page now shows the new status straight away instead of waiting for the server. If the change is rejected, the ticket returns to its previous status and a message explains why, so what you see always matches what was saved.
- **Editing status and assignee:** Changing a ticket's status or assignee now happens in a menu next to the header buttons instead of a separate dialog. The ticket stays open on the same tab and scroll position, so you can keep working where you were.
- **Citation previews in chat:** Citations in assistant answers can now appear as numbered badges next to the text they support, with a preview of the source, heading and snippet on hover or keyboard focus. Answers without citations look as before, with no empty sources section.
- **Agent names in the assistant:** Asked to assign a ticket, the assistant could invent an agent name that does not exist. It now knows the current list of agents and is told to use only those names and to list the valid ones when yours is not among them.
- **Answer grounding check:** Assistant answers based on knowledge-base articles could stream out without being checked against those articles. The assistant now always checks such an answer at least once before it starts replying, so the check no longer depends on the assistant choosing to run it.
- **Consistent look:** Colours, spacing and corner rounding now follow one shared scale across the app, so some elements shift by a few pixels. Status and priority chips now look the same in the queue, on the board and on the ticket page.

### What's Changed

- **Frontend redesign:** This release brings together the complete frontend redesign.

### Bug Fixes

- **Long titles on board cards:** On older Chrome versions, a long ticket title on the board could stretch its card without limit. Titles are now cut to two lines with an ellipsis, so cards in a column keep a consistent height.
- **Assistant send button:** The send button in the assistant chat sat on the edge of its panel, hanging over the border. It now sits inside the panel and stays aligned with the input at any window width.
- **Ticket list headers:** In the ticket list, the Category column header overlapped the Due header and read as "CategoryUE". The headers now sit side by side in uppercase like the others, and header and row cells stay aligned in both light and dark themes.
- **Assistant confirmations:** The assistant could say a change was made when it was not, or ask you to confirm something you had already requested. It is now told to report a change only after it has actually succeeded, and to carry out a requested change without asking again unless your intent is genuinely unclear.
- **Summary times:** Times in the streamed ticket summary were shown in UTC, for example 10:07 for a comment written at 12:07 local time. Summary times now use the same time zone as the ticket page, so the summary matches the timestamps shown next to it.
- **Knowledge-base search errors:** A knowledge-base search that broke was reported as a successful search. Such failures now count as errors on the dashboard, so its error rate reflects real failures and an unavailable search reads differently from a failed one.
- **Grounding by meaning:** The grounding check marked correct paraphrases, translated answers and hedged answers as not backed by the source articles. These answers are now judged by meaning, so a correct answer is no longer flagged just for using different words or another language.
