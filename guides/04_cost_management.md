# Guide 04: Cost management (your $30/month)

## The layers of protection

1. **Hard cap (admin).** Your key's workspace has a $30/month spend limit. Requests stop at the
   limit; you can't be overcharged.
2. **Status line (you, live).** The bottom of every Claude Code session shows
   `session $x | month ~$y/$30`. The month figure turns yellow at 70% and red at 90%.
3. **Cost log (you, daily).** At the end of each lab run `/cost`, then:
   ```bash
   uv run labcheck log w1d3 0.47 "fixed TF-101, one retry"
   uv run labcheck budget
   ```
4. **Caps on scripted runs (Weeks 4–6).** Every `claude -p` call, Agent SDK run and CI job in
   this course sets `--max-turns` and `--max-budget-usd` (or `max_turns` / `max_budget_usd`).

> The status line and `labcheck budget` are **estimates** from Claude Code. They don't include
> `claude -p` or GitHub Actions runs. The Anthropic Console (via your admin) is the source of truth.

## The course budget

| Week | Cap | Typical lab |
|---|---|---|
| 1 | $3 | $0.30–0.60 |
| 2 | $4 | $0.50–0.80 |
| 3 | $5 | $0.60–1.00 |
| 4 | $6 | $0.80–1.20 |
| 5 | $7 | $1.00–1.40 |
| 6 | $6 | the capstone is the big one (~$4); the mock exam is free |

Any four consecutive weeks add up to less than $27, so you stay under $30 even if a calendar
month boundary lands mid-course.

## The ten habits

1. **`/clear` between tasks.** Old context isn't free.
2. **Point, don't wander.** "Fix `is_overdue` in @practice-app/src/taskforge/services.py" beats "find the overdue bug".
3. **Plan first for multi-file work.** Use plan mode (Shift+Tab); cheap thinking prevents expensive rework.
4. **Sonnet by default, Opus on purpose.** Switch with `/model` and switch back.
5. **Lower `/effort` for easy tasks.**
6. **Keep CLAUDE.md lean** (under ~100 lines). Move rarely needed detail into skills or path-scoped rules, which load on demand.
7. **Delegate reading to Haiku subagents** so big file dumps never enter your main context.
8. **Filter noisy output.** `uv run pytest -q`, not `-vv`; `git log --oneline -20`, not `git log`.
9. **Disconnect MCP servers you aren't using** (`/mcp`). Their tool definitions take up context.
10. **Cap every automation:** `--max-turns`, `--max-budget-usd`, CI `if:` guards and `concurrency`.

## When a session suddenly gets expensive

Run `/context`. The usual suspects:
- a large file or command output pasted or read early on: `/compact` or `/clear`
- many MCP tools loaded: disable unused servers
- a long back-and-forth debugging loop: stop, `/clear`, and restate the problem precisely with what you've learned
