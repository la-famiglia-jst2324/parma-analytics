"""Report generation business layer module."""

import polars as pl

from parma_analytics.db.prod.report_data_query import fetch_data, fetch_measurement_data
from parma_analytics.db.prod.subscribed_companies import (
    get_subscribed_companies as fetch_subscribed_companies,
)


def get_subscribed_companies(user_id):
    """Gets subscribed companies for a particular user.

    Args:
        userId: The id for a particular user

    Returns:
        list: The list of the subscribed companies for that user
    """
    user_id = 549
    return fetch_subscribed_companies(user_id)


def generate_report(companies: list) -> pl.DataFrame:
    """Generate a report."""
    df = fetch_data(companies)
    measurement_types = df["measurement_type"].unique().to_list()
    measurement_data = {}
    for measurement_type in measurement_types:
        measurements = df.filter(df["measurement_type"] == measurement_type)
        company_measurement_ids = measurements["company_measurement_id"].to_list()
        measurement_table = f"measurement_{measurement_type}_value"
        measurement_data[measurement_type] = fetch_measurement_data(
            company_measurement_ids, measurement_table.lower()
        )
    return df, measurement_data
