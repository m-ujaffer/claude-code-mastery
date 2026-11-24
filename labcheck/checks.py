"""One check function per lab. Each one inspects the repo and records results.

Checks are deliberately behavioural (run tests, parse config) rather than
"did you type exactly this": any good solution should pass.
"""

from __future__ import annotations

import ast
import json
import os
import re
import shutil
import stat
import subprocess
import sys

import yaml

from labcheck.core import Ctx, Lab, as_list, read_cost_log

LABS: dict[str, Lab] = {}


def lab(lab_id: str, title: str):
    def register(func):
        LABS[lab_id] = Lab(lab_id, title, func)
        return func

    return register


def notes_answered(c: Ctx, rel: str, keys: list[str]) -> bool:
    """Each `- key:` line in a notes template must have an answer after the colon."""
    text = c.read(rel)
    unanswered = [
        k for k in keys
        if not re.search(rf"^[ \t]*[-*]?[ \t]*\**{re.escape(k)}\**[ \t]*:[ \t]*\S", text, re.M | re.I)
    ]
    return c.check(
        bool(text) and not unanswered,
        f"{rel} is filled in",
        f"answer: {', '.join(unanswered)}" if text else f"create {rel} from the template in the lab",
    )


# =============================================================== Week 1


PROGRESS_BRANCH = re.compile(r"^[a-z]+(-[a-z]+)+$")  # firstname-lastname, e.g. jane-doe


@lab("w1d1", "Your first Claude Code session")
def w1d1(c: Ctx):
    local = c.git("branch", "--format=%(refname:short)").split()
    mine = [b for b in local if PROGRESS_BRANCH.match(b)]
    if c.check(bool(mine), "a personal progress branch named firstname-lastname exists",
               "git switch -c jane-doe   (lowercase, hyphenated: see step 1)"):
        remote = c.git("branch", "-r", "--format=%(refname:short)").split()
        pushed = [b for b in mine if f"origin/{b}" in remote]
        c.check(bool(pushed), f"your branch {mine[0]} is pushed to GitHub",
                f"git push -u origin {mine[0]}")
    c.check(shutil.which("claude") is not None, "Claude Code CLI is installed",
            "rebuild the Codespace or see setup/troubleshooting.md")
    key = os.environ.get("ANTHROPIC_API_KEY", "")
    c.check(key.startswith("sk-ant-"), "ANTHROPIC_API_KEY is set in this Codespace",
            "add it as a Codespaces secret, then rebuild (setup/SETUP-codespaces.md)")
    if c.exists("notes/taskforge-overview.md"):
        text = c.read("notes/taskforge-overview.md").lower()
        c.check(all(w in text for w in ("repository", "services")) and len(text) > 400,
                "overview explains the repository and services layers",
                "ask Claude to expand the overview (step 6)")
    c.cost_logged("w1d1")


@lab("w1d2", "Permission modes, mentions, bash mode and rewind")
def w1d2(c: Ctx):
    notes_answered(c, "notes/w1d2-modes.md",
                   ["default", "acceptEdits", "plan", "@ mention", "! bash", "esc", "rewind"])
    main = c.read("practice-app/src/taskforge/main.py")
    c.check("def health" in main and "/version" not in main,
            "the experiment was rewound: main.py has no /version endpoint",
            "use /rewind (or git restore practice-app) to undo step 2")
    c.cost_logged("w1d2")


@lab("w1d3", "Fix TF-101 test-first")
def w1d3(c: Ctx):
    c.hidden_tests("test_w1d3.py", "TF-101")
    c.own_tests_pass()
    n = c.count_tests("practice-app/tests/test_services.py")
    c.check(n >= 5, f"regression tests added to test_services.py ({n} tests, need ≥5)",
            "write tests for 'due today' and 'done but past due'")
    c.cost_logged("w1d3")


