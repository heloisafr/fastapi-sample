import pytest
from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_custom_validation_ok() -> None:
    """
    Custom validation
    """
    response = client.get("/custom-validation/items", params={"id": "isbn-9781529046137"})
    assert response.status_code == 200
    assert "id" in response.json()
    assert "name" in response.json()


def test_custom_validation_error() -> None:
    """
    Custom validation
    """
    response = client.get("/custom-validation/items", params={"id": "123"})
    assert response.status_code == 422
    assert "Invalid ID format, it must start with " in response.text


