import logging

from fastapi.testclient import TestClient
from starlette import status

logger = logging.getLogger(__name__)


def test_crawling_finished(client: TestClient):
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"welcome": "at parma-analytics"}