@lab("w1d4", "Prompting for code: TF-102")
def w1d4(c: Ctx):
    c.hidden_tests("test_w1d4.py", "TF-102")
    c.own_tests_pass()
    c.headings_present("notes/w1d4-prompts.md", ["Vague prompt", "Precise prompt", "What I learned"])
    costs = re.findall(r"\$\s?\d+\.\d+", c.read("notes/w1d4-prompts.md"))
    c.check(len(costs) >= 2, "both prompt costs recorded (e.g. $0.21)", "copy the numbers from /cost")
    c.cost_logged("w1d4")


@lab("w1d5", "Context hygiene + TF-103 mini-feature")
def w1d5(c: Ctx):
    c.hidden_tests("test_w1d5.py", "TF-103")
    c.own_tests_pass()
    notes_answered(c, "notes/w1d5-context.md", ["before /compact", "after /compact", "model used"])
    week1 = [r for r in read_cost_log(c.root) if r.get("lab", "").startswith("w1")]
    c.remind(len(week1) >= 4, f"week 1 cost log has {len(week1)} entries (aim for 5)")


# =============================================================== Week 2


@lab("w2d6", "CLAUDE.md: project memory")
def w2d6(c: Ctx):
    if not c.exists("CLAUDE.md", "run /init from the repo root, then trim it"):
        return
    text = c.read("CLAUDE.md")
    lines = text.count("\n") + 1
    c.check(lines <= 120, f"CLAUDE.md is lean ({lines} lines, limit 120)",
            "every line costs tokens in every session: cut it down")
    c.check("uv run pytest" in text, "CLAUDE.md tells Claude how to run the tests")
    c.check("clock" in text, "CLAUDE.md mentions the clock.today() convention")
    c.check(len(re.findall(r"^##\s", text, re.M)) >= 3, "CLAUDE.md has at least 3 ## sections")
    c.check(re.search(r"(^|\s)@[\w./-]+\.md", text) is not None,
            "CLAUDE.md uses an @import", "e.g. 'See @practice-app/README.md for the layout'")
    c.cost_logged("w2d6")


@lab("w2d7", "Rules, memory and checking that they work")
def w2d7(c: Ctx):
    rules = sorted((c.root / ".claude" / "rules").glob("**/*.md"))
    c.check(bool(rules), ".claude/rules/ contains at least one rule file")
    scoped = [r for r in rules if c.frontmatter(str(r.relative_to(c.root))).get("paths")]
    c.check(bool(scoped), "a rule is path-scoped with `paths:` frontmatter",
            "e.g. paths: [\"practice-app/tests/**\"]")
    notes_answered(c, "notes/w2d7-memory.md", ["rule tested", "result without rule", "result with rule"])
    c.cost_logged("w2d7")


@lab("w2d8", "Plan mode: TF-104 tags")
def w2d8(c: Ctx):
    c.hidden_tests("test_w2d8.py", "TF-104")
    c.own_tests_pass()
    c.exists("notes/plans/tf-104-plan.md", "save the approved plan (step 4)")
    c.cost_logged("w2d8")


@lab("w2d9", "Git and GitHub workflow: TF-105")
def w2d9(c: Ctx):
    c.hidden_tests("test_w2d9.py", "TF-105")
    c.own_tests_pass()
    log = c.git("log", "--all", "--format=%s")
    c.check(re.search(r"^(feat|fix)(\(.+\))?!?: .*TF-105", log, re.M | re.I) is not None,
            "a Conventional Commit mentions TF-105 (e.g. 'feat(tasks): record completed_at (TF-105)')")
    # The branch may be deleted after a squash-merge, so the reflog counts too.
    branches = c.git("branch", "--all", "--format=%(refname:short)") + c.git("reflog", "-n", "500")
    c.check(re.search(r"tf-105", branches, re.I) is not None, "work was done on a TF-105 branch")
    c.cost_logged("w2d9")


