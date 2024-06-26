import logging
from datetime import datetime, timedelta
from unittest.mock import ANY, AsyncMock, MagicMock, patch

import httpx
import pytest
from httpx import AsyncClient
from sqlalchemy.orm import sessionmaker

from parma_analytics.bl.mining_module_manager import MiningModuleManager
from parma_analytics.bl.scraping_model import ScrapingPayloadModel
from parma_analytics.db.prod.engine import get_engine
from parma_analytics.db.prod.models.company import Company
from parma_analytics.db.prod.models.company_data_source import CompanyDataSource
from parma_analytics.db.prod.models.company_data_source_identifier import (
    CompanyDataSourceIdentifier,
)
from parma_analytics.db.prod.models.types import (
    DataSource,
    ScheduledTask,
)


@pytest.fixture
def mock_async_client():
    return MagicMock(spec=AsyncClient, get=AsyncMock(), post=AsyncMock())


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


@patch("parma_analytics.bl.mining_module_manager.Session")
@patch("parma_analytics.bl.mining_module_manager.get_engine")
def test_manage_session_success(mock_get_engine, mock_session_class):
    # Setup
    mock_session = MagicMock()
    mock_session_class.return_value = mock_session
    mock_get_engine.return_value = MagicMock()

    # Running the test
    with MiningModuleManager._manage_session() as session:
        assert session is mock_session

    # Assertions
    mock_session.commit.assert_called_once()
    mock_session.close.assert_called_once()


@patch("parma_analytics.bl.mining_module_manager.Session")
@patch("parma_analytics.bl.mining_module_manager.get_engine")
def test_manage_session_exception(mock_get_engine, mock_session_class):
    # Setup
    mock_session = MagicMock()
    mock_session_class.return_value = mock_session
    mock_get_engine.return_value = MagicMock()

    # Running the test
    with pytest.raises(Exception):
        with MiningModuleManager._manage_session() as session:
            assert session is mock_session
            raise Exception("Test Exception")

    # Assertions
    mock_session.rollback.assert_called_once()
    mock_session.close.assert_called_once()


@patch("parma_analytics.bl.mining_module_manager.get_company_id_bll")
@patch("parma_analytics.bl.mining_module_manager.call_discover_endpoint")
@patch("parma_analytics.bl.mining_module_manager.process_discovery_response")
@patch(
    "parma_analytics.bl.mining_module_manager.MiningModuleManager._fetch_identifiers"
)
def test_create_payload_success(
    mock_fetch_identifiers,
    mock_process_discovery_response,
    mock_call_discover_endpoint,
    mock_get_company_id_bll,
):
    # Setup
    mock_fetch_identifiers.return_value = {"some_key": ["identifier1", "identifier2"]}

    task_id = 123
    companies = [
        CompanyDataSource(
            id=1,
            company_id=1,
            data_source_id=1,
            is_data_source_active=True,
            health_status="UP",
            created_at=datetime.now(),
            modified_at=datetime.now(),
        ),
        CompanyDataSource(
            id=2,
            company_id=2,
            data_source_id=1,
            is_data_source_active=True,
            health_status="UP",
            created_at=datetime.now(),
            modified_at=datetime.now(),
        ),
    ]
    data_source = DataSource(id=1, source_name="DataSource1")

    mining_module_manager = MiningModuleManager()

    # Run the test
    payload = mining_module_manager._create_payload(task_id, companies, data_source)

    # Assertions
    assert isinstance(payload, ScrapingPayloadModel)
    assert payload.companies is not None
    assert payload.task_id == task_id
    assert all(str(company.company_id) in payload.companies for company in companies)
    for company in companies:
        assert payload.companies[str(company.company_id)] == {
            "some_key": ["identifier1", "identifier2"]
        }

    mock_fetch_identifiers.assert_called()
    mock_get_company_id_bll.assert_not_called()
    mock_call_discover_endpoint.assert_not_called()
    mock_process_discovery_response.assert_not_called()


