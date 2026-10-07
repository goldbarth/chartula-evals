gpt-5.6-sol-pre-prompt-change-baseline-run-1-2026-09-24, rendered by Chartula from v1.9.0

--- Technical ---

### Changed

- Add the complete M9 Frontend Redesign milestone and the v1.9.0 release notes to `main`. ([#244](https://github.com/goldbarth/ServiceDeskLite/pull/244))

### Added

- Add inline citation badges anchored in sanitized Markdown answers, with hover and focus tooltips and unanchored citations retained in the sources list. ([#245](https://github.com/goldbarth/ServiceDeskLite/pull/245))
- Add a primary ticket action derived from the first actionable `SuggestedNextSteps` entry, with remaining steps available from an overflow menu. ([#237](https://github.com/goldbarth/ServiceDeskLite/pull/237))
- Add a keyboard-operated `CommandPalette` that opens from every page with `Ctrl/Cmd+K` and provides navigation and debounced, cancellable ticket search. ([#236](https://github.com/goldbarth/ServiceDeskLite/pull/236))
- Add optimistic status updates with rollback and concurrency handling to the ticket board and detail view. ([#235](https://github.com/goldbarth/ServiceDeskLite/pull/235))
- Replace status and assignee dialogs with inline `MudMenu` popovers that preserve the current ticket view. ([#234](https://github.com/goldbarth/ServiceDeskLite/pull/234))
- Add inline citation badges with hover and keyboard-focus previews to assistant answers, while retaining unanchored citations in the numbered sources list. ([#233](https://github.com/goldbarth/ServiceDeskLite/pull/233))
- Add the active agent roster to the chat system prompt through `GetAgentsHandler` so assignments use valid names. ([#221](https://github.com/goldbarth/ServiceDeskLite/pull/221))
- Enforce one `check_grounding` call through `tool_choice` after retrieval and before the first streamed token. ([#218](https://github.com/goldbarth/ServiceDeskLite/pull/218))
- Add centralized design tokens in `Theme/DesignTokens.cs` for color, spacing, radius, elevation, and semantic chip colors. ([#213](https://github.com/goldbarth/ServiceDeskLite/pull/213))

### Fixed

- Fix board card title clamping by wrapping the title link in `board-card__title-row` and allowing long titles to shrink. ([#240](https://github.com/goldbarth/ServiceDeskLite/pull/240))
- Fix the assistant composer layout by targeting the `MudPaper` panel with `::deep .assistant-chat`, keeping the send button inside the panel. ([#239](https://github.com/goldbarth/ServiceDeskLite/pull/239))
- Fix the ticket queue `Category` header overlap by assigning the column a width and using the same uppercase label styling as neighboring headers. ([#238](https://github.com/goldbarth/ServiceDeskLite/pull/238))
- Add system-prompt rules that prohibit unverified write claims and avoid unnecessary confirmation of requested changes. ([#223](https://github.com/goldbarth/ServiceDeskLite/pull/223))
- Fix `BuildTicketPrompt` to render created, due, comment, and event timestamps in `Anthropic:UserTimeZone`. ([#222](https://github.com/goldbarth/ServiceDeskLite/pull/222))
- Fix `search_knowledge_base` to return `IsError: true` for technical failures while preserving the non-error unavailable path. ([#220](https://github.com/goldbarth/ServiceDeskLite/pull/220))
- Add `SemanticGroundingEvaluator` to score substantive answer sentences by embedding similarity, with `LexicalGroundingEvaluator` as the fallback. ([#219](https://github.com/goldbarth/ServiceDeskLite/pull/219))

--- Customer ---

### What's New

- **Citations in Markdown answers:** Citation badges now appear after cited passage titles in sanitized Markdown answers, with matching numbers in the Sources list and source details on hover or focus. Citations that cannot be placed inline remain in the Sources list, so you can still find every source without matching evidence manually.
- **Suggested ticket actions:** The first actionable suggested step now appears as the primary control in the ticket header, while remaining suggestions are available in the overflow menu. You can act on status and assignment suggestions directly, and tickets without actionable suggestions retain the existing controls.
- **Command palette:** Press Ctrl+K or Cmd+K from any page to open a command palette for navigation and ticket search. You can use the arrow keys and Enter to open a result, then press Esc to close the palette and return focus to where it was.
- **Immediate status updates:** Ticket status changes now appear immediately on the board and ticket detail view, and rejected changes return to the previous status with an error code. You can make rapid status changes without waiting for each response or manually restoring a rejected move.
- **Inline ticket editing:** Status and assignee choices now open in the ticket header instead of in dialogs. You can change either value while keeping the ticket open on the same tab and at the same scroll position.
- **Assistant citation badges:** Citations now appear as numbered badges beside the passage titles they support in assistant answers, with source, heading, and snippet details available on hover or keyboard focus. Citations that cannot be placed inline remain in the numbered Sources list, so you can still review every source.
- **Assistant agent roster:** The assistant now receives the active agent roster with each chat request. It can name valid agents without first attempting an assignment, and it lists valid choices instead of inventing or approximating a name that is not on the roster.
- **Grounding checks:** Assistant and autonomous worker answers based on retrieved passages now undergo at least one grounding check before the first response text is streamed. You can rely on retrieved answers being checked even when the model does not initiate the check itself.
- **Consistent visual styles:** Spacing, corner radius, elevation, colors, and semantic chip styles now use one shared design scale across the interface. You can rely on status and priority styling remaining consistent between the queue, board, and ticket detail views.

### What's Changed

- **Frontend redesign release:** Version 1.9.0 brings the complete M9 Frontend Redesign into one release, including Markdown assistant answers, saved-view query parameters, suppressed grounding transcript entries, and the dark-mode toggle. You can rely on these frontend changes shipping together from the same release point.

### Bug Fixes

- **Board card titles:** Long ticket titles on board cards could grow beyond two lines and expand their cards. Titles now remain at two lines with an ellipsis, so you no longer have to work around inconsistent card heights or lane widths.
- **Assistant composer layout:** The assistant send button could sit flush against or over the panel edge, and the intended panel layout did not apply. The composer now stays inset and aligned at narrow and wide widths, so you no longer have to adjust the page width to use it cleanly.
- **Ticket queue headers:** The Category header could overlap Due in the ticket queue and appeared in a different case from neighboring headers. The columns now remain aligned and display side by side, so you no longer have to interpret the merged “CategoryUE” heading.
- **Assistant write confirmations:** The assistant now reports a change only after its tool call succeeds, and it does not ask you to reconfirm a change you already requested. It asks before writing only when a genuine decision remains, so you can rely on confirmations reflecting completed actions without unnecessary repeated prompts.
- **Summary timestamps:** Ticket summaries could show timestamps in UTC while the ticket detail view showed local time. Summary creation, due, comment, and event times now use the configured user timezone, so you no longer have to reconcile conflicting times between the summary and ticket view.
- **Knowledge-base search errors:** A failed knowledge-base search could appear as a successful result and look the same as an unavailable search. Technical failures now count as errors while unavailable searches remain a separate outcome, so you can rely on the dashboard error rate reflecting actual failures.
- **Semantic grounding scores:** Grounding checks could mark correct paraphrases, translations, and requested hedging as ungrounded because they used different words from the source. Answers are now compared with retrieved passages by meaning when Voyage is available, with the word-overlap check retained as a fallback, so you no longer have to treat those wording differences as unsupported by default.
