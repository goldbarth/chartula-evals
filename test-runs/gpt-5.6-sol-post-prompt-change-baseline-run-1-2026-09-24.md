gpt-5.6-sol-post-prompt-change-baseline-run-1-2026-09-24, rendered by Chartula from v1.9.0

--- Technical ---

### Changed

- Add the complete M9 Frontend Redesign milestone and v1.9.0 release notes to `main`. ([#244](https://github.com/goldbarth/ServiceDeskLite/pull/244))

### Added

- Add inline citation badges anchored in sanitized Markdown answers, with hover and focus tooltips and unanchored citations retained in the sources list. ([#245](https://github.com/goldbarth/ServiceDeskLite/pull/245))
- Add a primary ticket action derived from the first actionable `SuggestedNextSteps` entry, with remaining steps in an overflow menu. ([#237](https://github.com/goldbarth/ServiceDeskLite/pull/237))
- Add a keyboard-operated `CommandPalette` on Ctrl/Cmd+K with `NavRegistry` navigation entries and debounced, cancellable ticket search. ([#236](https://github.com/goldbarth/ServiceDeskLite/pull/236))
- Add optimistic status updates with rollback, concurrency protection, and ProblemDetails `code` notifications on the board and detail view. ([#235](https://github.com/goldbarth/ServiceDeskLite/pull/235))
- Replace status and assignee dialogs with inline `MudMenu` popovers that update the current ticket without navigation. ([#234](https://github.com/goldbarth/ServiceDeskLite/pull/234))
- Add `AnswerCitationLayout` to place citation badges beside matching answer text and retain unmatched citations in the numbered sources list. ([#233](https://github.com/goldbarth/ServiceDeskLite/pull/233))
- Add the active agent roster to each chat system prompt through `GetAgentsHandler`. ([#221](https://github.com/goldbarth/ServiceDeskLite/pull/221))
- Enforce one `check_grounding` call through `tool_choice` after retrieval and before the first streamed token. ([#218](https://github.com/goldbarth/ServiceDeskLite/pull/218))
- Add `Theme/DesignTokens.cs` as the shared source for palette, spacing, radius, elevation, and semantic chip colors. ([#213](https://github.com/goldbarth/ServiceDeskLite/pull/213))

### Fixed

- Fix two-line board card title clamping by wrapping the title link in `board-card__title-row`. ([#240](https://github.com/goldbarth/ServiceDeskLite/pull/240))
- Fix the assistant composer layout by targeting the `MudPaper` panel through `::deep .assistant-chat`. ([#239](https://github.com/goldbarth/ServiceDeskLite/pull/239))
- Fix the `Category` header overlap by assigning the column a 140px width and using `tickets-table__label`. ([#238](https://github.com/goldbarth/ServiceDeskLite/pull/238))
- Add system-prompt rules that prohibit unsupported write claims and unnecessary confirmation requests. ([#223](https://github.com/goldbarth/ServiceDeskLite/pull/223))
- Render ticket summary timestamps in `Anthropic:UserTimeZone`, including created, due, comment, and event times. ([#222](https://github.com/goldbarth/ServiceDeskLite/pull/222))
- Fix `search_knowledge_base` to return `IsError: true` for non-transient technical failures while preserving successful unavailable results. ([#220](https://github.com/goldbarth/ServiceDeskLite/pull/220))
- Add `SemanticGroundingEvaluator` to score grounding through Voyage embeddings, with `LexicalGroundingEvaluator` as the fallback. ([#219](https://github.com/goldbarth/ServiceDeskLite/pull/219))

--- Customer ---

### What's New

- **Inline citation badges:** Assistant answers now show numbered citation badges after cited passage titles in sanitized Markdown, with source details on hover or keyboard focus. The badge numbers match the Sources list, and citations that cannot be anchored remain in that list so you can still trace the supporting evidence.
- **Suggested ticket actions:** The first actionable suggested step now appears as the primary control in the ticket header, while remaining suggestions appear in the overflow menu. You can act on status and assignment suggestions directly, and the existing ticket controls remain available when there are no actionable suggestions.
- **Command palette:** You can now open a command palette from any page with Ctrl+K or Cmd+K to find navigation destinations and tickets. Arrow keys move through results, Enter opens one, and Esc closes the palette and restores your previous focus.
- **Immediate status updates:** Ticket status changes on the board and detail page now appear immediately, including when you drag a board card. You can rely on rejected changes returning to the previous status with an error code, while rapid changes reconcile to the latest status accepted by the server.
- **Inline ticket editing:** Changing a ticket’s status or assignee now happens in popover menus instead of dialogs. You can make either change without leaving the ticket, losing your scroll position, or switching away from the current tab.
- **Citations beside answers:** Assistant citations now appear as numbered badges beside matching titles in answer text, with source, heading, and snippet details available on hover or keyboard focus. Citations that cannot be placed inline remain in the numbered Sources list, while answers without citations remain unchanged.
- **Accurate agent names:** The assistant now receives the active agent roster with every chat request. When handling assignments, it is instructed to use only exact roster names and to list valid agents instead of inventing or guessing a match.
- **Required grounding checks:** After retrieving knowledge-base passages, the assistant and autonomous worker must run at least one grounding check before streaming an answer. You can rely on the first answer after retrieval being checked unless the model already performed the check itself.
- **Consistent interface styling:** Spacing, corner radius, elevation, colors, and status and priority chips now use one shared design scale across the interface. You can rely on these visual treatments remaining consistent between the queue, board, ticket details, and other pages.

### What's Changed

- **Frontend redesign release:** Version 1.9.0 brings the complete M9 Frontend Redesign into one release, including Markdown assistant answers, dark mode, saved-view query parameters, and ticket interface updates. You can rely on these changes being available together from the v1.9.0 release point.

### Bug Fixes

- **Board card titles:** Long ticket titles on board cards previously grew beyond two lines and could stretch their lane. They now stay within a two-line title area with an ellipsis, keeping cards at a bounded height even for long or unbreakable titles.
- **Assistant send button:** The assistant send button could sit flush against or over the edge of its panel, especially at narrow widths. It now remains inside the panel and aligned with the input, while messages scroll within the restored panel layout.
- **Ticket queue headers:** The Category header in the ticket queue previously overlapped Due and appeared in a different case from neighboring headers. Category and Due now remain aligned side by side, with Category displayed in uppercase while remaining a non-sortable label.
- **Assistant write confirmations:** The assistant is now instructed not to claim that a change occurred unless a tool reported success in the current conversation. When you have already requested a change, it is also instructed to proceed without asking again unless a genuine decision, missing detail, ambiguous ticket, hard-to-reverse action, or uncertain routing suggestion requires confirmation.
- **Summary timestamps:** Ticket summaries previously showed timestamps in UTC instead of the user timezone used by the ticket detail view. Created, due, comment, and event times now use the configured user timezone and include its UTC offset, so summary times match the surrounding ticket information.
- **Knowledge-base search errors:** A failed knowledge-base search previously appeared as a successful result, making technical failures look like normal unavailability. Failures now count as errors while an unavailable knowledge base remains a non-error outcome, so you can rely on the dashboard error rate distinguishing the two.
- **Semantic grounding scores:** Grounding checks now compare the meaning of answer sentences with retrieved passages instead of relying only on shared words. Correct paraphrases and translations can now be recognized as supported, with the previous word-overlap method retained when semantic evaluation is unavailable or fails.