@patch("parma_analytics.bl.mining_module_manager.get_company_id_bll")
@patch("parma_analytics.bl.mining_module_manager.call_discover_endpoint")
@patch("parma_analytics.bl.mining_module_manager.process_discovery_response")
@patch(
    "parma_analytics.bl.mining_module_manager.MiningModuleManager._fetch_identifiers"
)
def test_create_payload_discovery(
    mock_fetch_identifiers,
    mock_process_discovery_response,
    mock_call_discover_endpoint,
    mock_get_company_id_bll,
    caplog,
):
    # Setup
    mock_fetch_identifiers.side_effect = [None, {"some_key": ["identifier1"]}]
    mock_get_company_id_bll.side_effect = [
        Company(name="Test Company Name"),
        Company(name="Test Company Name"),
    ]

    task_id = 123
    companies = [
        CompanyDataSource(
            id=1,
            company_id=1,
            data_source_id=1,
            is_data_source_active=True,
            health_status="UP",
            created_at=datetime.now(),
            modified_at=datetime.now(),
        ),
    ]
    data_source = DataSource(id=1, source_name="DataSource1")

    mining_module_manager = MiningModuleManager()

    # Run the test
    with caplog.at_level(logging.INFO):
        payload = mining_module_manager._create_payload(task_id, companies, data_source)

    # Assertions
    assert isinstance(payload, ScrapingPayloadModel)
    assert payload.companies is not None
    assert payload.task_id == task_id
    assert all(str(company.company_id) in payload.companies for company in companies)
    for company in companies:
        assert payload.companies[str(company.company_id)] == {
            "some_key": ["identifier1"]
        }

    mock_fetch_identifiers.assert_called()
    mock_get_company_id_bll.assert_called()
    mock_call_discover_endpoint.assert_called()
    mock_process_discovery_response.assert_called()


@patch("parma_analytics.bl.mining_module_manager.get_company_id_bll")
@patch("parma_analytics.bl.mining_module_manager.call_discover_endpoint")
@patch("parma_analytics.bl.mining_module_manager.process_discovery_response")
@patch(
    "parma_analytics.bl.mining_module_manager.MiningModuleManager._fetch_identifiers"
)
def test_create_payload_discovery_no_company(
    mock_fetch_identifiers,
    mock_process_discovery_response,
    mock_call_discover_endpoint,
    mock_get_company_id_bll,
    caplog,
):
    # Setup
    mock_fetch_identifiers.side_effect = [None, {"some_key": ["identifier1"]}]
    mock_get_company_id_bll.side_effect = [None, None]

    task_id = 123
    companies = [
        CompanyDataSource(
            id=1,
            company_id=1,
            data_source_id=1,
            is_data_source_active=True,
            health_status="UP",
            created_at=datetime.now(),
            modified_at=datetime.now(),
        ),
    ]
    data_source = DataSource(id=1, source_name="DataSource1")

    mining_module_manager = MiningModuleManager()

    # Run the test
    with caplog.at_level(logging.INFO):
        payload = mining_module_manager._create_payload(task_id, companies, data_source)

    # Assertions
    log_messages = [record.message for record in caplog.records]
    assert f"Company not found with id: {1}" in log_messages[0]
    assert isinstance(payload, ScrapingPayloadModel)
    assert payload.task_id == task_id
    assert payload.companies == {}

    mock_fetch_identifiers.assert_called()
    mock_get_company_id_bll.assert_called()


