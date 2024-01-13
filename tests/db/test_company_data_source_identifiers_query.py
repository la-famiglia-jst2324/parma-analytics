from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest
from company_data_source_identifiers_query import (
    create_company_data_source_identifier,
    delete_company_data_source_identifier,
    get_company_data_source_identifiers,
    update_company_data_source_identifier,
)
from models.company_data_source import CompanyDataSource
from models.company_data_source_identifier import (
    CompanyDataSourceIdentifier,
    IdentifierType,
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
    with patch(
        "models.company_data_source_identifier.CompanyDataSourceIdentifier",
        return_value=mock_company_data_source_identifier,
    ):
        result = create_company_data_source_identifier(
            mock_db,
            1,
            "key",
            IdentifierType.AUTOMATICALLY_DISCOVERED,
            "property",
            "value",
            datetime.now(),
        )
    assert isinstance(result, CompanyDataSourceIdentifier)


def test_update_company_data_source_identifier(
    mock_db, mock_company_data_source_identifier
):
    mock_db.query.return_value.filter.return_value.first.return_value = (
        mock_company_data_source_identifier
    )
    result = update_company_data_source_identifier(
        mock_db,
        1,
        "key",
        IdentifierType.AUTOMATICALLY_DISCOVERED,
        "property",
        "value",
        datetime.now(),
    )
    assert result is not None


def test_delete_company_data_source_identifier(
    mock_db, mock_company_data_source_identifier
):
    mock_db.query.return_value.filter.return_value.first.return_value = (
        mock_company_data_source_identifier
    )
    result = delete_company_data_source_identifier(mock_db, 1)
    assert result is True
