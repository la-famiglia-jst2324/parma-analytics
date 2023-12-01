import pytest
from starlette.testclient import TestClient
from parma_analytics.api.main import app
from unittest.mock import patch, MagicMock


# Fixture to check if the FastAPI app exists
@pytest.fixture
def client():
    assert app
    return TestClient(app)


# Mock the get_db dependency
def mock_get_db():
    db = MagicMock()
    return db


@patch("parma_analytics.db.prod.engine.get_db", new_callable=mock_get_db)
@patch("parma_analytics.bl.list_source_measurements_bll")
def test_create_source_measurement(mock_bll, mock_get_db, client):
    mock_bll.return_value = 1  # Mock the return value of the business logic function
    response = client.post(
        "/source-measurement",
        json={
            "type": "type1",
            "measurement_name": "name1",
            "source_module_id": 1,
            "company_id": 1,
        },
    )
    assert response.status_code == 201
    assert response.json()["id"] == 1
    assert response.json()["creation_msg"] == "Source Measurement successfully created"
    mock_get_db.assert_called_once()
    mock_bll.assert_called_once()


@patch("parma_analytics.db.prod.engine.get_db", new_callable=mock_get_db)
@patch("parma_analytics.bl.list_source_measurements_bll")
def test_read_all_source_measurements(mock_bll, mock_get_db, client):
    mock_bll.return_value = []  # Mock the return value of the business logic function
    response = client.get("/source-measurement")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    mock_get_db.assert_called_once()
    mock_bll.assert_called_once()
