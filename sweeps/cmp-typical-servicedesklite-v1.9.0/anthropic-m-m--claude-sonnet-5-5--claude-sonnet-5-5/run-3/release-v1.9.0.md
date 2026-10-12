---
title: Release 1.9.0
description: This release completes the Frontend Redesign, with a shared design system, inline editing, a command palette and citation badges, and hardens the assistant's grounding, write honesty and agent handling.
publishedAt: 2026-07-14
---

### What's New

- **Citation badges in assistant answers:** Answers in the assistant chat now show numbered citation badges right after the cited passage title, with a tooltip on hover or focus showing the title, source, heading and snippet. Each badge shares its number with its entry in the Sources list, and a citation whose title does not appear in the answer stays in that list only. Badges are placed only when the assistant quotes the passage title word for word, which its instructions already ask it to do.
- **Suggested next step button:** The ticket header now turns the first suggested next step into a button: a status change runs it directly, and an assignment opens an agent picker. The remaining suggestions sit in an overflow menu, so you no longer have to open the generic controls for the most likely action. Suggestions that cannot be run appear as plain text, and a ticket with no suggestions keeps the existing controls.
- **Command palette:** Pressing Ctrl+K (Cmd+K on Mac) opens a command palette on any page, even while a text field has focus. It lists navigation links and matching tickets as you type, and you can move with the arrow keys, open with Enter and close with Esc, which returns focus to where it was. You no longer have to reach for the mouse to jump to a page or ticket.
- **Instant status updates:** A status change on the board or the ticket detail now shows immediately instead of waiting for the server. If the server rejects the change, the previous state is restored and a message shows the error code. You can now count on the screen not holding a status the server never accepted, including after two quick changes on one ticket.
- **Inline status and assignee changes:** Changing a ticket's status or assignee now happens in a menu next to the header buttons rather than in a dialog. The ticket stays open on its current tab and scroll position, so you no longer lose your place to make a quick change. Errors appear as a message instead of a modal.
- **Citation badges in assistant chat:** Assistant answers can now show numbered citation badges tied to the claims they support, with a tooltip on hover or keyboard focus showing source, heading and snippet. Citations not anchored in the text are listed in a numbered sources list, and answers without citations look unchanged.
- **Agent names in assistant:** When asked to assign a ticket, the assistant now knows the current list of agents and is told to use only those exact names. If your name is not on the list, it lists the valid agents instead of guessing the closest one, so it no longer invents agent names.
- **Grounding check enforced:** After the assistant retrieves knowledge-base passages, a grounding check is now required before it answers, rather than left to the model's choice. You can rely on at least one check having run after any retrieval, for both the chat assistant and the autonomous worker. The result is not shown to users.
- **Consistent design styling:** Colours, spacing, corner radius and status and priority chip styles now come from one shared set of design values across the web app. Status and priority chips that had drifted apart between the queue, board and detail views now look the same, so you see consistent styling everywhere. Spacing and corner sizes shift by a few pixels in places as they snap to the common scale.

### What's Changed

- **v1.9.0 release:** The v1.9.0 release brings the complete Frontend Redesign into one release. In the assistant, Markdown answers show citations as a sources list below the answer, and the grounding score no longer appears in the transcript.

### Bug Fixes

- **Board card titles:** Long ticket titles on board cards could grow the card without limit in some older Chrome versions. Titles are now clamped to two lines with an ellipsis, so cards in a lane keep a consistent height.
- **Assistant send button:** In the assistant chat, the send button sat flush against the right edge of the composer panel and hung over it. The panel's padding and layout now apply, so the button stays inside the panel and aligned with the input at any width.
- **Ticket queue Category header:** On the tickets page, the Category column header overlapped Due and read as "CategoryUE". Category now has its own width and an uppercase label like its neighbours, so the headers sit side by side and line up with the cells below. Category is still not sortable.
- **Assistant write honesty:** The assistant could state that a change had been made without having made it, and could ask for confirmation of changes you had already requested. It now reports a change only after the tool call succeeded, and makes requested changes without asking again. It still asks when the ticket match is ambiguous, information is missing, or a hard-to-reverse action is in doubt.
- **Summary timestamps:** Times in the streamed ticket summary appeared in UTC, so a comment written at 12:07 local time showed as 10:07. Summaries now use your configured time zone, so they match the timestamps in the ticket detail view.
- **Knowledge-base search errors:** A knowledge-base search that failed because of a database or embedding service error was reported as a normal successful search. It is now reported as an error, separate from the case where search is unavailable, so the dashboard error rate reflects real failures.
- **Grounding scoring:** The grounding check marked correct paraphrases, correct translations and cautious hedged answers as ungrounded because it only compared words. It now compares meaning, so such answers are scored as supported by their source passages. Without a Voyage key or if embedding fails, it falls back to the earlier word-based check.