@lab("w2d10", "TDD: TF-106 stats with coverage")
def w2d10(c: Ctx):
    c.hidden_tests("test_w2d10.py", "TF-106")
    proc = c.run(sys.executable, "-m", "pytest", "practice-app/tests", "-p", "no:cacheprovider",
                 "--cov=taskforge.services", "--cov-report=term", env=c.pytest_env())
    match = re.search(r"services\.py\s+\d+\s+\d+\s+(\d+)%", proc.stdout)
    pct = int(match.group(1)) if match else 0
    c.check(proc.returncode == 0 and pct >= 90, f"services.py coverage from your tests: {pct}% (need ≥90%)",
            "uv run pytest --cov=taskforge.services --cov-report=term-missing")
    c.cost_logged("w2d10")


# =============================================================== Week 3


@lab("w3d11", "Settings and permissions")
def w3d11(c: Ctx):
    perms = c.settings().get("permissions", {})
    deny, ask = as_list(perms.get("deny")), as_list(perms.get("ask"))
    c.check(any(".env" in r for r in deny), "reading .env files is denied")
    c.check(any(r.startswith("Bash(git push") for r in ask),
            "`git push` requires confirmation (an `ask` rule)")
    c.check(any("rm -rf" in r or r.startswith("Bash(rm ") for r in deny),
            "destructive `rm` commands are denied")
    c.check(c.path(".claude/settings.local.json").exists(),
            ".claude/settings.local.json exists for personal overrides")
    ignored = c.run("git", "check-ignore", "-q", ".claude/settings.local.json").returncode == 0
    c.check(ignored, "settings.local.json is git-ignored")
    c.cost_logged("w3d11")


@lab("w3d12", "Skills and slash commands")
def w3d12(c: Ctx):
    rel = ".claude/skills/tf-issue/SKILL.md"
    if c.exists(rel, "create the tf-issue skill (step 3)"):
        fm = c.frontmatter(rel)
        c.check(len(str(fm.get("description", ""))) >= 30, "skill has a meaningful description")
        c.check("$ARGUMENTS" in c.read(rel) or "$0" in c.read(rel), "skill uses its arguments")
        c.check(fm.get("disable-model-invocation") is True,
                "skill is manual-only (disable-model-invocation: true)")
    cmds = list((c.root / ".claude" / "commands").glob("*.md"))
    c.check(bool(cmds), "a classic slash command exists in .claude/commands/")
    c.cost_logged("w3d12")


def _hook_commands(settings: dict, event: str) -> list[tuple[str, str]]:
    out = []
    for entry in settings.get("hooks", {}).get(event, []) or []:
        for h in entry.get("hooks", []) or []:
            out.append((entry.get("matcher", ""), h.get("command", "")))
    return out


@lab("w3d13", "Hooks: guardrails and auto-formatting")
def w3d13(c: Ctx):
    settings = c.settings()
    pre = _hook_commands(settings, "PreToolUse")
    post = _hook_commands(settings, "PostToolUse")
    c.check(any("Bash" in m for m, _ in pre), "a PreToolUse hook is registered for Bash")
    c.check(any(("Edit" in m or "Write" in m) and "ruff" in cmd for m, cmd in post)
            or any("ruff" in c.read(p) for p in _script_paths(post)),
            "a PostToolUse hook runs ruff after edits")
    rel = ".claude/hooks/block-dangerous.py"
    if c.exists(rel):
        def run(cmd: str) -> int:
            payload = json.dumps({"hook_event_name": "PreToolUse", "tool_name": "Bash",
                                  "tool_input": {"command": cmd}})
            return subprocess.run([sys.executable, str(c.path(rel))], input=payload,
                                  capture_output=True, text=True, timeout=20).returncode
        c.check(run("rm -rf /") == 2, "hook blocks `rm -rf /` (exit code 2)")
        c.check(run("git push --force origin main") == 2, "hook blocks force-pushes")
        c.check(run("uv run pytest") == 0, "hook allows `uv run pytest`")
    c.cost_logged("w3d13")


