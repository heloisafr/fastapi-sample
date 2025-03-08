import pytest
import json
from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


@pytest.mark.parametrize(
    "item", [
        ({"name": "book", "price": 10.50}),
        ({"name": "book", "price": 11.50, "description": "A good book"}),
    ]
)
def test_request_body_create_item_ok(item) -> None:
    """
    Sample of request body
    This is the reason for json.dumps(item)
    """
    response = client.post("/items", data=json.dumps(item))
    assert response.status_code == 200
    for k, v in item.items():
        assert v == response.json()[k]


def test_request_body_create_item_missing_value() -> None:
    """
    Sample of request body
    This is the reason for json.dumps(item)
    """
    response = client.post("/items", data=json.dumps({"name": "book"}))
    assert response.status_code == 422
    assert "Field required" in response.text


def test_request_body_update_item_ok() -> None:
    """
    Sample of request body + path parameter
    This is the reason for json.dumps(item)
    """
    item = {"name": "book", "price": 11.50, "description": "New description"}
    response = client.put("/items/1", data=json.dumps(item))
    assert response.status_code == 200
    assert 1 == response.json()["item_id"]
    assert item["name"] == response.json()["name"]
    assert item["description"] == response.json()["description"]
    assert item["price"] == response.json()["price"]


def test_request_body_update_models_q_ok() -> None:
    """
    Sample of request body
    This is the reason for json.dumps(item)
    """
    item = {"name": "book", "price": 10.50, "description": "A good book"}
    response = client.put("/models/1?q=foo", data=json.dumps(item))
    assert response.status_code == 200
    assert 1 == response.json()["item_id"]
    assert item["name"] == response.json()["name"]
    assert item["description"] == response.json()["description"]
    assert item["price"] == response.json()["price"]
    assert "foo" == response.json()["q"]
