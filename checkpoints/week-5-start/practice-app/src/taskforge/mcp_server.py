"""TaskForge MCP server: lets Claude query and update TaskForge through a small set of tools.

Run it (stdio):   uv run python -m taskforge.mcp_server
Register it:      claude mcp add --scope project taskforge -- uv run python -m taskforge.mcp_server

Tool design notes (Week 4, Day 17):
- Few, task-shaped tools rather than one tool per SQL table.
- Names are verbs; descriptions say *when* to use the tool and what comes back.
- Results are compact (no timestamps nobody asked for) to save the caller's context.
- Errors tell the model how to recover ("call list_projects to see valid ids").
  They are raised as ToolError: any other exception reaches the model only as
  "Error executing tool <name>", which gives it nothing to recover with.
- Read-only tools are annotated so clients can auto-approve them safely.
"""

from __future__ import annotations

import os
from pathlib import Path

from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError
from mcp.types import ToolAnnotations
from pydantic import ValidationError

from taskforge import repository, services
from taskforge.db import connect
from taskforge.legacy.report_builder import build_report
from taskforge.models import Status, TaskCreate

APP_DIR = Path(__file__).resolve().parents[2]
DB_PATH = os.environ.get("TASKFORGE_DB", str(APP_DIR / "taskforge.db"))
READ_ONLY = ToolAnnotations(readOnlyHint=True, openWorldHint=False)
MAX_LIMIT = 50

mcp = MCPServer(
    "taskforge",
    instructions=(
        "Tools for the TaskForge task tracker. Start with list_projects to find ids. "
        "Prefer project_stats over listing every task when you only need counts."
    ),
)
_conn = None


def db():
    global _conn
    if _conn is None:
        _conn = connect(DB_PATH)
    return _conn


def _summary(row) -> dict:
    task = services.to_task(db(), row)
    return {
        "id": task.id,
        "project_id": task.project_id,
        "title": task.title,
        "status": task.status.value,
        "priority": task.priority.value,
        "due_date": task.due_date.isoformat() if task.due_date else None,
        "is_overdue": task.is_overdue,
        "tags": task.tags,
    }


def _require_project(project_id: int) -> None:
    try:
        repository.get_project(db(), project_id)
    except repository.NotFoundError:
        raise ToolError(
            f"Project {project_id} does not exist. Call list_projects to see valid project ids."
        ) from None


# ------------------------------------------------------------------ tools


@mcp.tool(annotations=READ_ONLY)
def list_projects() -> list[dict]:
    """List every TaskForge project with its id, name and description.

    Call this first whenever you need a project_id for another tool.
    """
    return [
        {"id": r["id"], "name": r["name"], "description": r["description"]}
        for r in repository.list_projects(db())
    ]


@mcp.tool(annotations=READ_ONLY)
def find_tasks(
    project_id: int | None = None,
    status: str | None = None,
    priority: str | None = None,
    tag: str | None = None,
    overdue_only: bool = False,
    limit: int = 20,
) -> list[dict]:
    """Find tasks matching optional filters and return compact summaries.

    Filters combine with AND. status is one of todo, in_progress, done; priority is one of
    low, medium, high. Returns at most `limit` tasks (max 50) with id, title, status,
    priority, due_date, is_overdue and tags. For counts, use project_stats instead.
    """
    if project_id is not None:
        _require_project(project_id)
    rows = repository.list_tasks(
        db(), project_id=project_id, status=status, priority=priority, tag=tag,
        limit=None if overdue_only else min(limit, MAX_LIMIT),
    )
    tasks = [_summary(r) for r in rows]
    if overdue_only:
        tasks = [t for t in tasks if t["is_overdue"]]
    return tasks[: min(limit, MAX_LIMIT)]


@mcp.tool()
def create_task(
    project_id: int,
    title: str,
    priority: str = "medium",
    due_date: str | None = None,
    tags: list[str] | None = None,
) -> dict:
    """Create a task in a project and return its summary.

    due_date uses ISO format (YYYY-MM-DD). Titles are trimmed and must be 1-200 characters.
    Validation errors explain what to fix.
    """
    _require_project(project_id)
    try:
        body = TaskCreate(
            project_id=project_id, title=title, priority=priority,
            due_date=due_date, tags=tags or [],
        )
    except ValidationError as exc:
        problems = "; ".join(f"{'.'.join(map(str, e['loc']))}: {e['msg']}" for e in exc.errors())
        raise ToolError(f"Invalid task: {problems}") from None
    return _summary(repository.create_task(db(), body.model_dump()))


@mcp.tool()
def update_task_status(task_id: int, status: str) -> dict:
    """Move a task to todo, in_progress or done, and return its updated summary.

    Moving to done records completed_at; moving away from done clears it.
    """
    if status not in {s.value for s in Status}:
        raise ToolError("status must be one of: todo, in_progress, done")
    try:
        row = repository.update_task(db(), task_id, {"status": status})
    except repository.NotFoundError:
        raise ToolError(f"Task {task_id} does not exist. Use find_tasks to look up ids.") from None
    return _summary(row)


@mcp.tool(annotations=READ_ONLY)
def project_stats(project_id: int) -> dict:
    """Return counts by status, the overdue count and the completion rate for one project.

    This is the cheapest way to answer "how is project X doing?".
    """
    _require_project(project_id)
    return services.project_stats(db(), project_id).model_dump()


# -------------------------------------------------------------- resources


@mcp.resource("taskforge://backlog", mime_type="text/markdown")
def backlog() -> str:
    """The TaskForge backlog (ISSUES.md) with acceptance criteria for every TF issue."""
    return (APP_DIR / "ISSUES.md").read_text(encoding="utf-8")


@mcp.resource("taskforge://projects/{project_id}/report", mime_type="text/markdown")
def project_report(project_id: int) -> str:
    """A Markdown status report for one project."""
    _require_project(int(project_id))
    return build_report(db(), int(project_id), "md")


# ---------------------------------------------------------------- prompts


@mcp.prompt()
def triage_overdue(project_id: int) -> str:
    """Triage the overdue tasks of a project and propose next actions."""
    return (
        f"Use find_tasks with project_id={project_id} and overdue_only=true. "
        "Group the overdue tasks by priority. For each one, propose exactly one next action "
        "(do now, reschedule, or drop) with a one-line reason. Do not change any task: "
        "this is a proposal for a human to approve."
    )


if __name__ == "__main__":
    mcp.run()
