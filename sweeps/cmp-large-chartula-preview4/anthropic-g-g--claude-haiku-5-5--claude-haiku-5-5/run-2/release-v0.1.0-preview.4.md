---
title: Release 0.1.0-preview.4
description: "This release reshapes what Chartula writes and how it reports: changelog.json is now published without pull request descriptions, a preview is free, and runs show their progress and summary more clearly."
publishedAt: 2026-10-07
---

### What needs action

- **Breaking:** Pull request descriptions no longer appear in changelog.json, which is now schema version 2 and safe to publish. The complete facts, descriptions included, are kept in the run record under a new facts field. A version 1 consumer that read the description from changelog.json must now read it from the run record.
- **Breaking:** Running preview now makes no model call and needs no API key. It shows each fact with the audiences that carry it, each dropped change with the setting that dropped it, and what generate would send, so you can check the work and the prompt size before spending tokens.

### What's New

- **Clearer run summary:** The first line of a run's summary now states how the run went: generated, generated with review flags, partially generated with the number of failed audiences, or no audience rendered. Each rendering is headed by its audience's name, and the command's header opens stderr and stdout.
- **Easier doctor output:** chartula doctor groups its checks under Repository, Model and GitHub, and marks each as ok, warn, fail or skip. The verdict says whether a run would start, would stop at GitHub write, or would stop, so you know before running generate.
- **Visible progress:** A run now shows its progress on the terminal with an animated spinner for each step, and a finished step stays as a done line. Redirected output, CI and terminals without colour get plain lines, and the --plain option forces that form on any command.
- **Quoted pull request text:** Pull request titles and descriptions are now quoted between tags in the prompt, and descriptions longer than 8,000 characters are cut, so the model treats author text as material to rephrase rather than as instructions. This makes such steering less likely to work, but does not make it impossible.
- **Published releases are protected:** generate now stops before any model call when the release is already published, and tells you the release's link and how to proceed. Pass --replace-published to replace its notes deliberately; drafts from earlier runs are still updated without it.
- **Configuration template link:** When no chartula.yaml is found, chartula doctor now names the link to this version's configuration template, so you can find the file to copy without searching the repository.
- **Progress while a run works:** While a run works, each step is shown as it starts and its elapsed time ticks while a model call runs, so a slow run no longer looks stalled. Without a terminal, each step is one plain line.
- **Setup check with doctor:** chartula doctor checks the setup a run needs, including the token, the model endpoint and the repository, and reports each check as ok, warn or fail before anything is spent. It exits with 1 when a check fails, so CI can run it before generate.
- **Closed issues at every depth:** The closed issue numbers in a change are now read from the title and description at every depth. A rendering that keeps a number such as #12 from Closes #12 is no longer flagged. The depth setting now only controls what the model reads, and the old value still works.
- **Direct commits in the release:** A commit pushed straight to the main branch, outside any pull request, now appears in the release as a change of its own, and merge commits are skipped. The summary states how many commits had no pull request.
- **Version check:** chartula --version now prints the installed version and the build's commit, so you can check which build you are running without starting a run.
- **First tag and large range confirmation:** A first tag now renders from the first commit without any flag. A run that reads a large range, or a first tag, asks you to confirm the range before any request is made, and --yes confirms it up front in CI.

### What's Changed

- **Dependency updates:** Updates the nuget-minor-and-patch dependency group, bringing Anthropic to 12.53.0, coverlet.collector to 10.1.0 and Microsoft.Extensions.AI.OpenAI to 10.10.1.

### Bug Fixes

- **Help lists each option once:** chartula --help now lists each option once, under its group, with --replace-published placed under What a run writes.
- **Fewer false faithfulness flags:** The rule-based faithfulness check now matches names that a description wraps over several lines or that sit inside fenced code blocks, so a rendering that repeats them is no longer flagged. A name the facts do not contain is still flagged.
- **Empty technical release:** A release with nothing for the technical reader now gets a sentence saying so in CHANGELOG.md and the release notes, instead of an empty heading. changelog.json still holds an empty technical rendering.
- **Readable JSON files:** changelog.json and the run record now keep backticks, quotes and non-ASCII characters as written, instead of escaping them, so both files are easier to read.
- **Flags set apart from entries:** The flagged-for-review block of a rendering now stands apart from the last entry with a blank line and its own heading, so a flag no longer looks attached to the entry above it.
- **Header names missing credentials:** The run header now says unauthenticated and names the unset variable when no GitHub token or model key is set, instead of naming a source for a credential the run does not have.
- **Options checked before a run:** An unknown, misplaced or incomplete option now stops the run before anything starts, with a message pointing to chartula --help, and -h or --help after a command shows that command's help.
- **GitHub API URL without slash:** A GitHub API URL written without a trailing slash now works, so requests reach the right endpoint.
- **Empty exclude list:** An empty excludeCategories list in chartula.yaml now drops no category, as the documentation describes, instead of keeping the default Internal exclusion.
- **Clearer unreadable answer error:** A model answer the SDK cannot read is now reported as an unreadable answer that names the value at fault, rather than as an endpoint that could not be reached.
- **Two configuration files refused:** A run now stops with a configuration error when both chartula.yaml and chartula.yml exist in the directory, and names both paths and how to keep one.
- **Token checked before model calls:** generate now checks that the token may publish release notes before any model call, so a token without write access stops the run before it spends tokens.
- **Clearer --no-publish help:** The help for --no-publish now says it writes every file but publishes no GitHub release notes.
