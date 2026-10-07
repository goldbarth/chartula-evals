gpt-5.6-sol-pre-prompt-change-baseline-run-2-2026-09-24, rendered by Chartula from v1.9.0

--- Technical ---

### Changed

- Add the complete `M9 - Frontend Redesign` milestone and v1.9.0 release notes to `main`. ([#244](https://github.com/goldbarth/ServiceDeskLite/pull/244))

### Added

- Add inline citation badges to sanitized Markdown answers through `AssistantMarkdown.Render(markdown, citations)`. ([#245](https://github.com/goldbarth/ServiceDeskLite/pull/245))
- Add a primary ticket action based on the first actionable `SuggestedNextSteps` entry. ([#237](https://github.com/goldbarth/ServiceDeskLite/pull/237))
- Add a keyboard-operated `CommandPalette` that opens from every page with `Ctrl/Cmd+K`. ([#236](https://github.com/goldbarth/ServiceDeskLite/pull/236))
- Add optimistic status updates with rollback and concurrency handling to ticket board and detail views. ([#235](https://github.com/goldbarth/ServiceDeskLite/pull/235))
- Remove `AssignTicketDialog.razor` and `ChangeStatusDialog.razor` in favor of inline status and assignee popovers. ([#234](https://github.com/goldbarth/ServiceDeskLite/pull/234))
- Add inline citation badges with hover and keyboard-focus previews to assistant answers. ([#233](https://github.com/goldbarth/ServiceDeskLite/pull/233))
- Add the active agent roster to the chat system prompt through `GetAgentsHandler`. ([#221](https://github.com/goldbarth/ServiceDeskLite/pull/221))
- Send a forced `check_grounding` `tool_choice` before streaming a retrieved-knowledge answer when no check has run. ([#218](https://github.com/goldbarth/ServiceDeskLite/pull/218))
- Add `Theme/DesignTokens.cs` as the shared source for spacing, radius, elevation, palette, and semantic colors. ([#213](https://github.com/goldbarth/ServiceDeskLite/pull/213))

### Fixed

- Fix two-line board title clamping by wrapping the title in `board-card__title-row`. ([#240](https://github.com/goldbarth/ServiceDeskLite/pull/240))
- Fix the assistant composer layout by targeting `.assistant-chat` through `::deep .assistant-chat`. ([#239](https://github.com/goldbarth/ServiceDeskLite/pull/239))
- Fix the `Category` header overlap by assigning its column a `140px` width and using `tickets-table__label`. ([#238](https://github.com/goldbarth/ServiceDeskLite/pull/238))
- Add system-prompt rules that require successful tool results before claiming writes and prevent unnecessary confirmations. ([#223](https://github.com/goldbarth/ServiceDeskLite/pull/223))
- Fix summary timestamps by converting them to `Anthropic:UserTimeZone` in `BuildTicketPrompt`. ([#222](https://github.com/goldbarth/ServiceDeskLite/pull/222))
- Fix failed `search_knowledge_base` operations to return `IsError: true` while preserving the non-error unavailable path. ([#220](https://github.com/goldbarth/ServiceDeskLite/pull/220))
- Add `SemanticGroundingEvaluator` to score substantive answer sentences by semantic similarity, with `LexicalGroundingEvaluator` as the fallback. ([#219](https://github.com/goldbarth/ServiceDeskLite/pull/219))

--- Customer ---

### What's New

- **Inline citation badges:** Citation badges now appear beside cited passages in sanitized Markdown answers, with hover or focus previews and matching numbers in the Sources list. Citations whose titles do not appear in the answer remain in the Sources list, so you can still find every cited source.
- **Suggested ticket actions:** The first actionable suggested step now appears as the primary control in the ticket header, while remaining suggestions appear in an overflow menu. You can act on the recommendation directly, and the existing ticket controls remain available when there are no actionable suggestions.
- **Command palette:** You can now press Ctrl+K or Cmd+K on any page to search tickets or open navigation destinations. The palette supports arrow keys, Enter, and Esc, so you can use it without leaving the keyboard and return focus to where you started.
- **Immediate status updates:** Ticket status changes now appear immediately on the board and ticket detail page, and rejected changes return to the previous status with an error code. You can rely on rapid changes settling on the status accepted by the server instead of waiting for each response.
- **Inline ticket editing:** Status and assignee changes now open in the ticket header instead of a dialog. You can make either change without leaving the ticket, losing your scroll position, or switching away from the current tab.
- **Assistant citations:** Citations now appear as numbered badges beside the answer text they support, with source, heading, and snippet details available on hover or keyboard focus. Unmatched citations remain in a numbered Sources list, so you can still review them without an empty list appearing on answers that have no citations.
- **Agent roster awareness:** The assistant now receives the active agent roster with each chat request. When you ask it to assign a ticket, you can rely on it to use an exact roster name or list valid agents instead of inventing or approximating one.
- **Grounding checks:** Answers based on knowledge-base passages are now checked for grounding before the first response text is streamed. You can rely on at least one check after retrieval rather than depending on the assistant to perform it voluntarily.
- **Consistent visual styling:** Spacing, corner radius, elevation, semantic colors, and status and priority chip colors now use one shared design scale across the interface. You can rely on the same visual meaning and spacing patterns across the queue, board, ticket details, dashboard, and assistant.

### What's Changed

- **Frontend redesign release:** The complete M9 Frontend Redesign is now integrated into the v1.9.0 release, including Markdown answers, saved-view query parameters, dark mode, and the redesigned ticket and assistant interfaces. You can rely on these changes being available together from one release point.

### Bug Fixes

- **Board card titles:** Long board card titles could grow beyond two lines and stretch their cards or lane columns. Titles now stay within two lines with an ellipsis, so you no longer have to work around inconsistent card heights.
- **Assistant composer layout:** The assistant send button could sit flush with or beyond the panel edge because the panel layout was not applied. The composer now stays inside the panel with its input and button aligned at narrow and wide widths, so you no longer have to adjust the window to use it.
- **Ticket queue headers:** The Category header could overlap Due in the ticket queue and appear in a different case from neighboring headers. The columns now remain aligned with separate uppercase headers, so you no longer have to interpret the merged “CategoryUE” label.
- **Assistant write confirmations:** The assistant now reports a change only after its tool call succeeds and no longer asks you to reconfirm a change you already requested. You can rely on completed-change messages reflecting a successful result while still being asked when a genuine decision or missing detail requires your input.
- **Summary timestamps:** Ticket summaries could show timestamps in UTC instead of the user timezone used by the ticket detail view. Summary dates and times now use the configured user timezone and include its offset, so you no longer have to reconcile conflicting times.
- **Knowledge-base search errors:** A failed knowledge-base search could be reported as a successful result and counted as healthy. Technical failures are now recorded as errors while an unavailable knowledge base remains a separate result, so you can rely on the dashboard error rate to reflect actual search failures.
- **Semantic grounding:** Grounding checks could mark correct paraphrases, translations, and requested hedging as ungrounded because they did not repeat the source wording. Answers are now compared with retrieved passages by meaning when Voyage is available, with the previous word-overlap check as a fallback, so you no longer have to treat those wording differences as unsupported by default.
