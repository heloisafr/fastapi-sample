import pytest
from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


@pytest.mark.parametrize(
    "parameters, expected_length", [
        ("?skip=1&limit=10", 3),
        ("?skip=10", 0),
        ("", 4),
    ]
)
def test_query_parameters_read_items_ok(parameters, expected_length) -> None:
    """
    Test query parameters with default values
    """
    response = client.get(f"/items/{parameters}")
    assert response.status_code == 200
    assert len(response.json()) == expected_length


def test_query_parameters_read_things_none_ok() -> None:
    """
    Test query parameter with optional parameter, sending none
    """
    response = client.get("/things/1")
    assert response.status_code == 200
    assert "item_id" in response.json()
    assert "q" in response.json()
    assert 1 == response.json()["item_id"]
    assert response.json()["q"] is None


def test_query_parameters_read_things_something_ok() -> None:
    """
    Test query parameter with optional parameter, sending some value
    """
    response = client.get("/things/1/?q=something")
    assert response.status_code == 200
    assert "item_id" in response.json()
    assert "q" in response.json()
    assert 1 == response.json()["item_id"]
    assert "something" == response.json()["q"]


@pytest.mark.parametrize(
    "parameters, expected_description", [
        ("?short_description=1", "short"),
        ("?short_description=true", "short"),
        ("?short_description=on", "short"),
        ("?short_description=yes", "short"),
        ("?short_description=false", "long"),
        ("?short_description=no", "long"),
        ("", "long"),
    ]
)
def test_query_parameters_read_artifacts_ok(parameters, expected_description) -> None:
    """
    Test query parameters with default boolean value
    """
    response = client.get(f"/artifacts/1/{parameters}")
    assert response.status_code == 200
    assert "description" in response.json()
    assert expected_description in response.json()["description"]


def test_query_parameters_read_devices_ok() -> None:
    """
    Test query parameter with required parameter
    """
    response = client.get("/devices/1/?model=something")
    assert response.status_code == 200
    assert "item_id" in response.json()
    assert "model" in response.json()
    assert 1 == response.json()["item_id"]
    assert "something" == response.json()["model"]


def test_query_parameters_read_devices_error_missing_value() -> None:
    """
    Test query parameter with required parameter
    """
    response = client.get("/devices/1")
    assert response.status_code == 422
    assert "Field required" in response.text

