---
title: Release 1.9.0
description: This release completes the frontend redesign and makes the assistant more reliable.
publishedAt: 2026-07-14
---

### What's New

- **Inline citations in assistant answers:** Assistant answers now show numbered citation badges right after the passage they cite, with a preview of the title, source and snippet on hover or keyboard focus. Each badge shares its number with the matching entry in the Sources list, and a citation the answer does not quote by title still appears in that list, as long as the assistant quotes the passage title word for word, which it is instructed to do.
- **Suggested next step as a button:** The ticket header now turns the first suggested next step into a button that carries it out, such as changing the status or picking an agent to assign, with the other steps in an overflow menu. The usual status, assign and edit controls stay available, and a ticket with no suggestions shows no empty button.
- **Command palette:** Pressing Ctrl+K (Cmd+K on Mac) on any page opens a command palette for jumping to a page or finding a ticket by search, even while a text field has focus. You can work it entirely from the keyboard with the arrow keys, Enter and Esc, and Esc returns you to where you were.
- **Instant status changes:** A status change on the board or ticket detail page now shows right away instead of waiting for the server, so a dragged card stays in its new column. If the change is rejected, the ticket returns to its previous status and a message gives the reason.
- **Editing status and assignee:** Changing a ticket's status or assignee now happens in a menu on the ticket header instead of a separate dialog. The ticket stays open on the same tab and scroll position, so you can carry on where you were.
- **Assistant sources list:** Citations in assistant answers are now listed as a numbered Sources list below the answer. An answer without citations shows no empty Sources block.
- **Agent names in the assistant:** When asked to assign a ticket, the assistant could make up an agent name that does not exist. It now knows the current list of agents and is instructed to use only those names and to list the valid ones when a name you give is not on it.
- **Answer checks against the knowledge base:** After looking up knowledge base articles, the assistant now always checks its answer against them at least once before the answer starts appearing. You can count on that check having run for every answer drawn from the knowledge base, both in chat and for automatic ticket handling.
- **Consistent look across pages:** Colors, spacing and corner rounding now follow one consistent scale across the app, so the same status or priority looks the same in the queue, board and ticket detail. Board card titles no longer get cut off mid-letter.

### What's Changed

- **Release integration:** This release brings together the full frontend redesign in one version.

### Bug Fixes

- **Long board card titles:** A long title on a board card could make the card grow without limit. Titles are now cut to two lines with an ellipsis, so cards in a column keep a consistent height.
- **Assistant send button:** The send button in the assistant chat could hang over the edge of its panel. It now sits inside the panel and stays in line with the input at any window width.
- **Ticket queue column headers:** In the ticket queue, the Category column header overlapped the Due header. The headers now sit side by side in matching uppercase and stay aligned with the columns below in both themes.
- **Assistant confirmations:** The assistant is now instructed never to say a change was made unless the change actually went through, and not to ask again for confirmation once you have asked for a change. It still asks first when your request is ambiguous, is missing information, or is hard to undo.
- **Times in ticket summaries:** Times in ticket summaries could appear in UTC instead of your local time. Summaries now use the same time zone as the ticket detail view, so the times match what you see next to them.
- **Failed knowledge base searches:** When a knowledge base search failed, it was recorded as a successful search. Failures now show as errors on the dashboard, separate from searches that are unavailable, so the error rate there reflects real failures.
- **Checking answers by meaning:** The assistant's check of its answers against knowledge base articles flagged correct paraphrases and translations as unsupported. It now compares answers by meaning, so a correct reworded or translated answer counts as supported, except when the comparison service is unavailable and the check falls back to matching words.
