# Mock exam answers and explanations

Score yourself, then fill in `notes/mock-exam-result.md` (template in `notes/templates/`).
Domain key: **D1** agentic architecture (16) · **D2** Claude Code configuration (12) · **D3** prompt engineering and structured
output (12) · **D4** tool design and MCP (11) · **D5** context management and reliability (9).

| Q | Answer | Domain | Explanation | Revisit |
|---|---|---|---|---|
| 1 | **C** | D4 | Bound result size and offer aggregates, to protect the caller's context. | w4d17 |
| 2 | **C** | D4 | User scope applies across all your projects. | w4d16 |
| 3 | **B** | D1 | Distinct input types with distinct handling is the routing pattern. | w6d27 |
| 4 | **A** | D3 | A missing `structured_output` is a failure to handle explicitly, within retry caps. | w4d19 |
| 5 | **B** | D5 | Always-loaded context (memory, tools) is paid on every request. | w2d6, w2d7, w4d16 |
| 6 | **D** | D1 | Output can be judged by deterministic evaluators, so use an evaluator-optimizer with feedback. | w6d27 |
| 7 | **B** | D3 | Test-first with a frozen spec gives a trustworthy fix. | w1d3, w2d10 |
| 8 | **D** | D4 | Task-shaped, bounded, described with *when to use it* and *what it returns*. | w4d17 |
| 9 | **A** | D3 | Delimit untrusted data, say it isn't instructions, and limit tools (blast radius). | w4d18 |
| 10 | **C** | D1 | Loops need caps and an escalation path; lowering standards hides failures. | w6d27 |
| 11 | **D** | D4 | Tool poisoning; trust, review and pin servers, and keep defence in depth. | w4d18 |
| 12 | **A** | D2 | Path-scoped rules load only when relevant and shrink the always-on context. | w2d7 |
| 13 | **D** | D2 | Plugins via a marketplace give consistent, versioned distribution. | w3d15 |
| 14 | **A** | D2 | Repeatable procedure with supporting files that's used occasionally: a skill. | w3d12 |
| 15 | **D** | D5 | `/clear` between unrelated tasks. | w1d5 |
| 16 | **B** | D2 | Guards cut wasted runs while keeping the reviews that matter. | w5d24 |
| 17 | **C** | D1 | Irreversible, customer-facing actions need human approval before they happen. | w6d27 |
| 18 | **C** | D4 | Resources and prompts are application- or user-controlled; tools are model-controlled. | w4d18 |
| 19 | **B** | D2 | "Every time" calls for a deterministic hook, not an advisory instruction. | w3d13 |
| 20 | **D** | D2 | `disable-model-invocation: true` makes a skill manual only. | w3d12 |
| 21 | **C** | D1 | Agents are justified when the next step depends on what's discovered. | w6d27 |
| 22 | **A** | D1 | Orchestrator-workers gives each worker an isolated context and returns concise findings. | w5d21, w6d27 |
| 23 | **A** | D5 | Deterministic verification beats self-reports. | w2d9, w5d24 |
| 24 | **A** | D2 | Managed settings take precedence over everything and can't be overridden. | w3d11 |
| 25 | **B** | D2 | Least privilege, caps, structured output and exit checks; never bypass in automation. | w5d23 |
| 26 | **B** | D3 | Field descriptions plus few-shot examples drive consistency. | w4d19 |
| 27 | **D** | D2 | Project-scoped MCP config is the checked-in `.mcp.json`. | w4d16 |
| 28 | **B** | D4 | Every tool definition costs context and adds selection noise. | w4d16, w4d17 |
| 29 | **B** | D1 | Fixed steps call for a workflow; over-engineered multi-agent systems are less consistent and cost more. | w6d27 |
| 30 | **C** | D1 | Worktrees isolate parallel sessions; integration goes through tests and review. | w5d22 |
| 31 | **A** | D1 | Durable state in git and handoff files survives restarts and people. | w5d25 |
| 32 | **C** | D1 | Without verification, costly errors go undetected. That's a poor agent fit. | w6d27 |
| 33 | **B** | D5 | Instructions are advisory; permissions and hooks enforce. | w3d11, w3d13 |
| 34 | **D** | D4 | Environment variable expansion keeps secrets out of version control. | w4d16 |
| 35 | **B** | D5 | Pin behaviour before changing it. | w5d25 |
| 36 | **C** | D4 | Remote services use the HTTP transport; stdio is for local processes. | w4d16 |
| 37 | **B** | D5 | Subagents keep the reading out of the main context. | w5d21 |
| 38 | **C** | D2 | Personal overrides go in the git-ignored local settings. | w3d11 |
| 39 | **A** | D5 | External progress state plus small commits survive compaction and restarts. | w5d25 |
| 40 | **D** | D1 | Uncertain multi-file change: explore → plan → approve → implement test-first. | w2d8 |
| 41 | **A** | D5 | `/compact` with a focus keeps continuity at lower cost. | w1d5 |
| 42 | **C** | D1 | Fixed fields and a known procedure: the lowest rung (a single structured call in a batch) is cheapest and most reliable. | w6d27 |
| 43 | **D** | D1 | Destructive tools: human approval or deny by default, plus least-privilege credentials. | w3d11, w6d27 |
| 44 | **B** | D3 | Enforce a schema, then validate again in code: trust, but verify. | w4d19 |
| 45 | **C** | D3 | `stream-json` emits events as they happen. | w5d23 |
| 46 | **A** | D3 | An enum constrains the output space; clear definitions reduce ambiguity. | w4d19 |
| 47 | **C** | D4 | `allowed-tools` pre-approves only the reads; writes still need approval. | w4d20 |
| 48 | **A** | D4 | Consent before repository-defined processes run. | w4d16 |
| 49 | **C** | D3 | `json` returns `result` plus metadata such as cost and session id. | w5d23 |
| 50 | **A** | D2 | Accept-edits auto-approves file edits; commands still ask. | w1d2 |
| 51 | **B** | D3 | Explain the preference and the reason; modern models respond to rationale. | w1d4 |
| 52 | **B** | D3 | Give the model an explicit "unknown" path so it doesn't hallucinate. | w4d19 |
| 53 | **D** | D3 | Specific instructions with reasons; enforce hard requirements deterministically. | w2d7, w3d13 |
| 54 | **C** | D1 | The Agent SDK packages Claude Code's harness for your own code. | w6d26 |
| 55 | **A** | D1 | Subagents start cold; a trivial in-context edit gains nothing. | w5d21 |
| 56 | **D** | D4 | Anticipated failures go back as tool errors with recovery hints; crashes reveal nothing useful. | w4d17 |
| 57 | **A** | D5 | Budget and turn caps bound the worst case. | w5d23, w6d26 |
| 58 | **D** | D3 | Goal, constraints and verification are the core of a task prompt. | w1d4 |
| 59 | **D** | D2 | Only exit code 2 (or a JSON deny) blocks. Other non-zero codes are non-blocking errors. | w3d13 |
| 60 | **D** | D1 | Delegation needs an explicit output contract; sharing full context defeats isolation. | w5d21, w6d27 |
