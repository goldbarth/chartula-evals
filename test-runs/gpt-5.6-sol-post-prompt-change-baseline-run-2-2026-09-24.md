gpt-5.6-sol-post-prompt-change-baseline-run-2-2026-09-24, rendered by Chartula from v1.9.0

--- Technical ---

### Changed

- Add the complete M9 frontend redesign and `v1.9.0` release notes to `main`. ([#244](https://github.com/goldbarth/ServiceDeskLite/pull/244))

### Added

- Add inline citation badges anchored in sanitized Markdown answers, with hover and focus previews and unanchored citations retained in the sources list. ([#245](https://github.com/goldbarth/ServiceDeskLite/pull/245))
- Add a primary ticket action derived from the first actionable `SuggestedNextSteps` entry. ([#237](https://github.com/goldbarth/ServiceDeskLite/pull/237))
- Add a keyboard-operated command palette that opens on `Ctrl/Cmd+K` from every page. ([#236](https://github.com/goldbarth/ServiceDeskLite/pull/236))
- Add optimistic status changes with rollback and concurrency handling on the ticket board and detail view. ([#235](https://github.com/goldbarth/ServiceDeskLite/pull/235))
- Add inline status and assignee popovers in place of `AssignTicketDialog.razor` and `ChangeStatusDialog.razor`. ([#234](https://github.com/goldbarth/ServiceDeskLite/pull/234))
- Add inline citation badges with hover and keyboard-focus previews to assistant answers. ([#233](https://github.com/goldbarth/ServiceDeskLite/pull/233))
- Add the active agent roster to the chat system prompt for each request. ([#221](https://github.com/goldbarth/ServiceDeskLite/pull/221))
- Add a forced `check_grounding` tool choice after retrieval when no grounding check has run. ([#218](https://github.com/goldbarth/ServiceDeskLite/pull/218))
- Add `Theme/DesignTokens.cs` as the shared source for palette, spacing, radius, elevation, and semantic chip colors. ([#213](https://github.com/goldbarth/ServiceDeskLite/pull/213))

### Fixed

- Fix board card title clamping by wrapping the title link so `-webkit-line-clamp` can limit it to two lines. ([#240](https://github.com/goldbarth/ServiceDeskLite/pull/240))
- Fix the assistant composer layout so the send button remains inside its panel. ([#239](https://github.com/goldbarth/ServiceDeskLite/pull/239))
- Fix the ticket queue `Category` header so it no longer overlaps `Due`. ([#238](https://github.com/goldbarth/ServiceDeskLite/pull/238))
- Add system-prompt policies that prevent unsupported write confirmations and unnecessary confirmation requests. ([#223](https://github.com/goldbarth/ServiceDeskLite/pull/223))
- Fix ticket summary timestamps to use `Anthropic:UserTimeZone`. ([#222](https://github.com/goldbarth/ServiceDeskLite/pull/222))
- Fix failed `search_knowledge_base` calls to return `IsError: true` while preserving the non-error unavailable path. ([#220](https://github.com/goldbarth/ServiceDeskLite/pull/220))
- Add `SemanticGroundingEvaluator` to score grounding by semantic similarity, with `LexicalGroundingEvaluator` as the fallback. ([#219](https://github.com/goldbarth/ServiceDeskLite/pull/219))

--- Customer ---

### What's New

- **Inline citation badges:** Assistant answers rendered as Markdown can now show numbered citation badges after cited passage titles, with source details on hover or keyboard focus. Matching numbers stay consistent with the Sources list, while citations that cannot be anchored remain in that list so evidence is still available.
- **Suggested ticket actions:** The first actionable suggested next step now appears as the primary ticket control, with remaining suggestions in an overflow menu. You can rely on status and assignment suggestions to use the same actions as the standard controls, while tickets without actionable suggestions retain the existing controls.
- **Command palette:** You can now open a command palette from any page with Ctrl/Cmd+K to navigate or search for tickets. Arrow keys move through results, Enter opens the selection, and Esc closes the palette and restores your previous focus.
- **Immediate status updates:** Status changes on the board and ticket details now appear immediately, while rejected changes restore the previous status and show the error code. Rapid changes to the same ticket reconcile with the server so you can rely on the displayed status matching an accepted change.
- **Inline ticket editing:** Status and assignee changes now open in popovers on the ticket instead of dialogs. You can apply a change without leaving the ticket, losing your scroll position, or changing the open tab.
- **Citation previews:** Assistant citations can now appear as numbered badges beside the cited answer text, with source, heading, and snippet details available on hover or keyboard focus. Citations that cannot be placed inline remain in the numbered Sources list, and answers without citations remain unchanged.
- **Agent roster guidance:** The assistant now receives the active agent roster with every chat request. When assigning a ticket, you can rely on it to use listed names exactly and present valid agents instead of inventing or approximating a name that is not present.
- **Grounding checks:** After retrieving knowledge-base passages, the assistant and autonomous worker now perform at least one grounding check before streaming an answer unless they have already checked it themselves. You can rely on retrieved answers being checked once during the run before their first streamed text.
- **Consistent visual design:** Spacing, corner radius, elevation, colors, and semantic chip styles now follow one shared design scale across the interface. You can rely on status and priority indicators using consistent styling across the queue, board, and ticket details.

### What's Changed

- **Frontend redesign release:** The complete M9 Frontend Redesign is now integrated into v1.9.0, including Markdown assistant answers, dark mode, saved-view queries, updated ticket pages, and the revised assistant composer. You can rely on these frontend changes being available together from the same release point.

### Bug Fixes

- **Board card titles:** Long ticket titles on board cards could grow without a two-line limit or stretch the lane when they contained unbreakable text. Titles now stay within two lines with an ellipsis, so cards keep a bounded, consistent height.
- **Assistant send button:** The assistant send button could sit flush against or over the panel edge because the panel layout and padding were not applied. The composer now stays inside the panel, with its input and button aligned at narrow and wide widths.
- **Ticket queue headers:** The Category header in the ticket queue could overlap Due and appear in a different case from neighboring headers. Category and Due now remain aligned side by side, and Category uses the same uppercase presentation as the other headers.
- **Assistant write confirmations:** The assistant could claim a ticket change without a successful tool result or ask again after you had already requested the change. You can now rely on it to report writes only after confirmed success and to proceed without needless reconfirmation unless required information or a genuine decision is missing.
- **Summary timestamps:** Ticket summaries could show timestamps in UTC instead of the user timezone used by the ticket details. Summary creation, due, comment, and event times now use the configured user timezone and include its UTC offset, so the summary and ticket view remain consistent.
- **Knowledge-base failures:** A failed knowledge-base search could be reported as a successful result, making a technical failure look like normal unavailability. Technical failures are now recorded as errors while unavailable searches remain a separate non-error result, so dashboard error rates reflect actual failures.
- **Semantic grounding scores:** Correct paraphrases and translations could receive low grounding scores because evaluation depended on shared words with the source. Grounding now compares answer sentences with retrieved passages by meaning, with the previous word-overlap method retained when semantic evaluation is unavailable, so supported paraphrases and translations can be recognized.
