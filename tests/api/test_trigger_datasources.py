import requests
from parma_analytics.api import app


def test_create_trigger_data_sources():
    assert app
    test_data = {
        "trigger_data": {
            1: [3, 4, 5, 6],
            2: [2, 3, 4],
        }
    }

    response = requests.post("/trigger-datasources/", json=test_data)

    assert response.status_code == 201
    assert response.json() == {
        "return_message": "Trigger data sources created successfully"
    }
