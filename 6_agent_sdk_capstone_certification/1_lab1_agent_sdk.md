# Week 6 · Day 26: The Claude Agent SDK

| | |
|---|---|
| **Level** | Expert |
| **CCA-F domain** | 1 · Agentic architecture · 4 · Tool design · 3 · Structured output |
| **Time** | 10 min read · 35 min hands-on · 10 min verify & reflect · 5 min log |
| **Budget cap** | $0.80 |
| **Check** | `uv run labcheck w6d26` |

## 🎯 Goal

Build a standalone agent in Python on the same harness that powers Claude Code: its tools, permissions,
budgets and in-process custom tools.

## 📖 Primer

The **Claude Agent SDK** (`pip install claude-agent-sdk`; here it comes from `uv sync --all-groups`) packages Claude Code's agent loop
as a library:

```python
import asyncio
from claude_agent_sdk import (ClaudeAgentOptions, ResultMessage, AssistantMessage, TextBlock,
                              query, tool, create_sdk_mcp_server)

@tool("save_notes", "Save the final release notes as Markdown. Call exactly once.", {"markdown": str})
async def save_notes(args):
    ...
    return {"content": [{"type": "text", "text": "saved"}]}          # or add "is_error": True

server = create_sdk_mcp_server(name="notes", version="1.0.0", tools=[save_notes])

options = ClaudeAgentOptions(
    allowed_tools=["Read", "Grep", "Bash(git log *)", "mcp__notes__save_notes"],  # auto-approved
    disallowed_tools=["Edit", "Write"],
    mcp_servers={"notes": server},          # tool names: mcp__<key>__<tool>
    max_turns=10,
    max_budget_usd=0.30,
    setting_sources=[],                     # don't load local settings/CLAUDE.md, for reproducible runs
)

async for message in query(prompt="...", options=options):
    if isinstance(message, ResultMessage):
        print(message.total_cost_usd, message.num_turns, message.is_error)
```

Things to know:
- `allowed_tools` **auto-approves** tools. It doesn't restrict the rest; use `disallowed_tools` for that.
- The custom tool runs **in your process**, so it can call your own code directly. Errors go back to the model as
  `is_error` results it can read and react to.
- `max_budget_usd` is an estimate checked during the run, so leave headroom.
- `system_prompt={"type": "preset", "preset": "claude_code", "append": "..."}` keeps Claude Code's
  tool-use behaviour and adds your role.

**SDK vs `claude -p` vs the API:** use `claude -p` for scripts, the SDK when you need code-level control
(custom tools, message handling, embedding in a service), and the raw Messages API when you want to own the
whole loop yourself.

## 🛠️ Steps

Make sure the Agent SDK is installed (quick if it already is):

```bash
uv sync --all-groups
```

**1. Build a release-notes agent.** Ask Claude to create `sdk_agents/release_notes_agent.py` to this spec
(plan mode first, then review the plan):

- CLI args `--since` (git revision, default `HEAD~10`) and `--budget` (default `0.30`)
- an in-process tool `save_release_notes(markdown: str)` that writes `notes/release-notes-sample.md`, and
  returns an `is_error` result if the Markdown is under 50 characters or has no `##` heading
- options: `allowed_tools` = Read, Grep, Glob, `Bash(git log *)`, `Bash(git diff *)` and the save tool.
  `disallowed_tools` = Edit, Write. `max_turns=10`. `max_budget_usd` from `--budget`. `setting_sources=[]`.
  The system prompt is the claude_code preset with an appended role: group into Features / Fixes / Internal,
  reference TF-ids, and keep it under 250 words.
- print assistant text as it streams. At the end, print `turns`, `total_cost_usd` and `is_error`, and exit 1 on error.

**2. Read the code before running it.** Check: can this agent modify your repo in any way? (Bash is limited to two
git patterns, Edit/Write are disallowed, and the only write path is your tool, which writes one file.)

**3. Run it.**

```bash
uv run python sdk_agents/release_notes_agent.py --since HEAD~15
cat notes/release-notes-sample.md
```

**4. Test the error path.** Temporarily make your tool's validation stricter (for example, require a `## Breaking changes`
section) and run again. Does the agent read the error and fix its output? Revert the change.

**5. Test the budget.** Run with `--budget 0.02`. What does the `ResultMessage` say?

**6. Commit** the agent and the sample.

## ✅ Checkpoint

```bash
uv run labcheck w6d26
```

## 💰 Budget & cost log

Cap: **$0.80**. Log the sum of the `total_cost_usd` values printed by your runs, plus the authoring session:

```bash
uv run labcheck log w6d26 0.65 "release notes agent"
```

## 📤 Push your progress

```bash
git add -A && git commit -m "w6d26: The Claude Agent SDK" && git push
```

## 🚀 Stretch

- Rebuild it as a `claude -p --json-schema` script (Day 19 style) instead of an SDK agent with a save tool. Compare the two designs.
- Add a `PreToolUse` hook through the SDK options that logs every tool call to a file.

## 💼 Commercial application

The SDK is how teams turn "a thing Claude Code does well interactively" into **a product feature or an internal
service**: a support-ticket triager, a migration bot, a docs agent, with the same tools and safety model, under
their own control and observability.

## 🤔 Reflect

1. Why `setting_sources=[]` for an agent that runs on many machines?
2. Custom tool vs structured output for producing the final artefact: which would you choose, and why?
3. What else would you add before running this agent on every release?

## ➡️ Next

[Day 27: Agentic architecture design review](2_lab2_architecture_patterns.md)
