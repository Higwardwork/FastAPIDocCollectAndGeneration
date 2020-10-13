import json
import pytest
import starlette.responses
from app.api import crud


# GET
def test_get_file(test_app, monkeypatch):
    test_request_payload = {"title": "First", "description": "Описание"}

    async def mock_post(payload):
        return 1

    monkeypatch.setattr(crud, "post", mock_post)

    test_app.post("/template/", data=json.dumps(test_request_payload))

    test_data = {"id": 1}

    async def mock_get(id):
        return test_data

    monkeypatch.setattr(crud, "get_file", mock_get)

    response = test_app.get("/files/1")

    assert response.status_code == 200


def test_read_template_incorrect_id(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get_file", mock_get)

    response = test_app.get("/files/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Файл для шаблона не найден"
