"""Data access: every SQL statement for projects and tasks lives here."""

import sqlite3
from typing import Any

from taskforge import clock


class NotFoundError(Exception):
    """Raised when a row does not exist."""


class ConflictError(Exception):
    """Raised when a write would violate a uniqueness rule."""


# ---------------------------------------------------------------- projects


def create_project(conn: sqlite3.Connection, name: str, description: str = "") -> sqlite3.Row:
    try:
        cur = conn.execute(
            "INSERT INTO projects (name, description, created_at) VALUES (?, ?, ?)",
            (name, description, clock.now().isoformat()),
        )
    except sqlite3.IntegrityError as exc:
        raise ConflictError(f"project '{name}' already exists") from exc
    conn.commit()
    return get_project(conn, cur.lastrowid)


def get_project(conn: sqlite3.Connection, project_id: int) -> sqlite3.Row:
    row = conn.execute("SELECT * FROM projects WHERE id = ?", (project_id,)).fetchone()
    if row is None:
        raise NotFoundError(f"project {project_id} not found")
    return row


def list_projects(conn: sqlite3.Connection) -> list[sqlite3.Row]:
    return conn.execute("SELECT * FROM projects ORDER BY id").fetchall()


# ------------------------------------------------------------------- tasks


def create_task(conn: sqlite3.Connection, data: dict[str, Any]) -> sqlite3.Row:
    get_project(conn, data["project_id"])  # raises NotFoundError
    now = clock.now().isoformat()
    due = data.get("due_date")
    cur = conn.execute(
        """INSERT INTO tasks (project_id, title, description, status, priority,
                              due_date, created_at, updated_at)
           VALUES (?, ?, ?, 'todo', ?, ?, ?, ?)""",
        (
            data["project_id"],
            data["title"],
            data.get("description", ""),
            str(data.get("priority", "medium")),
            due.isoformat() if due else None,
            now,
            now,
        ),
    )
    _replace_tags(conn, cur.lastrowid, data.get("tags") or [])
    conn.commit()
    return get_task(conn, cur.lastrowid)


def get_task(conn: sqlite3.Connection, task_id: int) -> sqlite3.Row:
    row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if row is None:
        raise NotFoundError(f"task {task_id} not found")
    return row


def list_tasks(
    conn: sqlite3.Connection,
    project_id: int | None = None,
    status: str | None = None,
    priority: str | None = None,
    tag: str | None = None,
    limit: int | None = 50,
    offset: int = 0,
) -> list[sqlite3.Row]:
    """List tasks; every filter is optional and they all combine with AND."""
    where: list[str] = []
    params: list[Any] = []
    if project_id is not None:
        where.append("project_id = ?")
        params.append(project_id)
    if status is not None:
        where.append("status = ?")
        params.append(str(status))
    if priority is not None:
        where.append("priority = ?")
        params.append(str(priority))
    if tag is not None:
        where.append("id IN (SELECT task_id FROM task_tags WHERE tag = ?)")
        params.append(tag.strip().lower())
    sql = "SELECT * FROM tasks"
    if where:
        sql += " WHERE " + " AND ".join(where)
    sql += " ORDER BY id LIMIT ? OFFSET ?"
    params += [-1 if limit is None else limit, offset]
    return conn.execute(sql, params).fetchall()


def get_tags(conn: sqlite3.Connection, task_id: int) -> list[str]:
    rows = conn.execute("SELECT tag FROM task_tags WHERE task_id = ? ORDER BY tag", (task_id,))
    return [r["tag"] for r in rows]


def _replace_tags(conn: sqlite3.Connection, task_id: int, tags: list[str]) -> None:
    conn.execute("DELETE FROM task_tags WHERE task_id = ?", (task_id,))
    conn.executemany(
        "INSERT INTO task_tags (task_id, tag) VALUES (?, ?)", [(task_id, t) for t in tags]
    )


UPDATABLE = ("title", "description", "status", "priority", "due_date", "completed_at")


def update_task(conn: sqlite3.Connection, task_id: int, changes: dict[str, Any]) -> sqlite3.Row:
    current = get_task(conn, task_id)  # raises NotFoundError
    fields = {k: v for k, v in changes.items() if k in UPDATABLE}
    if fields.get("due_date") is not None:
        fields["due_date"] = fields["due_date"].isoformat()
    for key in ("status", "priority"):
        if fields.get(key) is not None:
            fields[key] = str(fields[key])

    # TF-105: completed_at follows status transitions.
    new_status = fields.get("status")
    if new_status == "done" and current["status"] != "done":
        fields["completed_at"] = clock.now().isoformat()
    elif new_status is not None and new_status != "done":
        fields["completed_at"] = None

    if fields or changes.get("tags") is not None:
        fields["updated_at"] = clock.now().isoformat()
        assignments = ", ".join(f"{k} = ?" for k in fields)
        conn.execute(f"UPDATE tasks SET {assignments} WHERE id = ?", [*fields.values(), task_id])
        if changes.get("tags") is not None:
            _replace_tags(conn, task_id, changes["tags"])
        conn.commit()
    return get_task(conn, task_id)


def delete_task(conn: sqlite3.Connection, task_id: int) -> None:
    get_task(conn, task_id)  # raises NotFoundError
    conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
