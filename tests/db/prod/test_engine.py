import sqlalchemy as sa

from parma_analytics.db.prod.engine import get_engine, get_session


def test_get_engine():
    engine = get_engine()
    with engine.connect() as conn:
        assert conn.execute(sa.text("SELECT 1")).fetchone() == (1,)


def test_get_session():
    with get_session() as session:
        assert session.execute(sa.text("SELECT 1")).fetchone() == (1,)
