# Admin guide: API keys, budgets and Codespaces for a cohort

This page is for whoever runs the course. Learners don't need it.

## Goals

1. Each engineer has **their own** API key.
2. Each key can spend at most **US$30 per calendar month**, and this is **enforced**, not just requested.
3. You can see usage per engineer.
4. Keys are easy to revoke when the cohort ends.
5. You can follow each engineer's progress from their branch in the shared course repo.

## 1. One Console workspace per engineer

In the [Anthropic Console](https://console.anthropic.com), **workspaces** group API keys and carry
their own **spend limits**. Spend limits are applied per workspace, so one workspace per
engineer gives you a hard per-person cap.

For each engineer:

1. **Settings → Workspaces → Create workspace**. Name it something like `ccm-2026q1-jdoe`.
2. In the workspace's **Limits**, set the **monthly spend limit to $30**. When the limit is
   reached, API requests from that workspace are rejected until the next month. Nothing
   is billed beyond the limit.
3. **API keys → Create key** inside that workspace. Name it after the engineer.
4. Send the key over a secure channel (your password manager's sharing feature, not email
   or chat).

> The Console UI changes from time to time. If a menu name differs, look for "Workspaces" and
> "Spend limits" in the Console docs. Organisations with many learners can script this
> with the Admin API (workspaces and API keys endpoints, which need an Admin key).

## 2. Organisation-level safety net

- Set an **organisation monthly spend limit** of roughly `number of engineers × $30 + 10%`.
- Turn **off auto-reload** of credits during the pilot, or set a conservative reload cap.
- Add a billing **email alert** at 50% and 80%.

## 3. Monitoring

- **Console → Usage / Cost**, grouped by workspace, gives per-engineer spend.
- Claude Code also reports a client-side estimate. Learners see it in their status line
  (`month ~$x/$30`) and in `uv run labcheck budget`. Those numbers are estimates and leave out
  headless and CI runs; the Console is the source of truth.
- Expect roughly **$25–32 per engineer over the six weeks** if they follow the labs. Most
  overspend comes from (a) switching to Opus for everything, (b) never running `/clear`,
  or (c) a runaway CI workflow in Week 5. That's why the CI lab caps `--max-turns` and is
  guarded with `if:` conditions.

## 4. The shared course repository

All learners work in **one** repository (yours), each on a personal branch named `firstname-lastname`
that they create and push on Day 1. Every lab ends with
`git add -A && git commit -m "wNdM: <lab title>" && git push`, so each branch's history *is* that learner's progress.

**Set-up checklist**
1. Host the repo in your GitHub organisation (private). Add learners with **Write** access. A GitHub team
   (for example `ccm-2026q1`) makes this one step.
2. **Protect `main`** (Settings → Branches / Rulesets): require a pull request with your review and block direct
   pushes. Learners' PRs go into their *own* branch. The only PRs into `main` are optional
   `community_contributions/` shares, which you review.
3. Mark the repo as **not** a template. Learners don't copy it.

**Tracking progress**

```bash
git fetch --all --prune
git for-each-ref --sort=-committerdate refs/remotes/origin \
  --format='%(refname:short)  %(committerdate:short)  %(subject)'
```

The latest `wNdM:` subject on each branch shows that learner's most recent completed day. To check someone's
work properly, which is free and offline:

```bash
git worktree add /tmp/jane-doe origin/jane-doe
uv run labcheck --all --root /tmp/jane-doe
git worktree remove /tmp/jane-doe
```

The `tests` workflow also runs on every push, so each learner's branch shows a green or red check in GitHub.

## 5. GitHub Codespaces

- Codespaces usage is billed to whoever owns the repository the Codespace is created from (a
  personal account's free quota, or your organisation). Check GitHub's current Codespaces
  pricing. A 2-core machine for about 30 course hours is usually a small cost per engineer.
- Recommended org policies: limit machine types to 2-core and 4-core, set an idle timeout of 30
  minutes or less, and set retention to cover the cohort length plus 2 weeks.
- Do **not** create a repo- or org-level `ANTHROPIC_API_KEY` **Codespaces** secret. A shared secret means a
  shared budget and no per-person cap. Each engineer stores their **own** key as a *user* Codespaces secret,
  scoped to the course repo (see SETUP-codespaces.md, Step 2).

## 6. GitHub Actions (Week 5, Day 24)

Learners can't install apps or set secrets in the shared repo, so do this once before Week 5:

1. Install the **Claude GitHub App** on the course repo (run `/install-github-app` in Claude Code as a repo admin,
   or follow the manual steps on the Claude Code docs' *GitHub Actions* page).
2. Create a **separate Console workspace for CI** (for example `ccm-2026q1-ci`) with its own monthly spend limit.
   Roughly `$1.50 × learners` is plenty for Day 24. Create a key in it.
3. Add that key as the **Actions** repository secret `ANTHROPIC_API_KEY`. This is separate from the learners'
   Codespaces secrets, so CI spend never comes out of anyone's $30.

The lab's workflow only runs on PRs that touch `practice-app/`, skips drafts, cancels superseded runs and is
capped with `--max-turns`. `pull_request` workflows run from the PR's own branch, so each learner's workflow works
without touching `main`. `@claude` comment triggers only run from `main`: if you want learners to try them, merge
the reference workflow (`solutions/week5/.github/workflows/claude-review.yml`) to `main` yourself.

## 7. End of cohort

- Revoke all keys (Console → API keys), or archive the workspaces.
- Ask learners to delete their Codespaces. Their work stays on their branches.
- Each branch's `notes/cost-log.csv` gives you real data to tune lab budgets for the next cohort.
- Archive or delete the learner branches once you've kept what you need.

## 8. Keeping the course current

Claude Code ships often. Before each cohort, read [UPDATING.md](UPDATING.md).