@patch("parma_analytics.bl.mining_module_manager.get_company_id_bll")
@patch("parma_analytics.bl.mining_module_manager.call_discover_endpoint")
@patch("parma_analytics.bl.mining_module_manager.process_discovery_response")
@patch(
    "parma_analytics.bl.mining_module_manager.MiningModuleManager._fetch_identifiers"
)
def test_create_payload_discovery_first_none(
    mock_fetch_identifiers,
    mock_process_discovery_response,
    mock_call_discover_endpoint,
    mock_get_company_id_bll,
):
    # Setup
    mock_identifiers = {"some_key": ["identifier1", "identifier2"]}
    mock_fetch_identifiers.side_effect = [None, mock_identifiers, mock_identifiers]
    company_entity_mock = MagicMock()
    company_entity_mock.name = "Test Company Name"
    mock_get_company_id_bll.return_value = company_entity_mock

    task_id = 123
    companies = [
        CompanyDataSource(
            id=1,
            company_id=1,
            data_source_id=1,
            is_data_source_active=True,
            health_status="Good",
            created_at=datetime.now(),
            modified_at=datetime.now(),
        ),
        CompanyDataSource(
            id=2,
            company_id=2,
            data_source_id=1,
            is_data_source_active=True,
            health_status="Good",
            created_at=datetime.now(),
            modified_at=datetime.now(),
        ),
    ]
    data_source = DataSource(id=1, source_name="DataSource1")

    mining_module_manager = MiningModuleManager()

    # Run the test
    payload = mining_module_manager._create_payload(task_id, companies, data_source)

    # Assertions
    assert isinstance(payload, ScrapingPayloadModel)
    assert payload.companies is not None
    assert payload.task_id == task_id
    assert all(str(company.company_id) in payload.companies for company in companies)
    for company in companies:
        assert payload.companies[str(company.company_id)] == mock_identifiers

    mock_fetch_identifiers.assert_called()
    mock_get_company_id_bll.assert_called()
    mock_call_discover_endpoint.assert_called()
    mock_process_discovery_response.assert_called()


@pytest.mark.asyncio
@patch("httpx.AsyncClient")
async def test_trigger_success(mock_async_client_class, mining_module_manager):
    # Setup
    mock_async_client_instance = (
        mock_async_client_class.return_value.__aenter__.return_value
    )
    mock_async_client_instance.post.return_value = AsyncMock(status_code=200)
    mock_data_source = MagicMock(spec=DataSource)
    mock_data_source.id = 1
    mock_data_source.name = "name"
    mock_data_source.invocation_endpoint = "http://example.com"
    invocation_endpoint = mock_data_source.invocation_endpoint + "/companies"
    task_id = 123
    companies_dict: dict[str, dict[str, list[str]]] = {}
    scraping_payload = ScrapingPayloadModel(task_id=task_id, companies=companies_dict)

    mining_module_manager._create_payload = MagicMock(return_value=scraping_payload)

    # Run the Test
    await mining_module_manager._trigger(mock_data_source, task_id)

    # Assertions
    mock_async_client_instance.post.assert_awaited_once_with(
        invocation_endpoint,
        headers=ANY,
        content='{"task_id":123,"companies":{}}',
        timeout=None,
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "exception, expected_error_log_substring",
    [
        (
            httpx.RequestError(
                "Request error", request=httpx.Request("POST", "http://test")
            ),
            "An error occurred while requesting",
        ),
        (
            httpx.HTTPStatusError(
                "HTTP error",
                request=httpx.Request("POST", "http://example.com/companies"),
                response=AsyncMock(),
            ),
            "Error response",
        ),
        (
            Exception("Unexpected error"),
            "An unexpected error occurred while sending request",
        ),
    ],
)
@patch("httpx.AsyncClient")
async def test_trigger_errors(
    mock_async_client_class,
    mining_module_manager,
    caplog,
    exception,
    expected_error_log_substring,
):
    # Setup
    mock_async_client_instance = (
        mock_async_client_class.return_value.__aenter__.return_value
    )
    mock_async_client_instance.post.side_effect = exception
    mock_data_source = MagicMock(spec=DataSource)
    mock_data_source.id = 1
    mock_data_source.name = "name"
    mock_data_source.invocation_endpoint = "http://example.com"
    task_id = 123
    companies_dict: dict[str, dict[str, list[str]]] = {}
    scraping_payload = ScrapingPayloadModel(task_id=task_id, companies=companies_dict)

    mining_module_manager._create_payload = MagicMock(return_value=scraping_payload)

    # Run the Test
    with caplog.at_level(logging.ERROR):
        await mining_module_manager._trigger(mock_data_source, task_id)

    # Assertions
    assert any(
        expected_error_log_substring in record.message for record in caplog.records
    )


