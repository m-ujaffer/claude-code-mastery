# Admin guide: API keys, budgets and Codespaces for a cohort

This page is for whoever runs the course. Learners don't need it.

## Goals

1. Each engineer has **their own** API key.
2. Each key can spend at most **US$30 per calendar month**, and this is **enforced**, not just requested.
3. You can see usage per engineer.
4. Keys are easy to revoke when the cohort ends.

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

## 4. GitHub Codespaces

- Codespaces usage is billed to whoever owns the repository the Codespace is created from (a
  personal account's free quota, or your organisation). Check GitHub's current Codespaces
  pricing. A 2-core machine for about 30 course hours is usually a small cost per engineer.
- Recommended org policies: limit machine types to 2-core and 4-core, set an idle timeout of 30
  minutes or less, and set retention to cover the cohort length plus 2 weeks.
- Do **not** create an org-level `ANTHROPIC_API_KEY` Codespaces secret, even if engineers
  create their copies inside your org. A shared secret means a shared budget and no per-person
  cap. Each engineer stores their **own** key as a *user* secret (see SETUP-codespaces.md, Step 2).

## 5. GitHub Actions (Week 5, Day 24)

In Day 24, learners add their own key as an **Actions repository secret** in their copy of the
repo. CI runs bill to the same workspace, so the $30 cap still applies. The lab's workflow only
runs on PRs that touch `practice-app/` and is capped with `--max-turns`.

## 6. End of cohort

- Revoke all keys (Console → API keys), or archive the workspaces.
- Ask learners to delete their Codespaces.
- Collect the `notes/cost-log.csv` files if you want data to tune lab budgets for the next cohort.

## 7. Keeping the course current

Claude Code ships often. Before each cohort, read [UPDATING.md](UPDATING.md).
