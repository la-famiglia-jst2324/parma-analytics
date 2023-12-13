import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session
from parma_analytics.db.prod.measurement_int_value_query import (
    MeasurementIntValue,
    create_measurement_int_value_query,
    get_measurement_int_value_query,
    list_measurement_int_values_query,
    update_measurement_int_value_query,
    delete_measurement_int_value_query,
)


@pytest.fixture
def mock_db():
    return MagicMock(spec=Session)


@pytest.fixture
def mock_measurement_int_value():
    return MagicMock(spec=MeasurementIntValue)


def test_create_measurement_int_value_query(mock_db, mock_measurement_int_value):
    data = {"company_measurement_id": 1, "value": 100}
    with patch(
        "parma_analytics.db.prod.measurement_int_value_query.MeasurementIntValue",
        return_value=mock_measurement_int_value,
    ):
        result = create_measurement_int_value_query(mock_db, data)
    mock_db.add.assert_called_once_with(mock_measurement_int_value)
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(mock_measurement_int_value)
    assert result == mock_measurement_int_value.id


def test_get_measurement_int_value_query(mock_db, mock_measurement_int_value):
    mock_db.query.return_value.filter.return_value.first.return_value = (
        mock_measurement_int_value
    )
    result = get_measurement_int_value_query(mock_db, 1)
    mock_db.query.assert_called_once_with(MeasurementIntValue)
    print(mock_db.query.return_value.filter.call_args_list)
    assert result == mock_measurement_int_value


def test_list_measurement_int_values_query(mock_db, mock_measurement_int_value):
    mock_db.query.return_value.all.return_value = [mock_measurement_int_value]
    result = list_measurement_int_values_query(mock_db)
    mock_db.query.assert_called_once_with(MeasurementIntValue)
    assert result == [mock_measurement_int_value]


def test_update_measurement_int_value_query(mock_db, mock_measurement_int_value):
    data = {"value": 200}
    mock_db.query.return_value.filter.return_value.first.return_value = (
        mock_measurement_int_value
    )
    result = update_measurement_int_value_query(mock_db, 1, data)
    mock_db.query.assert_called_once_with(MeasurementIntValue)
    assert mock_measurement_int_value.value == 200
    mock_db.commit.assert_called_once()
    assert result == mock_measurement_int_value


def test_delete_measurement_int_value_query(mock_db, mock_measurement_int_value):
    mock_db.query.return_value.filter.return_value.first.return_value = (
        mock_measurement_int_value
    )
    delete_measurement_int_value_query(mock_db, 1)
    mock_db.query.assert_called_once_with(MeasurementIntValue)
    mock_db.delete.assert_called_once_with(mock_measurement_int_value)
    mock_db.commit.assert_called_once()
