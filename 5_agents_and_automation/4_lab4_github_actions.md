# Week 5 · Day 24: Claude in CI with GitHub Actions

| | |
|---|---|
| **Level** | Advanced |
| **CCA-F domain** | 2 · Claude Code configuration & workflows |
| **Time** | 10 min read · 35 min hands-on · 10 min verify & reflect · 5 min log |
| **Budget cap** | $1.20 (including CI runs) |
| **Check** | `uv run labcheck w5d24` |

## 🎯 Goal

Add an automated Claude review to pull requests, plus an `@claude` helper, with the guards that stop CI from
quietly spending your budget.

## 📖 Primer

`anthropics/claude-code-action@v1` runs Claude Code inside a GitHub Actions job. Key inputs:

| Input | Use |
|---|---|
| `anthropic_api_key` | `${{ secrets.ANTHROPIC_API_KEY }}`, never inline |
| `prompt` | the task for automated runs. Omit it for interactive `@claude` mode |
| `claude_args` | CLI flags: `--max-turns 5 --model sonnet --allowedTools "..."` |
| `trigger_phrase` | default `@claude` |

**Cost and safety controls you must add:**
- **Path filters**: only run when `practice-app/**` changes
- **`if:` guards**: skip drafts; only respond to `@claude` from trusted authors
- **`concurrency`** with `cancel-in-progress`: a new push cancels the old review
- **`timeout-minutes`** and **`--max-turns`**
- **Minimal `permissions:`**: read contents, write PR comments, nothing more

## 🛠️ Steps

**1. Connect GitHub to Claude.** The simplest path is to run `/install-github-app` inside `claude` and follow
the prompts. It installs the Claude GitHub App on your repo and can store the API key secret for you. If that's not
possible in your org, follow the manual steps on the docs' *GitHub Actions* page: install the app, then add
`ANTHROPIC_API_KEY` under **Settings → Secrets and variables → Actions**.

> Your course key's $30 cap applies to CI too. That's why the guards below aren't optional.

**2. Write the workflow.** Ask Claude to create `.github/workflows/claude-review.yml` to this spec, then review it:

- triggers: `pull_request` (types opened, synchronize, ready_for_review) with `paths: ["practice-app/**"]`,
  and `issue_comment` (created)
- top-level `concurrency` group per PR or issue number with `cancel-in-progress: true`
- job **review**: `if:` PR event and not draft. `timeout-minutes: 10`. Permissions: `contents: read`,
  `pull-requests: write`, `id-token: write`. Steps: checkout with `fetch-depth: 1`, then `anthropics/claude-code-action@v1`
  with a `prompt` asking for a review against `CLAUDE.md` and `practice-app/ISSUES.md` (risks first, at most 5
  findings, one summary comment), and `claude_args: "--max-turns 5 --model sonnet"`
- job **assist**: `if:` the comment is on a PR, contains `@claude`, and `author_association == 'OWNER'`.
  No `prompt` (interactive mode). `claude_args: "--max-turns 8"`

**3. Push it, then open a PR that should trigger it.** For example, ask Claude to make a small improvement to
`practice-app/src/taskforge/api/projects.py` on a new branch, then `gh pr create --fill`.

**4. Watch it.** `gh pr checks --watch`, then read the review comment on the PR. Is it useful? Is it too noisy?

**5. Try `@claude`.** Comment on the PR: `@claude add a test for the change in this PR`. Watch the run, then review
the commit it pushes **before** merging.

**6. Check the cost.** Your CI runs show up in the Console (via your admin) rather than in your status line.
Estimate from the run logs (look for the cost summary) and log it.

## ✅ Checkpoint

```bash
uv run labcheck w5d24
```

## 💰 Budget & cost log

Cap: **$1.20** including CI.

```bash
uv run labcheck log w5d24 0.90 "CI review + @claude"
```

## 🚀 Stretch

- Make the review job post **inline** comments only for high-severity findings.
- Add a scheduled workflow (`on: schedule`) that runs your Day 23 nightly report. Think hard about the cost
  before enabling it, and set a tight `--max-budget-usd`.

## 💼 Commercial application

Automated first-pass review is one of the most widely adopted agent use cases: humans focus on design and
intent while Claude catches the mechanical issues. The organisations that succeed with it treat the workflow like
any other production system: guarded, observable, cost-capped and tuned to avoid noise.

## 🤔 Reflect

1. Which guard would have saved the most money if you'd left it out?
2. Why restrict `@claude` to trusted authors on a public repo?
3. Was the automated review signal or noise? What would you change in the prompt?

## ➡️ Next

[Day 25: Reliability on long tasks](5_lab5_long_task_reliability.md)
