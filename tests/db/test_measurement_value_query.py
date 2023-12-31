from unittest.mock import MagicMock

import pytest
from sqlalchemy.orm import Session

from parma_analytics.db.prod.measurement_value_query import MeasurementValueCRUD
from parma_analytics.db.prod.models.measurement_value_models import MeasurementTextValue


@pytest.fixture
def mock_db():
    return MagicMock(spec=Session)


@pytest.fixture
def mock_measurement_text_value():
    return MagicMock(spec=MeasurementTextValue)


def test_create_measurement_value(mock_db, mock_measurement_text_value):
    crud = MeasurementValueCRUD(mock_measurement_text_value)
    data = {"value": "test_value"}
    id = crud.create_measurement_value(mock_db, data)
    assert id is not None


def test_get_measurement_value(mock_db, mock_measurement_text_value):
    crud = MeasurementValueCRUD(mock_measurement_text_value)
    data = {"value": "test_value"}
    mock_instance = MagicMock()
    mock_instance.id = 1
    mock_db.query().filter().first.return_value = mock_instance
    crud.create_measurement_value = MagicMock(return_value=mock_instance.id)
    id = crud.create_measurement_value(mock_db, data)
    instance = crud.get_measurement_value(mock_db, id)
    assert instance is not None
    assert instance.id == id


def test_list_measurement_value(mock_db, mock_measurement_text_value):
    crud = MeasurementValueCRUD(mock_measurement_text_value)
    data = {"value": "test_value"}
    crud.create_measurement_value(mock_db, data)
    instances = crud.list_measurement_value(mock_db)
    assert instances


def test_update_measurement_value(mock_db, mock_measurement_text_value):
    crud = MeasurementValueCRUD(mock_measurement_text_value)
    data = {"value": "test_value"}
    id = crud.create_measurement_value(mock_db, data)
    new_data = {"value": "new_value"}
    crud.update_measurement_value(mock_db, id, new_data)
    instance = crud.get_measurement_value(mock_db, id)
    assert instance.value == "new_value"


def test_delete_measurement_value(mock_db, mock_measurement_text_value):
    crud = MeasurementValueCRUD(mock_measurement_text_value)
    data = {"value": "test_value"}
    id = crud.create_measurement_value(mock_db, data)
    crud.delete_measurement_value(mock_db, id)
    mock_db.query().filter().first.return_value = None
    instance = crud.get_measurement_value(mock_db, id)
    assert instance is None
