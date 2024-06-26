"""Report generation business layer module."""

import logging
from datetime import datetime
from typing import Any

from pydantic import BaseModel
from sqlalchemy.exc import SQLAlchemyError

from parma_analytics.db.prod.company_query import get_company_name
from parma_analytics.db.prod.data_source_query import get_data_source_name
from parma_analytics.db.prod.engine import get_engine
from parma_analytics.db.prod.reporting import fetch_recent_value
from parma_analytics.db.prod.source_measurement_query import (
    get_source_measurement_query,
)
from parma_analytics.reporting.generate_report import ReportGenerator

logger = logging.getLogger(__name__)


class GenerateNewsInput(BaseModel):
    """Generate report parameters."""

    company_id: int
    source_measurement_id: int
    company_measurement_id: int
    current_value: Any
    trigger_change: float | None = None
    previous_value: Any | None = None
    aggregation_method: str | None = None


def generate_news(
    news_generator_input: GenerateNewsInput,
):
    """Generate a report summary from GPT."""
    try:
        company_id = news_generator_input.company_id
        source_measurement_id = news_generator_input.source_measurement_id
        company_measurement_id = news_generator_input.company_measurement_id
        current_value = news_generator_input.current_value
        trigger_change = news_generator_input.trigger_change
        previous_value = news_generator_input.previous_value
        aggregation_method = news_generator_input.aggregation_method

        engine = get_engine()
        company_name = get_company_name(engine, company_id)
        source_module = get_source_measurement_query(engine, source_measurement_id)
        source_name = get_data_source_name(engine, source_module.source_module_id)
        measurement_table = f"measurement_{source_module.type.lower()}_value"
        last_recent_value = fetch_recent_value(
            engine, company_measurement_id, measurement_table
        )
        timestamp_difference = (
            (datetime.now() - last_recent_value["timestamp"]).days
            if last_recent_value and "timestamp" in last_recent_value
            else 0
        )
        report_params = {
            "company_name": company_name,
            "source_name": source_name,
            "metric_name": source_module.measurement_name,
            "trigger_change": trigger_change,
            "previous_value": previous_value,
            "current_value": current_value,
            "timeframe": timestamp_difference,
            "aggregated_method": aggregation_method,
            "type": source_module.type,
        }
        report_generator = ReportGenerator()
        report = report_generator.generate_report(report_params)
        return {"title": report["title"], "summary": report["summary"]}

    except SQLAlchemyError as e:
        logging.error(f"Database error occurred: {e}")
        raise e
    except Exception as e:
        logging.error(f"An error occurred while generating summary: {e}")
        raise e
