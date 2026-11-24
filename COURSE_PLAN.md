# Course plan: Claude Code Mastery (6 weeks · 30 labs · 1 hour a day)

This is the at-a-glance syllabus for learners, managers and instructors. Each lab is in its week folder,
and each is checked for free with `uv run labcheck <id>`.

## Design principles

1. **Learn by doing, in a sandbox.** Every lab runs in a GitHub Codespace on TaskForge, a deliberately small
   Python API with real bugs, missing features and legacy code.
2. **Basics to expert, cumulatively.** Each week builds on artefacts from the week before: CLAUDE.md, then skills, then a
   plugin; an MCP server, then a standup skill, then nightly automation; subagents, then a capstone.
3. **Budget-first.** $30/month per engineer, enforced by a Console workspace spend limit and made visible by
   the course status line. Every lab has a cap, every automated run has `--max-budget-usd`, and assessments are offline.
4. **Verifiable.** `labcheck` runs hidden acceptance tests and config checks with zero API spend. Reference
   solutions are verified end to end (`scripts/build_checkpoints.py --verify`).
5. **Certification-aligned.** Every lab is tagged with a CCA-F domain; the course ends with a 60-question timed mock.

## The 30 days

| Day | Lab | Level | CCA-F domain | Cap |
|---|---|---|---|---|
| **Week 1** | **Foundations** | | | **$3** |
| 1 | First session: explore a codebase, first file write, `/cost` | Basics | D2 | $0.40 |
| 2 | Permission modes, plan mode, `@` mentions, `!` bash, Esc, `/rewind` | Basics | D2 | $0.50 |
| 3 | Fix TF-101 test-first; reviewing diffs | Basics | D2, D3 | $0.60 |
| 4 | Prompting for code: vague vs precise, measured (TF-102) | Basics | D3 | $0.70 |
| 5 | Context and cost hygiene: `/context`, `/compact`, `/clear`, `/model` + TF-103 · quiz | Basics | D5 | $0.80 |
| **Week 2** | **Context & Memory** | | | **$4** |
| 6 | CLAUDE.md: `/init`, trimming, `@imports`, hierarchy | Intermediate | D2, D5 | $0.60 |
| 7 | Path-scoped rules, `/memory`, testing whether a rule works | Intermediate | D5, D2 | $0.60 |
| 8 | Plan mode for multi-file work (TF-104 tags) | Intermediate | D1, D2 | $1.00 |
| 9 | Git/GitHub: branches, Conventional Commits, PRs, CI diagnosis (TF-105) | Intermediate | D2 | $0.80 |
| 10 | TDD red/green/refactor with coverage (TF-106) · quiz | Intermediate | D3, D2 | $0.90 |
| **Week 3** | **Configuration & Extensibility** | | | **$5** |
| 11 | Settings hierarchy, allow/ask/deny, secrets, sandboxing | Intermediate | D2 | $0.60 |
| 12 | Skills (`SKILL.md`, arguments, manual vs model-invoked) and commands | Intermediate | D2 | $0.90 |
| 13 | Hooks: PreToolUse guard, PostToolUse formatter, Stop notification | Intermediate+ | D2, D5 | $1.00 |
| 14 | Output styles, status line, installing plugins | Intermediate | D2 | $0.80 |
| 15 | Package a team plugin + local marketplace · quiz | Intermediate+ | D2 | $1.20 |
| **Week 4** | **Tools & MCP** | | | **$6** |
| 16 | Connect MCP servers: scopes, `.mcp.json`, `${VAR}` secrets | Advanced | D4 | $0.80 |
| 17 | Build a TaskForge MCP server: tool design | Advanced | D4 | $1.20 |
| 18 | Resources, prompts, MCP security (tool poisoning, least privilege) | Advanced | D4 | $1.00 |
| 19 | Structured output: `claude -p --json-schema`, prompts for machines | Advanced | D3 | $1.00 |
| 20 | Mini-project: MCP-powered standup skill · quiz | Advanced | D4, D2 | $1.20 |
| **Week 5** | **Agents & Automation** | | | **$7** |
| 21 | Subagents: Explore, custom read-only reviewer, Haiku test writer | Advanced | D1, D5 | $1.20 |
| 22 | Parallel sessions with git worktrees (TF-107 + TF-108) | Advanced | D1 | $1.60 |
| 23 | Headless pipelines: JSON, sessions, exit codes, budget caps | Advanced | D2, D3, D5 | $1.00 |
| 24 | Claude in CI: `claude-code-action@v1`, guards and cost controls | Advanced | D2 | $1.20 |
| 25 | Long-task reliability: characterisation tests and handoffs (TF-109) · quiz | Advanced+ | D5, D1 | $1.40 |
| **Week 6** | **Agent SDK, Capstone & Certification** | | | **$6** |
| 26 | Claude Agent SDK: in-process tools, budgets, results | Expert | D1, D4, D3 | $0.80 |
| 27 | Agentic architecture design review (pattern ladder) | Expert | D1 | $0.40 |
| 28 | Capstone build (PR triage bot / ops assistant / refactor agent) | Expert | all | $2.50 |
| 29 | Capstone review, hardening, cost and limitations write-up | Expert | all | $1.50 |
| 30 | Timed 60-question mock CCA-F exam and readiness plan | Expert | all | $0 |

**Total ≈ $31 over 6 weeks.** Any 4 consecutive weeks stay under $27, so the $30/month cap holds wherever the
month boundary falls.

## CCA-F domain coverage

| Domain | Weight | Labs |
|---|---|---|
| D1 Agentic architecture & orchestration | 27% | 8, 21, 22, 25, 26, 27, 28 |
| D2 Claude Code configuration & workflows | 20% | 1–7, 9, 11–15, 23, 24 |
| D3 Prompt engineering & structured output | 20% | 3, 4, 10, 19, 23, 26 |
| D4 Tool design & MCP integration | 18% | 16–20, 26 |
| D5 Context management & reliability | 15% | 5, 6, 7, 13, 21, 25 |

## Assessment

| What | When | Cost |
|---|---|---|
| `labcheck` per lab (hidden acceptance tests, config checks) | daily | free |
| Weekly quizzes (10 scenario questions each) | days 5, 10, 15, 20, 25 | free |
| Capstone, scored on a 50-point rubric (pass ≥ 35) | days 28–29 | ~$4 |
| Mock CCA-F exam (60 questions, 120 minutes; ready at ≥ 72%) | day 30 | free |

## Graduation criteria

- `uv run labcheck --all` passes (30/30)
- Capstone ≥ 35/50 on the rubric
- Mock exam ≥ 72%, with a written study plan for any domain below 70%
