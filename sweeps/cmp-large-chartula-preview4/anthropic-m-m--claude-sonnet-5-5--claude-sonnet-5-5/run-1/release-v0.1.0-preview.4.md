---
title: Release 0.1.0-preview.4
description: This release adds a free preview, a doctor command, run progress and a clearer terminal layout, protects publishing and private descriptions, and fixes several configuration and output problems.
publishedAt: 2026-10-07
---

### What needs action

- **Breaking:** The published changelog.json no longer contains pull request descriptions, so notes written for reviewers or internal links cannot leak when you publish it. The complete facts, descriptions included, are kept in the local run record instead; if you read descriptions from changelog.json, read them from the run record's facts now.
- **Breaking:** preview no longer prints renderings; it shows the facts, which audiences carry each one, what was dropped and why, and what generate would send. It makes no model call and needs no key, so you can check a release for the cost of the GitHub requests only. To see the written prose without publishing, run generate with --no-publish.

### What's New

- **Run summary and help layout:** A run's summary now opens on a line saying how the run went, such as review flags found or audiences that failed, and each rendering sits under its audience name. Commands open with a header and the help is grouped, so you can read the outcome from the first line.
- **Doctor report layout:** chartula doctor now groups its checks under Repository, Model and GitHub and marks each status with a symbol and word. Its closing line says whether a run would start and names a GitHub write warning when generate would stop there, so you can rely on it not promising a run that would stop. Plain output keeps the old columns.
- **Progress spinner and --plain:** A run now shows a spinner on the step it is working on, and finished steps stay listed as done or failed. In terminals that cannot show it, such as redirected output, CI or when you pass --plain, you get plain lines instead, so a slow step no longer looks like a hang.
- **Pull request text quoted for the model:** Pull request titles and descriptions are now marked off as quoted material in what the model reads, and descriptions over 8,000 characters are cut in the prompt only. The model is told to treat that text as material to rephrase, not instructions, which makes text written to steer it less likely to work but does not rule it out.
- **Replacing published releases:** generate on a tag whose release is already published now stops before any model call instead of replacing its notes. It prints the release link and what to do, so hand-written notes are no longer overwritten unasked; pass --replace-published to replace them. doctor warns about this case too.
- **Config template hint:** When doctor finds no chartula.yaml, it now also gives the link to the config template for your installed version. You can start from the template that matches the settings your version accepts.
- **Step progress:** A run now prints each step while it works: reading pull requests, rendering each audience and checking each rendering. You can tell a slow run from a hanging one and no longer need to abort one that is about to finish.
- **chartula doctor:** The new chartula doctor command checks everything a run needs, one line per check, and exits 1 if something would stop a run. You can find setup problems before anything is spent, and run it in CI ahead of generate.
- **Closed issue numbers:** Closed issue numbers, such as the one in Closes #12, are now taken from the same text the model reads, at every depth. A rendering that keeps such a number is no longer flagged at the default depth. The old depth value title-description-and-issues in chartula.yaml still works and reads as title-and-description.
- **Commits without a pull request:** Commits pushed straight to main without a pull request now appear in the release next to the pull requests. Chore and ci pushes are dropped as Internal, and merge commits without a pull request are skipped, so a direct fix no longer ships unmentioned.
- **Version command:** chartula --version now prints the installed version and exits 0, from any directory and without a key or token. You can name the exact build in a bug report.
- **First tag and large ranges:** A first tag now renders from the first commit without a flag, and --whole-history is gone. A first tag or a range above 200 commits asks for confirmation before any GitHub request or model call. Without a terminal the run stops unless you pass --yes, so nothing is spent on a range nobody approved.

### What's Changed

- **Dependency updates:** Dependencies were updated: Anthropic, coverlet.collector and Microsoft.Extensions.AI.OpenAI.

### Bug Fixes

- **Help listing:** chartula --help listed --replace-published under the wrong group and --audience twice. Each option now appears once under its own group, so the help matches what the command accepts.
- **False flags on wrapped names:** The rule-based check flagged names that a description wrapped over two lines or that sat near fenced code blocks, although the facts contained them. Such names are now matched, so you no longer have to dismiss these flags.
- **Releases with nothing technical:** A release with nothing for technical readers used to produce an empty heading in CHANGELOG.md and empty release notes. It now carries the sentence saying the release has no features, fixes, performance improvements or breaking changes, so an empty entry is not mistaken for lost text. The renderings.technical field in changelog.json stays empty.
- **Readable JSON files:** changelog.json and the run record now write backticks and non-ASCII characters as themselves instead of escaped codes. The files are easier to read and diff, and parsers read the same values as before.
- **Flag layout:** Flags printed under a rendering looked like part of its last entry. They now follow a blank line under their own Flagged for review heading, so you can tell they may concern any entry.
- **Credential line in run header:** The run header named GITHUB_TOKEN or the model key as the source even when the variable was unset. It now says unauthenticated and that the variable is not set, so the header agrees with the warning that follows.
- **Option checking:** Commands now refuse options they do not take, misspelled options and options missing a value before anything starts, suggesting the closest option. --help after a command prints help and starts nothing, so a mistyped option such as --nopublish no longer publishes.
- **GitHub API URL:** A GitHub API URL set without a trailing slash, such as an Enterprise address ending in /api/v3, sent requests to the wrong path and failed with a 404. The slash is now added, so either form works.
- **Empty excludeCategories:** Setting filter.excludeCategories to an empty list was ignored, so Internal changes were still dropped. An empty list now drops no category, so you can keep internal work in a release.
- **Unreadable model answers:** An answer the model endpoint returned but the SDK could not read was reported as an unreachable endpoint. It is now reported as an unreadable answer with the offending value, so you no longer have to look for a network problem.
- **Two config files:** With both chartula.yaml and chartula.yml present, the .yml file was silently ignored. The run now stops with an error naming both paths, so you keep one file and delete the other.
- **Publish check up front:** generate with a token that cannot publish used to spend every model call before failing at the end. It now checks the token before the first model call and stops, so a run that could not publish costs nothing. Use --no-publish to write the files without publishing.
- **--no-publish help text:** The help text said --no-publish wrote only some files. It now says every file is written and only the GitHub release notes are not published, matching what the option does.
