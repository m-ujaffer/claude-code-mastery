# Mock exam: Claude Certified Architect – Foundations (practice)

**60 questions · 120 minutes · no notes, no Claude** · Answers and explanations:
[answers/mock_exam_answers.md](answers/mock_exam_answers.md)

> This is an unofficial practice exam written for this course. It mirrors the published domain weights and
> the scenario style, but these aren't real exam questions. Choose the **best** answer: several options may
> be workable, and only one is what an architect should recommend.

---

**1.** Your MCP tool returns 5,000 rows when asked for "all tasks". What's the best design fix?
- A) Nothing; more data is better
- B) Compress the JSON
- C) Cap and paginate results, return compact fields, and offer an aggregate tool for counts
- D) Return a CSV string instead

**2.** What's the right scope for an MCP server you personally use across all your projects?
- A) project
- B) managed
- C) user
- D) local to every repo

**3.** A support assistant must handle three request types (billing, technical, account) with very different procedures. Which pattern fits best?
- A) One large prompt containing all three procedures
- B) Routing: classify the request, then hand it to a specialised prompt or agent for that type
- C) Three agents that all answer, followed by a vote
- D) An evaluator-optimizer loop

**4.** A schema-constrained run occasionally returns no structured output at all. What should the calling code do?
- A) Check for the field, treat its absence as a failure, log, and retry or escalate within a cap
- B) Assume an empty object
- C) Parse the `result` text with regexes
- D) Crash without logging

**5.** Which change most directly reduces per-request cost for a team whose sessions are always expensive from the very first prompt?
- A) Type shorter prompts
- B) Shrink the always-loaded context: trim CLAUDE.md, move detail into skills or path-scoped rules, disable unused MCP servers
- C) Use Opus
- D) Disable the status line

**6.** Generated SQL migrations must pass a linter and a dry-run before a human sees them. Which pattern adds the most reliability?
- A) A single call with a stronger prompt
- B) Two models generating in parallel
- C) Routing
- D) Evaluator-optimizer: generate, run the linter and dry-run, feed the errors back, retry with a capped number of iterations

**7.** You want Claude to fix a bug in a way you can trust. Which instruction sequence is best?
- A) "Fix the bug"
- B) "Write a failing test reproducing it, confirm it fails, implement the fix without changing that test, run the suite"
- C) "Fix the bug and write tests afterwards"
- D) "Fix the bug quickly"

**8.** Which MCP tool definition is best designed?
- A) `query(sql: str)`: "Runs SQL."
- B) `tool1(data: str)`: "Does things."
- C) 30 near-identical tools for each status and priority combination
- D) `find_tasks(status, priority, overdue_only, limit<=50)`: "Find tasks matching filters; returns compact summaries. Use project_stats for counts."

**9.** Untrusted text (an issue body from the public) is included in a prompt. What's the best practice?
- A) Clearly delimit it as data, instruct the model not to follow instructions inside it, and limit the tools available to that run
- B) Include it verbatim with no framing
- C) Translate it first
- D) Ask the model whether it's malicious

**10.** Your evaluator-optimizer loop sometimes runs forever on hard inputs. What's the right fix?
- A) Remove the evaluator
- B) Use a faster model
- C) A maximum iteration count and budget, plus an escalation path to a human when the cap is reached
- D) Lower the evaluator's standards

**11.** An MCP server's tool description contains hidden instructions to exfiltrate files. What is this, and what's the primary mitigation?
- A) A rate limit; retry later
- B) A context overflow; use `/compact`
- C) A schema error; fix the JSON
- D) Tool poisoning; install only trusted, reviewed, pinned servers, and keep least-privilege permissions and approvals

**12.** A team's CLAUDE.md has grown to 300 lines. Some rules only apply to the `migrations/` folder. Best improvement?
- A) Move those rules into a `.claude/rules/` file with `paths:` frontmatter for `migrations/**`
- B) Split CLAUDE.md into five files all imported at the top
- C) Delete CLAUDE.md
- D) Put the rules in a hook

