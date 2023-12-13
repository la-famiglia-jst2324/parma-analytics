import pytest
from fastapi.testclient import TestClient
from starlette import status

from parma_analytics.api import app


# Fixture to check if the FastAPI app exists
@pytest.fixture
def client():
    assert app
    return TestClient(app)


def test_register_new_company(client):
    # Replace this dictionary with your test data
    test_data = {
        "id": "123",
        "company_name": "Example Company",
        "description": "A sample company",
        "added_by": "John Doe",
    }

    response = client.post("/new-company", json=test_data)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        "id": 123,
        "company_name": "Example Company",
        "return_message": "New company forwarded to data sourcing successfully",
    }


def test_register_new_company_missing_field(client):
    # Test with missing 'company_name' field
    invalid_data = {
        "company_name": "Example Company",
        "description": "A sample company",
    }

    response = client.post("/new-company", json=invalid_data)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    response_json = response.json()
    assert "detail" in response_json
    assert len(response_json) > 0

    actual_errors = response.json()["detail"][0]
    print("Actual Errors in Response:", actual_errors)

    # Check for the expected error structure
    expected_error = {
        "type": "missing",
        "msg": "Field required",
    }

    assert all(actual_errors.get(key) == value for key, value in expected_error.items())
