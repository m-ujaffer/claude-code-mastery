# taskforge-toolkit

The TaskForge team's Claude Code workflow, packaged as a plugin.

| Component | Type | What it does |
|---|---|---|
| `/taskforge-toolkit:tf-issue TF-###` | skill (manual) | Implements a backlog issue test-first, stopping early if it's already done |
| `/taskforge-toolkit:review-diff` | command | Read-only review of the current diff against the team checklist |
| `block-dangerous.py` | PreToolUse hook | Blocks `rm -rf`, force pushes, hard resets, `curl \| sh` and reading `.env` files |

## Install

```bash
claude plugin marketplace add <owner>/<repo>      # the repo containing .claude-plugin/marketplace.json
claude plugin install taskforge-toolkit@taskforge-team
```

Try it locally without installing: `claude --plugin-dir ./plugins/taskforge-toolkit`

## Develop

`claude plugin validate ./plugins/taskforge-toolkit` before every PR. Bump `version` in
`.claude-plugin/plugin.json` when behaviour changes.
