# Week 4 · Day 17: Build an MCP server for TaskForge

| | |
|---|---|
| **Level** | Advanced |
| **CCA-F domain** | 4 · Tool design & MCP integration |
| **Time** | 10 min read · 35 min hands-on · 10 min verify & reflect · 5 min log |
| **Budget cap** | $1.20 |
| **Check** | `uv run labcheck w4d17` |

## 🎯 Goal

Build a stdio MCP server that exposes TaskForge to any MCP client, and design its tools so a model uses
them **correctly and cheaply**.

## 📖 Primer

With the official Python SDK (version 2.x; the high-level class used to be called `FastMCP`):

```python
from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError

mcp = MCPServer("taskforge")

@mcp.tool()
def project_stats(project_id: int) -> dict:
    """Return counts by status, overdue count and completion rate for one project.
    This is the cheapest way to answer "how is project X doing?"."""
    ...
    raise ToolError("Project 9 does not exist. Call list_projects to see valid ids.")

if __name__ == "__main__":
    mcp.run()          # stdio by default
```

The function name becomes the tool name, the type hints become the input schema, and the docstring
becomes the description.

**Tool design checklist**

1. **Task-shaped, not table-shaped.** `find_tasks(status, overdue_only, ...)` beats `select_from_tasks(sql)`.
2. **Few tools.** Every tool definition is context in every request. Five good tools beat fifteen thin ones.
3. **Descriptions say *when* to use the tool and *what comes back*.** "Call this first to get a project_id."
4. **Compact results.** Return what the model needs, not every column. Cap list sizes.
5. **Errors that teach.** Raise `ToolError("…what went wrong… and what to do instead")`. Any other
   exception reaches the model only as "Error executing tool X".
6. **Annotate read-only tools** (`ToolAnnotations(readOnlyHint=True)`) so clients can treat them as safe.
7. **Validate with your existing models.** Reuse `TaskCreate`, so the MCP path and the HTTP path can't drift apart.

## 🛠️ Steps

**1. Plan the tool surface (plan mode).** `/clear`, then `Shift+Tab` to plan mode:

> Design an MCP server for TaskForge at practice-app/src/taskforge/mcp_server.py using the Python MCP SDK
> 2.x (`from mcp.server.mcpserver import MCPServer`). Propose at most 5 tools covering: listing projects,
> finding tasks with filters (including overdue_only), creating a task, changing a task's status, and project
> stats. For each, give the name, parameters, description text and return shape. Reuse repository.py,
> services.py and models.TaskCreate. Errors must be ToolError messages that tell the model how to recover.

Challenge the design against the checklist above, then approve.

**2. Implement.** Let Claude implement it. The DB path should honour `TASKFORGE_DB`, defaulting to
`practice-app/taskforge.db`.

**3. Test it without a model** (free). Ask Claude to write a quick script, or do it yourself:

```bash
uv run python -c "
import asyncio, taskforge.mcp_server as m
async def main():
    for t in await m.mcp.list_tools(): print(t.name, '-', (t.description or '')[:70])
    print(await m.mcp.call_tool('project_stats', {'project_id': 999}))
asyncio.run(main())"
```

The second call should fail with your helpful message, not a traceback.

**4. Register it** for the team:

```bash
claude mcp add --scope project taskforge -- uv run python -m taskforge.mcp_server
uv run python -m taskforge.seed      # demo data, if your DB is empty
```

**5. Use it from Claude.** Restart `claude`, approve the server, then:

> Using only the taskforge MCP tools, tell me which project is in the worst shape and why.

Watch which tools it chooses. Did it use `project_stats`, or list every task? If it chose badly, **improve the
descriptions**, not the prompt, and try again in a fresh session.

**6. Commit** the server and `.mcp.json`.

## ✅ Checkpoint

```bash
uv run labcheck w4d17
```

## 💰 Budget & cost log

Cap: **$1.20**.

```bash
uv run labcheck log w4d17 0.95 "TaskForge MCP server"
```

## 📤 Push your progress

```bash
git add -A && git commit -m "w4d17: Build an MCP server for TaskForge" && git push
```

## 🚀 Stretch

- Write pytest tests for the MCP tools (call `mcp.call_tool(...)` against a temporary DB).
- Add `limit` validation: what should happen when the model asks for 10,000 tasks?

## 💼 Commercial application

Wrapping an internal service in MCP makes it usable by **every** MCP client (Claude Code, Claude apps,
your own agents) with one implementation. The quality of the tool descriptions decides whether that
integration feels magical or flaky.

## 🤔 Reflect

1. Which description change most improved Claude's tool choice in step 5?
2. Why reuse `TaskCreate` instead of validating again in the MCP layer?
3. What would make `find_tasks` dangerous for context size, and how did you cap it?

## ➡️ Next

[Day 18: Resources, prompts and MCP security](3_lab3_resources_prompts_security.md)