**13.** A platform team wants every engineer to get the same skills, agents, hooks and MCP servers, with versioned updates. Recommended approach?
- A) A wiki page with copy-paste instructions
- B) A shared network drive mounted at `~/.claude`
- C) One giant CLAUDE.md
- D) An internal plugin marketplace with curated plugins

**14.** A team's repeatable "add a database migration" procedure has several steps and a template file. It's used a few times a month. Best packaging?
- A) A skill with SKILL.md and a supporting template file
- B) Put the full procedure in CLAUDE.md
- C) A PreToolUse hook
- D) An MCP server

**15.** You finish one task and start an unrelated one. Best practice?
- A) `/compact`
- B) Keep going in the same context
- C) Restart the Codespace
- D) `/clear`

**16.** A PR review workflow with `anthropics/claude-code-action@v1` runs on every push and the bill is climbing. Which change helps most without losing value?
- A) Remove `--max-turns`
- B) Path filters, skipping draft PRs, and `concurrency` with `cancel-in-progress`
- C) Use Opus
- D) Run it on a schedule every 5 minutes

**17.** Where should human approval sit in an agent that drafts and *sends* customer refund emails?
- A) Nowhere; the agent is accurate
- B) After sending, in a weekly audit
- C) Before sending: the agent drafts and a human approves irreversible, customer-facing actions
- D) Only for refunds over $10,000

**18.** In MCP, which primitive is chosen by the **user or application** rather than by the model?
- A) Tools
- B) Sampling
- C) Resources (and prompts)
- D) Hooks

**19.** A rule must run **every** time Claude edits a Python file: format it with the team formatter. What's the right mechanism?
- A) A line in CLAUDE.md
- B) A PostToolUse hook matching Edit|Write
- C) A skill
- D) An output style

**20.** You want a skill to be usable only when a human types its slash command, never chosen automatically by Claude. What do you set?
- A) `allowed-tools`
- B) `model: haiku`
- C) `context: fork`
- D) `disable-model-invocation: true`

**21.** A design review asks why you chose a single agent with tools instead of a workflow. Which justification is strongest?
- A) Agents are more modern
- B) Workflows can't call models
- C) The steps vary per input and can't be known in advance, so the model must decide the next action
- D) Agents are cheaper

**22.** An agent researches a question across 40 internal documents. The main conversation keeps hitting its context limits. Best architectural change?
- A) Have worker subagents each read a subset and return concise findings to an orchestrator
- B) Switch to a model with a larger context window and keep the design
- C) Ask the agent to "be more concise"
- D) Disable tool use

**23.** An agent reports "all tests pass", but CI fails. What's the best process improvement?
- A) Make verification deterministic: run tests in CI, gate merges on them, and have the agent show the actual command output
- B) Trust the agent less, informally
- C) Ask the agent to double-check
- D) Switch models

**24.** A security team needs a rule that no project or user setting can override. Where does it go?
- A) Managed settings deployed by IT
- B) The project `.claude/settings.json`
- C) `~/.claude/settings.json`
- D) CLAUDE.md

**25.** A nightly script runs `claude -p`. Which combination makes it safest and most predictable?
- A) `--permission-mode bypassPermissions`
- B) A least-privilege `--allowedTools` list, `--max-turns`, `--max-budget-usd`, JSON output, and checking the exit status
- C) `--verbose` only
- D) Running it interactively in tmux

**26.** Which prompt change most improves consistency of a free-text `summary` field across thousands of runs?
- A) "IMPORTANT: BE CONSISTENT"
- B) A precise field description plus one or two worked examples (few-shot)
- C) A higher temperature
- D) A longer system prompt about the company's history

**27.** Where should a repository's shared MCP server configuration live?
- A) `~/.claude.json`, under project scope
- B) CLAUDE.md
- C) `.claude/settings.local.json`
- D) `.mcp.json` at the repository root (project scope)

**28.** Why does connecting many MCP servers with dozens of tools each degrade an agent, even if they're never called?
- A) It doesn't
- B) Tool definitions consume context in every request and make correct tool selection harder
- C) MCP servers slow down the network
- D) Claude Code limits you to one server

