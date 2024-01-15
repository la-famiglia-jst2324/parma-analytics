"""Functions for fetching data from the database."""
import polars as pl

from pathlib import Path

from parma_analytics.bl.schedule_manager import QUERIES_DIR
from parma_analytics.db.prod.engine import get_session
from parma_analytics.db.prod.queries.loader import read_query_file

QUERIES_DIR = Path(__file__).parent.parent / "db" / "prod" / "queries"


# from sqlalchemy.sql import text


def fetch_data(companies: list) -> pl.DataFrame:
    """Fetch data from the database."""
    with get_session() as db:
        result = db.execute(
            read_query_file(QUERIES_DIR / "fetch_report_data.sql"),
            {"companies": tuple(companies)},
        )
        rows = [dict(zip(result.keys(), row)) for row in result.fetchall()]
        df = pl.DataFrame(rows)
        return df


def fetch_measurement_data(
    measurement_ids: list, measurement_table: str
) -> pl.DataFrame:
    """Fetch measurement data from the database.

    Args:
        measurement_ids: list of measurement ids.
        measurement_table: name of the table containing the measurement data.

    Returns:
        A DataFrame containing the measurement data.
    """
    with get_session() as db:
        result = db.execute(
            read_query_file(
                QUERIES_DIR / "fetch_measurement_data.sql",
                {"measurement_table": measurement_table},
            ),
            {"measurement_ids": tuple(measurement_ids)},
        )
        rows = [dict(zip(result.keys(), row)) for row in result.fetchall()]
        df = pl.DataFrame(rows)
        return df
