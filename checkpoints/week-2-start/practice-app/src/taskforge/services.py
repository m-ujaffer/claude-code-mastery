"""Business rules that sit between the API layer and the repository."""

import sqlite3
from datetime import date

from taskforge import clock
from taskforge.models import Status, Task


def is_overdue(due_date: date | None, status: str, today: date | None = None) -> bool:
    """Return True if a task is past its due date.

    Business rule (see ISSUES.md): a task is overdue when its due date is
    strictly before today and it is not done.
    """
    if due_date is None or status == Status.DONE:
        return False
    today = today or clock.today()
    return due_date < today


def to_task(row: sqlite3.Row) -> Task:
    """Convert a database row into the API model."""
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
        is_overdue=is_overdue(due, row["status"]),
    )
