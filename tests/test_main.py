from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_home_ok():
    response = client.get("/")
    assert response.status_code == 200
    assert "The API is up" in response.json()["msg"]

