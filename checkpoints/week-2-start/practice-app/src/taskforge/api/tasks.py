"""/tasks endpoints."""

import sqlite3

from fastapi import APIRouter, Depends, HTTPException, Query, Response

from taskforge import repository, services
from taskforge.api.deps import get_db
from taskforge.models import Priority, Status, Task, TaskCreate, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("", response_model=Task, status_code=201)
def create_task(body: TaskCreate, db: sqlite3.Connection = Depends(get_db)):
    try:
        row = repository.create_task(db, body.model_dump())
    except repository.NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return services.to_task(row)


@router.get("", response_model=list[Task])
def list_tasks(
    project_id: int | None = None,
    status: Status | None = None,
    priority: Priority | None = None,
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: sqlite3.Connection = Depends(get_db),
):
    rows = repository.list_tasks(
        db, project_id=project_id, status=status, priority=priority, limit=limit, offset=offset
    )
    return [services.to_task(r) for r in rows]


@router.get("/{task_id}", response_model=Task)
def get_task(task_id: int, db: sqlite3.Connection = Depends(get_db)):
    try:
        return services.to_task(repository.get_task(db, task_id))
    except repository.NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.patch("/{task_id}", response_model=Task)
def update_task(task_id: int, body: TaskUpdate, db: sqlite3.Connection = Depends(get_db)):
    try:
        row = repository.update_task(db, task_id, body.model_dump(exclude_unset=True))
    except repository.NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return services.to_task(row)


@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int, db: sqlite3.Connection = Depends(get_db)):
    try:
        repository.delete_task(db, task_id)
    except repository.NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return Response(status_code=204)
