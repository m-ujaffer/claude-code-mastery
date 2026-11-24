# Week 3 · Day 15: Package a team plugin (mini-project)

| | |
|---|---|
| **Level** | Intermediate → Advanced |
| **CCA-F domain** | 2 · Claude Code configuration & workflows |
| **Time** | 5 min read · 35 min hands-on · 10 min verify · 10 min quiz |
| **Budget cap** | $1.20 |
| **Check** | `uv run labcheck w3d15` |

## 🎯 Goal

Bundle this week's work (the `tf-issue` skill, the `review-diff` command and the guard hook) into an
installable **plugin**, publish it through a **local marketplace**, and install it the way a teammate would.

## 📖 Primer

```
plugins/taskforge-toolkit/
├── .claude-plugin/
│   └── plugin.json          # manifest: only "name" is required
├── skills/tf-issue/SKILL.md
├── commands/review-diff.md
├── hooks/
│   ├── hooks.json           # same shape as settings "hooks", wrapped in {"hooks": {...}}
│   └── block-dangerous.py
└── README.md
```

- Everything except `plugin.json` goes at the **plugin root**, not inside `.claude-plugin/`.
- Inside plugin files, reference your own files with `${CLAUDE_PLUGIN_ROOT}`.
- Plugin skills are **namespaced**: `/taskforge-toolkit:tf-issue`.
- A **marketplace** is a repo or directory with `.claude-plugin/marketplace.json` listing plugins.
- Test locally without installing: `claude --plugin-dir ./plugins/taskforge-toolkit`.
- Validate: `claude plugin validate <dir>`.

## 🛠️ Steps

**1. Scaffold.** In `claude`:

> Create a Claude Code plugin at plugins/taskforge-toolkit. Copy (don't move) our tf-issue skill
> (with checklist.md), the review-diff command, and the block-dangerous hook. The hook goes in
> hooks/hooks.json, referencing the script via ${CLAUDE_PLUGIN_ROOT}. Write .claude-plugin/plugin.json
> with name "taskforge-toolkit", a description, version 0.1.0 and an author. Add a README covering what's
> inside, how to install it, and what each component does.

Review every file. In particular, check that `hooks.json` has the top-level `"hooks"` key, and that the
manifest name matches the folder name.

**2. Validate.**

```bash
claude plugin validate ./plugins/taskforge-toolkit
```

Fix anything it reports.

**3. Try it without installing.**

```bash
claude --plugin-dir ./plugins/taskforge-toolkit
```

Inside, run `/help` and find `/taskforge-toolkit:tf-issue`. Exit.

**4. Publish via a local marketplace.** Create `.claude-plugin/marketplace.json` at the repo root:

```json
{
  "name": "taskforge-team",
  "description": "TaskForge team tooling",
  "owner": { "name": "Your Name" },
  "plugins": [
    {
      "name": "taskforge-toolkit",
      "source": "./plugins/taskforge-toolkit",
      "description": "Issue workflow skill, diff review command and safety hook"
    }
  ]
}
```

Then validate and install it like a teammate would:

```bash
claude plugin validate .
claude plugin marketplace add ./
claude plugin install taskforge-toolkit@taskforge-team
claude plugin list
```

**5. Use it.** Start `claude` and run `/taskforge-toolkit:review-diff`. Then **uninstall** it (your project
`.claude/` already has the originals, and double hooks would run twice):

```bash
claude plugin uninstall taskforge-toolkit@taskforge-team   # or: /plugin → Installed → uninstall
```

**6. Commit** `plugins/` and `.claude-plugin/`. Your teammates can now run
`claude plugin marketplace add <your-github-user>/<repo>` and install it.

**7. Take the Week 3 quiz:** [assessments/week3_quiz.md](../assessments/week3_quiz.md).

## ✅ Checkpoint

```bash
uv run labcheck w3d15
uv run labcheck budget
```

## 💰 Budget & cost log

Cap: **$1.20**.

```bash
uv run labcheck log w3d15 0.90 "team plugin"
```

Week 3 total should be **≤ $5**.

## 🚀 Stretch

- Bump the version to 0.2.0 with a change, and read the docs on how teammates receive plugin updates.
- Add the course status line to the plugin. What's the right way to ship a status line? (Hint: is it a plugin component, or a setting?)
- Share your plugin in `community_contributions/` with a short README.

## 💼 Commercial application

This is how platform and DevEx teams roll out Claude Code at scale: **one internal marketplace**, a few
well-reviewed plugins (conventions, workflows, guardrails, internal MCP servers), and admins who can require
them org-wide. You just built the prototype.

## 🤔 Reflect

1. Why is the plugin's skill namespaced, and what problem does that prevent?
2. What should **never** go into a widely shared plugin?
3. How would you roll out a breaking change to a hook that 200 engineers have installed?

## ➡️ Next

Week 4: [Tools & MCP](../4_tools_and_mcp/README.md)
