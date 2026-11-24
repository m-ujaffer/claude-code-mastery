"""Deterministic fact gathering. No model calls here."""

from __future__ import annotations

import re
import subprocess
from collections import Counter

ISSUE_RE = re.compile(r"\bTF-\d{3}\b")


def git(*args: str) -> str:
    return subprocess.run(["git", *args], capture_output=True, text=True, check=True).stdout


def issue_ids(*texts: str) -> list[str]:
    """All TF-### ids mentioned anywhere in the given texts, sorted and unique."""
    return sorted({m for t in texts for m in ISSUE_RE.findall(t)})


def suggest_reviewers(log_lines: list[str], author: str, limit: int = 2) -> list[str]:
    """Most frequent recent authors of the touched files, excluding the PR author."""
    counts = Counter(line.strip() for line in log_lines if line.strip() and line.strip() != author)
    return [name for name, _ in counts.most_common(limit)]


def gather(base: str) -> dict:
    diff = git("diff", f"{base}...HEAD")
    files = [f for f in git("diff", "--name-only", f"{base}...HEAD").splitlines() if f]
    messages = git("log", "--format=%s", f"{base}..HEAD")
    author = git("log", "-1", "--format=%an").strip()
    history = git("log", "-n", "50", "--format=%an", "--", *files).splitlines() if files else []
    return {
        "diff": diff,
        "files": files,
        "issues": issue_ids(diff, messages),
        "reviewers": suggest_reviewers(history, author),
    }
