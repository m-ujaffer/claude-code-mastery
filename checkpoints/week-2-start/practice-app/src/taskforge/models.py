"""Pydantic request/response models."""

from datetime import date, datetime
from enum import StrEnum

from pydantic import BaseModel, field_validator

TITLE_MAX = 200


class Status(StrEnum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class Priority(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


def clean_title(value: str) -> str:
    """TF-102: trim, then reject blank titles and titles over TITLE_MAX characters."""
    value = value.strip()
    if not value:
        raise ValueError("title must not be blank")
    if len(value) > TITLE_MAX:
        raise ValueError(f"title must be at most {TITLE_MAX} characters")
    return value


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

    @field_validator("title")
    @classmethod
    def _title(cls, v: str) -> str:
        return clean_title(v)


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: Status | None = None
    priority: Priority | None = None
    due_date: date | None = None

    @field_validator("title")
    @classmethod
    def _title(cls, v: str | None) -> str | None:
        return None if v is None else clean_title(v)


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
