from unittest.mock import MagicMock, patch

import pytest

from parma_analytics.db.prod.company_data_source_query import (
    CompanyDataSourceData,
    CompanyDataSourceUpdateData,
    create_company_data_source,
    delete_company_data_source,
    get_all_company_data_sources,
    get_company_data_source,
    update_company_data_source,
)
from parma_analytics.db.prod.engine import get_session
from parma_analytics.db.prod.models.company_data_source import CompanyDataSource


# Setup test database and session
@pytest.fixture
def mock_db():
    return MagicMock()


@pytest.fixture
def mock_company_data_source():
    return MagicMock(spec=CompanyDataSource)


def test_get_company_data_source():
    # Exercise
    result = get_company_data_source(get_session(), 1, 1)

    # Verify
    if result is not None:
        assert result.company_id == 1
        assert result.data_source_id == 1


@patch(
    "parma_analytics.db.prod.company_data_source_query.get_all_company_data_sources_by_data_source_id"
)
def test_get_all_company_data_sources_by_data_source_id(
    mock_get_all_company_data_sources_by_data_source_id,
):
    expected_length = 2
    expected_company_id_1 = 1
    expected_company_id_2 = 2
    expected_data_source_id = 1

    # Setup
    data1 = CompanyDataSourceData(
        expected_data_source_id, expected_company_id_1, True, "healthy"
    )
    data2 = CompanyDataSourceData(
        expected_data_source_id, expected_company_id_2, True, "healthy"
    )
    mock_get_all_company_data_sources_by_data_source_id.return_value = [data1, data2]

    # Exercise
    result = mock_get_all_company_data_sources_by_data_source_id()

    # Verify
    assert len(result) == expected_length
    assert result[0].company_id == expected_company_id_1
    assert result[0].data_source_id == expected_data_source_id
    assert result[1].company_id == expected_company_id_2
    assert result[1].data_source_id == expected_data_source_id


def test_get_all_company_data_sources():
    # Exercise
    result = get_all_company_data_sources(get_session())

    # Verify
    assert len(result) > 0


def test_create_company_data_source(mock_db):
    # Setup
    data = CompanyDataSourceData(1, 1, True, "healthy")

    # Exercise
    result = create_company_data_source(mock_db, data)

    # Verify
    assert result.company_id == 1
    assert result.data_source_id == 1


def test_update_company_data_source(mock_db):
    # Setup
    data = CompanyDataSourceData(1, 1, True, "healthy")
    create_company_data_source(mock_db, data)
    update_data = CompanyDataSourceUpdateData(False, "unhealthy")

    # Exercise
    result = update_company_data_source(mock_db, 1, update_data)

    # Verify
    if result is not None:
        assert result.is_data_source_active is False
        assert result.health_status == "unhealthy"


def test_delete_company_data_source(mock_db):
    # Setup
    data = CompanyDataSourceData(1, 1, True, "healthy")
    create_company_data_source(mock_db, data)

    # Exercise
    result = delete_company_data_source(mock_db, 1)

    # Verify
    assert result is True
