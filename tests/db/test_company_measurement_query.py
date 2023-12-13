from unittest.mock import MagicMock, patch

import pytest
from sqlalchemy.orm import Session

from parma_analytics.db.prod.company_source_measurement_query import (
    CompanyMeasurement,
    create_company_measurement_query,
    delete_company_measurement_query,
    get_by_company_and_measurement_ids_query,
    get_company_measurement_query,
    list_company_measurements_query,
    update_company_measurement_query,
)


@pytest.fixture
def mock_db():
    return MagicMock(spec=Session)


@pytest.fixture
def mock_company_measurement():
    return MagicMock(spec=CompanyMeasurement)


def test_create_company_measurement_query(mock_db, mock_company_measurement):
    data = {"sourceMeasurementId": 1, "companyId": 1}
    with patch(
        "parma_analytics.db.prod.company_measurement_query.CompanyMeasurement",
        return_value=mock_company_measurement,
    ):
        result = create_company_measurement_query(mock_db, data)
    mock_db.add.assert_called_once_with(mock_company_measurement)
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(mock_company_measurement)
    assert result == mock_company_measurement


def test_get_company_measurement_query(mock_db, mock_company_measurement):
    mock_db.query.return_value.filter.return_value.first.return_value = (
        mock_company_measurement
    )
    result = get_company_measurement_query(mock_db, 1)
    mock_db.query.assert_called_once_with(CompanyMeasurement)
    assert result == mock_company_measurement


def test_get_by_company_and_measurement_ids_query(mock_db, mock_company_measurement):
    mock_db.query.return_value.filter.return_value.first.return_value = (
        mock_company_measurement
    )
    result = get_by_company_and_measurement_ids_query(mock_db, 1, 1)
    mock_db.query.assert_called_once_with(CompanyMeasurement)
    assert result == mock_company_measurement


def test_list_company_measurements_query(mock_db, mock_company_measurement):
    mock_db.query.return_value.all.return_value = [mock_company_measurement]
    result = list_company_measurements_query(mock_db)
    mock_db.query.assert_called_once_with(CompanyMeasurement)
    assert result == [mock_company_measurement]


def test_update_company_measurement_query(mock_db, mock_company_measurement):
    new_source_measurement_id = 2
    new_company_id = 2
    data = {
        "source_measurement_id": new_source_measurement_id,
        "company_id": new_company_id,
    }
    mock_db.query.return_value.filter.return_value.first.return_value = (
        mock_company_measurement
    )
    result = update_company_measurement_query(mock_db, 1, data)
    assert result.source_measurement_id == new_source_measurement_id
    assert result.company_id == new_company_id
    mock_db.query.assert_called_once_with(CompanyMeasurement)
    assert mock_company_measurement.source_measurement_id == new_source_measurement_id
    assert mock_company_measurement.company_id == new_company_id


def test_delete_company_measurement_query(mock_db, mock_company_measurement):
    mock_db.query.return_value.filter.return_value.first.return_value = (
        mock_company_measurement
    )
    delete_company_measurement_query(mock_db, 1)
    mock_db.query.assert_called_once_with(CompanyMeasurement)
    mock_db.query.return_value.filter.return_value.first.assert_called_once()
    mock_db.delete.assert_called_once_with(mock_company_measurement)
    mock_db.commit.assert_called_once()
