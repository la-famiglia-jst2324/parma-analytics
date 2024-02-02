"""This module contains the functions for registering measurement values."""
import asyncio
import logging
from datetime import datetime
from typing import Any

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from parma_analytics.analytics.sentiment_analysis.sentiment_analysis import (
    get_sentiment,
)
from parma_analytics.bl.generate_report import (
    GenerateNewsInput,
    generate_news,
)
from parma_analytics.db.prod.company_source_measurement_query import (
    create_company_measurement_query,
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
from parma_analytics.db.prod.models.news import News
from parma_analytics.db.prod.reporting import get_users_subscribed_to_company
from parma_analytics.reporting.gmail.email_service import EmailService
from parma_analytics.reporting.news_comparison_engine import (
    check_notification_rules,
    create_news,
    get_source_module_id,
)
from parma_analytics.reporting.slack.send_slack_messages import SlackService
from parma_analytics.sourcing.normalization.normalization_model import NormalizedData

logger = logging.getLogger(__name__)


def register_values(normalized_measurement: NormalizedData) -> int | None:
    """Registers a new measurement value and returns the id.

    Args:
        normalized_measurement: The normalized measurement data.

    Returns:
        The created measurement value id.
    """

    # Inner function to handle the creation of news and notifications
    async def create_news_and_send_notifications():
        # create news and send notifications, only if rules are satisfied
        if comparison_engine_result.is_rules_satisfied:
            try:
                news_input = GenerateNewsInput(
                    company_id=company_id,
                    source_measurement_id=source_measurement_id,
                    company_measurement_id=company_measurement.company_measurement_id,
                    current_value=value,
                    trigger_change=comparison_engine_result.percentage_difference,
                    previous_value=comparison_engine_result.previous_value,
                    aggregation_method=comparison_engine_result.aggregation_method,
                )
                result = await generate_news(news_input)
            except SQLAlchemyError as e:
                logger.error(f"A database error occurred while generating summary: {e}")
            except Exception as e:
                logger.error(f"An error occurred while generating news: {e}")

            await create_news(
                News(
                    message=result["summary"],
                    company_id=company_id,
                    data_source_id=data_source_id,
                    trigger_factor=comparison_engine_result.percentage_difference,
                    title=result["title"],
                    timestamp=timestamp,
                    source_measurement_id=source_measurement_id,
                )
            )
            await send_notifications(company_id=company_id, text=result["summary"])

    source_measurement_id = normalized_measurement.source_measurement_id
    company_id = normalized_measurement.company_id
    value = normalized_measurement.value
    timestamp = normalized_measurement.timestamp
    measurement_type = normalized_measurement.type
    try:
        with get_session() as session:
            company_measurement = get_by_company_and_measurement_ids_query(
                session, company_id, source_measurement_id
            )
            if company_measurement is None:
                company_measurement = create_company_measurement_query(
                    session,
                    {
                        "source_measurement_id": source_measurement_id,
                        "company_id": company_id,
                    },
                )
            measurement_type = measurement_type.lower()

            # Don't create value for nested measurement
            if normalized_measurement.value is None:
                return None

            # need to check rules before creating a news
            # and sending a notification
            comparison_engine_result = check_notification_rules(
                source_measurement_id=source_measurement_id,
                value=value,
                timestamp=timestamp,
                measurement_type=measurement_type,
                company_measurement=company_measurement,
            )

            data_source_id = get_source_module_id(
                source_measurement_id=source_measurement_id
            )

            # Run the async function to create news and send notifications
            asyncio.run(create_news_and_send_notifications())

            created_measurement_id = handle_value(
                session,
                measurement_type,
                value,
                timestamp,
                company_measurement.company_measurement_id,
            )

            return created_measurement_id

    except SQLAlchemyError as e:
        logging.error(f"Database error occurred: {e}")
        return -1
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return -1


# Determines and calls the create measurement for each measurement type
def handle_value(
    session: Session,
    measurement_type: str,
    value: Any,
    timestamp: datetime,
    company_measurement_id: int,
) -> int:
    """Registers a value of a specific type and returns the id.

    Args:
        session: The database session.
        measurement_type: The type of the measurement to be registered.
        value: The value to be registered.
        timestamp: The timestamp when the value was registered.
        company_measurement_id: The ID of the company measurement.

    Returns:
        The created measurement value id.
    """
    query_functions = {
        "int": MeasurementValueCRUD(MeasurementIntValue).create_measurement_value,
        "float": MeasurementValueCRUD(MeasurementFloatValue).create_measurement_value,
        "paragraph": MeasurementValueCRUD(
            MeasurementParagraphValue
        ).create_measurement_value,
        "text": MeasurementValueCRUD(MeasurementTextValue).create_measurement_value,
        "comment": MeasurementValueCRUD(
            MeasurementCommentValue
        ).create_measurement_value,
        "link": MeasurementValueCRUD(MeasurementLinkValue).create_measurement_value,
        "image": MeasurementValueCRUD(MeasurementImageValue).create_measurement_value,
        "date": MeasurementValueCRUD(MeasurementDateValue).create_measurement_value,
        "nested": MeasurementValueCRUD(MeasurementNestedValue).create_measurement_value,
    }

    if measurement_type in query_functions:
        measurement_id = query_functions[measurement_type](
            session,
            {
                "value": value,
                "timestamp": timestamp,
                "company_measurement_id": company_measurement_id,
            },
        )

        # perform sentiment analysis for comment measurement value
        if measurement_type == "comment":
            sentiment_score = asyncio.run(get_sentiment(value))
            comment = session.query(MeasurementCommentValue).get(measurement_id)
            # update sentiment_score
            comment.sentiment_score = sentiment_score
            session.commit()

        return measurement_id
    else:
        raise ValueError(f"Invalid measurement type: {measurement_type}")


def send_notifications(company_id: int, text: str):
    """Sends notifications to users subscribed to a company.

    Args:
        company_id (int): The ID of the company.
        text (str): The content of the notification.

    Returns:
        None
    """
    # need to find users subscribed to the company
    user_ids = get_users_subscribed_to_company(get_engine(), company_id)
    for user in user_ids:
        user_id = user[0]
        slack_service = SlackService()
        email_service = EmailService(user_id)
        slack_service.send_notification(user_id=user_id, content=text)
        email_service.send_notification_email(notification_message=text)
