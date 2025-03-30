import pytest
from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_path_parameters_declaration_order_ok():
    """
    Testing if the correct end-point is called since we have 2 similar end-points:
    /path/items/book
    /path/items/{item_id}
    """
    response = client.get("/path/items/book")
    assert response.status_code == 200
    assert "item_id" in response.json()
    assert "book" == response.json()["item_id"]


def test_path_parameters_ok():
    response = client.get("/path/items/1")
    assert response.status_code == 200
    assert "item_id" in response.json()
    assert 1 == response.json()["item_id"]


def test_path_parameters_error_wrong_type():
    response = client.get("/path/items/pen")
    assert response.status_code == 422
    assert "Input should be a valid integer" in response.text


def test_path_parameters_with_validation_ok():
    response = client.get("/path/devices/1")
    assert response.status_code == 200
    assert "device_id" in response.json()
    assert 1 == response.json()["device_id"]


def test_path_parameters_with_validation_error():
    response = client.get("/path/devices/0")
    assert response.status_code == 422
    assert "Input should be greater than or equal to 1" in response.text


def test_path_parameters_with_enum_ok():
    response = client.get("/path/models/alexnet")
    assert response.status_code == 200
    assert "model_name" in response.json()
    assert "alexnet" == response.json()["model_name"]


def test_path_parameters_with_enum_error():
    response = client.get("/path/models/other-cnn")
    assert response.status_code == 422
    assert "Input should be 'alexnet', 'resnet' or 'lenet'" in response.text


@pytest.mark.parametrize(
    "path", [
        "home/docs/my-file.txt",
        "my-file.txt",
    ]
)
def test_path_parameters_with_path_ok(path):
    response = client.get(f"/path/files/{path}")
    assert response.status_code == 200
    assert "file_path" in response.json()
    assert path == response.json()["file_path"]


