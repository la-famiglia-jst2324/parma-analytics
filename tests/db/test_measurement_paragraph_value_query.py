from unittest.mock import MagicMock, patch

import pytest
from sqlalchemy.orm import Session

from parma_analytics.db.prod.measurement_paragraph_value_query import (
    MeasurementParagraphValue,
    create_measurement_paragraph_value_query,
    delete_measurement_paragraph_value_query,
    get_measurement_paragraph_value_query,
    list_measurement_paragraph_values_query,
    update_measurement_paragraph_value_query,
)


@pytest.fixture
def mock_db():
    return MagicMock(spec=Session)


@pytest.fixture
def mock_measurement_paragraph_value():
    return MagicMock(spec=MeasurementParagraphValue)


def test_create_measurement_paragraph_value_query(
    mock_db, mock_measurement_paragraph_value
):
    data = {"company_measurement_id": 1, "value": "test paragraph"}
    with patch(
        "parma_analytics.db.prod.measurement_paragraph_value_query.MeasurementParagraphValue",
        return_value=mock_measurement_paragraph_value,
    ):
        result = create_measurement_paragraph_value_query(mock_db, data)
    mock_db.add.assert_called_once_with(mock_measurement_paragraph_value)
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(mock_measurement_paragraph_value)
    assert result == mock_measurement_paragraph_value.id


def test_get_measurement_paragraph_value_query(
    mock_db, mock_measurement_paragraph_value
):
    mock_db.query.return_value.filter.return_value.first.return_value = (
        mock_measurement_paragraph_value
    )
    result = get_measurement_paragraph_value_query(mock_db, 1)
    mock_db.query.assert_called_once_with(MeasurementParagraphValue)
    assert result == mock_measurement_paragraph_value


def test_list_measurement_paragraph_values_query(
    mock_db, mock_measurement_paragraph_value
):
    mock_db.query.return_value.all.return_value = [mock_measurement_paragraph_value]
    result = list_measurement_paragraph_values_query(mock_db)
    mock_db.query.assert_called_once_with(MeasurementParagraphValue)
    assert result == [mock_measurement_paragraph_value]


def test_update_measurement_paragraph_value_query(
    mock_db, mock_measurement_paragraph_value
):
    data = {"value": "updated test paragraph"}
    mock_db.query.return_value.filter.return_value.first.return_value = (
        mock_measurement_paragraph_value
    )
    result = update_measurement_paragraph_value_query(mock_db, 1, data)
    assert result.value == "updated test paragraph"
    mock_db.query.assert_called_once_with(MeasurementParagraphValue)
    assert mock_measurement_paragraph_value.value == "updated test paragraph"


def test_delete_measurement_paragraph_value_query(
    mock_db, mock_measurement_paragraph_value
):
    mock_db.query.return_value.filter.return_value.first.return_value = (
        mock_measurement_paragraph_value
    )
    delete_measurement_paragraph_value_query(mock_db, 1)
    mock_db.query.assert_called_once_with(MeasurementParagraphValue)
    mock_db.query.return_value.filter.return_value.first.assert_called_once()
    mock_db.delete.assert_called_once_with(mock_measurement_paragraph_value)
    mock_db.commit.assert_called_once()