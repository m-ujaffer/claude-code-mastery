"""Load demo data:  uv run python -m taskforge.seed"""

from datetime import timedelta

from taskforge import clock, repository
from taskforge.db import connect
from taskforge.main import DEFAULT_DB


def seed(db_path: str = DEFAULT_DB) -> None:
    conn = connect(db_path)
    if repository.list_projects(conn):
        print("Database already has data; delete it first to reseed.")
        return
    today = clock.today()
    web = repository.create_project(conn, "Website relaunch", "Q3 marketing site rebuild")
    ops = repository.create_project(conn, "Ops hygiene", "Recurring infrastructure chores")
    demo = [
        (web["id"], "Write homepage copy", "high", today + timedelta(days=3)),
        (web["id"], "Pick a colour palette", "low", today - timedelta(days=2)),
        (web["id"], "Set up analytics", "medium", today),
        (ops["id"], "Rotate database credentials", "high", today - timedelta(days=10)),
        (ops["id"], "Clean up old S3 buckets", "low", None),
    ]
    for project_id, title, priority, due in demo:
        repository.create_task(
            conn,
            {"project_id": project_id, "title": title, "priority": priority, "due_date": due},
        )
    print(f"Seeded 2 projects and {len(demo)} tasks into {db_path}")


if __name__ == "__main__":
    seed()
