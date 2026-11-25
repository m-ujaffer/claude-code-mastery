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

**Supply-chain hardening: pin third-party actions.** `@v1` is a *tag*, and the action's maintainers can move it to new
code at any time. This step receives your API key, so whatever code the tag points to can read that key. In production
workflows, pin the action to a full 40-character commit SHA and keep the tag as a comment:

```yaml
- uses: anthropics/claude-code-action@<40-char-commit-sha> # v1
```

Find the commit the tag currently points to (it's an annotated tag, so use the `^{}` line):

```bash
git ls-remote https://github.com/anthropics/claude-code-action.git 'refs/tags/v1' 'refs/tags/v1^{}'
```

Then let **Dependabot** (`.github/dependabot.yml` with `package-ecosystem: "github-actions"`) or Renovate propose SHA
bumps as reviewable PRs. In this lab, either `@v1` or a pinned SHA passes labcheck.

## 🛠️ Steps

**1. Check the CI connection.** In the shared course repo, your instructor has already installed the Claude GitHub
App and added an `ANTHROPIC_API_KEY` **Actions** secret, backed by a separate, spend-limited CI workspace
(see `setup/ADMIN-api-keys.md`). You don't need to do anything. In your own repos at work, you'd run
`/install-github-app` inside `claude`, or follow the manual steps on the docs' *GitHub Actions* page.

> CI runs are shared across the cohort's CI budget. That's why the guards below aren't optional.

**2. Write the workflow.** Ask Claude to create `.github/workflows/claude-review.yml` to this spec, then review it:

- triggers: `pull_request` (types opened, synchronize, ready_for_review) with `paths: ["practice-app/**"]`,
  and `issue_comment` (created)
- top-level `concurrency` group per PR or issue number with `cancel-in-progress: true`
- job **review**: `if:` PR event and not draft. `timeout-minutes: 10`. Permissions: `contents: read`,
  `pull-requests: write`, `id-token: write`. Steps: checkout with `fetch-depth: 1`, then `anthropics/claude-code-action@v1`
  with a `prompt` asking for a review against `CLAUDE.md` and `practice-app/ISSUES.md` (risks first, at most 5
  findings, one summary comment), and `claude_args: "--max-turns 5 --model sonnet"`
- job **assist**: `if:` the comment is on a PR, contains `@claude`, and the author is trusted
  (`author_association` is `OWNER`, `MEMBER` or `COLLABORATOR`).
  No `prompt` (interactive mode). `claude_args: "--max-turns 8"`

**3. Push it, then open a PR that should trigger it.** Commit the workflow to your personal branch and push. Then
ask Claude to make a small improvement to `practice-app/src/taskforge/api/projects.py` on a new branch named
`<your-branch>-ci-demo`, push it, and open a PR **into your personal branch**:
`gh pr create --fill --base <your-branch>`. For `pull_request` events, GitHub runs the workflow file from the PR
itself, so your new workflow runs even though it isn't on `main`.

**4. Watch it.** `gh pr checks --watch`, then read the review comment on the PR. Is it useful? Is it too noisy?

**5. Merge** the PR into your personal branch once you've read the review (`gh pr merge --squash --delete-branch`),
then `git pull`.

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

## 📤 Push your progress

```bash
git add -A && git commit -m "w5d24: Claude in CI with GitHub Actions" && git push
```

## 🚀 Stretch

- **Why didn't `@claude` work?** Comment `@claude add a test for the change in this PR` on your PR. Nothing happens,
  because `issue_comment` workflows only ever run from the repo's **default branch** (`main`), and your workflow
  lives on your branch. This is a deliberate GitHub security rule: comments can't run workflow code from
  unmerged branches. If your instructor has merged a reference workflow to `main`, try it, then review the commit
  it pushes **before** merging.
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
