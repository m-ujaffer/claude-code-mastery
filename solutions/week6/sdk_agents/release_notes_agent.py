"""Release-notes agent built on the Claude Agent SDK (Week 6, Day 26).

    uv run python sdk_agents/release_notes_agent.py --since HEAD~15 --budget 0.30

Safety model:
- Bash is auto-approved only for `git log` and `git diff`; Edit and Write are disallowed.
- The only way to write anything is our in-process tool, which writes one known file.
- Turns and spend are capped; local settings and CLAUDE.md are not loaded (reproducible runs).
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    ResultMessage,
    TextBlock,
    create_sdk_mcp_server,
    query,
    tool,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "notes" / "release-notes-sample.md"

ROLE = """You write release notes for TaskForge, a task-tracking API.
Group changes under '## Features', '## Fixes' and '## Internal' (omit empty sections).
Reference backlog ids like TF-104 and use practice-app/ISSUES.md for their titles.
Write for API users, not developers: what changed for them. Under 250 words.
When finished, call save_release_notes exactly once with the final Markdown."""


@tool(
    "save_release_notes",
    "Save the final release notes as Markdown. Call exactly once, at the end. "
    "Returns an error explaining what to fix if the notes are incomplete.",
    {"markdown": str},
)
async def save_release_notes(args: dict) -> dict:
    text = args["markdown"].strip()
    if len(text) < 50 or "## " not in text:
        return {
            "content": [{"type": "text", "text": "Rejected: include at least one '## ' section and a real summary."}],
            "is_error": True,
        }
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(text + "\n", encoding="utf-8")
    return {"content": [{"type": "text", "text": f"Saved {len(text)} characters to {OUT.relative_to(ROOT)}."}]}


NOTES_SERVER = create_sdk_mcp_server(name="release-notes", version="1.0.0", tools=[save_release_notes])


def build_options(budget: float) -> ClaudeAgentOptions:
    return ClaudeAgentOptions(
        cwd=str(ROOT),
        model="sonnet",
        system_prompt={"type": "preset", "preset": "claude_code", "append": ROLE},
        mcp_servers={"notes": NOTES_SERVER},
        allowed_tools=[
            "Read", "Grep", "Glob",
            "Bash(git log *)", "Bash(git diff *)",
            "mcp__notes__save_release_notes",
        ],
        disallowed_tools=["Edit", "Write"],
        max_turns=10,
        max_budget_usd=budget,
        setting_sources=[],
    )


async def run(since: str, budget: float) -> int:
    prompt = (
        f"Write release notes for the changes in {since}..HEAD. "
        "Start with `git log --oneline` for that range, inspect diffs only where the message is unclear."
    )
    async for message in query(prompt=prompt, options=build_options(budget)):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(block.text)
        elif isinstance(message, ResultMessage):
            cost = message.total_cost_usd or 0.0
            print(f"\n[done] turns={message.num_turns} total_cost_usd={cost:.4f} "
                  f"is_error={message.is_error}", file=sys.stderr)
            return 1 if message.is_error else 0
    return 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--since", default="HEAD~10", help="git revision to start from")
    parser.add_argument("--budget", type=float, default=0.30, help="max spend in USD (estimate)")
    args = parser.parse_args()
    return asyncio.run(run(args.since, args.budget))


if __name__ == "__main__":
    sys.exit(main())