def _script_paths(entries: list[tuple[str, str]]) -> list[str]:
    paths = []
    for _, cmd in entries:
        for token in cmd.replace('"', " ").split():
            token = token.replace("${CLAUDE_PROJECT_DIR}/", "").replace("$CLAUDE_PROJECT_DIR/", "")
            if token.startswith(".claude/"):
                paths.append(token)
    return paths


@lab("w3d14", "Output styles, status line and plugins")
def w3d14(c: Ctx):
    styles = list((c.root / ".claude" / "output-styles").glob("*.md"))
    c.check(bool(styles), "a custom output style exists in .claude/output-styles/")
    for s in styles[:1]:
        fm = c.frontmatter(str(s.relative_to(c.root)))
        c.check(bool(fm.get("description")), f"{s.name} has a description")
    c.check("branch" in c.read(".claude/statusline.py").lower(),
            "status line shows the git branch (step 5)")
    notes_answered(c, "notes/w3d14-plugins.md", ["plugin installed", "what it added", "would my team use it"])
    c.cost_logged("w3d14")


@lab("w3d15", "Package a team plugin")
def w3d15(c: Ctx):
    base = "plugins/taskforge-toolkit"
    manifest = c.json(f"{base}/.claude-plugin/plugin.json")
    c.check(isinstance(manifest, dict) and manifest.get("name") == "taskforge-toolkit",
            "plugin.json is valid and named taskforge-toolkit")
    if isinstance(manifest, dict):
        c.check(bool(manifest.get("description")) and bool(manifest.get("version")),
                "plugin.json has a description and version")
    skills = list((c.root / base / "skills").glob("*/SKILL.md"))
    c.check(bool(skills), "plugin ships at least one skill")
    agents_or_cmds = list((c.root / base / "agents").glob("*.md")) + list((c.root / base / "commands").glob("*.md"))
    c.check(bool(agents_or_cmds), "plugin ships a command or an agent")
    hooks = c.json(f"{base}/hooks/hooks.json")
    c.check(isinstance(hooks, dict) and "hooks" in hooks, "hooks/hooks.json is valid with a top-level 'hooks' key")
    c.exists(f"{base}/README.md")
    c.cost_logged("w3d15")


# =============================================================== Week 4

SECRET_PATTERNS = re.compile(r"(sk-ant-[\w-]{10,}|ghp_[\w]{10,}|github_pat_[\w]{10,})")


@lab("w4d16", "Connect an MCP server")
def w4d16(c: Ctx):
    data = c.json(".mcp.json")
    servers = data.get("mcpServers", {}) if isinstance(data, dict) else {}
    c.check(bool(servers), ".mcp.json defines at least one server", "claude mcp add --scope project ...")
    c.check(not SECRET_PATTERNS.search(c.read(".mcp.json")),
            ".mcp.json contains no literal secrets (use ${VAR} expansion)")
    notes_answered(c, "notes/w4d16-mcp.md", ["server added", "scope chosen", "tools it exposes", "one task it did"])
    c.cost_logged("w4d16")


MCP_PROBE = r"""
import asyncio, inspect, json
import taskforge.mcp_server as mod

def find_server():
    for value in vars(mod).values():
        if all(hasattr(value, a) for a in ("list_tools", "list_resources", "list_prompts", "run")) \
                and not inspect.isclass(value) and not inspect.ismodule(value):
            return value
    raise SystemExit("no MCP server object (MCPServer) found in taskforge.mcp_server")

async def call(fn):
    result = fn()
    return await result if inspect.isawaitable(result) else result

async def main():
    server = find_server()
    tools = await call(server.list_tools)
    res = await call(server.list_resources)
    tmpl = await call(server.list_resource_templates) if hasattr(server, "list_resource_templates") else []
    prompts = await call(server.list_prompts)
    print(json.dumps({
        "tools": [{"name": t.name, "description": t.description or "",
                   "schema": getattr(t, "input_schema", None) or getattr(t, "inputSchema", None)} for t in tools],
        "resources": len(res) + len(tmpl),
        "prompts": len(prompts),
    }))
asyncio.run(main())
"""


