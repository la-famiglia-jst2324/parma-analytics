import json
import logging
from datetime import datetime
from typing import get_args
from unittest import mock
from unittest.mock import ANY, AsyncMock, MagicMock, patch

import pytest
from httpx import AsyncClient, HTTPStatusError, InvalidURL, Request, RequestError
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker

from parma_analytics.bl.mining_module_manager import MiningModuleManager
from parma_analytics.bl.mining_trigger_payloads import GITHUB_PAYLOAD, REDDIT_PAYLOAD
from parma_analytics.db.prod.engine import get_engine
from parma_analytics.db.prod.models.base import Base
from parma_analytics.db.prod.models.types import (
    DataSource,
    Frequency,
    HealthStatus,
    ScheduleType,
    ScheduledTask,
    TaskStatus,
)


@pytest.fixture
def mock_async_client():
    return MagicMock(spec=AsyncClient, get=AsyncMock(), post=AsyncMock())


@pytest.fixture
def mock_os_getenv():
    with patch("os.getenv") as mock_getenv:
        mock_getenv.return_value = "prod"
        yield mock_getenv


def get_enum_values(literal):
    return get_args(literal)


def create_enums(engine):
    enums = {
        "Frequency": get_enum_values(Frequency),
        "HealthStatus": get_enum_values(HealthStatus),
        "ScheduleType": get_enum_values(ScheduleType),
        "TaskStatus": get_enum_values(TaskStatus),
    }

    for enum_name, values in enums.items():
        values_list = ", ".join(f"'{value}'" for value in values)
        check_enum_exists = text(
            f"SELECT EXISTS "
            f"(SELECT 1 FROM pg_type WHERE typname = '{enum_name.lower()}');"
        )
        create_enum = text(f"CREATE TYPE {enum_name} AS ENUM ({values_list});")
        with engine.begin() as conn:
            result = conn.execute(check_enum_exists).scalar()
            if not result:
                conn.execute(create_enum)


@pytest.fixture(scope="function")
def db_session():
    engine = get_engine()
    _session = sessionmaker(bind=engine)
    session = _session()
    create_enums(engine)
    Base.metadata.create_all(engine)
    yield session
    session.close()


@pytest.fixture
def mining_module_manager(db_session):
    manager = MiningModuleManager()
    manager.session = db_session
    yield manager


def create_data_source(db_session) -> DataSource:
    new_data_source = DataSource(
        source_name="Test Source",
        is_active=True,
        frequency="DAILY",
        health_status="UP",
        description="Test data source",
        created_at=datetime.now(),
        modified_at=datetime.now(),
        max_run_seconds=300,
        version="1.0",
        invocation_endpoint="http://test-endpoint.com",
    )
    db_session.add(new_data_source)
    db_session.commit()
    return new_data_source


def create_scheduled_task(db_session, data_source) -> ScheduledTask:
    new_task = ScheduledTask(
        data_source_id=data_source.id,
        schedule_type="ON_DEMAND",
        scheduled_at=datetime.now(),
        status="PENDING",
    )
    db_session.add(new_task)
    db_session.commit()
    return new_task


def test_context_manager_enter_exit(mining_module_manager):
    try:
        with mining_module_manager as manager:
            assert manager.session is not None
    except Exception:
        pytest.fail("Context manager raised an exception")


def test_set_task_status_success_with_id_integration(db_session):
    # Setup
    new_data_source = create_data_source(db_session)
    new_task = create_scheduled_task(db_session, new_data_source)
    task_id = new_task.task_id

    # Run the Test
    MiningModuleManager.set_task_status_success_with_id(task_id, "Test Result")

    # Assertions
    db_session.refresh(new_task)
    assert new_task.status == "SUCCESS"
    assert new_task.result_summary == "Test Result"

    # Cleanup
    db_session.delete(new_task)
    db_session.delete(new_data_source)
    db_session.commit()


def test_schedule_task_success(db_session, mining_module_manager):
    # Setup
    new_data_source = create_data_source(db_session)
    new_task = create_scheduled_task(db_session, new_data_source)

    # Run the Test
    mining_module_manager._schedule_task(new_task)

    # Assertions
    db_session.refresh(new_task)
    assert new_task.started_at is not None

    # Cleanup
    db_session.delete(new_task)
    db_session.delete(new_data_source)
    db_session.commit()


def test_schedule_task_error(db_session, mining_module_manager):
    # Setup
    new_data_source = create_data_source(db_session)
    new_task = create_scheduled_task(db_session, new_data_source)

    # Run the Test
    with patch.object(db_session, "commit", side_effect=Exception("Commit error")):
        result = mining_module_manager._schedule_task(new_task)

    # Assertions
    assert result is None
    assert new_task.started_at is None

    # Cleanup
    db_session.delete(new_task)
    db_session.commit()


@patch("parma_analytics.bl.mining_module_manager.MiningModuleManager._trigger")
def test_trigger_datasources_success(
    mock_trigger, db_session, mining_module_manager, mock_async_client, caplog
):
    mock_trigger.return_value = None

    data_source = create_data_source(db_session)
    data_source_id = data_source.id
    scheduled_task = create_scheduled_task(db_session, data_source)

    task_id = scheduled_task.task_id
    task_ids = [scheduled_task.task_id]

    mock_async_client_instance = mock_async_client.return_value.__aenter__.return_value
    mock_async_client_instance.post.return_value = MagicMock(status_code=200)

    # Run the Test
    with caplog.at_level(logging.INFO):
        mining_module_manager.trigger_datasources(task_ids)

    # Assertions
    db_session.refresh(scheduled_task)
    assert scheduled_task.started_at is not None
    log_messages = [record.message for record in caplog.records]
    assert f"Triggering mining modules for task_ids [{task_id}]" in log_messages[0]
    assert f"Triggering mining module for task_id {task_id}" in log_messages[1]
    assert f"Task {task_id} scheduled (data source {data_source_id})" in log_messages[2]
    assert "Other payload not implemented yet." in log_messages[3]

    # Clean up
    db_session.delete(scheduled_task)
    db_session.delete(data_source)
    db_session.commit()


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
