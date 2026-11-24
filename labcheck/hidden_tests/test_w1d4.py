"""TF-102: title validation."""


def test_title_is_trimmed(make_task):
    assert make_task(title="  Buy milk  ")["title"] == "Buy milk"


def test_blank_title_rejected(client, project):
    for title in ["", "   ", "\t\n"]:
        resp = client.post("/tasks", json={"project_id": project["id"], "title": title})
        assert resp.status_code == 422, f"title={title!r} should be rejected"


def test_title_length_limit(client, project):
    ok = client.post("/tasks", json={"project_id": project["id"], "title": "a" * 200})
    assert ok.status_code == 201
    too_long = client.post("/tasks", json={"project_id": project["id"], "title": "a" * 201})
    assert too_long.status_code == 422


def test_length_measured_after_trim(client, project):
    resp = client.post("/tasks", json={"project_id": project["id"], "title": " " + "a" * 200 + " "})
    assert resp.status_code == 201


def test_patch_validates_title(client, make_task):
    task = make_task()
    assert client.patch(f"/tasks/{task['id']}", json={"title": "   "}).status_code == 422
    assert client.patch(f"/tasks/{task['id']}", json={"title": "b" * 201}).status_code == 422
    resp = client.patch(f"/tasks/{task['id']}", json={"title": "  Renamed "})
    assert resp.status_code == 200
    assert resp.json()["title"] == "Renamed"
