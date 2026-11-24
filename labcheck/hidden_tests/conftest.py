"""Shared fixtures for labcheck's hidden acceptance tests.

These tests check the *behaviour* described in practice-app/ISSUES.md through
the public HTTP API, so any reasonable implementation passes.
"""

import datetime as dt

import pytest
from fastapi.testclient import TestClient

from taskforge import clock
from taskforge.main import create_app

TODAY = dt.date(2026, 3, 10)
NOW = dt.datetime(2026, 3, 10, 9, 0, 0, tzinfo=dt.UTC)


@pytest.fixture(autouse=True)
def frozen_clock(monkeypatch):
    monkeypatch.setattr(clock, "today", lambda: TODAY)
    monkeypatch.setattr(clock, "now", lambda: NOW)


@pytest.fixture
def app(tmp_path):
    return create_app(str(tmp_path / "hidden.db"))


@pytest.fixture
def client(app):
    with TestClient(app) as c:
        yield c


@pytest.fixture
def project(client):
    resp = client.post("/projects", json={"name": "Hidden"})
    assert resp.status_code == 201, resp.text
    return resp.json()


@pytest.fixture
def make_task(client, project):
    def _make(title="Task", **fields):
        payload = {"project_id": project["id"], "title": title, **fields}
        status = payload.pop("status", None)
        resp = client.post("/tasks", json=payload)
        assert resp.status_code == 201, resp.text
        task = resp.json()
        if status:
            resp = client.patch(f"/tasks/{task['id']}", json={"status": status})
            assert resp.status_code == 200, resp.text
            task = resp.json()
        return task

    return _make


def days(n: int) -> str:
    return (TODAY + dt.timedelta(days=n)).isoformat()


def parse_ts(value: str) -> dt.datetime:
    return dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