@pytest.mark.asyncio
@patch(
    "parma_analytics.bl.mining_module_manager.ensure_appropriate_scheme",
    return_value=None,
)
async def test_trigger_with_invalid_endpoint(mock_ensure_scheme, caplog):
    # Setup
    mock_data_source = MagicMock(spec=DataSource)
    mock_data_source.id = 1
    mock_data_source.name = "name"
    mock_data_source.invocation_endpoint = "http://invalid-endpoint.com"
    task_id = 123

    mining_module_manager = MiningModuleManager()

    # Run the Test
    with caplog.at_level(logging.ERROR):
        await mining_module_manager._trigger(mock_data_source, task_id)

    # Assertions
    expected_error_message = (
        f"Invalid invocation endpoint: "
        f"{mock_data_source.invocation_endpoint} "
        f"for data source {mock_data_source.id}"
    )
    assert any(expected_error_message in record.message for record in caplog.records)


@patch(
    "parma_analytics.bl.mining_module_manager.get_company_data_source_identifiers_bll"
)
def test_fetch_identifiers_success(mock_get_identifiers, mining_module_manager):
    # Setup
    company_id = 1
    data_source = DataSource(id=2, source_name="TestDataSource")

    mock_identifier = CompanyDataSourceIdentifier(
        id=1,
        company_data_source_id=1,
        identifier_type="AUTOMATICALLY_DISCOVERED",
        property="test_property",
        value="test_value",
        validity=datetime.now() + timedelta(days=1),
    )

    mock_get_identifiers.return_value = [mock_identifier]

    # Run the test
    result = mining_module_manager._fetch_identifiers(company_id, data_source)

    # Assertions
    assert isinstance(result, dict)
    assert "test_property" in result
    assert result["test_property"] == ["test_value"]
    mock_get_identifiers.assert_called_once_with(company_id, data_source.id)


@patch(
    "parma_analytics.bl.mining_module_manager.get_company_data_source_identifiers_bll"
)
def test_fetch_identifiers_no_identifier(mock_get_identifiers, mining_module_manager):
    # Setup
    company_id = 1
    data_source = DataSource(id=2, source_name="TestDataSource")

    mock_get_identifiers.return_value = None

    # Run the test
    result = mining_module_manager._fetch_identifiers(company_id, data_source)

    # Assertions
    assert isinstance(result, dict)
    assert result == {}
    mock_get_identifiers.assert_called_once_with(company_id, data_source.id)


@patch(
    "parma_analytics.bl.mining_module_manager.get_company_data_source_identifiers_bll"
)
@patch("parma_analytics.bl.mining_module_manager.rediscover_identifiers")
def test_fetch_identifiers_empty_identifier(
    mock_rediscover_identifiers, mock_get_identifiers, mining_module_manager
):
    # Setup
    company_id = 1
    data_source = DataSource(id=2, source_name="TestDataSource")

    mock_identifier = CompanyDataSourceIdentifier(
        id=1,
        company_data_source_id=1,
        identifier_type="AUTOMATICALLY_DISCOVERED",
        property="test_property",
        value="test_value",
        validity=datetime.now() + timedelta(days=1),
    )

    # First call to returns an empty list, triggering recursion
    # Second call returns a non-empty list, ending the recursion
    get_identifiers_return_array = [[], [mock_identifier]]
    mock_get_identifiers.side_effect = get_identifiers_return_array

    # Run the test
    result = mining_module_manager._fetch_identifiers(company_id, data_source)

    # Assertions
    assert len(result) > 0
    mock_rediscover_identifiers.assert_called_once_with(data_source, company_id)
    assert mock_get_identifiers.call_count == len(get_identifiers_return_array)


