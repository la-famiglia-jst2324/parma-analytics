import logging

import pytest
from fastapi.testclient import TestClient
from starlette import status

from parma_analytics.api import app
from parma_analytics.api.dependencies.sourcing_auth import (
    authenticate_sourcing_request,
    authorize_sourcing_request,
)
from tests.api.dependencies.mock_sourcing_auth import (
    mock_authenticate_sourcing_request,
    mock_authorization_header,
    mock_authorize_sourcing_request,
)

logger = logging.getLogger(__name__)


# Fixture to check if the FastAPI app exists
@pytest.fixture
def client():
    assert app
    app.dependency_overrides.update(
        {
            authorize_sourcing_request: mock_authorize_sourcing_request,
            authenticate_sourcing_request: mock_authenticate_sourcing_request,
        }
    )
    return TestClient(app)


def test_crawling_finished(client):
    incoming_msg = "Crawling job completed successfully"

    test_data = {"incoming_message": incoming_msg}

    response = client.post(
        "/crawling-finished", json=test_data, headers=mock_authorization_header
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        "incoming_message": incoming_msg,
        "return_message": "Notified about crawling finished",
    }


def test_crawling_finished_missing_field(client):
    # Test with missing 'incoming_message' field
    invalid_data = {"dummy_json": "empty"}

    response = client.post(
        "/crawling-finished", json=invalid_data, headers=mock_authorization_header
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    response_json = response.json()
    assert "detail" in response_json
    assert len(response_json) > 0
    actual_errors = response.json()["detail"][0]

    logger.warning(f"Actual Errors in Response: {actual_errors}")

    # Check for the expected error structure
    expected_error = {"type": "missing", "msg": "Field required"}

    assert all(actual_errors.get(key) == value for key, value in expected_error.items())
