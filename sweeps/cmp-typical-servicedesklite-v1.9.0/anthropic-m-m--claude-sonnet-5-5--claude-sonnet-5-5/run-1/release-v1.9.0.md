---
title: Release 1.9.0
description: This release completes the Frontend Redesign, with inline status edits, a command palette, suggested-action buttons and citation badges, and makes the assistant more reliable and honest.
publishedAt: 2026-07-14
---

### What's New

- **Inline citation badges in answers:** Citation badges such as [1] now appear inline in the assistant's formatted answer, next to the cited passage title, with a tooltip showing the title, source, heading and snippet on hover or focus. Each badge shares its number with the entry in the Sources list, so you can match claims to sources; a citation whose title the answer does not quote stays in the Sources list only.
- **Suggested next step button:** The ticket header now shows the first suggested next step as a primary button, and a status change runs immediately or an assign step opens an agent picker. The remaining suggestions sit in an overflow menu, so you no longer have to open a separate control for the most likely next step; with no suggestions, the usual Change Status, Assign and Edit controls remain.
- **Command palette:** Pressing Ctrl+K (Cmd+K on Mac) on any page opens a command palette, even while a text field has focus. It lists navigation targets and matching tickets as you type, and you can use the arrow keys, Enter and Esc, so you no longer have to reach for the mouse to move around.
- **Instant status updates:** Changing a ticket's status on the board or the detail view now shows the new status immediately instead of waiting for the server. If the change is rejected, the ticket returns to its previous state and a message gives the error code, so you can trust what the board shows.
- **Inline status and assignee changes:** Change Status and Assign on a ticket now open as small menus in the header instead of dialogs. The change applies immediately while the ticket stays open on the same tab and scroll position, so you no longer lose your place; errors appear as a message.
- **Citation badges in assistant chat:** Assistant citations can now appear as inline badges in the answer text, with a tooltip showing source, heading and snippet on hover or keyboard focus. Citations the assistant did not anchor in its answer stay in a numbered sources list, and an answer without citations shows no empty sources block.
- **Agent names in assistant:** The assistant is now given the current list of agents with every chat request and told to use only those names. When you ask it to assign a ticket to a name not on the list, it lists the valid agents instead of guessing, so you no longer risk it inventing an agent.
- **Grounding check required:** After the assistant retrieves knowledge-base passages, it is now required to run a grounding check on its answer once, before the answer begins streaming. This applies to the interactive assistant and the autonomous worker, so a retrieval-based answer can no longer skip the check; the result is not shown to you, and the check runs only once, not for every passage in a long chain.
- **Consistent visual styling:** The web app's colors, spacing, corner radii and status and priority chip colors now come from one shared set of values, so the queue, board and ticket detail show the same chip colors. Spacing and corner sizes snap to a fixed scale, so some elements shift by one to four pixels, and board card titles are no longer cut off mid-letter.

### What's Changed

- **Version 1.9.0 release:** Release 1.9.0 brings the complete Frontend Redesign into the main line. The assistant page shows formatted answers with citations in a sources list below, and the grounding score no longer appears in the transcript.

### Bug Fixes

- **Board card titles:** Long ticket titles on board cards could grow the card without limit in some older Chrome versions. Titles are now limited to two lines with an ellipsis, so cards in a lane keep a consistent height there; newer Chrome versions were not affected.
- **Assistant send button:** On the assistant page, the send button sat flush against the right edge of the composer panel and hung over it. The panel now has its intended padding, so the send button stays inside the panel and aligned with the input at narrow widths too.
- **Ticket list column headers:** In the ticket list, the Category column header overlapped the Due header and read as "CategoryUE". Category now has its own width and uppercase label like its neighbours, so the headers sit side by side and line up with the cells below.
- **Assistant write honesty:** The assistant is now told never to say a change was made unless the tool call ran and reported success in the conversation. It is also told to make a change you already asked for without asking again, and to ask first only for genuine decisions such as an ambiguous ticket match or missing information.
- **Summary timestamps:** Times in streamed ticket summaries could appear in UTC, such as 10:07 for a comment written at 12:07 local time. Summaries now use the configured user timezone, so they match the times shown in the ticket detail view.
- **Failed knowledge-base search:** A knowledge-base search that failed because of a technical error was reported as a successful search. It is now reported as an error, distinct from the case where the knowledge base is unavailable, so the dashboard's error rate reflects real failures.
- **Grounding by meaning:** The grounding check marked correct paraphrases, translated answers and cautious hedging as ungrounded because it compared words only. It now compares meaning, so such answers are no longer wrongly scored low; without an embedding service it falls back to the earlier word-based check.
