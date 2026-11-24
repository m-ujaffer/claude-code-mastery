"""Characterisation tests for the legacy report builder (TF-109).

These were written *before* the refactor, against the original code, to pin
its exact output. They must keep passing, unchanged, after the refactor.
"""

import datetime as dt

import pytest

from taskforge import clock, repository
from taskforge.db import connect
from taskforge.legacy.report_builder import build_report


@pytest.fixture
def conn(monkeypatch):
    monkeypatch.setattr(clock, "today", lambda: dt.date(2026, 3, 10))
    monkeypatch.setattr(clock, "now", lambda: dt.datetime(2026, 3, 10, tzinfo=dt.UTC))
    c = connect(":memory:")
    p = repository.create_project(c, "A&B", "")
    for title, prio, due, status in [
        ("<Fix> & ship", "high", dt.date(2026, 3, 1), "in_progress"),
        ("Done thing", "high", dt.date(2026, 1, 1), "done"),
        ("Later", "low", None, "todo"),
    ]:
        t = repository.create_task(
            c, {"project_id": p["id"], "title": title, "priority": prio, "due_date": due}
        )
        c.execute("UPDATE tasks SET status = ? WHERE id = ?", (status, t["id"]))
    c.commit()
    return c


def test_text_report(conn):
    assert build_report(conn, 1, "text") == (
        "PROJECT REPORT: A&B\n"
        "===================\n"
        "Total tasks: 3\nDone: 1\nIn progress: 1\nOverdue: 1\n"
        "Open high priority: 1\nCompletion: 33%\n\n"
        "[~] <Fix> & ship (OVERDUE)\n[x] Done thing\n[ ] Later\n"
    )


def test_markdown_report(conn):
    out = build_report(conn, 1, "md")
    assert out.startswith("# Project report: A&B\n\n| Metric | Value |\n|---|---|\n")
    assert "- [ ] <Fix> & ship **(high)** _overdue since 2026-03-01_\n" in out
    assert "- [x] Done thing **(high)**\n" in out
    assert out.endswith("- [ ] Later\n")


def test_html_report_escapes(conn):
    out = build_report(conn, 1, "html")
    assert out.startswith("<h1>Project report: A&amp;B</h1>\n<ul>\n")
    assert '<tr class="overdue"><td>&lt;Fix&gt; &amp; ship</td>' in out
    assert "<td>Later</td><td>todo</td><td>low</td><td>-</td>" in out


def test_empty_project_and_unknown_format(conn):
    repository.create_project(conn, "Empty", "")
    assert "Completion: n/a" in build_report(conn, 2, "text")
    assert build_report(conn, 1, "pdf") == ""
