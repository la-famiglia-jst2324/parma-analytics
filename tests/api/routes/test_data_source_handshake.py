import json
import logging
from http import HTTPStatus
from unittest.mock import Mock, patch

import pytest
import requests
from fastapi.testclient import TestClient

from parma_analytics.api import app
from parma_analytics.db.mining.models import NormalizationSchemaIn

logger = logging.getLogger(__name__)


@pytest.fixture
def client():
    assert app
    return TestClient(app)


@pytest.fixture
def mock_jwt_handler():
    with patch(
        "parma_analytics.utils.jwt_handler.JWTHandler.create_jwt",
        return_value="mock.jwt.token",
    ) as mock:
        yield mock


@pytest.fixture
def mock_requests_get():
    mock_response = Mock(
        status_code=HTTPStatus.OK,
        json=lambda: {
            "frequency": "daily",
            "normalization_map": "{'Source': 'DataSource'}",
        },
    )
    with patch("requests.get", return_value=mock_response) as mock:
        yield mock


@pytest.fixture
def mock_requests_get_failure_400_bad_request():
    mock_response = Mock(status_code=HTTPStatus.BAD_REQUEST)
    with patch("requests.get", return_value=mock_response) as mock:
        yield mock


@pytest.fixture
def mock_store_normalization_schema():
    with patch(
        "parma_analytics.api.routes.data_source_handshake.store_normalization_schema"
    ) as mock:
        yield mock


def test_perform_handshake_success(
    client, mock_jwt_handler, mock_requests_get, mock_store_normalization_schema
):
    mock_data_source_id = 123
    mock_invocation_endpoint = "https://example.com/data-source"

    response = client.get(
        f"/handshake?invocation_endpoint={mock_invocation_endpoint}&data_source_id={mock_data_source_id}"
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"frequency": "daily"}
    expected_normalization_schema = NormalizationSchemaIn(
        schema={"Source": "DataSource"}
    )
    mock_store_normalization_schema.assert_called_once_with(
        "DataSource", expected_normalization_schema
    )


def test_perform_handshake_success_without_schema(
    client, mock_jwt_handler, mock_requests_get, mock_store_normalization_schema
):
    mock_data_source_id = 123
    mock_invocation_endpoint = "example.com/data-source"

    response = client.get(
        f"/handshake?invocation_endpoint={mock_invocation_endpoint}&data_source_id={mock_data_source_id}"
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"frequency": "daily"}
    expected_normalization_schema = NormalizationSchemaIn(
        schema={"Source": "DataSource"}
    )
    mock_store_normalization_schema.assert_called_once_with(
        "DataSource", expected_normalization_schema
    )


def test_perform_handshake_failure(
    client,
    mock_jwt_handler,
    mock_requests_get_failure_400_bad_request,
    mock_store_normalization_schema,
):
    mock_data_source_id = 123
    mock_invocation_endpoint = "https://example.com/data-source"

    response = client.get(
        f"/handshake?invocation_endpoint={mock_invocation_endpoint}&data_source_id={mock_data_source_id}"
    )

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert response.json() == {
        "detail": "An error occurred: 502: Failed to initialize the data source"
    }


def test_perform_handshake_request_exception(
    client, mock_jwt_handler, mock_store_normalization_schema
):
    mock_data_source_id = 123
    mock_invocation_endpoint = "https://example.com/data-source"

    with patch(
        "requests.get", side_effect=requests.exceptions.RequestException("Error")
    ):
        response = client.get(
            f"/handshake?invocation_endpoint={mock_invocation_endpoint}&data_source_id={mock_data_source_id}"
        )

        assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
        assert "Error" in response.json().get("detail")


def test_perform_handshake_success_with_string_response(
    client, mock_jwt_handler, mock_store_normalization_schema
):
    mock_data_source_id = 123
    mock_invocation_endpoint = "https://example.com/data-source"
    mock_response_json_string = json.dumps(
        {"frequency": "daily", "normalization_map": "{'Source': 'DataSource'}"}
    )

    with patch(
        "requests.get",
        return_value=Mock(
            status_code=HTTPStatus.OK, json=lambda: mock_response_json_string
        ),
    ):
        response = client.get(
            f"/handshake?invocation_endpoint={mock_invocation_endpoint}&data_source_id={mock_data_source_id}"
        )

        # Assertions
        assert response.status_code == HTTPStatus.OK
        assert response.json() == {"frequency": "daily"}
        mock_store_normalization_schema.assert_called_once_with(
            "DataSource", NormalizationSchemaIn(schema={"Source": "DataSource"})
        )
