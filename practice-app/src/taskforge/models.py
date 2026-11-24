"""Pydantic request/response models."""

from datetime import date, datetime
from enum import StrEnum

from pydantic import BaseModel


class Status(StrEnum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class Priority(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ProjectCreate(BaseModel):
    name: str
    description: str = ""


class Project(BaseModel):
    id: int
    name: str
    description: str
    created_at: datetime


class TaskCreate(BaseModel):
    project_id: int
    title: str
    description: str = ""
    priority: Priority = Priority.MEDIUM
    due_date: date | None = None


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: Status | None = None
    priority: Priority | None = None
    due_date: date | None = None


class Task(BaseModel):
    id: int
    project_id: int
    title: str
    description: str
    status: Status
    priority: Priority
    due_date: date | None
    created_at: datetime
    updated_at: datetime
    is_overdue: bool
