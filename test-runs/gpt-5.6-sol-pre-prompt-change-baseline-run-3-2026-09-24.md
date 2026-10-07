gpt-5.6-sol-pre-prompt-change-baseline-run-3-2026-09-24, rendered by Chartula from v1.9.0

--- Technical ---

### Changed

- Add the complete `M9 - Frontend Redesign` milestone and v1.9.0 release notes to `main`. ([#244](https://github.com/goldbarth/ServiceDeskLite/pull/244))

### Added

- Add inline citation badges anchored within sanitized assistant Markdown answers. ([#245](https://github.com/goldbarth/ServiceDeskLite/pull/245))
- Add a primary ticket action based on the first actionable `SuggestedNextSteps` entry. ([#237](https://github.com/goldbarth/ServiceDeskLite/pull/237))
- Add a keyboard-operated command palette available from every page through `Ctrl/Cmd+K`. ([#236](https://github.com/goldbarth/ServiceDeskLite/pull/236))
- Add optimistic ticket status updates with rollback on board and detail views. ([#235](https://github.com/goldbarth/ServiceDeskLite/pull/235))
- Replace status and assignee dialogs with inline popovers that update the open ticket in place. ([#234](https://github.com/goldbarth/ServiceDeskLite/pull/234))
- Add inline assistant citation badges with hover and keyboard-focus previews. ([#233](https://github.com/goldbarth/ServiceDeskLite/pull/233))
- Add the active agent roster to the chat system prompt for each request. ([#221](https://github.com/goldbarth/ServiceDeskLite/pull/221))
- Enforce one `check_grounding` call through `tool_choice` after retrieval when no check has run. ([#218](https://github.com/goldbarth/ServiceDeskLite/pull/218))
- Add `Theme/DesignTokens.cs` as the single source for spacing, radius, elevation, palette, and semantic chip colors. ([#213](https://github.com/goldbarth/ServiceDeskLite/pull/213))

### Fixed

- Fix board card titles to clamp at two lines by wrapping the title link in `board-card__title-row`. ([#240](https://github.com/goldbarth/ServiceDeskLite/pull/240))
- Fix the assistant composer layout by targeting `.assistant-chat` through `::deep .assistant-chat`. ([#239](https://github.com/goldbarth/ServiceDeskLite/pull/239))
- Fix the `Category` ticket queue header width and styling so it no longer overlaps `Due`. ([#238](https://github.com/goldbarth/ServiceDeskLite/pull/238))
- Add system-prompt policies that prohibit unverified write claims and unnecessary confirmations. ([#223](https://github.com/goldbarth/ServiceDeskLite/pull/223))
- Fix summary timestamps to render in `Anthropic:UserTimeZone`. ([#222](https://github.com/goldbarth/ServiceDeskLite/pull/222))
- Fix failed `search_knowledge_base` operations to return `IsError: true`. ([#220](https://github.com/goldbarth/ServiceDeskLite/pull/220))
- Add `SemanticGroundingEvaluator` to score grounding by embedding similarity, with `LexicalGroundingEvaluator` as the fallback. ([#219](https://github.com/goldbarth/ServiceDeskLite/pull/219))

--- Customer ---

### What's New

- **Inline citation badges:** Assistant answers can now show numbered citation badges beside cited passages in sanitized Markdown, with source details on hover or keyboard focus. Badge numbers match the Sources list, and citations that cannot be placed inline remain in that list so you can still find every source.
- **Suggested ticket actions:** The first actionable suggested step now appears as the primary ticket control, while remaining suggestions are available from the overflow menu. You can carry out suggested status changes or assignments directly, and the existing ticket controls remain available when no suggestion applies.
- **Command palette:** You can now press Ctrl+K or Cmd+K from any page to open a command palette for navigation and ticket search. Use the arrow keys and Enter to open a result, or press Esc to close the palette and return focus to where it was.
- **Immediate status updates:** Ticket status changes now appear immediately on the board and ticket detail view while the server processes them. You can rely on rejected changes returning to the previous status with an error code, while rapid changes reconcile to the latest server-approved state.
- **Inline ticket editing:** Changing a ticket’s status or assignee now happens in menus within the ticket header instead of dialogs. You can make either change without leaving the ticket or losing your scroll position or open tab.
- **Assistant citation previews:** Assistant citations can now appear as numbered badges beside the text they support, with source, heading, and snippet details available on hover or keyboard focus. Citations that cannot be placed inline remain in the numbered Sources list, and answers without citations remain unchanged.
- **Assistant agent roster:** The assistant can now name the active agents when handling assignment requests. You can rely on it to use exact roster names and list valid agents instead of inventing or approximating a name that is not present.
- **Grounding checks:** Answers based on retrieved knowledge now receive at least one grounding check before their first streamed text, for both the interactive assistant and autonomous worker. You can rely on the check being enforced even when the model does not request it itself.
- **Consistent visual styling:** Spacing, corner radius, elevation, colors, and status and priority chips now use one shared design scale across the interface. You can rely on these visual styles remaining consistent between the queue, board, ticket details, and other pages.

### What's Changed

- **Frontend redesign release:** The complete M9 Frontend Redesign is now integrated into the v1.9.0 release. You can rely on its combined interface changes shipping from one release point.

### Bug Fixes

- **Board card titles:** Long ticket titles on board cards could grow beyond two lines and make cards uneven. Titles now stay within two lines with an ellipsis, so you no longer have to work around unbounded card heights or stretched lane columns.
- **Assistant send button:** The assistant send button could sit flush against or over the edge of its panel, particularly at narrow widths. The composer now remains inset and aligned within the panel, so you no longer have to adjust the page width to keep its controls in place.
- **Ticket queue headers:** The Category header in the ticket queue could overlap Due and appear in a different case from neighboring headers. The columns now remain aligned and readable side by side, so you no longer have to interpret the combined “CategoryUE” heading.
- **Assistant change confirmations:** The assistant could claim a change succeeded without a successful tool result or ask you to reconfirm a change you had already requested. You can now rely on it to report writes only after success and proceed without repeated confirmation unless a genuine decision or missing detail remains.
- **Summary timestamps:** Ticket summaries could show timestamps in UTC instead of the user timezone used by the ticket detail view. Summary dates and times now use the configured user timezone and include its offset, so you no longer have to reconcile conflicting times.
- **Knowledge-base search failures:** A failed knowledge-base search could be reported as a successful tool result and counted as healthy. Technical failures are now recorded as errors and remain distinct from an unavailable knowledge base, so you can rely on the dashboard error rate reflecting them.
- **Grounding by meaning:** Grounding checks could mark correct paraphrases, translations, and requested hedged answers as ungrounded because they relied on matching words. Checks now compare answer meaning with retrieved passages, with the previous word-based method retained as a fallback, so you can rely on supported answers being recognized across different wording and languages.
