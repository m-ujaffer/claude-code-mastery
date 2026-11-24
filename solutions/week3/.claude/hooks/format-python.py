#!/usr/bin/env python3
"""PostToolUse hook for Edit|Write: format and auto-fix any Python file Claude touched."""

import json
import subprocess
import sys


def main() -> int:
    try:
        event = json.load(sys.stdin)
    except ValueError:
        return 0
    path = (event.get("tool_input") or {}).get("file_path", "")
    if not path.endswith(".py"):
        return 0
    for cmd in (["uv", "run", "ruff", "format", "--quiet", path],
                ["uv", "run", "ruff", "check", "--fix", "--quiet", path]):
        subprocess.run(cmd, capture_output=True, timeout=60)
    return 0  # formatting problems are never a reason to block Claude


if __name__ == "__main__":
    sys.exit(main())
