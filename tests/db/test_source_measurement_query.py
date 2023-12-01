import pytest
from unittest.mock import Mock
from unittest.mock import create_autospec
from sqlalchemy import text
from sqlalchemy.orm import Session
from parma_analytics.db.prod.source_measurement_query import (
    SourceMeasurement,
    create_source_measurement_query,
    get_source_measurement_query,
    list_source_measurements_query,
    update_source_measurement_query,
    delete_source_measurement_query,
    mapping_list,
)


@pytest.fixture
def mock_db():
    return create_autospec(Session)


@pytest.fixture
def mock_result():
    result = Mock()
    result.fetchone.return_value = Mock(_asdict=lambda: {"id": 1})
    result.fetchall.return_value = [
        Mock(_asdict=lambda: {"id": 1}),
        Mock(_asdict=lambda: {"id": 2}),
    ]
    return result


def test_create_source_measurement_query(mock_db, mock_result):
    mock_db.execute.return_value = mock_result
    source_measurement_data = {
        "type": "type1",
        "measurement_name": "name1",
        "source_module_id": 1,
        "company_id": 1,
    }
    id = create_source_measurement_query(mock_db, source_measurement_data)
    mock_db.execute.assert_called_once_with(
        text(
            """INSERT INTO source_measurement (type, measurement_name, source_module_id, company_id, created_at, modified_at)
                    VALUES (:type, :measurement_name, :source_module_id, :company_id, NOW(), NOW()) RETURNING *"""
        ),
        source_measurement_data,
    )
    assert id == 1


def test_get_source_measurement_query(mock_db, mock_result):
    mock_db.execute.return_value = mock_result
    source_measurement = get_source_measurement_query(mock_db, 1)
    mock_db.execute.assert_called_once_with(
        text(
            """SELECT id, type, measurement_name, source_module_id, company_id, created_at, modified_at
                 FROM source_measurement WHERE id = :id"""
        ),
        {"id": 1},
    )
    assert isinstance(source_measurement, SourceMeasurement)


def test_list_source_measurements_query(mock_db, mock_result):
    mock_db.execute.return_value = mock_result
    source_measurements = list_source_measurements_query(mock_db, page=1, page_size=2)
    mock_db.execute.assert_called_once_with(
        text("""SELECT * FROM source_measurement LIMIT :limit OFFSET :offset"""),
        {"limit": 2, "offset": 0},
    )
    assert len(source_measurements) == 2
    assert all(isinstance(sm, SourceMeasurement) for sm in source_measurements)


def test_update_source_measurement_query(mock_db, mock_result):
    mock_db.execute.return_value = mock_result
    source_measurement_data = {
        "type": "type1",
        "measurement_name": "name1",
        "source_module_id": 1,
        "company_id": 1,
    }
    source_measurement = update_source_measurement_query(
        mock_db, 1, source_measurement_data
    )
    mock_db.execute.assert_called_once_with(
        text(
            """UPDATE source_measurement SET type = :type, measurement_name = :measurement_name, source_module_id = :source_module_id, company_id = :company_id, modified_at = NOW() WHERE id = :id RETURNING *"""
        ),
        {
            "type": "type1",
            "measurement_name": "name1",
            "source_module_id": 1,
            "company_id": 1,
            "id": "1",
        },
    )
    assert isinstance(source_measurement, SourceMeasurement)


def test_delete_source_measurement_query(mock_db):
    delete_source_measurement_query(mock_db, 1)
    mock_db.execute.assert_called_once_with(
        text("""DELETE FROM source_measurement WHERE id = :id"""), {"id": 1}
    )
    mock_db.commit.assert_called_once()
