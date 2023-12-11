from collections.abc import Iterator

import pytest
from firebase_admin.firestore import firestore as firestore_types

from parma_analytics.db.mining.engine import get_engine


@pytest.fixture(scope="module")
def engine() -> Iterator[firestore_types.Client]:
    yield get_engine()
