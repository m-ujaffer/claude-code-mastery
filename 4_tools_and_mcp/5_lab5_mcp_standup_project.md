# Week 4 · Day 20: Mini-project, an MCP-powered standup

| | |
|---|---|
| **Level** | Advanced |
| **CCA-F domain** | 4 · Tool design & MCP integration · 2 · Workflows |
| **Time** | 5 min read · 35 min hands-on · 10 min verify · 10 min quiz |
| **Budget cap** | $1.20 |
| **Check** | `uv run labcheck w4d20` |

## 🎯 Goal

Combine a **skill** (the procedure) with **MCP tools** (the capabilities) into a one-command workflow your
team could actually use every morning.

## 📖 Primer

Skills can pre-approve exactly the tools they need with `allowed-tools`. MCP tools are named
`mcp__<server>__<tool>`:

```markdown
---
name: standup
description: Produce a daily standup summary for a TaskForge project from live task data.
argument-hint: <project name or id>
allowed-tools: mcp__taskforge__list_projects, mcp__taskforge__find_tasks, mcp__taskforge__project_stats
---
```

This gives you **least privilege by construction**: the skill can read, but any write still asks.

## 🛠️ Steps

**1. Seed realistic data** (if your DB is sparse):

> Using the taskforge MCP tools, create 8 realistic tasks across the two projects: mixed priorities,
> some due in the past, some tagged "blocked". Then mark 3 of them done.

(This step uses the **write** tools. Notice they still ask for approval.)

**2. Write the skill** `.claude/skills/standup/SKILL.md`. The body should:
- resolve `$ARGUMENTS` to a project via `list_projects` (by id or by name)
- call `project_stats` once, then `find_tasks` for overdue tasks and for tasks tagged `blocked`
- output **exactly** this Markdown shape:

```markdown
## Standup: <project> (<date>)
**Health:** <one line using completion rate and overdue count>
### 🔴 Overdue (<n>)
- <title> (<priority>, due <date>)
### 🚧 Blocked (<n>)
- ...
### ✅ Suggested focus today
1. ...
```

- **never** modify tasks
- stay under about 200 words

**3. Run it.**

```
/standup Website relaunch
```

Check: was it correct against the data? Did it stay read-only? Run `/cost`. Is that a reasonable price for a daily habit?

**4. Iterate on cost.** Try adding `model: haiku` to the skill's frontmatter and run it again. Is the quality still
acceptable? Keep whichever you'd choose for a team.

**5. Save a sample** of the output to `notes/standup-sample.md`, and commit the skill.

**6. Take the Week 4 quiz:** [assessments/week4_quiz.md](../assessments/week4_quiz.md).

## ✅ Checkpoint

```bash
uv run labcheck w4d20
uv run labcheck budget
```

## 💰 Budget & cost log

Cap: **$1.20**.

```bash
uv run labcheck log w4d20 0.80 "standup skill"
```

Week 4 total should be **≤ $6**.

## 📤 Push your progress

```bash
git add -A && git commit -m "w4d20: Mini-project, an MCP-powered standup" && git push
```

## 🚀 Stretch

- Run it headless as a scheduled job: `claude -p "/standup 1" --max-turns 6 --max-budget-usd 0.15`.
- Add the skill and the MCP server to your `taskforge-toolkit` plugin (plugins can ship `.mcp.json`).

## 💼 Commercial application

"Skill + MCP" is the pattern behind most useful internal agents: incident summaries from your observability
tools, sprint reports from your tracker, release checklists from CI. The skill encodes *how your team works*;
MCP provides *access to where the data lives*.

## 🤔 Reflect

1. What would break if the skill didn't restrict `allowed-tools`?
2. Haiku or Sonnet for this skill, and why?
3. Which part of this would you test automatically, and how?

## ➡️ Next

Week 5: [Agents & Automation](../5_agents_and_automation/README.md)
