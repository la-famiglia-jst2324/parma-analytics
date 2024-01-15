import logging
from typing import Any
from unittest.mock import patch

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


@pytest.mark.parametrize(
    "source_name", [" ", "foo"]
)  # source_name shouldn't be empty because we are using it in URL for crawling db
@pytest.mark.parametrize("company_id", ["", "foo"])
@pytest.mark.parametrize("raw_data", [{}, {"foo": "bar"}])
def test_feed_raw_data_success(
    client: TestClient, source_name: str, company_id: str, raw_data: dict[str, Any]
):
    test_data = {
        "source_name": source_name,
        "company_id": company_id,
        "raw_data": raw_data,
    }

    mock_return = type("", (), {})()
    mock_return.id = "123"

    with patch(
        "parma_analytics.api.routes.feed_raw_data.store_raw_data"
    ) as mock_method:
        mock_method.return_value = mock_return
        response = client.post(
            "/feed-raw-data", json=test_data, headers=mock_authorization_header
        )

    assert mock_method.called
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["document_id"] == "123"


def test_feed_raw_data_missing_field(client: TestClient):
    test_data = {
        "company_id": "foo",
        "raw_data": {"foo": "bar"},
    }

    mock_return = type("", (), {})()
    mock_return.id = "123"

    with patch(
        "parma_analytics.api.routes.feed_raw_data.store_raw_data"
    ) as mock_method:
        mock_method.return_value = mock_return
        response = client.post(
            "/feed-raw-data", json=test_data, headers=mock_authorization_header
        )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
