# Reference solutions

**Try the lab first.** Solutions are most useful *after* you've had a go: compare approaches, not keystrokes.

Each `weekN/` folder is an **overlay**. It mirrors the repo layout and contains files as they look at the
end of week N. Your code doesn't need to match. It needs to pass `uv run labcheck`.

| Week | Highlights |
|---|---|
| 1 | TaskForge fixes TF-101 to TF-103, example notes |
| 2 | Lean `CLAUDE.md`, path-scoped rules, TF-104 to TF-106, a saved plan |
| 3 | Settings with allow/ask/deny, hooks, skills, a command, an output style, a status line with branch, the `taskforge-toolkit` plugin and marketplace |
| 4 | `.mcp.json`, the TaskForge MCP server (`taskforge/mcp_server.py`), triage schema and script, standup skill |
| 5 | Subagents, TF-107/TF-108, nightly headless script, `claude-review.yml`, the TF-109 refactor and its handoff |
| 6 | Agent SDK release-notes agent, capstone design doc, sample capstone (PR triage bot), mock-exam result |

Instructors: `uv run python scripts/build_checkpoints.py --verify` applies every overlay to a temporary copy of
the repo and runs all 30 lab checks.
