"""/tasks endpoints."""

import csv
import io
import sqlite3

from fastapi import APIRouter, Depends, HTTPException, Query, Response

from taskforge import repository, services
from taskforge.api.deps import get_db
from taskforge.models import Priority, Status, Task, TaskCreate, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["tasks"])

CSV_COLUMNS = ["id", "project_id", "title", "status", "priority", "due_date"]


@router.post("", response_model=Task, status_code=201)
def create_task(body: TaskCreate, db: sqlite3.Connection = Depends(get_db)):
    try:
        row = repository.create_task(db, body.model_dump())
    except repository.NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return services.to_task(db, row)


@router.get("", response_model=list[Task])
def list_tasks(
    project_id: int | None = None,
    status: Status | None = None,
    priority: Priority | None = None,
    tag: str | None = None,
    q: str | None = None,
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: sqlite3.Connection = Depends(get_db),
):
    rows = repository.list_tasks(
        db, project_id=project_id, status=status, priority=priority, tag=tag, q=q,
        limit=limit, offset=offset,
    )
    return [services.to_task(db, r) for r in rows]


# Declared before /{task_id} so "export.csv" is not parsed as a task id (TF-107).
@router.get("/export.csv")
def export_csv(project_id: int | None = None, db: sqlite3.Connection = Depends(get_db)):
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(CSV_COLUMNS)
    for row in repository.list_tasks(db, project_id=project_id, limit=None):
        writer.writerow([row[c] if row[c] is not None else "" for c in CSV_COLUMNS])
    return Response(content=buf.getvalue(), media_type="text/csv")


@router.get("/{task_id}", response_model=Task)
def get_task(task_id: int, db: sqlite3.Connection = Depends(get_db)):
    try:
        return services.to_task(db, repository.get_task(db, task_id))
    except repository.NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.patch("/{task_id}", response_model=Task)
def update_task(task_id: int, body: TaskUpdate, db: sqlite3.Connection = Depends(get_db)):
    try:
        row = repository.update_task(db, task_id, body.model_dump(exclude_unset=True))
    except repository.NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return services.to_task(db, row)


@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int, db: sqlite3.Connection = Depends(get_db)):
    try:
        repository.delete_task(db, task_id)
    except repository.NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return Response(status_code=204)
