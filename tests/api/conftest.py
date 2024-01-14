import logging

import pytest
from fastapi.testclient import TestClient

from parma_analytics.api import app

logger = logging.getLogger(__name__)


@pytest.fixture
def client() -> TestClient:
    assert app
    return TestClient(app)
