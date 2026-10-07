gpt-5.6-sol-post-prompt-change-baseline-run-3-2026-09-24, rendered by Chartula from v1.9.0

--- Technical ---

### Changed

- Add the complete M9 Frontend Redesign milestone and the v1.9.0 release notes to `main`. ([#244](https://github.com/goldbarth/ServiceDeskLite/pull/244))

### Added

- Add inline citation badges anchored in sanitized Markdown answers, with unanchored citations retained in the sources list. ([#245](https://github.com/goldbarth/ServiceDeskLite/pull/245))
- Add a primary ticket action based on the first actionable `SuggestedNextSteps` entry. ([#237](https://github.com/goldbarth/ServiceDeskLite/pull/237))
- Add a keyboard-operated command palette that opens from every page with `Ctrl/Cmd+K`. ([#236](https://github.com/goldbarth/ServiceDeskLite/pull/236))
- Add optimistic status changes with rollback and reconciliation on the ticket board and detail view. ([#235](https://github.com/goldbarth/ServiceDeskLite/pull/235))
- Replace status and assignee dialogs with inline `MudMenu` popovers. ([#234](https://github.com/goldbarth/ServiceDeskLite/pull/234))
- Add inline citation badges with hover and keyboard-focus previews to assistant answers. ([#233](https://github.com/goldbarth/ServiceDeskLite/pull/233))
- Add the active agent roster to the chat system prompt for each request. ([#221](https://github.com/goldbarth/ServiceDeskLite/pull/221))
- Enforce one `check_grounding` call through `tool_choice` after passages are retrieved. ([#218](https://github.com/goldbarth/ServiceDeskLite/pull/218))
- Add `Theme/DesignTokens.cs` as the shared source for palette, spacing, radius, elevation, and semantic chip colours. ([#213](https://github.com/goldbarth/ServiceDeskLite/pull/213))

### Fixed

- Fix board card titles to clamp at two lines by wrapping the title link in `board-card__title-row`. ([#240](https://github.com/goldbarth/ServiceDeskLite/pull/240))
- Fix the assistant composer layout by targeting the panel with `::deep .assistant-chat`. ([#239](https://github.com/goldbarth/ServiceDeskLite/pull/239))
- Fix the `Category` header overlap by assigning the column a width and using `tickets-table__label`. ([#238](https://github.com/goldbarth/ServiceDeskLite/pull/238))
- Add system-prompt policies that prevent unverified write claims and needless confirmation requests. ([#223](https://github.com/goldbarth/ServiceDeskLite/pull/223))
- Fix summary timestamps to use `Anthropic:UserTimeZone`. ([#222](https://github.com/goldbarth/ServiceDeskLite/pull/222))
- Fix failed `search_knowledge_base` calls to return `IsError: true` while preserving the non-error unavailable path. ([#220](https://github.com/goldbarth/ServiceDeskLite/pull/220))
- Add `SemanticGroundingEvaluator` to score grounding by semantic similarity, with `LexicalGroundingEvaluator` as the fallback. ([#219](https://github.com/goldbarth/ServiceDeskLite/pull/219))

--- Customer ---

### What's New

- **Inline citation badges:** Citation badges now appear beside cited passages in sanitized assistant answers, with details available on hover or keyboard focus and matching numbers in the Sources list. Citations whose titles are not quoted exactly remain in the Sources list, so you can still find every cited source.
- **Suggested ticket actions:** The first actionable suggested step now appears as the primary control in the ticket header, while remaining suggestions are available from the overflow menu. You can act on a recommendation directly, and the existing ticket controls remain available when there are no actionable suggestions.
- **Command palette:** A command palette now opens from any page with Ctrl+K or Cmd+K and lets you search tickets or open navigation destinations by keyboard. You can move through results with the arrow keys, open one with Enter, and close with Esc while returning focus to its previous location.
- **Immediate status changes:** Ticket status changes now appear immediately on the board and detail view, and rejected changes return to the exact previous state with the error code shown in a notification. You can rely on rapid changes reconciling with the latest status accepted by the server.
- **Inline ticket editing:** Status and assignee changes now open in popovers within the ticket header instead of dialogs. You can update either field while keeping the ticket open on the same tab and at the same scroll position.
- **Citation previews:** Assistant citations now appear as numbered badges beside matching titles in answer text, with source, heading, and snippet details on hover or keyboard focus. Citations that cannot be placed inline remain in the numbered Sources list, and answers without citations remain unchanged.
- **Agent roster awareness:** The assistant now receives the active agent roster on every chat request, including when the roster is empty. You can rely on it being instructed to use exact roster names and list valid agents instead of inventing or approximating a name.
- **Grounding checks:** Answers based on retrieved knowledge-base passages now undergo at least one grounding check before the first response text is streamed. This applies to the interactive assistant and autonomous worker, so you can rely on the check being required even when the model does not initiate it.
- **Consistent visual styling:** Spacing, corner radius, elevation, colors, and semantic chip styles now use one shared design scale throughout the interface. You can rely on status and priority styling remaining consistent across the queue, board, and ticket details.

### What's Changed

- **Frontend redesign release:** The complete M9 Frontend Redesign is now integrated into the v1.9.0 release, including Markdown assistant answers and the saved-view query updates. You can rely on these changes being available together from one release point.

### Bug Fixes

- **Board card titles:** Long ticket titles on board cards could grow without limit instead of stopping after two lines. They now remain within two lines with an ellipsis, so cards keep a bounded and consistent height.
- **Assistant send button:** The assistant send button could sit flush with or extend over the panel edge because the panel layout was not applied. It now stays inside the panel and aligned with the input at narrow and wide widths.
- **Ticket queue headers:** The Category header in the ticket queue could overlap Due and appear in a different case from neighboring headers. The two headers now remain aligned side by side, and Category matches the surrounding uppercase labels.
- **Assistant write confirmations:** The assistant could claim a ticket change without a successful tool result or ask again for confirmation after you had already requested the change. It is now instructed to report a change only after confirmed success and to proceed without repeated confirmation unless a genuine user decision is still needed.
- **Summary timestamps:** Ticket summary timestamps could appear in UTC instead of the user timezone shown in ticket details. Created, due, comment, and event times now use the configured user timezone, so summaries and ticket details show matching local times.
- **Knowledge-base search failures:** A technical knowledge-base search failure could be reported as a successful result and treated the same as an unavailable search. Failures are now reported as errors while unavailable searches remain distinct, so dashboard error rates reflect technical failures.
- **Semantic grounding scores:** Grounding checks could mark correct paraphrases and translations as ungrounded because they relied on shared words. Answers are now compared with retrieved passages by meaning when Voyage is available, with the lexical check retained as a fallback, so paraphrases and translations can be recognized as supported.
