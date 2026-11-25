# Guide 02: Just enough git and GitHub

Claude Code is excellent at git, but **you** need to understand what it's doing so you
can review it. This is the minimum.

## The mental model

```
working tree  --git add-->  staging area  --git commit-->  local history  --git push-->  GitHub
```

## Your branch in this course

The whole cohort shares one repository. You work on **your own branch**, `firstname-lastname` (e.g. `jane-doe`),
which you create on Day 1. In this course it plays the role that `main` plays in a normal team repo:

- every day ends with `git add -A && git commit -m "wNdM: <lab title>" && git push`
- feature branches start from your branch and carry your name: `jane-doe-tf-105`
- pull requests go **into your branch** (`--base jane-doe`), never into `main`

## Everyday commands

```bash
git status                            # what's changed?
git diff                              # what exactly changed (unstaged)?
git diff --staged                     # what's about to be committed?
git switch -c jane-doe-tf-105         # new feature branch, from your personal branch
git add -A && git commit -m "feat(tasks): record completed_at (TF-105)"
git push -u origin HEAD               # publish the branch
git log --oneline --graph -15         # recent history
git switch jane-doe && git pull       # back to your personal branch, up to date
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
gh pr create --fill --base jane-doe   # PR into your personal branch, using the commit message
gh pr view --web                      # open it in the browser
gh pr checks                          # CI status
gh pr merge --squash --delete-branch  # merge it into your branch and tidy up
```

## Worktrees (Week 5)

A worktree is a second checkout of the same repo in another folder, on another branch,
so two Claude sessions can work in parallel without stepping on each other.

```bash
git worktree add ../tf-107 -b jane-doe-tf-107
git worktree list
git worktree remove ../tf-107
```

## Undo, safely

| Situation | Command |
|---|---|
| Throw away unstaged edits to one file | `git restore path/to/file` |
| Unstage something | `git restore --staged path/to/file` |
| Undo the last commit but keep the changes | `git reset --soft HEAD~1` |
| Set changes aside for a moment | `git stash` … `git stash pop` |
| "I committed on `main` by mistake" | `git switch jane-doe && git merge main`, then ask your instructor to help reset your local `main` |

Avoid `git push --force` on shared branches. In Week 3 you'll write a hook that blocks it.
