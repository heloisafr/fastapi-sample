from fastapi.testclient import TestClient

from src.query_parameters import app

client = TestClient(app)


def test_query_parameters_read_items_ok():
    response = client.get("/items/?skip=0&limit=10")
    assert response.status_code == 200
    print(response.text)
    assert len(response.json()) == 4
    # assert 1 == response.json()["item_id"]