def _probe_mcp(c: Ctx) -> dict | None:
    proc = c.run(sys.executable, "-c", MCP_PROBE, env=c.pytest_env(), timeout=60)
    if proc.returncode != 0:
        c.check(False, "taskforge.mcp_server imports and lists its tools",
                (proc.stderr.strip().splitlines() or ["?"])[-1])
        return None
    return json.loads(proc.stdout.strip().splitlines()[-1])


@lab("w4d17", "Build an MCP server for TaskForge")
def w4d17(c: Ctx):
    if not c.exists("practice-app/src/taskforge/mcp_server.py"):
        return
    info = _probe_mcp(c)
    if info is None:
        return
    tools = info["tools"]
    c.check(len(tools) >= 3, f"server exposes {len(tools)} tools (need ≥3)")
    weak = [t["name"] for t in tools if len(t["description"]) < 40]
    c.check(not weak, "every tool has a helpful description (≥40 chars)",
            f"improve: {', '.join(weak)}" if weak else "")
    bad = [t["name"] for t in tools if not re.fullmatch(r"[a-z][a-z0-9_]*", t["name"])]
    c.check(not bad, "tool names are snake_case verbs", ", ".join(bad))
    servers = (c.json(".mcp.json") or {}).get("mcpServers", {})
    c.check(any("mcp_server" in json.dumps(s) for s in servers.values()),
            ".mcp.json registers the taskforge server")
    c.cost_logged("w4d17")


@lab("w4d18", "MCP resources, prompts and security")
def w4d18(c: Ctx):
    info = _probe_mcp(c)
    if info:
        c.check(info["resources"] >= 1, "server exposes at least one resource")
        c.check(info["prompts"] >= 1, "server exposes at least one prompt")
    notes_answered(c, "notes/w4d18-mcp-security.md",
                   ["tool poisoning", "least privilege", "secrets", "what I would review before installing a server"])
    c.cost_logged("w4d18")


@lab("w4d19", "Structured output from headless Claude")
def w4d19(c: Ctx):
    schema = c.json("schemas/triage.schema.json")
    ok = isinstance(schema, dict)
    if c.check(ok, "schemas/triage.schema.json is valid JSON"):
        import jsonschema
        try:
            jsonschema.Draft202012Validator.check_schema(schema)
            valid_schema = True
        except jsonschema.SchemaError:
            valid_schema = False
        c.check(valid_schema, "it is a valid JSON Schema")
        c.check(set(schema.get("required", [])) >= {"issue_id", "type", "severity", "summary"},
                "schema requires issue_id, type, severity, summary")
        sample = c.json("notes/triage-output.json")
        items = sample if isinstance(sample, list) else [sample]
        try:
            for item in items:
                jsonschema.validate(item, schema)
            sample_ok = sample is not None
        except jsonschema.ValidationError:
            sample_ok = False
        c.check(sample_ok, "notes/triage-output.json validates against the schema")
    script = c.read("scripts/triage.sh")
    c.check("claude -p" in script or "claude --print" in script, "scripts/triage.sh runs claude headless")
    c.check("--json-schema" in script, "triage.sh enforces the schema with --json-schema")
    c.check("--max-budget-usd" in script and "--max-turns" in script, "triage.sh caps budget and turns")
    c.cost_logged("w4d19")


@lab("w4d20", "Mini-project: MCP-powered standup skill")
def w4d20(c: Ctx):
    rel = ".claude/skills/standup/SKILL.md"
    if c.exists(rel):
        text = c.read(rel)
        c.check("mcp__" in text, "standup skill uses TaskForge MCP tools (mcp__<server>__<tool>)")
        fm = c.frontmatter(rel)
        c.check(bool(fm.get("allowed-tools")), "skill pre-approves only the tools it needs (allowed-tools)")
    c.exists("notes/standup-sample.md", "save one real standup output")
    c.cost_logged("w4d20")


