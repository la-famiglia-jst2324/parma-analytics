"""This module contains the functions for registering measurement values."""

import logging
from datetime import datetime
from typing import Any

from models.measurement_value_models import (
    MeasurementCommentValue,
    MeasurementDateValue,
    MeasurementFloatValue,
    MeasurementImageValue,
    MeasurementIntValue,
    MeasurementLinkValue,
    MeasurementNestedValue,
    MeasurementParagraphValue,
    MeasurementTexthValue,
)
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from parma_analytics.db.prod.company_source_measurement_query import (
    create_company_measurement_query,
    get_by_company_and_measurement_ids_query,
)
from parma_analytics.db.prod.engine import get_session
from parma_analytics.db.prod.measurement_value_query import MeasurementValueCRUD
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

            # Call the function
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
        "text": MeasurementValueCRUD(MeasurementTexthValue).create_measurement_value,
        "comment": MeasurementValueCRUD(
            MeasurementCommentValue
        ).create_measurement_value,
        "link": MeasurementValueCRUD(MeasurementLinkValue).create_measurement_value,
        "image": MeasurementValueCRUD(MeasurementImageValue).create_measurement_value,
        "date": MeasurementValueCRUD(MeasurementDateValue).create_measurement_value,
        "nested": MeasurementValueCRUD(MeasurementNestedValue).create_measurement_value,
    }

    if measurement_type in query_functions:
        return query_functions[measurement_type](
            session,
            {
                "value": value,
                "timestamp": timestamp,
                "company_measurement_id": company_measurement_id,
            },
        )
    else:
        raise ValueError(f"Invalid measurement type: {measurement_type}")