**29.** A team built a five-agent system for a task with fixed, known steps. Results are inconsistent and expensive. What should an architect recommend?
- A) Add a sixth agent to supervise
- B) Replace it with a deterministic workflow (prompt chain) that has validation between steps
- C) Raise every agent's effort
- D) Switch all agents to Haiku

**30.** Two independent backlog items touch separate modules. An engineer wants Claude to work on both at once. Best setup?
- A) One session, alternating prompts
- B) Two sessions in the same directory
- C) Two sessions in separate git worktrees on separate branches, integrated through tests and review
- D) One session with two subagents editing the same checkout

**31.** A long-running agent task must survive restarts and be resumable by a different engineer. What's the most robust mechanism?
- A) Small committed steps plus a written handoff or plan file (goal, done, next, risks, verification) the agent re-reads
- B) Keep the session open
- C) A larger context window
- D) Auto-compaction

**32.** Which is the best signal that an agent is a poor fit for a task?
- A) The task has many steps
- B) The task involves code
- C) Errors are costly, hard to detect, and there's no way to verify outputs
- D) The task needs tools

**33.** A CLAUDE.md instruction says "never read .env", but Claude reads it with a shell command anyway. What's the reliable fix?
- A) Repeat the instruction in caps
- B) Enforce it: a deny rule for the relevant tool patterns and/or a PreToolUse hook that blocks such commands
- C) Delete `.env`
- D) Use plan mode

**34.** A remote MCP server needs a bearer token. How should the shared configuration be written?
- A) Commit the token in `.mcp.json`
- B) Put the token in the server's name
- C) Email it to the team
- D) Reference an environment variable (`${TOKEN}`) in the header; each engineer supplies it from their secret store

**35.** Before an agent refactors code whose exact output is relied on by customers, what's essential?
- A) A new style guide
- B) Characterisation tests that pin current behaviour, run after every step
- C) A different model
- D) A larger context window

**36.** Which MCP transport is appropriate for a vendor-hosted service your team connects to over the network?
- A) stdio
- B) Unix pipes only
- C) HTTP
- D) Email

**37.** A large read-heavy investigation is polluting the main session. Best technique?
- A) Read the files manually and paste them in
- B) Delegate it to a (cheap-model) subagent that returns only a summary
- C) Raise effort to max
- D) Use plan mode

**38.** Which belongs in `.claude/settings.local.json` rather than `.claude/settings.json`?
- A) Team-wide deny rules for `.env` files
- B) The shared MCP server list
- C) A personal allow rule for a command only you use
- D) Team hooks

**39.** A multi-day agent migration loses track of what's done after context compaction. What helps most?
- A) An external, regularly updated progress file (plan or handoff) plus small committed steps, which the agent re-reads at the start of each step
- B) Never compact
- C) Bigger model
- D) More detailed initial prompt only

**40.** In Claude Code, an engineer must make a change touching the schema, repository, API and tests, and isn't sure of the approach. Best workflow?
- A) Accept-edits mode and one big prompt
- B) Ask for the code in one message and review afterwards
- C) Parallel sessions on each layer
- D) Plan mode: explore, propose and refine the plan, then approve and implement with tests first

**41.** Mid-task, the context is large but you need continuity. Which command is most appropriate?
- A) `/compact` with instructions about what to keep
- B) `/clear`
- C) `/exit`
- D) `/model opus`

**42.** A team wants to extract the invoice number, date and total from 5,000 PDFs every night. The fields are always present. What's the most appropriate design?
- A) An autonomous agent with file and web tools per document
- B) An orchestrator agent that spawns a subagent per field
- C) A single model call per document with structured (schema-validated) output, run as a batch workflow
- D) An evaluator-optimizer loop for every document

**43.** An agent can call `delete_customer`. What's the most important safeguard?
- A) A good tool description
- B) A faster model
- C) Logging only
- D) Require explicit human approval (or deny it by default), and give the agent least-privilege credentials

**44.** A downstream service parses Claude's output. Which approach gives the most reliable machine-readable results?
- A) "Respond in JSON please"
- B) Enforce a JSON Schema (e.g. `--json-schema`) and validate again in code before use
- C) Regex the free text
- D) Ask for YAML

