import pytest
from parma_analytics.api import app
from fastapi.testclient import TestClient
from starlette import status


# Fixture to check if the FastAPI app exists
@pytest.fixture
def client():
    assert app
    return TestClient(app)


def test_register_new_company():
    # Replace this dictionary with your test data
    test_data = {
        "company_name": "Example Company",
        "description": "A sample company",
        "added_by": "John Doe",
    }

    response = client.post("/new-company", json=test_data)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        "company_name": "Example Company",
        "return_message": "New company forwarded to data sourcing successfully",
    }


def test_register_new_company_missing_field():
    # Test with missing 'company_name' field
    invalid_data = {
        "description": "A sample company",
        "added_by": "John Doe",
    }

    response = client.post("/new-company", json=invalid_data)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "detail" in response.json()
    assert any(
        error["msg"] == "field required" and error["type"] == "value_error.missing"
        for error in response.json()["detail"]
    )
