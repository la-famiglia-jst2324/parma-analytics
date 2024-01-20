from unittest.mock import MagicMock

import pytest

from parma_analytics.db.prod.company_data_source_query import (
    CompanyDataSourceData,
    CompanyDataSourceUpdateData,
    create_company_data_source,
    delete_company_data_source,
    get_all_company_data_sources,
    get_all_company_data_sources_by_data_source_id,
    get_company_data_source,
    update_company_data_source,
)
from parma_analytics.db.prod.models.company_data_source import CompanyDataSource


# Setup test database and session
@pytest.fixture
def mock_db():
    return MagicMock()


@pytest.fixture
def mock_company_data_source():
    return MagicMock(spec=CompanyDataSource)


def test_get_company_data_source(mock_db):
    # Setup
    data = CompanyDataSourceData(1, 1, True, "healthy")
    mock_db.query.return_value.filter.return_value.first.return_value = data

    # Exercise
    result = get_company_data_source(mock_db, 1, 1)

    # Verify
    if result is not None:
        assert result.company_id == 1
        assert result.data_source_id == 1


def test_get_all_company_data_sources_by_data_source_id(mock_db):
    # Setup
    res_length = 2
    data1 = CompanyDataSourceData(1, 1, True, "healthy")
    data2 = CompanyDataSourceData(1, 2, True, "healthy")
    mock_db.query.return_value.filter.return_value.all.return_value = [data1, data2]

    # Exercise
    result = get_all_company_data_sources_by_data_source_id(mock_db, 1)

    # Verify
    assert len(result) == res_length


def test_get_all_company_data_sources(mock_db):
    # Setup
    res_length = 2
    data1 = CompanyDataSourceData(1, 1, True, "healthy")
    data2 = CompanyDataSourceData(2, 2, True, "healthy")
    mock_db.query(CompanyDataSourceData).return_value.all.return_value = [data1, data2]

    # Exercise
    result = get_all_company_data_sources(mock_db)

    # Verify
    assert len(result) == res_length


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
