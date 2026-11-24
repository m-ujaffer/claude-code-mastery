import pytest
from fastapi.testclient import TestClient

from taskforge.main import create_app


@pytest.fixture
def client(tmp_path):
    """A TestClient backed by a fresh, throwaway SQLite database."""
    app = create_app(str(tmp_path / "test.db"))
    with TestClient(app) as c:
        yield c


@pytest.fixture
def project(client):
    return client.post("/projects", json={"name": "Demo"}).json()
