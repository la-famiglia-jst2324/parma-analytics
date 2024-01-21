"""Report generation business layer module."""

import logging
from datetime import datetime

from sqlalchemy.exc import SQLAlchemyError

from parma_analytics.db.prod.company_query import get_company_name
from parma_analytics.db.prod.data_source_query import get_data_source_name
from parma_analytics.db.prod.engine import get_engine
from parma_analytics.db.prod.reporting import fetch_recent_value
from parma_analytics.db.prod.source_measurement_query import (
    get_source_measurement_query,
)
from parma_analytics.reporting.generate_report import ReportGenerator


def generate_report(
    company_id: int,
    source_measurement_id: int,
    company_measurement_id: int,
    current_value: int | float,
    trigger_change: float,
):
    """Generate a report summary from GPT."""
    try:
        engine = get_engine()
        company_name = get_company_name(engine, company_id)
        source_module = get_source_measurement_query(engine, source_measurement_id)
        source_name = get_data_source_name(engine, source_module.source_module_id)
        measurement_table = f"measurement_{source_module.type.lower()}_value"
        last_recent_value = fetch_recent_value(
            engine, company_measurement_id, measurement_table
        )
        timestamp_difference = (datetime.now() - last_recent_value["timestamp"]).days
        report_params = {
            "company_name": company_name,
            "source_name": source_name,
            "trigger_change": trigger_change * 100,
            "current_value": current_value,
            "metric_name": source_module.measurement_name,
            "timeframe": timestamp_difference,
        }
        report_generator = ReportGenerator()
        return report_generator.generate_report_summary(report_params)
    except SQLAlchemyError as e:
        logging.error(f"Database error occurred: {e}")
        raise e
    except Exception as e:
        logging.error(f"An error occurred while generating summary: {e}")
        raise e
