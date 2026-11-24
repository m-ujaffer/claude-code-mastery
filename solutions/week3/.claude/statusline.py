#!/usr/bin/env python3
"""Course status line: model | session cost | month-to-date estimate | context use.

Claude Code pipes a JSON blob to this script on stdin every time the status
line refreshes. We print one line back. Along the way we keep a small ledger
of session costs in notes/.cost-ledger.json, so you can see roughly how much
of your US$30 monthly budget you have used.

The numbers are Claude Code's client-side *estimates* for interactive
sessions. Headless runs (`claude -p`) and CI runs are not included. Your
admin's Anthropic Console is the source of truth.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import datetime

MONTHLY_BUDGET = float(os.environ.get("COURSE_MONTHLY_BUDGET", "30"))
LEDGER = os.path.join("notes", ".cost-ledger.json")

GREEN, YELLOW, RED, DIM, RESET = "\033[32m", "\033[33m", "\033[31m", "\033[2m", "\033[0m"


def update_ledger(session_id: str, session_cost: float) -> float:
    """Record this session's cost; return the month-to-date total."""
    month = datetime.now().strftime("%Y-%m")
    try:
        with open(LEDGER) as f:
            ledger = json.load(f)
    except (OSError, ValueError):
        ledger = {}

    sessions = ledger.setdefault(month, {})
    entry = sessions.setdefault(session_id, {"banked": 0.0, "last": 0.0})
    # /clear resets the session's cost counter. If the number went down,
    # bank what we had seen so far so it is not lost.
    if session_cost < entry["last"]:
        entry["banked"] += entry["last"]
    entry["last"] = session_cost

    try:
        os.makedirs(os.path.dirname(LEDGER), exist_ok=True)
        tmp = LEDGER + ".tmp"
        with open(tmp, "w") as f:
            json.dump(ledger, f, indent=1)
        os.replace(tmp, LEDGER)
    except OSError:
        pass  # never break the status line over bookkeeping

    return sum(e["banked"] + e["last"] for e in sessions.values())


def git_branch() -> str:
    """Current branch, or '' if git is slow, missing, or we're not in a repo."""
    try:
        out = subprocess.run(["git", "branch", "--show-current"], capture_output=True,
                             text=True, timeout=1)
        return out.stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return ""


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except ValueError:
        print("statusline: no data")
        return

    model = (data.get("model") or {}).get("display_name", "?")
    cost = float((data.get("cost") or {}).get("total_cost_usd") or 0.0)
    session_id = data.get("session_id") or "unknown"
    ctx = (data.get("context_window") or {}).get("used_percentage")

    month_total = update_ledger(session_id, cost)
    share = month_total / MONTHLY_BUDGET if MONTHLY_BUDGET else 0
    colour = GREEN if share < 0.7 else YELLOW if share < 0.9 else RED

    parts = [
        f"[{model}]",
        f"session ${cost:.2f}",
        f"{colour}month ~${month_total:.2f}/${MONTHLY_BUDGET:.0f}{RESET}",
    ]
    if ctx is not None:
        parts.append(f"ctx {ctx:.0f}%")
    branch = git_branch()
    if branch:
        parts.append(f"⎇ {branch}")
    print(f" {DIM}|{RESET} ".join(parts))


if __name__ == "__main__":
    main()
