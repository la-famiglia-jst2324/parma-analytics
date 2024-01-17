import json
import logging
from unittest import mock
from unittest.mock import ANY, AsyncMock, MagicMock, patch

import pytest
from httpx import AsyncClient, HTTPStatusError, InvalidURL, Request, RequestError
from sqlalchemy.orm import sessionmaker

from parma_analytics.bl.mining_module_manager import MiningModuleManager
from parma_analytics.bl.mining_trigger_payloads import GITHUB_PAYLOAD, REDDIT_PAYLOAD
from parma_analytics.db.prod.engine import get_engine
from parma_analytics.db.prod.models.types import (
    DataSource,
    ScheduledTask,
)


@pytest.fixture
def mock_async_client():
    return MagicMock(spec=AsyncClient, get=AsyncMock(), post=AsyncMock())


@pytest.fixture
def mock_os_getenv():
    with patch("os.getenv") as mock_getenv:
        mock_getenv.return_value = "prod"
        yield mock_getenv


@pytest.fixture(scope="function")
def db_session():
    engine = get_engine()
    _session = sessionmaker(bind=engine)
    session = _session()
    yield session
    session.close()


@pytest.fixture
def mining_module_manager(db_session):
    manager = MiningModuleManager()
    manager.session = db_session
    yield manager


@patch("parma_analytics.db.prod.engine.get_engine")
def test_context_manager_enter_exit(mock_get_engine, mining_module_manager):
    mock_engine = MagicMock()
    mock_session = MagicMock()
    mock_get_engine.return_value = mock_engine
    mining_module_manager.session = mock_session

    try:
        with mining_module_manager as manager:
            assert manager.session is not None
    except Exception:
        pytest.fail("Context manager raised an exception")

    mock_session.close.assert_called_once()


@patch("parma_analytics.db.prod.engine.get_engine")
@patch("parma_analytics.bl.mining_module_manager.MiningModuleManager._manage_session")
def test_set_task_status_success_with_id_integration(
    mock_manage_session, mock_get_engine
):
    # Setup
    mock_engine = MagicMock()
    mock_session = MagicMock()
    mock_get_engine.return_value = mock_engine

    mock_task = MagicMock(spec=ScheduledTask)
    task_id = 123
    mock_task.task_id = task_id

    mock_query = MagicMock()
    mock_query.filter.return_value.with_for_update.return_value.first.return_value = (
        mock_task
    )
    mock_session.query.return_value = mock_query

    mock_manage_session.return_value.__enter__.return_value = mock_session

    # Run the test
    MiningModuleManager.set_task_status_success_with_id(task_id, "Test Result")

    # Assertions
    assert mock_task.status == "SUCCESS"
    assert mock_task.result_summary == "Test Result"
    mock_session.commit.assert_called()


def test_schedule_task_success(mining_module_manager):
    # Setup
    mock_session = MagicMock()
    mock_task = MagicMock(spec=ScheduledTask)
    mock_task.data_source_id = 1

    mining_module_manager.session = mock_session

    (
        mock_session.query.return_value.filter.return_value.with_for_update.return_value.first
    ).return_value = mock_task

    # Run the Test
    result = mining_module_manager._schedule_task(mock_task)

    # Assertions
    assert result is not None
    assert result.started_at is not None
    mock_session.commit.assert_called()


def test_schedule_task_error(mining_module_manager):
    # Setup
    mock_session = MagicMock()
    mock_task = MagicMock(spec=ScheduledTask)
    mock_task.data_source_id = 1

    mock_session.commit.side_effect = Exception("Commit error")
    mock_session.rollback.side_effect = lambda: setattr(mock_task, "started_at", None)

    mining_module_manager.session = mock_session

    (
        mock_session.query.return_value.filter.return_value.with_for_update.return_value.first
    ).return_value = mock_task

    # Run the Test
    result = mining_module_manager._schedule_task(mock_task)

    # Assertions
    assert result is None
    assert mock_task.started_at is None


@pytest.mark.parametrize(
    "source_id, task_id",
    [
        (1, 123),
        (2, 456),
        (3, 789),
    ],
)
@patch("parma_analytics.bl.mining_module_manager.MiningModuleManager._trigger")
def test_trigger_datasources_success(
    mock_trigger, source_id, task_id, mock_async_client, caplog
):
    # Setup
    mock_trigger.return_value = None

    mock_data_source = MagicMock(spec=DataSource)
    mock_data_source.id = source_id

    mock_scheduled_task = MagicMock(spec=ScheduledTask)
    mock_scheduled_task.task_id = task_id
    mock_scheduled_task.data_source = mock_data_source

    mock_session = MagicMock()
    (
        mock_session.query.return_value.filter.return_value.with_for_update.return_value.first
    ).return_value = mock_scheduled_task

    mining_module_manager = MiningModuleManager()
    mining_module_manager.session = mock_session

    task_ids = [mock_scheduled_task.task_id]

    mock_async_client_instance = mock_async_client.return_value.__aenter__.return_value
    mock_async_client_instance.post.return_value = MagicMock(status_code=200)

    # Run the Test
    with caplog.at_level(logging.INFO):
        mining_module_manager.trigger_datasources(task_ids)

    # Assertions
    assert mock_scheduled_task.started_at is not None
    log_messages = [record.message for record in caplog.records]
    assert f"Triggering mining modules for task_ids [{task_id}]" in log_messages[0]
    assert f"Triggering mining module for task_id {task_id}" in log_messages[1]
    assert f"Task {task_id} scheduled (data source {source_id})" in log_messages[2]
    assert "Other payload not implemented yet." in log_messages[3]


