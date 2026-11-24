# Week 2 · Day 9: Git and GitHub workflow (TF-105)

| | |
|---|---|
| **Level** | Intermediate |
| **CCA-F domain** | 2 · Claude Code configuration & workflows |
| **Time** | 5 min read · 40 min hands-on · 10 min verify & reflect · 5 min log |
| **Budget cap** | $0.80 |
| **Check** | `uv run labcheck w2d9` |

## 🎯 Goal

Run the whole branch → commit → PR → CI → merge loop with Claude as your git co-pilot, and
practise reviewing what it does to your history.

## 📖 Primer

Claude Code is very good at git: it writes commit messages from diffs, creates PRs with `gh`,
resolves conflicts and reads CI failures. Your job is to keep the history **reviewable**:
small commits, honest messages, no force-pushes to shared branches.

Read [Guide 02](../guides/02_git_and_github.md) if git isn't second nature yet.

## 🛠️ Steps

Read **TF-105** in [ISSUES.md](../practice-app/ISSUES.md). Make sure Days 6–8 are committed and pushed:
`git status`, then `git push`. You should be on your personal branch (`git branch --show-current`).

> **Branches in the shared course repo.** Your personal branch (`jane-doe`) plays the role that `main` plays in a
> normal team repo. Feature branches start from it and PRs merge back **into it**, never into `main`. Prefix
> feature branches with your name (`jane-doe-tf-105`) so they don't clash with other learners'.

**1. Branch.** Start `claude` (`/clear` if needed):

> Create a branch named `<my current branch>-tf-105` (for example jane-doe-tf-105) from my current branch.

**2. Implement test-first** (you know the drill):

> Implement TF-105 from @practice-app/ISSUES.md. Tests first in practice-app/tests, including
> "editing a done task doesn't change completed_at". Use clock.now(). Run the suite.

**3. Commit in two logical commits.**

> Make two commits: first the failing tests (test: ...), then the implementation
> (feat(tasks): ... (TF-105)). Use Conventional Commits.

Check with `!git log --oneline -5`. Are the messages accurate?

**4. Push and open a PR.**

> Push the branch and open a pull request with gh **into my personal branch** (`--base jane-doe`, not main).
> The description should summarise the change, list the acceptance criteria from TF-105 as a checklist,
> and explain how it was tested.

Open the PR in the browser (`!gh pr view --web`). The **tests** workflow in `.github/workflows/tests.yml`
runs on it.

**5. Make CI fail on purpose** to practise diagnosis. Add an unused import to `services.py`, commit and push.
When CI goes red:

> CI is failing on my PR. Use gh to read the failing job's logs, explain the cause, fix it, and push.

**6. Merge** when green:

> Squash-merge the PR with gh and delete the feature branch, then switch back to my personal branch and pull.

(Squash-merging gives you one commit on your personal branch. The individual commits are still visible on the PR.)

## ✅ Checkpoint

```bash
uv run labcheck w2d9
```

## 💰 Budget & cost log

Cap: **$0.80**.

```bash
uv run labcheck log w2d9 0.70 "TF-105 PR flow"
```

## 📤 Push your progress

```bash
git add -A && git commit -m "w2d9: Git and GitHub workflow (TF-105)" && git push
```

## 🚀 Stretch

- **Merge conflict drill:** create two branches that both edit the same line of `README.md`,
  merge one, then ask Claude to resolve the conflict in the other. Review its resolution carefully.
- Ask Claude to write a `.github/pull_request_template.md` that matches your team's needs.

## 💼 Commercial application

Most of an engineer's "git time" is mechanical: messages, PR descriptions, CI log spelunking.
Delegating that, while keeping a human review of the history, is one of the most reliable
productivity wins teams report.

## 🤔 Reflect

1. Was Claude's PR description accurate? What would you edit before asking a colleague to review?
2. How did Claude find the CI failure? Which `gh` commands did it use?
3. Why split tests and implementation into separate commits?

## ➡️ Next

[Day 10: TDD with Claude](5_lab5_tdd.md)
