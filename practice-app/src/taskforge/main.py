"""FastAPI application factory.

Run locally from the repo root:
    uv run uvicorn taskforge.main:app --reload
Then open http://localhost:8000/docs
"""

import os
from pathlib import Path

from fastapi import FastAPI

from taskforge import __version__
from taskforge.api import projects, tasks
from taskforge.db import connect

# practice-app/taskforge.db, wherever you start the server from
DEFAULT_DB = os.environ.get(
    "TASKFORGE_DB", str(Path(__file__).resolve().parents[2] / "taskforge.db")
)


def create_app(db_path: str | None = None) -> FastAPI:
    app = FastAPI(title="TaskForge", version=__version__)
    app.state.db = connect(db_path or DEFAULT_DB)
    app.include_router(projects.router)
    app.include_router(tasks.router)

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "version": __version__}

    return app


app = create_app()
