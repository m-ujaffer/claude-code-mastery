# Week 3 · Day 11: Settings and permissions

| | |
|---|---|
| **Level** | Intermediate |
| **CCA-F domain** | 2 · Claude Code configuration & workflows |
| **Time** | 10 min read · 35 min hands-on · 10 min verify & reflect · 5 min log |
| **Budget cap** | $0.60 |
| **Check** | `uv run labcheck w3d11` |

## 🎯 Goal

Understand where Claude Code's settings come from, and write a permission policy that's
**fast where it's safe** and **strict where it matters**.

## 📖 Primer

**Settings files**, from highest to lowest precedence:

| File | Who | Commit? |
|---|---|---|
| Managed settings (set by IT, can't be overridden) | Organisation | n/a |
| Command-line flags, e.g. `--settings`, `--permission-mode` | This run | n/a |
| `.claude/settings.local.json` | You, this project | ❌ git-ignored |
| `.claude/settings.json` | The team, this project | ✅ |
| `~/.claude/settings.json` | You, all projects | n/a |

Project settings are read from the directory you **launch** `claude` from. Lists such as
`permissions.allow` **merge** across files; scalar values are overridden by the higher-precedence file.

**Permission rules** use `Tool(specifier)` syntax:

```json
{
  "permissions": {
    "allow": ["Bash(uv run pytest *)", "Bash(git diff *)"],
    "ask":   ["Bash(git push *)"],
    "deny":  ["Read(./.env)", "Read(./.env.*)", "Bash(rm -rf *)"]
  }
}
```

`deny` beats `ask`, which beats `allow`. A deny rule is a guardrail the model can't talk its way past.

## 🛠️ Steps

**1. Read the course defaults** in `.claude/settings.json`. For each `allow` and `deny` entry, explain
to yourself *why* it's there. Start `claude` and run `/permissions` to see the effective rules and
where each one comes from.

**2. Prove a deny rule works.** Create a fake secret:

```bash
echo 'FAKE_TOKEN=not-a-real-secret' > .env
```

In Claude, ask: *"What's in .env?"* It should be blocked. Now ask: *"Use bash to print .env."* What happens?
`cat .env` isn't covered by `Read(./.env)`. That gap is exactly why Day 13 adds a hook. Note it.

**3. Write the team policy.** Edit `.claude/settings.json` (by hand or with Claude) so that:
- `git push` of any kind is **ask**
- `rm -rf` is **denied** (add `"Bash(rm -rf *)"`)
- `uv run ruff *` and `uv run labcheck *` stay **allowed**
- `.env` reads stay **denied**

**4. Personal overrides.** Create `.claude/settings.local.json` with something only *you* want, for example:

```json
{ "permissions": { "allow": ["Bash(gh pr view *)"] } }
```

Confirm git ignores it: `git check-ignore -v .claude/settings.local.json`

**5. Test the policy.** `/clear` and ask Claude to:
- run the tests (no prompt expected)
- `git push` (an **ask** prompt is expected, so decline)
- `rm -rf practice-app/tests` (**denied** is expected)

**6. Sandboxing (read only).** Claude Code can also sandbox the Bash tool, restricting filesystem and network
access at the OS level. Skim the *Sandboxing* page in the docs and write one sentence in your head about
how it complements permission rules. (Your Codespace is already a sandbox at the machine level.)

**7. Clean up and commit.** `rm .env`, then commit `.claude/settings.json`.

## ✅ Checkpoint

```bash
uv run labcheck w3d11
```

## 💰 Budget & cost log

Cap: **$0.60**.

```bash
uv run labcheck log w3d11 0.40 "permissions"
```

## 📤 Push your progress

```bash
git add -A && git commit -m "w3d11: Settings and permissions" && git push
```

## 🚀 Stretch

- Start Claude with `claude --permission-mode plan`. When would a team script do that?
- Find out what **managed settings** are and why a security team would use them for things like
  disabling `bypassPermissions` org-wide.

## 💼 Commercial application

Security teams approve agent tools when there's a **policy they can read**: checked-in project
settings for team defaults, plus managed settings for org-wide non-negotiables. A clear allow/ask/deny
file is often what gets Claude Code through a security review.

## 🤔 Reflect

1. Why did `Read(./.env)` not stop `cat .env`? What does that teach you about permission rules?
2. What's in your `allow` list that you'd **not** allow on a production repo?
3. Where should an org-wide "never push to main" rule live?

## ➡️ Next

[Day 12: Skills and slash commands](2_lab2_skills_and_commands.md)
