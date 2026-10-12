---
title: Release 1.9.0
description: This release brings together the frontend redesign with changes to ticket workflows, assistant citations and safeguards for assistant answers and actions.
publishedAt: 2026-07-14
---

### What's New

- **Citations in Markdown answers:** You can now see numbered citation badges beside cited passages in Markdown answers when the assistant quotes the passage title verbatim. Badge numbers match the Sources list, where citations without a matching title remain available.
- **Suggested ticket actions:** You can now act on the first actionable suggestion directly from the ticket header, with remaining suggestions in the overflow menu. The existing status, assignment and editing controls remain available even when there are no suggestions.
- **Command palette:** You can now open navigation and ticket search from any page with Ctrl/Cmd+K, including while typing in a text field. Arrow keys and Enter let you open a result, while Esc closes the palette and returns focus to where you were.
- **Immediate status updates:** Status changes now appear immediately on the board and ticket detail page, before the server responds. Rejected changes restore the previous state and show an error code, while rapid board changes reconcile with the status accepted by the server.
- **Inline ticket editing:** You can now change status or assignment through menus in the ticket header instead of dialogs. Your ticket stays open on the same tab and at the same scroll position when you select a change.
- **Citation previews:** You can now hover over or keyboard-focus an inline citation badge to see its source, heading and snippet when the citation title matches the answer text. Sources remain available even when a citation cannot be placed inline or a response contains no answer text.
- **Assistant assignment guidance:** The chat assistant now receives the active agent roster with every request, so it can name valid agents without first attempting an assignment. It is instructed to use those exact names and list valid choices when a requested name is absent, rather than inventing or choosing a similar name.
- **Required grounding check:** Answers using retrieved knowledge-base passages now undergo at least one grounding check before streaming, in both chat and the autonomous worker. This guarantees a check after retrieval, but not coverage of every passage retrieved later in a long run, and the verdict is not displayed.
- **Consistent visual styling:** Spacing, rounded corners and colors now follow shared scales across the interface. Status and priority chips use the same colors in the queue, board and ticket detail views.

### What's Changed

- **Frontend redesign release:** The complete frontend redesign is now brought together in v1.9.0. The integrated assistant view renders Markdown, keeps the send button inside its panel and leaves grounding information out of the transcript.

### Bug Fixes

- **Long board titles:** Long ticket titles could make board cards grow without bounds in older Chrome versions. Titles now stop at two lines with an ellipsis, keeping card heights bounded and preventing unbreakable titles from stretching lane columns.
- **Assistant composer layout:** The assistant's send button could hang over the panel edge. The input and button now stay aligned inside the panel at narrow widths, with messages scrolling internally and the composer staying pinned.
- **Ticket queue headers:** The Category header overlapped Due in the ticket queue. Headers and their column contents now stay aligned in both themes, with Category styled in uppercase like its neighbors.
- **Assistant change confirmations:** The assistant could claim a change had happened without executing it or ask again after you had already requested it. The chat instructions now require a successful tool result before claiming completion and direct the assistant to proceed without repeated confirmation unless a genuine user decision remains.
- **Summary timestamps:** Ticket summaries showed UTC times that disagreed with the local timestamps beside them. Created, due, comment and event times now use the same user timezone as chat and ticket details, with the timezone and UTC offset supplied to the assistant.
- **Knowledge-base search failures:** Technical knowledge-base search failures were counted as successful calls and were indistinguishable from an unavailable service. Dashboard error rates now include those failures, and search results distinguish a technical error from an unavailable knowledge base.
- **Meaning-based grounding:** Correct paraphrases and translations could be judged unsupported because their words differed from the source. When Voyage embeddings are available and succeed, grounding now assesses meaning rather than word overlap; otherwise it falls back to the existing word-based check.