@patch(
    "parma_analytics.bl.mining_module_manager.get_company_data_source_identifiers_bll"
)
@patch("parma_analytics.bl.mining_module_manager.rediscover_identifiers")
def test_fetch_identifiers_with_expired_identifiers(
    mock_rediscover_identifiers, mock_get_identifiers, mining_module_manager
):
    # Setup
    company_id = 123
    data_source = DataSource(id=456, source_name="TestDataSource")

    # First call returns an expired identifier, second call returns a valid identifier
    expired_identifier = CompanyDataSourceIdentifier(
        id=1,
        company_data_source_id=company_id,
        identifier_type="AUTOMATICALLY_DISCOVERED",
        property="test_property",
        value="expired_value",
        validity=datetime.now() - timedelta(days=1),
    )

    valid_identifier = CompanyDataSourceIdentifier(
        id=2,
        company_data_source_id=company_id,
        identifier_type="AUTOMATICALLY_DISCOVERED",
        property="test_property",
        value="valid_value",
        validity=datetime.now() + timedelta(days=1),
    )

    # First call with expired identifier
    # Second call with valid identifier
    get_identifiers_return_array = [[expired_identifier], [valid_identifier]]
    mock_get_identifiers.side_effect = get_identifiers_return_array

    # Run the test
    result = mining_module_manager._fetch_identifiers(company_id, data_source)

    # Assertions
    assert len(result) > 0
    assert result["test_property"] == ["valid_value"]
    mock_rediscover_identifiers.assert_called_once_with(data_source, company_id)
    assert mock_get_identifiers.call_count == len(get_identifiers_return_array)


@patch("httpx.AsyncClient")
@patch("parma_analytics.bl.mining_module_manager.MiningModuleManager._create_payload")
async def test_trigger_no_payload(
    mock_create_payload, mock_async_client_class, mining_module_manager, caplog
):
    # Setup
    scraping_payload = ScrapingPayloadModel(task_id=123, companies={})
    scraping_payload.model_dump_json = MagicMock(return_value=None)
    mock_create_payload.return_value = scraping_payload

    mock_data_source = MagicMock(spec=DataSource)
    mock_data_source.source_name = "DataSourceName"
    task_id = 123

    # Run the Test
    with caplog.at_level(logging.INFO):
        await mining_module_manager._trigger(mock_data_source, task_id)

    # Assertions
    log_messages = [record.message for record in caplog.records]
    assert "Missing payload for datasource DataSourceName" in log_messages[0]


@patch("parma_analytics.db.prod.engine.get_engine")
@patch("parma_analytics.bl.mining_module_manager.MiningModuleManager._manage_session")
def test_set_task_status_success_with_id_success(mock_manage_session, mock_get_engine):
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


@patch("parma_analytics.db.prod.engine.get_engine")
@patch("parma_analytics.bl.mining_module_manager.MiningModuleManager._manage_session")
def test_set_task_status_success_with_id_failure_task_empty(
    mock_manage_session, mock_get_engine
):
    # Setup
    mock_engine = MagicMock()
    mock_session = MagicMock()
    mock_get_engine.return_value = mock_engine

    task_id = 123

    mock_query = MagicMock()
    mock_query.filter.return_value.with_for_update.return_value.first.return_value = (
        None
    )
    mock_session.query.return_value = mock_query

    mock_manage_session.return_value.__enter__.return_value = mock_session

    # Run the test
    with pytest.raises(Exception) as excinfo:
        MiningModuleManager.set_task_status_success_with_id(task_id, "Test Result")

    # Assertions
    assert "Task not found!" in str(excinfo.value)
    mock_session.rollback.assert_called()


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
    mock_data_source.source_name = "name"

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


