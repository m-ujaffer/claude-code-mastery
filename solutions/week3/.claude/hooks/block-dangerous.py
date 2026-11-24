#!/usr/bin/env python3
"""PreToolUse hook for Bash: block destructive or secret-leaking commands.

Claude Code sends the event as JSON on stdin. Exit code 2 blocks the tool call,
and whatever we print to stderr is shown to Claude as the reason.
Regexes are a best-effort guard, not a sandbox: they make the common mistakes impossible.
"""

import json
import re
import sys

RULES = [
    (r"\brm\s+(-\w*r\w*f\w*|-\w*f\w*r\w*|(-\w+\s+)*--recursive\s+--force|--force\s+--recursive)\b",
     "recursive force delete"),
    (r"\bgit\s+push\b.*(\s--force\b|\s-f\b|\s--force-with-lease\b)", "force push"),
    (r"\bgit\s+reset\s+--hard\b", "hard reset (discards work)"),
    (r"\b(curl|wget)\b[^|]*\|\s*(sudo\s+)?(sh|bash|zsh)\b", "piping a download into a shell"),
    (r"\b(cat|less|more|head|tail|bat|strings)\b[^|;&]*\.env(\.\w+)?\b", "reading a .env secrets file"),
]


def main() -> int:
    try:
        event = json.load(sys.stdin)
    except ValueError:
        return 0  # not our business; never break the session on bad input
    command = (event.get("tool_input") or {}).get("command", "")
    for pattern, reason in RULES:
        if re.search(pattern, command):
            print(
                f"Blocked by project hook: {reason}. If this is really needed, ask the human to run it.",
                file=sys.stderr,
            )
            return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