**45.** You need tokens to stream for a live progress display in your own UI. Which option?
- A) `--output-format json`
- B) `--max-turns 1`
- C) `--output-format stream-json` (with `--verbose`)
- D) `--continue`

**46.** A classifier must choose one of four categories but sometimes invents a fifth. Best fix?
- A) Constrain the output with an enum in the schema and define each category clearly
- B) Ask it nicely
- C) Post-process with string similarity
- D) Use a bigger model

**47.** A skill should only be able to read data through MCP tools, never write. What's the most direct control?
- A) A sentence in the skill body
- B) `model: haiku`
- C) `allowed-tools` listing only the read-only `mcp__server__tool` names, so writes still require approval
- D) An output style

**48.** Claude Code prompts for approval before starting servers defined in a cloned repo's `.mcp.json`. Why?
- A) Repository content shouldn't be able to start processes on your machine without your consent
- B) Licensing
- C) To measure usage
- D) Servers need warming up

**49.** A headless run must return the result plus cost and session metadata. Which output format?
- A) `text`
- B) `markdown`
- C) `json`
- D) `html`

**50.** An engineer wants Claude to auto-approve file edits for this session but keep asking before shell commands. Which mode?
- A) Accept edits
- B) Plan
- C) Bypass permissions
- D) Default

**51.** Claude Code keeps over-engineering solutions with extra abstractions. Best prompt adjustment?
- A) "Never write classes"
- B) State the preference and the reason: "Prefer the smallest change that meets the acceptance criteria; we optimise for reviewability"
- C) Switch to Haiku
- D) Disable plan mode

**52.** An extraction prompt must handle documents where a field is genuinely missing. What should the schema and prompt specify?
- A) Nothing; the model will figure it out
- B) An explicit representation for "unknown" or "absent" (e.g. null or `unknown`), and instructions to use it instead of guessing
- C) Fill it with a plausible value
- D) Fail the whole batch

**53.** A team writes instructions in ALL CAPS ("YOU MUST ALWAYS…") and still sees inconsistent compliance. What usually works better with current models?
- A) More caps and exclamation marks
- B) Repeating the instruction five times
- C) Moving it to the end of the file
- D) Calm, specific instructions with the reason behind them, plus verification such as tests or hooks for hard requirements

**54.** You're building a product feature that needs Claude Code's tools, permissions and agent loop inside your own Python service. What should you use?
- A) Screen-scrape the CLI
- B) A cron job running the interactive CLI
- C) The Claude Agent SDK
- D) A browser extension

**55.** Which task benefits **least** from a subagent?
- A) Renaming a variable on a line you're both already looking at
- B) Searching a large codebase for usages of a deprecated API
- C) An independent second-opinion review of a diff
- D) Summarising long CI logs

**56.** An MCP tool fails because of a bad id. In the Python MCP SDK, how should the tool signal it so the model can recover?
- A) Let any exception propagate
- B) Return an empty list
- C) `sys.exit(1)`
- D) Raise the SDK's tool error type with a message explaining the problem and the recovery step

**57.** A scripted run must never exceed a cost ceiling, even if the model loops. Which mechanism enforces it?
- A) `--max-budget-usd` (or `max_budget_usd` in the SDK) together with `--max-turns`
- B) A polite instruction about cost
- C) Haiku
- D) A smaller prompt

**58.** A task prompt for Claude Code reads "improve the code". What's the most important missing element?
- A) A deadline
- B) Emojis
- C) The engineer's name
- D) A concrete goal, with constraints and how success is verified (tests, acceptance criteria)

**59.** A PreToolUse hook script exits with code 1 and prints an error. What happens?
- A) The tool call is blocked
- B) Claude Code exits
- C) The session is rewound
- D) It's treated as a non-blocking error, and the tool call proceeds

**60.** An orchestrator delegates to three workers. Workers' summaries keep omitting details the orchestrator later needs. Best fix?
- A) Give workers the orchestrator's full context
- B) Make workers use Opus
- C) Merge everything into one agent
- D) Specify the exact output format and required fields in the delegation (a contract), and validate it
