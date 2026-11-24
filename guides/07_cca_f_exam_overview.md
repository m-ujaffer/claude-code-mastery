# Guide 07: The Claude Certified Architect – Foundations (CCA-F) exam

> **Verify before you book.** These details came from Anthropic's announcements and public
> exam-prep write-ups when the course was written (late 2026). Exam guides get revised, so
> always check the **official exam guide** on Anthropic's site for the current version,
> domains, weights, price and eligibility.

## The exam at a glance

| | |
|---|---|
| **Name** | Claude Certified Architect – Foundations (exam code reported as CCAR-F / CCA-F) |
| **Launched** | March 2026, together with the Claude Partner Network |
| **Format** | About 60 scenario-based multiple-choice questions, 120 minutes |
| **Passing score** | Scaled score of 720 (reported) |
| **Fee** | About US$125 (reported) |
| **Access** | Reported to be through the **Claude Partner Network**, which organisations join. Ask your admin whether your company is a member. |
| **Free prep** | Anthropic Academy courses (anthropic.skilljar.com) are open to everyone |

There is also a higher-level **Professional** exam. This course targets Foundations.

## The five domains and where this course covers them

| Domain | Weight | Labs | What you should be able to do |
|---|---|---|---|
| **1. Agentic architecture & orchestration** | 27% | w2d8, w5d21, w5d22, w5d25, w6d26, w6d27, w6d28 | Choose between a single agent, a workflow, orchestrator-workers and evaluator-optimizer. Design subagent boundaries. Plan, then execute. Add human-in-the-loop checkpoints. Recover from errors on long tasks. |
| **2. Claude Code configuration & workflows** | 20% | w1d1–w1d5, w2d6, w2d7, w2d9, w3d11–w3d15, w5d23, w5d24 | Use the CLAUDE.md hierarchy and rules, settings precedence, permissions, skills and slash commands, hooks, plugins, plan mode vs direct execution, headless mode, and CI integration. |
| **3. Prompt engineering & structured output** | 20% | w1d4, w2d10, w4d19, w5d23, w6d26 | Write clear task specs with constraints and verification. Use few-shot examples. Get JSON schema–validated output and parse it robustly. |
| **4. Tool design & MCP integration** | 18% | w4d16–w4d20, w6d26 | Use MCP transports and scopes. Design tools well: names, descriptions, schemas, errors. Understand resources and prompts. Apply MCP security and least privilege. |
| **5. Context management & reliability** | 15% | w1d5, w2d6, w2d7, w5d21, w5d25 | Manage the context budget with `/clear`, `/compact` and subagents. Use memory and handoffs, retries, guardrails and cost controls. |

## How the questions feel

Questions are **scenarios**: "A team wants X under constraint Y. What's the best approach?"
They reward the judgement you practise in the labs:

- the **simplest** architecture that meets the requirement, rather than the fanciest
- **least privilege** for tools, permissions and CI tokens
- **verification built in**: tests, schemas, review gates
- **context discipline**: delegating, summarising, starting fresh
- knowing **which feature fits**: a hook (deterministic, always runs) vs a CLAUDE.md rule (advisory) vs a skill (on-demand procedure) vs a subagent (isolated context)

## Your study path

1. Finish all 30 labs. The weekly quizzes in [assessments/](../assessments) are exam-style.
2. Week 6, Day 30: take the **timed mock exam** (`assessments/mock_exam_cca_f.md`) and do the gap analysis.
3. Re-do the labs for your two weakest domains, and take the matching Anthropic Academy courses.
4. Book the exam once you're scoring **≥ 72%** on the mock with time to spare.