# =============================================================== Week 5


def _agent(c: Ctx, name: str) -> dict:
    return c.frontmatter(f".claude/agents/{name}.md")


@lab("w5d21", "Subagents")
def w5d21(c: Ctx):
    reviewer, writer = _agent(c, "code-reviewer"), _agent(c, "test-writer")
    c.check(bool(reviewer.get("description")), ".claude/agents/code-reviewer.md exists with a description")
    rtools = as_list(reviewer.get("tools"))
    c.check(bool(rtools) and not ({"Edit", "Write"} & set(rtools)),
            "code-reviewer is read-only (tools list without Edit/Write)")
    c.check(bool(writer.get("description")), ".claude/agents/test-writer.md exists with a description")
    c.check(str(writer.get("model", "")).lower() == "haiku" or str(reviewer.get("model", "")).lower() == "haiku",
            "at least one subagent runs on the cheaper haiku model")
    notes_answered(c, "notes/w5d21-subagents.md", ["main context before", "main context after", "when not to use a subagent"])
    c.cost_logged("w5d21")


@lab("w5d22", "Parallel work with git worktrees: TF-107 + TF-108")
def w5d22(c: Ctx):
    c.hidden_tests("test_w5d22.py", "TF-107/TF-108")
    c.own_tests_pass()
    log = c.git("log", "--all", "--format=%s")
    c.check("TF-107" in log and "TF-108" in log, "commits for both TF-107 and TF-108 exist")
    merges = c.git("log", "--merges", "--format=%s")
    c.remind(bool(merges.strip()), "branches were merged back (a merge commit exists)")
    c.cost_logged("w5d22")


@lab("w5d23", "Headless mode and scripted pipelines")
def w5d23(c: Ctx):
    rel = "scripts/nightly_report.sh"
    if not c.exists(rel):
        return
    text = c.read(rel)
    for flag in ("-p", "--output-format json", "--max-turns", "--max-budget-usd", "--allowedTools"):
        c.check(flag in text, f"nightly_report.sh uses {flag}")
    mode = c.path(rel).stat().st_mode
    c.check(bool(mode & stat.S_IXUSR), "script is executable (chmod +x)")
    c.check(c.run("bash", "-n", rel).returncode == 0, "script has valid bash syntax")
    c.check("total_cost_usd" in text, "script reads total_cost_usd from the JSON result")
    c.cost_logged("w5d23")


@lab("w5d24", "Claude in CI with GitHub Actions")
def w5d24(c: Ctx):
    rel = ".github/workflows/claude-review.yml"
    if not c.exists(rel):
        return
    try:
        wf = yaml.safe_load(c.read(rel)) or {}
    except yaml.YAMLError:
        c.check(False, "workflow is valid YAML")
        return
    text = c.read(rel)
    c.check(re.search(r"anthropics/claude-code-action@(v1\b|[0-9a-f]{40}\b)", text) is not None,
            "uses anthropics/claude-code-action@v1 (or pinned to a full commit SHA)")
    c.check("secrets.ANTHROPIC_API_KEY" in text, "API key comes from repository secrets")
    c.check("--max-turns" in text, "claude_args caps --max-turns")
    triggers = wf.get("on", wf.get(True, {}))  # YAML 1.1 parses `on:` as True
    c.check(bool(triggers), "workflow has triggers")
    jobs = wf.get("jobs", {})
    guarded = any("if" in j for j in jobs.values()) or "paths" in json.dumps(triggers, default=str)
    c.check(guarded, "runs are guarded (an `if:` condition or a `paths:` filter) to control cost")
    c.check(any("permissions" in j for j in jobs.values()) or "permissions" in wf,
            "job declares explicit, minimal permissions")
    c.check("concurrency" in wf or any("concurrency" in j for j in jobs.values()),
            "concurrency group cancels superseded runs")
    c.cost_logged("w5d24")


