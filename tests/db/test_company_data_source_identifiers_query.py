from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest

from parma_analytics.bl.company_data_source_identifiers_bll import (
    IdentifierData,
    IdentifierUpdateData,
)
from parma_analytics.db.prod.company_data_source_identifiers_query import (
    create_company_data_source_identifier,
    delete_company_data_source_identifier,
    get_company_data_source_identifiers,
    update_company_data_source_identifier,
)
from parma_analytics.db.prod.models.company_data_source import CompanyDataSource
from parma_analytics.db.prod.models.company_data_source_identifier import (
    CompanyDataSourceIdentifier,
)


@pytest.fixture
def mock_db():
    return MagicMock()


@pytest.fixture
def mock_company_data_source_identifier():
    return MagicMock(spec=CompanyDataSourceIdentifier)


def test_get_company_data_source_identifiers(mock_db):
    mock_db.query.return_value.filter.return_value.first.return_value = (
        CompanyDataSource()
    )
    result = get_company_data_source_identifiers(mock_db, 1, 1)
    assert result is not None


def test_create_company_data_source_identifier(
    mock_db, mock_company_data_source_identifier
):
    identifier_data = IdentifierData(
        company_data_source_id=1,
        identifier_type="AUTOMATICALLY_DISCOVERED",
        property="property",
        value="value",
        validity=datetime.now(),
    )
    with patch(
        "parma_analytics.db.prod.models.company_data_source_identifier.CompanyDataSourceIdentifier",
        return_value=mock_company_data_source_identifier,
    ):
        result = create_company_data_source_identifier(mock_db, identifier_data)
    assert isinstance(result, CompanyDataSourceIdentifier)


def test_update_company_data_source_identifier(
    mock_db, mock_company_data_source_identifier
):
    update_data = IdentifierUpdateData(
        identifier_type="AUTOMATICALLY_DISCOVERED",
        property="property",
        value="value",
        validity=datetime.now(),
    )
    mock_db.query.return_value.filter.return_value.first.return_value = (
        mock_company_data_source_identifier
    )
    result = update_company_data_source_identifier(mock_db, 1, update_data)
    assert result is not None


def test_delete_company_data_source_identifier(
    mock_db, mock_company_data_source_identifier
):
    mock_db.query.return_value.filter.return_value.first.return_value = (
        mock_company_data_source_identifier
    )
    result = delete_company_data_source_identifier(mock_db, 1)
    assert result is True
