import logging
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from starlette import status

from parma_analytics.api import app
from parma_analytics.api.dependencies.sourcing_auth import (
    authenticate_sourcing_request,
    authorize_sourcing_request,
)
from parma_analytics.bl.mining_module_manager import MiningModuleManager
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


def test_crawling_finished_success(client):
    test_data = {
        "task_id": 12345,
        "errors": None,
    }

    with patch.object(
        MiningModuleManager, "set_task_status_success_with_id"
    ) as mock_method:
        response = client.post(
            "/crawling-finished", json=test_data, headers=mock_authorization_header
        )

    assert mock_method.called
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        "task_id": test_data["task_id"],
        "errors": test_data["errors"],
        "return_message": "Notified about crawling finished",
    }


def test_crawling_finished_with_errors(client):
    errors = {
        "error1": {"error_type": "Type1", "error_description": "Description1"},
        "error2": {"error_type": "Type2", "error_description": "Description2"},
    }
    test_data = {
        "task_id": 12345,
        "errors": errors,
    }

    with patch.object(
        MiningModuleManager, "set_task_status_success_with_id"
    ) as mock_method:
        response = client.post("/crawling-finished", json=test_data)

    assert mock_method.called
    response_json = response.json()
    assert response_json["task_id"] == test_data["task_id"]
    assert response_json["errors"] == errors
    assert response_json["return_message"] == "Notified about crawling finished"


def test_crawling_finished_exception_handling(client):
    test_data = {
        "task_id": 12345,
        "errors": None,
    }

    with patch.object(
        MiningModuleManager,
        "set_task_status_success_with_id",
        side_effect=Exception("Test Exception"),
    ):
        response = client.post(
            "/crawling-finished", json=test_data, headers=mock_authorization_header
        )

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert "Test Exception" in response.json().get("detail", "")


def test_crawling_finished_missing_field(client):
    # Test with missing 'task_id' field
    invalid_data = {"errors": None}

    response = client.post(
        "/crawling-finished", json=invalid_data, headers=mock_authorization_header
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    response_json = response.json()
    assert "detail" in response_json
    assert len(response_json["detail"]) > 0
    actual_errors = response_json["detail"][0]

    logger.warning(f"Actual Errors in Response: {actual_errors}")

    # Check for the expected error structure
    expected_error = {"type": "missing", "msg": "Field required"}

    assert all(actual_errors.get(key) == value for key, value in expected_error.items())
