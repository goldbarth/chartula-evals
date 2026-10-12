---
title: Release 0.1.0-preview.4
description: This release makes changelog.json safe to publish, makes preview free, and adds a doctor command and clearer run output.
publishedAt: 2026-10-07
---

### What needs action

- **Breaking:** Changes to a pull request description no longer appear in changelog.json, which is safe to publish. The description is kept in full in the local run record, so you can still read it there.
- **Breaking:** preview now makes no model call and needs no API key, so it shows what generate would send and the facts it would render from without costing anything. Each dropped change is listed with the setting that dropped it.

### What's New

- **Clearer run output:** Each run now opens with a header naming its command, and its summary's first line tells you how the run went: generated, generated with review flags, partially generated, or no audience rendered. Each audience's rendering now sits under its name.
- **Clearer doctor report:** chartula doctor groups its checks under Repository, Model and GitHub, and marks each as ok, warn, fail or skip. Its closing line says whether a run would start, and warnings under GitHub write say whether generate would stop.
- **Run progress and --plain:** Progress is shown as a spinner in a terminal and as plain lines elsewhere. The new --plain option forces plain output on every command.
- **Pull request text is quoted:** Pull request titles and descriptions are now quoted to the model between tags and cut when very long, so text in them is less likely to change what the model writes. This makes injected instructions less likely to work but does not rule them out.
- **Published releases are protected:** generate stops before any model call if the release is already published, unless you pass --replace-published. Your hand-written notes are no longer replaced without you asking.
- **Config template hint:** When chartula.yaml is missing, doctor now names the config template for your installed version, so you can find it without the repository.
- **Steps shown while a run works:** Each step of a run is shown while it works: reading pull requests, rendering each audience, and checking each rendering, with a running count and time.
- **New chartula doctor command:** chartula doctor checks the setup a run needs, such as git, the tag, the repository, the configuration, the model endpoint and GitHub access, before anything is spent. It exits with 1 if a check fails, so a CI job can run it before generate.
- **Closed issues read at every depth:** Closed issue numbers are now read from the text the model reads, at the default depth too, so a rendering that keeps a reference such as #12 from Closes #12 is no longer flagged. Existing configuration values still work.
- **Direct commits are included:** Commits pushed directly to the default branch, with no pull request, now appear in the release as changes of their own. Merge commits without a pull request are skipped, and the run reports how many commits were rendered this way.
- **Version command:** chartula --version prints the installed version and its build, and works from any directory without configuration or a key.
- **First tag and large ranges:** A first tag now renders from the first commit without any flag. Before the run reads GitHub or calls the model, it asks you to confirm a first tag or a range above 200 commits, and --yes confirms it up front.

### What's Changed

- **Dependency updates:** Dependency update: Anthropic and related NuGet packages, minor and patch versions.

### Bug Fixes

- **Help text and roadmap:** chartula --help lists each option once under its group, and the roadmap is current.
- **Fewer false review flags:** The rule-based check no longer flags a name that the facts contain when it is wrapped across lines or sits next to a fenced code block in the rendering.
- **Empty technical release:** A release with nothing for technical readers now says so in CHANGELOG.md and the release notes, instead of an empty heading. changelog.json still holds an empty technical rendering.
- **Readable JSON files:** changelog.json and the run record now keep backticks, quotes and non-ASCII characters readable, escaping only what JSON requires.
- **Flags set apart:** Flags in a rendering are set apart from its last entry under a Flagged for review heading, so they no longer read as part of that entry.
- **Run header for missing credentials:** The run header says unauthenticated, naming the unset variable, when no GitHub token or model key is set, instead of naming a source for it.
- **Option checks:** The CLI now refuses an option a command does not take, or an unknown or incomplete option, before anything starts. --help is honoured after a command name.
- **GitHub API URL:** A GitHub API URL written without a trailing slash now resolves to the right endpoint.
- **Empty exclude list:** An empty excludeCategories list now drops no category, as documented, instead of keeping the default.
- **Unreadable model answers:** A model answer the SDK cannot read is now reported as unreadable, with the value that failed, instead of as an endpoint that could not be reached.
- **Two configuration files refused:** A run now stops with a message if both chartula.yaml and chartula.yml exist, naming both paths, instead of silently ignoring one.
- **Publish check before model calls:** generate now checks that the token may publish release notes before the first model call, so a run that cannot publish stops at once instead of after all its model calls.
- **--no-publish help text:** chartula --help now says that --no-publish writes every file but publishes no GitHub release notes.
