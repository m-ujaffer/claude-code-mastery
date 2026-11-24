"""TF-106: project stats."""

from conftest import days


def test_stats_shape_and_values(client, project, make_task):
    make_task("a")
    make_task("b", status="in_progress", due_date=days(-1))
    make_task("c", status="done", due_date=days(-3))
    make_task("d", status="done")
    resp = client.get(f"/projects/{project['id']}/stats")
    assert resp.status_code == 200, resp.text
    assert resp.json() == {
        "project_id": project["id"],
        "total": 4,
        "by_status": {"todo": 1, "in_progress": 1, "done": 2},
        "overdue": 1,
        "completion_rate": 0.5,
    }


def test_empty_project(client, project):
    body = client.get(f"/projects/{project['id']}/stats").json()
    assert body["total"] == 0
    assert body["by_status"] == {"todo": 0, "in_progress": 0, "done": 0}
    assert body["completion_rate"] == 0.0


def test_rounding(client, project, make_task):
    make_task("a", status="done")
    make_task("b")
    make_task("c")
    assert client.get(f"/projects/{project['id']}/stats").json()["completion_rate"] == 0.33


def test_missing_project_404(client):
    assert client.get("/projects/999/stats").status_code == 404
