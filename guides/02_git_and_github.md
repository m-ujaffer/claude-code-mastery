# Guide 02: Just enough git and GitHub

Claude Code is excellent at git, but **you** need to understand what it's doing so you
can review it. This is the minimum.

## The mental model

```
working tree  --git add-->  staging area  --git commit-->  local history  --git push-->  GitHub
```

## Everyday commands

```bash
git status                       # what's changed?
git diff                         # what exactly changed (unstaged)?
git diff --staged                # what's about to be committed?
git switch -c feature/tf-105     # new branch
git add -A && git commit -m "feat(tasks): record completed_at (TF-105)"
git push -u origin HEAD          # publish the branch
git log --oneline --graph -15    # recent history
git switch main && git pull      # back to main, up to date
```

## Conventional Commits (used from Week 2)

`<type>(<scope>): <summary>`, where type is one of `feat`, `fix`, `refactor`, `test`, `docs`, or `chore`.

```
fix(services): tasks due today are not overdue (TF-101)
feat(tasks): filter by status and priority (TF-103)
refactor(legacy): split report builder into renderers (TF-109)
```

## Pull requests with the GitHub CLI

`gh` is already logged in inside your Codespace.

```bash
gh pr create --fill              # PR from the current branch, using the commit message
gh pr view --web                 # open it in the browser
gh pr checks                     # CI status
gh pr merge --squash             # merge it
```

## Worktrees (Week 5)

A worktree is a second checkout of the same repo in another folder, on another branch,
so two Claude sessions can work in parallel without stepping on each other.

```bash
git worktree add ../tf-107 -b feature/tf-107
git worktree list
git worktree remove ../tf-107
```

## Undo, safely

| Situation | Command |
|---|---|
| Throw away unstaged edits to one file | `git restore path/to/file` |
| Unstage something | `git restore --staged path/to/file` |
| Undo the last commit but keep the changes | `git reset --soft HEAD~1` |
| "I want to see what main looked like" | `git stash` … `git stash pop` |

Avoid `git push --force` on shared branches. In Week 3 you'll write a hook that blocks it.
