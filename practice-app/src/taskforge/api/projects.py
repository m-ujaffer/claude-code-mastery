"""/projects endpoints."""

import sqlite3

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import PlainTextResponse

from taskforge import repository, services
from taskforge.api.deps import get_db
from taskforge.legacy.report_builder import build_report
from taskforge.models import Project, ProjectCreate, Task

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("", response_model=Project, status_code=201)
def create_project(body: ProjectCreate, db: sqlite3.Connection = Depends(get_db)):
    try:
        row = repository.create_project(db, body.name, body.description)
    except repository.ConflictError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    return Project(**dict(row))


@router.get("", response_model=list[Project])
def list_projects(db: sqlite3.Connection = Depends(get_db)):
    return [Project(**dict(r)) for r in repository.list_projects(db)]


@router.get("/{project_id}", response_model=Project)
def get_project(project_id: int, db: sqlite3.Connection = Depends(get_db)):
    try:
        return Project(**dict(repository.get_project(db, project_id)))
    except repository.NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/{project_id}/tasks", response_model=list[Task])
def project_tasks(project_id: int, db: sqlite3.Connection = Depends(get_db)):
    try:
        repository.get_project(db, project_id)
    except repository.NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return [services.to_task(r) for r in repository.list_tasks(db, project_id=project_id)]


@router.get("/{project_id}/report", response_class=PlainTextResponse)
def project_report(
    project_id: int,
    fmt: str = Query("text", pattern="^(text|md|html)$"),
    db: sqlite3.Connection = Depends(get_db),
):
    try:
        repository.get_project(db, project_id)
    except repository.NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return build_report(db, project_id, fmt)
