---
title: Release 1.9.0
description: Release v1.9.0 ships with the badge feature complete, includes new functionality for inline citation badges, primary action buttons, and a command palette, along with design tokens and bug fixes.
publishedAt: 2026-07-14
---

### What's New

- **Saving over a network drive:** A document saved to a network drive could lose the changes made while the connection dropped. Every change is kept now, so you no longer have to keep a local copy open as a backup while you work.
- **Primary action button:** The most likely next step should be a button that runs it. A ticket with no suggestions falls back to the current generic action, with no empty button. The action goes through the same command handler the manual path uses - no new automation, no new endpoint.
- **Command palette on Ctrl+K:** A keyboard-first command palette that opens over any page, anchored on the power-user Ctrl/Cmd+K chord. The palette opens from every page and does not swallow the browser shortcut when a text field has focus (capture-phase handler intercepts only Ctrl/Cmd+K).
- **Optimistic status updates:** Every status change waited for the full server round trip; on the Kanban board the dragged card snapped back to its source column until the API answered. Status now renders immediately and reconciles with the server afterwards.
- **Inline status and assignee edit:** Changing status or assignee never navigates or opens a modal. Scroll position and any open tab survive the change (only in-place state updates).
- **Inline citation badges with hover preview:** Citations render as inline badges where the model anchored them. An answer without citations renders unchanged, with no empty sources block.
- **Inject agent roster into system prompt:** The model can name the valid agents without a failed assign_ticket call first (roster is in the system prompt of every chat request).
- **Enforce grounding check via tool_choice:** check_grounding was the only safety property in the assistant phrased as a prompt request. AgentLoop forces check_grounding through tool_choice once IRagRetrievalContext holds passages and no check has run this run.
- **Design tokens - one scale for spacing, radius, elevation, and semantic color:** Theme/DesignTokens.cs is now the single source for the palette, the spacing and radius scales, elevation, and the semantic chip colours. All 16 scoped stylesheets and wwwroot/app.css read from the tokens.

### What's Changed

- **Release v1.9.0:** Integrates the complete M9 - Frontend Redesign milestone into main and adds the v1.9.0 release notes, so the release can be tagged from a single coherent point.

### Bug Fixes

- **Wrap board card title:** A title longer than two lines is clamped to two, with an ellipsis. Cards in a lane keep a consistent height.
- **Keep send button inside panel:** The send button sits within the composer panel's bounds. The input and the button stay aligned at narrow widths.
- **Stop category header overlapping due:** Category no longer overlaps DUE at a 1600px viewport. Category matches its neighbours (uppercase) and is deliberately not a sort label.
- **Write-honesty and confirmation policy:** Write honesty: never state a change happened unless the tool call was made and its result reported success in this conversation. No needless confirmation: when the user already asked for a change, make it - no re-asking.
- **Render summary timestamps in user timezone:** Summary timestamps are rendered in Anthropic:UserTimeZone, matching the ticket detail view. A regression test pins a fixed timezone (Europe/Berlin) and replays the field case: 10:07 UTC renders as 12:07.
- **Report failed knowledge-base search as error:** The catch branch returns IsError: true, distinct from the honest unavailable degradation path (still IsError: false). The error flag flows to the dashboard (the invocation records result.IsError).
- **Score grounding by meaning:** Score grounding by meaning, not word overlap. SemanticGroundingEvaluator embeds each substantive answer sentence with the retrieved passages in one Voyage call and scores each sentence by cosine similarity to its nearest passage.
