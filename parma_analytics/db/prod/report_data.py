from pathlib import Path

import polars as pl
from sqlalchemy.sql import text

from parma_analytics.db.prod.engine import get_session


def fetch_data() -> pl.DataFrame:
    with get_session() as db:
        query_file_path = Path("parma_analytics/db/queries/fetch_report_data.sql")
        query = text(query_file_path.read_text())
        result = db.execute(query)
        rows = [dict(zip(result.keys(), row)) for row in result.fetchall()]
        df = pl.DataFrame(rows)
        return df


def fetch_measurement_data(
    measurement_ids: list, measurement_table: str
) -> pl.DataFrame:
    with get_session() as db:
        query = text(
            f"""
        SELECT
            company_measurement_id,
            value,
            created_at
        FROM
            {measurement_table}
        WHERE
            company_measurement_id IN :measurement_ids
        ORDER BY
            company_measurement_id, created_at;
        """
        )

        result = db.execute(query, {"measurement_ids": tuple(measurement_ids)})
        rows = [dict(zip(result.keys(), row)) for row in result.fetchall()]
        df = pl.DataFrame(rows)
        return df
