from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_home_ok():
    response = client.get("/")
    assert response.status_code == 200
    assert "The API is up" in response.json()["msg"]


def test_read_item_ok():
    response = client.get("/items/1")
    assert response.status_code == 200
    assert "item_id" in response.json()
    assert 1 == response.json()["item_id"]


def test_read_item_error_wrong_type():
    response = client.get("/items/book")
    print(response.status_code)
    print(response.text)
    assert response.status_code == 422
    assert "Input should be a valid integer" in response.text


def test_read_item_error_missing_value():
    response = client.get("/items/")
    print(response.status_code)
    print(response.text)
    assert response.status_code == 404

