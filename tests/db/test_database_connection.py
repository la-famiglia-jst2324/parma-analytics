"""Verifies basic connectivity to the SQL database."""
import sqlalchemy as sa

from parma_analytics.db.prod.engine import get_engine


def test_database_reachable():
    """Verifies that the database is reachable.""" ""
    engine = get_engine()

    with engine.connect() as conn:
        res = conn.execute(sa.text("SELECT 1")).scalar_one()
        assert res == 1
