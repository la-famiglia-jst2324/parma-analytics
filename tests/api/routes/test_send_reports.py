from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient
from starlette import status

from parma_analytics.api import app


@pytest.fixture
def client():
    return TestClient(app)


@patch(
    "parma_analytics.api.routes.send_reports.send_reports", MagicMock(return_value=None)
)
def test_weekly_reports(client: TestClient):
    response = client.get("/weekly-reports")
    assert response.status_code == status.HTTP_200_OK
    assert response.text == "Weekly reports sent successfully"
