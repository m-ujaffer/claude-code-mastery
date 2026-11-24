"""TF-109: the refactored report builder must produce byte-identical output."""

from pathlib import Path

import pytest

from taskforge import repository
from taskforge.legacy.report_builder import build_report

GOLDEN = Path(__file__).parent / "golden"


def build_fixture(conn):
    import datetime as dt

    p = repository.create_project(conn, "R&D <Lab>", "golden fixture")
    rows = [
        ("Design <schema> & API", "high", dt.date(2026, 3, 1), "in_progress"),
        ("Write tests", "medium", dt.date(2026, 3, 20), "todo"),
        ("Ship v1", "high", dt.date(2026, 2, 1), "done"),
        ("Old chore", "low", dt.date(2026, 1, 15), "todo"),
        ("Someday", "low", None, "todo"),
    ]
    for title, prio, due, status in rows:
        t = repository.create_task(
            conn, {"project_id": p["id"], "title": title, "priority": prio, "due_date": due}
        )
        if status != "todo":
            conn.execute("UPDATE tasks SET status = ? WHERE id = ?", (status, t["id"]))
    conn.commit()
    empty = repository.create_project(conn, "Empty", "")
    return p["id"], empty["id"]


@pytest.mark.parametrize("fmt", ["text", "md", "html"])
def test_report_matches_golden(app, fmt):
    pid, empty_id = build_fixture(app.state.db)
    assert build_report(app.state.db, pid, fmt) == (GOLDEN / f"report.{fmt}").read_text()
    assert build_report(app.state.db, empty_id, fmt) == (GOLDEN / f"empty.{fmt}").read_text()
