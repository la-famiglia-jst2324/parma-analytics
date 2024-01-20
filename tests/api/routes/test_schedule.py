from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient
from starlette import status

from parma_analytics.api import app
from parma_analytics.api.routes.schedule import _schedule_tasks


@pytest.fixture
def client():
    return TestClient(app)


def test_schedule_endpoint_success(client: TestClient):
    with patch(
        "parma_analytics.api.routes.schedule._schedule_tasks"
    ) as mock_schedule_tasks:
        response = client.get("/schedule")
        assert response.status_code == status.HTTP_200_OK
        mock_schedule_tasks.assert_called_once()


def test_schedule_tasks_successful():
    with patch("parma_analytics.api.routes.schedule.get_engine") as mock_get_engine:
        with patch(
            "parma_analytics.api.routes.schedule.ScheduleManager"
        ) as mock_schedule_manager:
            mock_schedule_manager_instance = MagicMock()
            mock_schedule_manager.return_value = mock_schedule_manager_instance
            mock_schedule_manager_instance.enter.return_value = (
                mock_schedule_manager_instance
            )
            mock_schedule_manager_instance.exit = MagicMock()
            mock_schedule_manager_instance.schedule_tasks = MagicMock()
            mock_get_engine.return_value = "mock_engine"

            _schedule_tasks()
            mock_get_engine.assert_called_once()
