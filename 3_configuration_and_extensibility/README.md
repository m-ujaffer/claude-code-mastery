# Week 3: Configuration & Extensibility (Intermediate)

**Theme:** turn Claude Code into *your team's* tool, safely.
**Week budget:** $5

| Day | Lab | You'll practise | Cap |
|---|---|---|---|
| 11 | [Settings and permissions](1_lab1_settings_and_permissions.md) | settings hierarchy, allow/deny/ask, secrets, sandboxing | $0.60 |
| 12 | [Skills and slash commands](2_lab2_skills_and_commands.md) | `SKILL.md`, frontmatter, `$ARGUMENTS`, manual vs model-invoked | $0.90 |
| 13 | [Hooks](3_lab3_hooks.md) | PreToolUse guardrails, PostToolUse formatting, Stop notifications | $1.00 |
| 14 | [Output styles, status line and plugins](4_lab4_styles_statusline_plugins.md) | `/output-style`, statusline scripts, `/plugin` | $0.80 |
| 15 | [Package a team plugin](5_lab5_team_plugin.md) | plugin manifest, local marketplace, `claude plugin validate` | $1.20 |

**Key idea of the week:** pick the right mechanism.

| Need | Use | Why |
|---|---|---|
| "Always/never do X", and it **must** happen | **Hook** | deterministic: runs every time, whatever the model decides |
| Background knowledge or conventions | **CLAUDE.md / rules** | advisory: always (or path-scoped) in context |
| A repeatable procedure, used sometimes | **Skill / slash command** | loaded on demand, so cheap when unused |
| Isolated work that returns a summary | **Subagent** (Week 5) | separate context window |
| External systems and data | **MCP server** (Week 4) | tools and resources over a standard protocol |
| Share all of the above | **Plugin** | one installable bundle |

**End of week:** [Week 3 quiz](../assessments/week3_quiz.md).
