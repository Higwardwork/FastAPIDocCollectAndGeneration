from starlette.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_hello():
    response = client.get("/status")
    assert response.status_code == 200
    assert response.json() == {"status": True}
