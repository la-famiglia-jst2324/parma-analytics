"""Module to get send reports based on user subscription."""

import logging
from typing import Any

from sqlalchemy.orm import Session

from parma_analytics.db.prod.company_query import get_company_name
from parma_analytics.db.prod.company_source_measurement_query import (
    get_by_company_and_measurement_ids_query,
)
from parma_analytics.db.prod.engine import get_engine, get_session
from parma_analytics.db.prod.measurement_value_query import MeasurementValueCRUD
from parma_analytics.db.prod.models.measurement_value_models import (
    MeasurementCommentValue,
    MeasurementDateValue,
    MeasurementFloatValue,
    MeasurementImageValue,
    MeasurementIntValue,
    MeasurementLinkValue,
    MeasurementNestedValue,
    MeasurementParagraphValue,
    MeasurementTextValue,
)
from parma_analytics.db.prod.news_query import get_news_of_company
from parma_analytics.db.prod.reporting import fetch_company_ids_for_user
from parma_analytics.db.prod.source_measurement_query import (
    get_all_source_measurements_from_parent,
    get_source_measurement_query,
)
from parma_analytics.db.prod.user_query import get_user
from parma_analytics.reporting.generate_html import generate_html_report
from parma_analytics.reporting.gmail.email_service import EmailService
from parma_analytics.reporting.slack.send_slack_messages import SlackService


def send_reports():
    """Method to send report."."""
    with get_session() as session:
        try:
            user_ids = get_user(session)
            for user_id in user_ids:
                company_ids = fetch_company_ids_for_user(session, user_id.id)
                news_by_company: dict[str, Any] = {}

                for company_id in company_ids:
                    if company_id.company_id is not None:
                        messages = get_news_of_company(session, company_id.company_id)
                        company_name = get_company_name(
                            get_engine(), company_id.company_id
                        )
                        if messages and company_name:
                            news_by_company[company_name] = []

                            for message in messages:
                                if message.message:
                                    if "funding rounds" in message.message:
                                        new_message = handle_funding_round(
                                            message, company_id.company_id, company_name
                                        )
                                        news_by_company[company_name].append(
                                            new_message
                                        )
                                    else:
                                        news_by_company[company_name].append(
                                            message.message
                                        )
                if news_by_company:
                    user_id_int = user_id.id
                    html = generate_html_report(news_by_company)
                    email_service = EmailService(user_id_int)
                    email_service.send_report_email(html)

                    content = ""

                    for company_name, news_list in news_by_company.items():
                        content += f"{company_name}\n"

                        for news_message in news_list:
                            content += f"- {news_message}\n"
                    slack_service = SlackService()
                    slack_service.send_report(user_id_int, content)
        except Exception as e:
            logging.error(f"An error occurred in reporting/send_reports: {e}")
            raise e


def handle_funding_round(message, company_id, name):
    """Method to handle if change in funding round has happened."""
    source_measurement_id = message.source_measurement_id
    source_measurement = get_source_measurement_query(
        get_engine(), source_measurement_id
    )
    if source_measurement.parent_measurement_id is not None:
        child_source_measurements = get_all_source_measurements_from_parent(
            get_engine(), source_measurement.parent_measurement_id
        )
        message_for_funding = f"{message.message}\n"
        child_data_value = {}
        for child_source_measurement in child_source_measurements:
            measurement_type = child_source_measurement.type.lower()
            with get_session() as session:
                company_measurement = get_by_company_and_measurement_ids_query(
                    session, company_id, child_source_measurement.id
                )
                company_measurement_id = company_measurement.company_measurement_id
                recent_value = handle_value(
                    session, measurement_type, company_measurement_id
                )
                child_data_value[
                    child_source_measurement.measurement_name
                ] = recent_value
        if child_data_value:
            for (
                measurement_name,
                recent_value,
            ) in child_data_value.items():
                message_for_funding += f"- {measurement_name} - {recent_value}\n"
        return message_for_funding


def handle_value(session: Session, measurement_type: str, company_measurement_id: int):
    """Get the recent measurement value based by company_measurement id and type."""
    query_functions = {
        "int": MeasurementValueCRUD(MeasurementIntValue).get_recent_measurement_value,
        "float": MeasurementValueCRUD(
            MeasurementFloatValue
        ).get_recent_measurement_value,
        "paragraph": MeasurementValueCRUD(
            MeasurementParagraphValue
        ).get_recent_measurement_value,
        "text": MeasurementValueCRUD(MeasurementTextValue).get_recent_measurement_value,
        "comment": MeasurementValueCRUD(
            MeasurementCommentValue
        ).get_recent_measurement_value,
        "link": MeasurementValueCRUD(MeasurementLinkValue).get_recent_measurement_value,
        "image": MeasurementValueCRUD(
            MeasurementImageValue
        ).get_recent_measurement_value,
        "date": MeasurementValueCRUD(MeasurementDateValue).get_recent_measurement_value,
        "nested": MeasurementValueCRUD(
            MeasurementNestedValue
        ).get_recent_measurement_value,
    }

    if measurement_type in query_functions:
        get_recent_function = query_functions[measurement_type]
        recent_measurement_value = get_recent_function(session, company_measurement_id)
        return recent_measurement_value.value
