---
description: Review the current git diff against the team checklist (read-only)
allowed-tools: Bash(git diff *), Bash(git diff), Read
---
Run `git diff` and `git diff --staged`. Review the changes against
the checklist in the tf-issue skill folder (${CLAUDE_PLUGIN_ROOT}/skills/tf-issue/checklist.md). Report risks first (with file:line), then nits.
Do not edit any files.
