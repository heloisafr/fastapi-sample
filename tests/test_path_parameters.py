import pytest
from fastapi.testclient import TestClient

from src.path_parameters import app

client = TestClient(app)


def test_path_parameters_read_item_ok():
    response = client.get("/items/1")
    assert response.status_code == 200
    assert "item_id" in response.json()
    assert 1 == response.json()["item_id"]


def test_path_parameters_read_item_error_wrong_type():
    response = client.get("/items/pen")
    assert response.status_code == 422
    assert "Input should be a valid integer" in response.text


def test_path_parameters_read_item_book_ok():
    response = client.get("/items/book")
    assert response.status_code == 200
    assert "item_id" in response.json()
    assert "book" == response.json()["item_id"]


def test_path_parameters_get_model_ok():
    response = client.get("/models/alexnet")
    assert response.status_code == 200
    assert "model_name" in response.json()
    assert "alexnet" == response.json()["model_name"]


def test_path_parameters_get_model_invalid_model_error():
    response = client.get("/models/other-cnn")
    assert response.status_code == 422
    assert "Input should be 'alexnet', 'resnet' or 'lenet'" in response.text


@pytest.mark.parametrize(
    "path", [
        "/home/docs/my-file.txt",
        "my-file.txt",
    ]
)
def test_path_parameters_get_file_ok(path):
    response = client.get(f"/files/{path}")
    assert response.status_code == 200
    assert "file_path" in response.json()
    assert path == response.json()["file_path"]


