import pytest
from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_query_parameters_optional_ok() -> None:
    """
    Test query parameter with optional parameter, sending some value
    """
    response = client.get("/things/1/?q=something")
    assert response.status_code == 200
    assert "item_id" in response.json()
    assert "q" in response.json()
    assert 1 == response.json()["item_id"]
    assert "something" == response.json()["q"]


def test_query_parameters_optional_none_ok() -> None:
    """
    Test query parameter with optional parameter, sending none
    """
    response = client.get("/things/1")
    assert response.status_code == 200
    assert "item_id" in response.json()
    assert "q" in response.json()
    assert 1 == response.json()["item_id"]
    assert response.json()["q"] is None


@pytest.mark.parametrize(
    "parameters, expected_length", [
        ("?skip=1&limit=10", 3),
        ("?skip=10", 0),
        ("", 4),
    ]
)
def test_query_parameters_optional_default_ok(parameters, expected_length) -> None:
    """
    Test query parameters with default values
    """
    response = client.get(f"/things/{parameters}")
    assert response.status_code == 200
    assert len(response.json()) == expected_length


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
def test_query_parameters_optional_default_boolean_ok(parameters, expected_description) -> None:
    """
    Test query parameters with default boolean value
    """
    response = client.get(f"/things/1/123/blue/{parameters}")
    assert response.status_code == 200
    assert "description" in response.json()
    assert expected_description in response.json()["description"]


def test_query_parameters_optional_with_validation_ok() -> None:
    """
    Test query parameter with optional parameter with min_length, max_length and pattern validation
    """
    response = client.get("/things/1/123/?q=something")
    assert response.status_code == 200
    assert "q" in response.json()
    assert "something" == response.json()["q"]


@pytest.mark.parametrize(
    "q, expected_error",
    [
        ("somethings", "String should have at most 9 characters"),
        ("new", "String should have at least 4 characters"),
        ("thing", "String should match pattern"),
    ]
)
def test_query_parameters_optional_with_validation_error(q, expected_error) -> None:
    """
    Test query parameter with optional parameter with min_length, max_length and pattern validation
    """
    response = client.get(f"/things/1/123/?q={q}")
    assert response.status_code == 422
    assert expected_error in response.text


@pytest.mark.parametrize(
    "model, expected_model", [
        (None, ""),
        ("something", "something")
    ]
)
def test_query_parameters_required_ok(model, expected_model) -> None:
    """
    Test query parameter with required parameter
    """
    response = client.get("/devices/1/", params={"model":model})
    assert response.status_code == 200
    assert "item_id" in response.json()
    assert "model" in response.json()
    assert 1 == response.json()["item_id"]
    assert expected_model == response.json()["model"]


def test_query_parameters_required_error() -> None:
    """
    Test query parameter with required parameter
    """
    response = client.get("/devices/1")
    assert response.status_code == 422
    assert "Field required" in response.text


def test_query_parameters_required_with_validation_ok() -> None:
    """
    Test query parameter with required parameter and min_length validation
    """
    response = client.get("/devices", params={"model": "something"})
    assert response.status_code == 200
    assert "model" in response.json()
    assert "something" == response.json()["model"]


@pytest.mark.parametrize(
    "params, expected_error", [
        (None, "Field required"),
        ({"model": None}, "String should have at least 4 characters"),
        ({"model": "new"}, "String should have at least 4 characters")
    ]
)
def test_query_parameters_required_with_validation_error(params, expected_error) -> None:
    """
    Test query parameter with required parameter and min_length validation
    """
    response = client.get("/devices", params=params)
    assert response.status_code == 422
    assert expected_error in response.text


@pytest.mark.parametrize(
    "params, expected_error", [
        (None, "Field required"),
        ({"model": None}, "String should have at least 5 characters"),
        ({"model": "new"}, "String should have at least 5 characters")
    ]
)
def test_query_parameters_required_can_be_none_with_validation_error(params, expected_error) -> None:
    """
    Test query parameter with required parameter and min_length validation
    Even though required could be None
    """
    response = client.get("/devices/1/123/", params=params)
    assert response.status_code == 422
    assert expected_error in response.text


def test_query_parameters_list_ok() -> None:
    """
    Query parameter (model) that receive a list of values
    """
    response = client.get("/artifacts/", params={"model": ["foo","boo"]})
    assert response.status_code == 200
    assert ["foo","boo"] == response.json()["model"]