@pytest.mark.parametrize("task_id", [0, 1, 123, 9999])
def test_construct_payload_github(task_id, mining_module_manager):
    # Setup
    mock_data_source = DataSource(source_name="github")
    expected_payload = json.dumps(
        {
            "task_id": task_id,
            "companies": GITHUB_PAYLOAD["companies"].copy(),
        }
    )

    # Run the Test
    result = mining_module_manager._construct_payload(mock_data_source, task_id)

    # Assertions
    assert result == expected_payload


@pytest.mark.parametrize("task_id", [0, 1, 123, 9999])
def test_construct_payload_affinity(task_id, mining_module_manager):
    # Setup
    mock_data_source = DataSource(source_name="affinity")
    expected_payload = None

    # Run the Test
    result = mining_module_manager._construct_payload(mock_data_source, task_id)

    # Assertions
    assert result == expected_payload


@pytest.mark.parametrize("task_id", [0, 1, 123, 9999])
def test_construct_payload_reddit(task_id, mining_module_manager):
    # Setup
    mock_data_source = DataSource(source_name="reddit")
    expected_payload = json.dumps(
        {
            "task_id": task_id,
            "companies": REDDIT_PAYLOAD["companies"].copy(),
        }
    )

    # Run the Test
    result = mining_module_manager._construct_payload(mock_data_source, task_id)

    # Assertions
    assert result == expected_payload


@pytest.mark.parametrize(
    "deployment_env, url, expected_scheme",
    [
        ("local", "http://example.com", "http"),
        ("local", "https://example.com", "http"),
        ("local", "example.com", "http"),
        ("prod", "http://example.com", "https"),
        ("prod", "https://example.com", "https"),
        ("prod", "example.com", "https"),
        ("staging", "http://example.com", "https"),
        ("staging", "https://example.com", "https"),
        ("staging", "example.com", "https"),
    ],
)
def test_ensure_appropriate_scheme_success(
    deployment_env, url, expected_scheme, mining_module_manager, mock_os_getenv
):
    # Setup
    mock_os_getenv.return_value = deployment_env

    # Run the Test
    result = mining_module_manager._ensure_appropriate_scheme(url)

    # Assertions
    assert result.startswith(
        expected_scheme
    ), f"URL scheme should be {expected_scheme} for deployment_env={deployment_env}"


@pytest.mark.parametrize(
    "deployment_env, url, expected_scheme",
    [
        ("local", "htt.://example.com", "http"),
        ("prod", "htt.://example.com", "https"),
        ("staging", "htt.://example.com", "https"),
    ],
)
def test_ensure_appropriate_scheme_error(
    deployment_env, url, expected_scheme, mining_module_manager, mock_os_getenv
):
    # Setup
    mock_os_getenv.return_value = deployment_env

    # Run the Test
    with mock.patch("httpx.URL", side_effect=InvalidURL(f"Invalid URL: {url}")):
        result = mining_module_manager._ensure_appropriate_scheme(url)

    # Assertions
    assert result is None, "URL scheme should be None due to InvalidURL"


def test_ensure_appropriate_scheme_error_empty_parameter(mining_module_manager):
    result = mining_module_manager._ensure_appropriate_scheme(None)

    # Assertions
    assert result is None, "Result should be None due to None parameter"


@pytest.mark.asyncio
@patch("httpx.AsyncClient")
async def test_trigger_post_success(mock_async_client_class, mining_module_manager):
    # Setup
    mock_async_client_instance = (
        mock_async_client_class.return_value.__aenter__.return_value
    )
    mock_async_client_instance.post.return_value = AsyncMock(status_code=200)

    data_source_id = 1
    invocation_endpoint = "http://test-endpoint.com/companies"
    json_payload = '{"some": "data"}'

    # Run the Test
    await mining_module_manager._trigger(
        data_source_id, invocation_endpoint, json_payload
    )

    # Assertions
    mock_async_client_instance.post.assert_awaited_once_with(
        invocation_endpoint, headers=ANY, content=json_payload, timeout=None
    )


@pytest.mark.asyncio
@patch("httpx.AsyncClient")
async def test_trigger_get_success(mock_async_client_class, mining_module_manager):
    # Setup
    mock_async_client_instance = (
        mock_async_client_class.return_value.__aenter__.return_value
    )
    mock_async_client_instance.get.return_value = AsyncMock(status_code=200)

    data_source_id = 1
    invocation_endpoint = "http://test-endpoint.com/companies"

    # Run the Test
    await mining_module_manager._trigger(data_source_id, invocation_endpoint, None)

    # Assertions
    mock_async_client_instance.get.assert_awaited_once_with(
        invocation_endpoint, headers=ANY, timeout=None
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "exception, log_message_part",
    [
        (
            RequestError("Request error", request=Request("POST", "http://test")),
            "Request error",
        ),
        (
            HTTPStatusError(
                "HTTP error",
                request=Request("POST", "http://test"),
                response=AsyncMock(),
            ),
            "Error response",
        ),
        (Exception("Unexpected error"), "Unexpected error"),
    ],
)
@patch("httpx.AsyncClient")
async def test_trigger_errors(
    mock_async_client_class, mining_module_manager, caplog, exception, log_message_part
):
    # Setup
    mock_async_client_instance = (
        mock_async_client_class.return_value.__aenter__.return_value
    )
    mock_async_client_instance.post.side_effect = exception

    data_source_id = 1
    invocation_endpoint = "http://test-endpoint.com/companies"
    json_payload = '{"some": "data"}'

    # Run the Test
    with caplog.at_level(logging.ERROR):
        await mining_module_manager._trigger(
            data_source_id, invocation_endpoint, json_payload
        )

    # Assertions
    assert log_message_part in caplog.text
    mock_async_client_instance.post.assert_awaited_once_with(
        invocation_endpoint, headers=ANY, content=json_payload, timeout=None
    )
