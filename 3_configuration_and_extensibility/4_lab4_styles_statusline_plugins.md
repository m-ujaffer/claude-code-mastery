# Week 3 · Day 14: Output styles, status line and plugins

| | |
|---|---|
| **Level** | Intermediate |
| **CCA-F domain** | 2 · Claude Code configuration & workflows |
| **Time** | 5 min read · 40 min hands-on · 10 min verify & reflect · 5 min log |
| **Budget cap** | $0.80 |
| **Check** | `uv run labcheck w3d14` |

## 🎯 Goal

Customise *how* Claude Code communicates (output styles), *what you see* (status line), and *what it
can do* (installing plugins), and judge which customisations are worth their context cost.

## 📖 Primer

- **Output styles** change Claude Code's system prompt to adapt its role and tone. Built-ins include
  *Explanatory* and *Learning*. Custom styles live in `.claude/output-styles/<name>.md` with frontmatter
  (`name`, `description`, optionally `keep-coding-instructions: true`). Switch with `/output-style`
  or the `outputStyle` setting.
- **Status line**: a command in `settings.json → statusLine` that receives session JSON on stdin and prints
  one line. The course one is `.claude/statusline.py`. Read it now; it's short.
- **Plugins** bundle skills, commands, agents, hooks and MCP servers into one installable unit, distributed
  through **marketplaces**. Manage them with `/plugin` or `claude plugin ...`.

## 🛠️ Steps

```bash
cp notes/templates/w3d14-plugins.md notes/w3d14-plugins.md
```

**1. Try a built-in style.** In `claude`, run `/output-style` and pick **Learning**. Ask:

> Add a `GET /projects/{id}/tasks?status=` filter reusing the repository function.

Notice how it behaves differently: it may ask *you* to write parts. Switch back to **Default** afterwards.

**2. Write a custom style.** Create `.claude/output-styles/reviewer-coach.md`:

```markdown
---
name: Reviewer Coach
description: Terse senior-reviewer voice. Leads with risks, explains trade-offs in one line each.
keep-coding-instructions: true
---
You are pairing with an engineer who is learning to review AI-written code.
- Before any edit, state the plan in at most 3 bullets.
- After any edit, list the top 2 risks a reviewer should check.
- Prefer the smallest change that meets the acceptance criteria.
```

Activate it, do a tiny change, and compare. Keep it or switch back. Your choice.

**3. Improve the status line.** Ask Claude:

> Extend @.claude/statusline.py to also show the current git branch (from `git branch --show-current`,
> with a 1s timeout, omitted if it fails). Keep the output on one line and keep it fast.

Restart `claude` and check the bottom line. Test it standalone: `echo '{}' | python3 .claude/statusline.py`.

**4. Install a plugin.** Run `/plugin` and browse the **Discover** tab of the official marketplace. Pick
**one** plugin relevant to code review or Python, install it (user scope is fine), and run `/context` before
and after. Write down what it added and what it costs in context.

**5. Decide.** Would your team want it? Answer in your notes. If not, uninstall it:
`/plugin` → Installed → uninstall.

**6. Commit** the style and the status line change.

## ✅ Checkpoint

```bash
uv run labcheck w3d14
```

## 💰 Budget & cost log

Cap: **$0.80**.

```bash
uv run labcheck log w3d14 0.55 "styles/statusline/plugins"
```

## 🚀 Stretch

- Use `/statusline` and let Claude generate a status line from a description. Compare it with yours.
- Show a ⚠️ in the status line when `context_window.used_percentage` is above 60%.

## 💼 Commercial application

Small ergonomic wins (seeing the branch, the cost and the context fill at a glance) change behaviour more
than any policy document. Teams often ship a standard status line and output style in their internal plugin,
which is exactly what you'll build tomorrow.

## 🤔 Reflect

1. When would the *Learning* style be the right default for a team?
2. How much context did the plugin cost, and was it worth it?
3. Why does the course status line say its numbers are "estimates"?

## ➡️ Next

[Day 15: Package a team plugin](5_lab5_team_plugin.md)
