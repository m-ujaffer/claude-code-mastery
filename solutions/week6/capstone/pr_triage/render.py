"""Turn facts + model judgement into a PR comment."""

from __future__ import annotations

ICONS = {"low": "🟢", "medium": "🟡", "high": "🔴"}


def render(facts: dict, triage: dict) -> str:
    lines = [
        f"### {ICONS[triage['risk']]} PR triage: {triage['risk']} risk",
        "",
        triage["rationale"],
        "",
        f"**Issues:** {', '.join(facts['issues']) or 'none referenced'}",
        f"**Suggested reviewers:** {', '.join(facts['reviewers']) or 'no history'}",
    ]
    if triage["missing_tests"]:
        lines += ["", "**Missing tests:**", *[f"- {t}" for t in triage["missing_tests"]]]
    lines += ["", "_Automated first pass. A human makes the call._"]
    return "\n".join(lines)