def _longest_function(source: str) -> tuple[str, int]:
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return ("<syntax error>", 999)
    longest = ("", 0)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
            length = node.end_lineno - node.lineno + 1
            if length > longest[1]:
                longest = (node.name, length)
    return longest


@lab("w5d25", "Reliability on long tasks: TF-109 refactor")
def w5d25(c: Ctx):
    c.hidden_tests("test_w5d25.py", "TF-109 golden-output")
    n = c.count_tests("practice-app/tests/test_report_builder.py")
    c.check(n >= 3, f"characterisation tests exist ({n} in test_report_builder.py)")
    c.own_tests_pass()
    name, length = _longest_function(c.read("practice-app/src/taskforge/legacy/report_builder.py"))
    c.check(length <= 40, f"longest function in report_builder.py: {name} ({length} lines, limit 40)")
    c.headings_present("notes/HANDOFF.md", ["Goal", "Done", "Next", "Risks"])
    c.cost_logged("w5d25")


# =============================================================== Week 6


@lab("w6d26", "Claude Agent SDK")
def w6d26(c: Ctx):
    rel = "sdk_agents/release_notes_agent.py"
    if not c.exists(rel):
        return
    src = c.read(rel)
    c.check("claude_agent_sdk" in src, "imports claude_agent_sdk")
    for opt in ("allowed_tools", "max_turns", "max_budget_usd"):
        c.check(re.search(rf"\b{opt}\s*=", src) is not None, f"ClaudeAgentOptions sets {opt}")
    c.check("create_sdk_mcp_server" in src and "@tool" in src, "defines a custom in-process tool")
    c.check("total_cost_usd" in src, "reports the run's total_cost_usd")
    c.check(c.run(sys.executable, "-m", "py_compile", rel).returncode == 0, "file compiles")
    c.exists("notes/release-notes-sample.md", "save one real output from your agent")
    c.cost_logged("w6d26")


@lab("w6d27", "Agentic architecture design review")
def w6d27(c: Ctx):
    rel = "docs/architecture/capstone-design.md"
    if c.exists(rel):
        c.headings_present(rel, ["Problem", "Pattern", "Components", "Guardrails",
                                 "Cost estimate", "Failure modes", "Human in the loop"])
    c.cost_logged("w6d27")


@lab("w6d28", "Capstone day 1: build")
def w6d28(c: Ctx):
    if c.exists("capstone/README.md"):
        c.headings_present("capstone/README.md", ["Brief", "How to run", "Architecture"])
    py = [p for p in (c.root / "capstone").rglob("*.py")] if c.path("capstone").exists() else []
    c.check(len(py) >= 2, f"capstone has code and tests ({len(py)} .py files)")
    c.cost_logged("w6d28")


@lab("w6d29", "Capstone day 2: review and ship")
def w6d29(c: Ctx):
    proc = c.run(sys.executable, "-m", "pytest", "capstone", "-q", "-p", "no:cacheprovider", env=c.pytest_env())
    c.check(proc.returncode == 0, "capstone tests pass (uv run pytest capstone)")
    c.headings_present("capstone/README.md", ["Cost", "Limitations"])
    c.exists("capstone/REVIEW.md", "record the review findings and what you fixed")
    c.cost_logged("w6d29")


@lab("w6d30", "Mock CCA-F exam and readiness")
def w6d30(c: Ctx):
    text = c.read("notes/mock-exam-result.md")
    m = re.search(r"score\s*:\s*(\d+)\s*/\s*60", text, re.I)
    c.check(m is not None, "notes/mock-exam-result.md records 'Score: NN/60'")
    if m:
        score = int(m.group(1))
        c.remind(score >= 43, f"mock score {score}/60 (≈72%+ suggests you're ready to book the exam)")
    c.headings_present("notes/mock-exam-result.md", ["Gap analysis", "Study plan"])
