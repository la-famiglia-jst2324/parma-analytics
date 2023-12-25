"""This module contains the functions for registering measurement values."""

import logging
from collections.abc import Callable
from datetime import datetime

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from parma_analytics.db.prod.company_source_measurement_query import (
    create_company_measurement_query,
    get_by_company_and_measurement_ids_query,
)
from parma_analytics.db.prod.engine import get_session
from parma_analytics.db.prod.measurement_comment_value_query import (
    create_measurement_comment_value_query,
)
from parma_analytics.db.prod.measurement_float_value_query import (
    create_measurement_float_value_query,
)
from parma_analytics.db.prod.measurement_int_value_query import (
    create_measurement_int_value_query,
)
from parma_analytics.db.prod.measurement_paragraph_value_query import (
    create_measurement_paragraph_value_query,
)
from parma_analytics.db.prod.measurement_text_value_query import (
    create_measurement_text_value_query,
)
from parma_analytics.sourcing.normalization.normalization_model import NormalizedData

logger = logging.getLogger(__name__)


def register_values(normalized_measurement: NormalizedData) -> int:
    """Registers a new measurement value and returns the id.

    Args:
        normalized_measurement: The normalized measurement data.

    Returns:
        The created measurement value id.
    """
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

            # Map the types to their corresponding functions
            type_functions: dict[str, Callable] = {
                "int": handle_int,
                "float": handle_float,
                "paragraph": handle_paragraph,
                "text": handle_text,
                "comment": handle_comment,
            }

            # Get the function for the type of the source_measurement
            handle_type = type_functions.get(measurement_type)

            # Call the function
            if handle_type is not None:
                created_measurement_id = handle_type(
                    session,
                    value,
                    timestamp,
                    company_measurement.company_measurement_id,
                )
            else:
                raise ValueError(f"Invalid type: {measurement_type}")

            return created_measurement_id

    except SQLAlchemyError as e:
        logging.error(f"Database error occurred: {e}")
        return -1
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return -1


# Define the functions for each type
def handle_int(
    session: Session, value: int, timestamp: datetime, company_measurement_id: int
) -> int:
    """Registers an int value and returns the id.

    Args:
        session: The database session.
        value: The value to be registered.
        timestamp: The timestamp when the value was registered.
        company_measurement_id: The ID of the company measurement.

    Returns:
        The created measurement value id.
    """
    return create_measurement_int_value_query(
        session,
        {
            "value": value,
            "timestamp": timestamp,
            "company_measurement_id": company_measurement_id,
        },
    )


def handle_float(
    session: Session, value: float, timestamp: datetime, company_measurement_id: int
) -> int:
    """Registers a float value and returns the id.

    Args:
        session: The database session.
        value: The value to be inserted into the database.
        timestamp: The timestamp when the value was registered.
        company_measurement_id: The ID of the company measurement.

    Returns:
        The created measurement value id.
    """
    return create_measurement_float_value_query(
        session,
        {
            "value": value,
            "timestamp": timestamp,
            "company_measurement_id": company_measurement_id,
        },
    )


def handle_paragraph(
    session: Session, value: str, timestamp: datetime, company_measurement_id: int
) -> int:
    """Registers a paragraph value and returns the id.

    Args:
        session: The database session.
        value: The value to be registered.
        timestamp: The timestamp when the value was registered.
        company_measurement_id: The ID of the company measurement.

    Returns:
        The created measurement value id.
    """
    return create_measurement_paragraph_value_query(
        session,
        {
            "value": value,
            "timestamp": timestamp,
            "company_measurement_id": company_measurement_id,
        },
    )


def handle_text(
    session: Session, value: str, timestamp: datetime, company_measurement_id: int
) -> int:
    """Registers a text value and returns the id.

    Args:
        session: The database session.
        value: The value to be registered.
        timestamp: The timestamp when the value was registered.
        company_measurement_id: The ID of the company measurement.

    Returns:
        The created measurement value id.
    """
    return create_measurement_text_value_query(
        session,
        {
            "value": value,
            "timestamp": timestamp,
            "company_measurement_id": company_measurement_id,
        },
    )


def handle_comment(
    session: Session, value: str, timestamp: datetime, company_measurement_id: int
) -> int:
    """Registers a comment value and returns the id.

    Args:
        session: The database session.
        value: The value to be registered.
        timestamp: The timestamp when the value was registered.
        company_measurement_id: The ID of the company measurement.

    Returns:
        The created measurement value id.
    """
    return create_measurement_comment_value_query(
        session,
        {
            "value": value,
            "timestamp": timestamp,
            "company_measurement_id": company_measurement_id,
        },
    )
