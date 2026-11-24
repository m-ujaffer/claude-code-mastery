"""Pydantic request/response models."""

from datetime import date, datetime
from enum import StrEnum

from pydantic import BaseModel, field_validator

TITLE_MAX = 200
MAX_TAGS = 10


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


def clean_tags(values: list[str]) -> list[str]:
    """TF-104: trim, lower-case, drop empties, de-duplicate, sort; at most MAX_TAGS."""
    tags = sorted({v.strip().lower() for v in values if v.strip()})
    if len(tags) > MAX_TAGS:
        raise ValueError(f"a task can have at most {MAX_TAGS} tags")
    return tags


class ProjectCreate(BaseModel):
    name: str
    description: str = ""


class Project(BaseModel):
    id: int
    name: str
    description: str
    created_at: datetime


class ProjectStats(BaseModel):
    project_id: int
    total: int
    by_status: dict[str, int]
    overdue: int
    completion_rate: float


class TaskCreate(BaseModel):
    project_id: int
    title: str
    description: str = ""
    priority: Priority = Priority.MEDIUM
    due_date: date | None = None
    tags: list[str] = []

    @field_validator("title")
    @classmethod
    def _title(cls, v: str) -> str:
        return clean_title(v)

    @field_validator("tags")
    @classmethod
    def _tags(cls, v: list[str]) -> list[str]:
        return clean_tags(v)


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: Status | None = None
    priority: Priority | None = None
    due_date: date | None = None
    tags: list[str] | None = None

    @field_validator("title")
    @classmethod
    def _title(cls, v: str | None) -> str | None:
        return None if v is None else clean_title(v)

    @field_validator("tags")
    @classmethod
    def _tags(cls, v: list[str] | None) -> list[str] | None:
        return None if v is None else clean_tags(v)


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
    completed_at: datetime | None = None
    is_overdue: bool
    tags: list[str] = []
