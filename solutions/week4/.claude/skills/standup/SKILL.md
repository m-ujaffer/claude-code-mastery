---
name: standup
description: Produce a daily standup summary for a TaskForge project from live task data. Use when asked for a standup, daily summary or "what's the status of <project>".
argument-hint: <project name or id>
allowed-tools: mcp__taskforge__list_projects, mcp__taskforge__find_tasks, mcp__taskforge__project_stats
model: haiku
---
# Standup for $ARGUMENTS

1. Call `list_projects` and resolve "$ARGUMENTS" to one project (match by id, or by case-insensitive name).
   If nothing matches, list the projects and stop.
2. Call `project_stats` once for that project.
3. Call `find_tasks` with `overdue_only: true`, then `find_tasks` with `tag: "blocked"` (each with `limit: 10`).
4. Never create or modify tasks. This skill is read-only.
5. Output exactly this shape, under 200 words:

```
## Standup: <project> (<today's date>)
**Health:** <one line using completion rate and overdue count>
### 🔴 Overdue (<n>)
- <title> (<priority>, due <date>)
### 🚧 Blocked (<n>)
- <title> (<priority>)
### ✅ Suggested focus today
1. <most important task, with a one-line reason>
2. ...
```
