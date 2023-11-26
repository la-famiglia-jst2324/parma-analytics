import pytest
from parma_analytics.api import app
from fastapi.testclient import TestClient
from starlette import status


# Fixture to check if the FastAPI app exists
@pytest.fixture
def client():
    assert app
    return TestClient(app)


def test_crawling_finished(client):
    incoming_msg = "Crawling job completed successfully"

    test_data = {"incoming_message": incoming_msg}

    response = client.post("/crawling-finished", json=test_data)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        "incoming_message": incoming_msg,
        "return_message": "Notified about crawling finished",
    }


def test_crawling_finished_missing_field(client):
    # Test with missing 'incoming_message' field
    invalid_data = {"dummy_json": "empty"}

    response = client.post("/crawling-finished", json=invalid_data)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "detail" in response.json()
    assert any(
        error["msg"] == "Field required" and error["type"] == "missing"
        for error in response.json()["detail"]
    )

    actual_errors = response.json()["detail"]
    print("Actual Errors in Response:", actual_errors)

    # Check for the expected error structure
    expected_error = {"type": "missing", "msg": "Field required"}
    assert expected_error in actual_errors
