def test_create_and_get_project(client):
    resp = client.post("/projects", json={"name": "Alpha", "description": "first"})
    assert resp.status_code == 201
    body = resp.json()
    assert body["name"] == "Alpha"

    fetched = client.get(f"/projects/{body['id']}").json()
    assert fetched == body


def test_duplicate_project_name_conflicts(client):
    client.post("/projects", json={"name": "Alpha"})
    assert client.post("/projects", json={"name": "Alpha"}).status_code == 409


def test_list_projects(client):
    client.post("/projects", json={"name": "A"})
    client.post("/projects", json={"name": "B"})
    assert [p["name"] for p in client.get("/projects").json()] == ["A", "B"]


def test_missing_project_is_404(client):
    assert client.get("/projects/999").status_code == 404


def test_project_tasks(client, project):
    client.post("/tasks", json={"project_id": project["id"], "title": "One"})
    tasks = client.get(f"/projects/{project['id']}/tasks").json()
    assert [t["title"] for t in tasks] == ["One"]


def test_report_text(client, project):
    client.post("/tasks", json={"project_id": project["id"], "title": "One"})
    resp = client.get(f"/projects/{project['id']}/report")
    assert resp.status_code == 200
    assert "PROJECT REPORT: Demo" in resp.text
    assert "[ ] One" in resp.text
