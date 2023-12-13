import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session
from parma_analytics.db.prod.measurement_float_value_query import (
    MeasurementFloatValue,
    create_measurement_float_value_query,
    get_measurement_float_value_query,
    list_measurement_float_values_query,
    update_measurement_float_value_query,
    delete_measurement_float_value_query,
)


@pytest.fixture
def mock_db():
    return MagicMock(spec=Session)


@pytest.fixture
def mock_measurement_float_value():
    return MagicMock(spec=MeasurementFloatValue)


def test_create_measurement_float_value_query(mock_db, mock_measurement_float_value):
    data = {"company_measurement_id": 1, "value": 100.0}
    with patch(
        "parma_analytics.db.prod.measurement_float_value_query.MeasurementFloatValue",
        return_value=mock_measurement_float_value,
    ):
        result = create_measurement_float_value_query(mock_db, data)
    mock_db.add.assert_called_once_with(mock_measurement_float_value)
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(mock_measurement_float_value)
    assert result == mock_measurement_float_value.id


def test_get_measurement_float_value_query(mock_db, mock_measurement_float_value):
    mock_db.query.return_value.filter.return_value.first.return_value = (
        mock_measurement_float_value
    )
    result = get_measurement_float_value_query(mock_db, 1)
    mock_db.query.assert_called_once_with(MeasurementFloatValue)
    assert result == mock_measurement_float_value


def test_list_measurement_float_values_query(mock_db, mock_measurement_float_value):
    mock_db.query.return_value.all.return_value = [mock_measurement_float_value]
    result = list_measurement_float_values_query(mock_db)
    mock_db.query.assert_called_once_with(MeasurementFloatValue)
    assert result == [mock_measurement_float_value]


def test_update_measurement_float_value_query(mock_db, mock_measurement_float_value):
    data = {"value": 200.0}
    mock_db.query.return_value.filter.return_value.first.return_value = (
        mock_measurement_float_value
    )
    result = update_measurement_float_value_query(mock_db, 1, data)
    assert result.value == 200.0
    mock_db.query.assert_called_once_with(MeasurementFloatValue)
    assert mock_measurement_float_value.value == 200.0


def test_delete_measurement_int_value_query(mock_db, mock_measurement_float_value):
    mock_db.query.return_value.filter.return_value.first.return_value = (
        mock_measurement_float_value
    )
    delete_measurement_float_value_query(mock_db, 1)
    mock_db.query.assert_called_once_with(MeasurementFloatValue)
    mock_db.query.return_value.filter.return_value.first.assert_called_once()
    mock_db.delete.assert_called_once_with(mock_measurement_float_value)
    mock_db.commit.assert_called_once()
