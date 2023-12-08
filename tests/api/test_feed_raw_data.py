import pytest
from parma_analytics.api import app
from fastapi.testclient import TestClient
from starlette import status


@pytest.fixture
def client():
    assert app
    return TestClient(app)


def test_feed_raw_data(client):
    test_data = {"source_name": "Linkedin", "raw_data": {"test": "Test data"}}
    response = client.post("/feed-raw-data", json=test_data)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["source_name"] == "Linkedin"
    assert response.json()["raw_data"] == {"test": "Test data"}
