from unittest.mock import MagicMock, patch

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


@pytest.fixture
def mock_db():
    return MagicMock()


@pytest.fixture
def mock_company_data_source():
    return MagicMock(spec=CompanyDataSource)


def test_get_company_data_source(mock_db, mock_company_data_source):
    mock_db.query.return_value.filter.return_value.first.return_value = (
        mock_company_data_source
    )
    result = get_company_data_source(mock_db, 1, 1)
    assert result is not None


def test_get_all_company_data_sources_by_data_source_id(
    mock_db, mock_company_data_source
):
    mock_db.query.return_value.filter.return_value.all.return_value = [
        mock_company_data_source
    ]
    result = get_all_company_data_sources_by_data_source_id(mock_db, 1)
    assert len(result) == 1


def test_get_all_company_data_sources(mock_db, mock_company_data_source):
    mock_db.query.return_value.all.return_value = [mock_company_data_source]
    result = get_all_company_data_sources(mock_db)
    assert len(result) == 1


def test_create_company_data_source(mock_db, mock_company_data_source):
    data = CompanyDataSourceData(1, 1, True, "healthy")
    with patch(
        "company_data_source_query.CompanyDataSource",
        return_value=mock_company_data_source,
    ):
        result = create_company_data_source(mock_db, data)
    assert isinstance(result, CompanyDataSource)


def test_update_company_data_source(mock_db, mock_company_data_source):
    update_data = CompanyDataSourceUpdateData(False, "unhealthy")
    mock_db.query.return_value.filter.return_value.first.return_value = (
        mock_company_data_source
    )
    result = update_company_data_source(mock_db, 1, update_data)
    assert result is not None


def test_delete_company_data_source(mock_db, mock_company_data_source):
    mock_db.query.return_value.filter.return_value.first.return_value = (
        mock_company_data_source
    )
    result = delete_company_data_source(mock_db, 1)
    assert result is True
