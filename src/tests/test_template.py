import json
import pytest

from app.api import crud


# POST
def test_create_template(test_app, monkeypatch):
    test_request_payload = {"title": "First", "description": "Описание"}
    test_response_payload = {"id": 1, "title": "First", "description": "Описание"}

    async def mock_post(payload):
        return 1

    monkeypatch.setattr(crud, "post", mock_post)

    response = test_app.post("/template/", data=json.dumps(test_request_payload))

    assert response.status_code == 201
    assert response.json() == test_response_payload


def test_create_template_invalid_json(test_app):
    response = test_app.post("/template/", data=json.dumps({"title": "Broken"}))
    assert response.status_code == 422


# GET
def test_read_template(test_app, monkeypatch):
    test_data = {"id": 1, "title": "First", "description": "Описание"}

    async def mock_get(id):
        return test_data

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.get("/template/1")

    assert response.status_code == 200
    assert response.json() == test_data


def test_read_template_incorrect_id(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.get("/template/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Template not found"


def test_read_all_templates(test_app, monkeypatch):
    test_data = [
        {"title": "First", "description": "Описание", "id": 1},
        {"title": "Second", "description": "Описание", "id": 2}
    ]

    async def mock_get_all():
        return test_data

    monkeypatch.setattr(crud, "get_all", mock_get_all)

    response = test_app.get("/template/")

    assert response.status_code == 200
    assert response.json() == test_data


def test_update_template(test_app, monkeypatch):
    test_update_data = {"title": "First", "description": "Описание", "id": 1}

    async def mock_get(id):
        return True

    monkeypatch.setattr(crud, "get", mock_get)

    async def mock_put(id, payload):
        return 1

    monkeypatch.setattr(crud, "put", mock_put)

    response = test_app.put("/template/1/", data=json.dumps(test_update_data))

    assert response.status_code == 200
    assert response.json() == test_update_data


@pytest.mark.parametrize(
    "id, payload, status_code",
    [
        [1, {}, 422],
        [1, {"descriptiion": "Broken"}, 422],
        [999, {"title": "First", "description": "Broken"}, 404],
    ],
)
def test_update_template_invalid(test_app, monkeypatch, id, payload, status_code):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.put(f"/template/{id}/", data=json.dumps(payload), )
    assert response.status_code == status_code


def test_remove_template(test_app, monkeypatch):
    test_data = {"title": "First", "description": "Описание", "id": 1}

    async def mock_get(id):
        return test_data

    monkeypatch.setattr(crud, "get", mock_get)

    async def mock_delete(id):
        return id

    monkeypatch.setattr(crud, "delete", mock_delete)

    response = test_app.delete("/template/1/")

    assert response.status_code == 200
    assert response.json() == test_data


def test_remove_template_incorrect_id(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.delete("/template/999/")
    assert response.status_code == 404
    assert response.json()["detail"] == "Template not found"
