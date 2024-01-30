from collections.abc import Iterator

import pytest
from sqlalchemy.orm import Session

from parma_analytics.db.prod.engine import get_session


@pytest.fixture
def session() -> Iterator[Session]:
    with get_session() as s:
        yield s