@pytest.mark.parametrize(
    "task_ids",
    [
        [123, 456, 789],
    ],
)
@patch("parma_analytics.bl.mining_module_manager.asyncio")
@patch("parma_analytics.bl.mining_module_manager.MiningModuleManager._trigger")
def test_trigger_datasources_empty_task(mock_trigger, mock_asyncio, task_ids, caplog):
    # Setup
    mock_session = MagicMock()
    (
        mock_session.query.return_value.filter.return_value.with_for_update.return_value.first
    ).return_value = None

    mining_module_manager = MiningModuleManager()
    mining_module_manager.session = mock_session

    mock_loop = MagicMock()
    mock_asyncio.new_event_loop.return_value = mock_loop

    # Run the Test
    with caplog.at_level(logging.ERROR):
        mining_module_manager.trigger_datasources(task_ids)

    # Assertions
    log_messages = [record.message for record in caplog.records]
    for task_id in task_ids:
        assert f"Task with id {task_id} not found." in log_messages

    mock_trigger.assert_not_called()
    mock_asyncio.set_event_loop.assert_called_once_with(mock_loop)
    mock_loop.run_until_complete.assert_not_called()
    mock_loop.close.assert_called_once()


@pytest.mark.parametrize(
    "task_ids",
    [
        [123, 456, 789],
    ],
)
@patch("parma_analytics.bl.mining_module_manager.asyncio")
@patch("parma_analytics.bl.mining_module_manager.MiningModuleManager._trigger")
@patch("parma_analytics.bl.mining_module_manager.MiningModuleManager._schedule_task")
def test_trigger_datasources_error_scheduling_task(
    mock_schedule_task, mock_trigger, mock_asyncio, task_ids, caplog
):
    # Setup
    mock_session = MagicMock()
    mock_scheduled_task = MagicMock()
    (
        mock_session.query.return_value.filter.return_value.with_for_update.return_value.first
    ).return_value = mock_scheduled_task

    mock_schedule_task.return_value = None

    mining_module_manager = MiningModuleManager()
    mining_module_manager.session = mock_session

    mock_loop = MagicMock()
    mock_asyncio.new_event_loop.return_value = mock_loop

    # Run the Test
    with caplog.at_level(logging.ERROR):
        mining_module_manager.trigger_datasources(task_ids)

    # Assertions
    log_messages = [record.message for record in caplog.records]
    for task_id in task_ids:
        assert f"Error scheduling task {task_id}" in log_messages

    mock_trigger.assert_not_called()
    mock_asyncio.set_event_loop.assert_called_once_with(mock_loop)
    mock_loop.run_until_complete.assert_not_called()
    mock_loop.close.assert_called_once()


@pytest.mark.parametrize(
    "task_ids",
    [
        [123, 456, 789],
    ],
)
@patch("parma_analytics.bl.mining_module_manager.asyncio")
@patch("parma_analytics.bl.mining_module_manager.MiningModuleManager._trigger")
def test_trigger_datasources_exception_handling(
    mock_trigger, mock_asyncio, task_ids, caplog
):
    # Setup
    mock_session = MagicMock()

    side_effects = [
        Exception(f"Test Exception for task {task_id}") for task_id in task_ids
    ]
    (
        mock_session.query.return_value.filter.return_value.with_for_update.return_value.first
    ).side_effect = side_effects

    mining_module_manager = MiningModuleManager()
    mining_module_manager.session = mock_session

    mock_loop = MagicMock()
    mock_asyncio.new_event_loop.return_value = mock_loop

    # Run the Test
    with caplog.at_level(logging.ERROR):
        mining_module_manager.trigger_datasources(task_ids)

    # Assertions
    for i, task_id in enumerate(task_ids):
        expected_message = (
            f"Error triggering "
            f"mining module for task_id {task_id}: "
            f"Test Exception for task {task_id}"
        )
        assert expected_message in caplog.records[i].message

    assert mock_session.rollback.call_count == len(task_ids)
    mock_asyncio.set_event_loop.assert_called_once_with(mock_loop)
    mock_loop.run_until_complete.assert_not_called()
    mock_loop.close.assert_called_once()
    mock_trigger.assert_not_called()
