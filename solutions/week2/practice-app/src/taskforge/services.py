"""Business rules that sit between the API layer and the repository."""

import sqlite3
from datetime import date

from taskforge import clock, repository
from taskforge.models import ProjectStats, Status, Task


def is_overdue(due_date: date | None, status: str, today: date | None = None) -> bool:
    """A task is overdue when its due date is strictly before today and it is not done."""
    if due_date is None or status == Status.DONE:
        return False
    today = today or clock.today()
    return due_date < today


def to_task(conn: sqlite3.Connection, row: sqlite3.Row) -> Task:
    """Convert a database row (plus its tags) into the API model."""
    due = date.fromisoformat(row["due_date"]) if row["due_date"] else None
    return Task(
        id=row["id"],
        project_id=row["project_id"],
        title=row["title"],
        description=row["description"],
        status=row["status"],
        priority=row["priority"],
        due_date=due,
        created_at=row["created_at"],
        updated_at=row["updated_at"],
        completed_at=row["completed_at"],
        is_overdue=is_overdue(due, row["status"]),
        tags=repository.get_tags(conn, row["id"]),
    )


def project_stats(conn: sqlite3.Connection, project_id: int) -> ProjectStats:
    """TF-106: counts by status, overdue count and completion rate for one project."""
    repository.get_project(conn, project_id)  # raises NotFoundError
    rows = repository.list_tasks(conn, project_id=project_id, limit=None)
    by_status = {s.value: 0 for s in Status}
    overdue = 0
    for row in rows:
        by_status[row["status"]] += 1
        due = date.fromisoformat(row["due_date"]) if row["due_date"] else None
        overdue += is_overdue(due, row["status"])
    total = len(rows)
    rate = round(by_status["done"] / total, 2) if total else 0.0
    return ProjectStats(
        project_id=project_id,
        total=total,
        by_status=by_status,
        overdue=overdue,
        completion_rate=rate,
    )
