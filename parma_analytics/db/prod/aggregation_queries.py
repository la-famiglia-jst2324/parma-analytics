"""Contains functions for performing aggregation queries on values.

It is responsible for getting the most recent measurement value before the given
timestamp for the specified company measurement ID and applying an aggregation method to
a set of values, including a new value.
"""

from datetime import datetime
from typing import Any

import numpy as np
from pydantic import BaseModel
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

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
from parma_analytics.db.prod.models.notification_rules import NotificationRules

# Union of all model classes
MeasurementValueType = (
    MeasurementParagraphValue
    | MeasurementIntValue
    | MeasurementFloatValue
    | MeasurementTextValue
    | MeasurementCommentValue
    | MeasurementLinkValue
    | MeasurementImageValue
    | MeasurementDateValue
    | MeasurementNestedValue
)


class IncomingData(BaseModel):
    """Incoming data model."""

    value: Any
    timestamp: datetime
    company_measurement_id: int


def get_most_recent_measurement_values(
    engine: Engine,
    data_table: type[MeasurementValueType],
    timestamp: datetime,
    company_measurement_id: int,
    notification_rule: NotificationRules | None = None,
) -> Any:
    """Get the most recent measurement value.

    Args:
        engine: Database engine.
        data_table: The measurement data table model class.
        timestamp: The reference timestamp to compare against.
        company_measurement_id: The company measurement ID.
        notification_rule: The notification rule (optional)
        to determine the aggregation method and number of aggregation entries.

    Returns:
        The most recent measurement value or the aggregated value
        based on the provided parameters.
    """
    aggregation_method = None
    num_aggregation_entries = None
    if notification_rule:
        aggregation_method = notification_rule.aggregation_method
        num_aggregation_entries = notification_rule.num_aggregation_entries

    if aggregation_method and num_aggregation_entries:
        aggregation_function = getattr(func, aggregation_method)
        with Session(engine) as session:
            subquery = (
                session.query(data_table.value)
                .filter(
                    data_table.timestamp < timestamp,
                    data_table.company_measurement_id == company_measurement_id,
                )
                .order_by(data_table.timestamp.desc())
                .limit(num_aggregation_entries)
                .subquery()
            )

            # Use SQLAlchemy's func.max to calculate the maximum value
            aggregated_value = session.query(
                aggregation_function(subquery.c.value)
            ).scalar()

            return aggregated_value
    # if num_aggregation_entries is not provided, but aggregation_method is provided,
    # then perform aggregation without limiting the number of entries
    elif aggregation_method and not num_aggregation_entries:
        aggregation_function = getattr(func, aggregation_method)
        with Session(engine) as session:
            subquery = (
                session.query(data_table.value)
                .filter(
                    data_table.timestamp < timestamp,
                    data_table.company_measurement_id == company_measurement_id,
                )
                .subquery()
            )

            query = session.query(aggregation_function(subquery.c.value))

            return query.scalar()

    elif not aggregation_method and not num_aggregation_entries:
        # Perform regular query
        with Session(engine) as session:
            return (
                session.query(data_table)
                .filter(
                    data_table.timestamp < timestamp,
                    data_table.company_measurement_id == company_measurement_id,
                )
                .order_by(data_table.timestamp.desc())
                .first()
                .value
            )


def apply_aggregation_method(
    engine: Engine,
    data_table: type[MeasurementValueType],
    incoming_data: IncomingData,
    notification_rule: NotificationRules | None = None,
) -> Any:
    """Apply an aggregation method to a set of values, including a new value.

    Args:
        engine: The database engine.
        data_table: The measurement data table model class.
        incoming_data: The incoming data containing the new value.
        notification_rule: The notification rule (optional)
        to determine the aggregation method and number of aggregation entries.

    Returns:
        The aggregated value, including the new value.
        If aggregation_method and num_aggregation_entries are provided,
        returns the aggregated value of the
        last num_aggregation_entries values plus the new value.
        If aggregation_method is provided but num_aggregation_entries is not,
        performs aggregation without limiting the number of entries.
        If neither aggregation_method nor num_aggregation_entries are provided,
        returns the new value.
    """
    new_value = incoming_data.value
    timestamp = incoming_data.timestamp
    company_measurement_id = incoming_data.company_measurement_id
    aggregation_method = None
    num_aggregation_entries = None
    if notification_rule:
        aggregation_method = notification_rule.aggregation_method
        num_aggregation_entries = notification_rule.num_aggregation_entries
    if aggregation_method and num_aggregation_entries:
        # Perform aggregation query
        with Session(engine) as session:
            # Create a subquery to fetch the values
            subquery = (
                session.query(data_table.value)
                .filter(
                    data_table.timestamp < timestamp,
                    data_table.company_measurement_id == company_measurement_id,
                )
                .order_by(data_table.timestamp.desc())
                .limit(num_aggregation_entries)
                .subquery()
            )

            # Retrieve the existing values
            values = [row[0] for row in session.query(subquery.c.value).all()]

            # Add the new value to the list
            values.append(new_value)
            return getattr(np, aggregation_method)(values)

            # Create a subquery to fetch the values

    elif aggregation_method and not num_aggregation_entries:
        # Perform aggregation without limiting the number of entries
        with Session(engine) as session:
            # Create a subquery to fetch the values
            subquery = (
                session.query(data_table.value)
                .filter(
                    data_table.timestamp < timestamp,
                    data_table.company_measurement_id == company_measurement_id,
                )
                .order_by(data_table.timestamp.desc())
                .subquery()
            )

            # Retrieve the existing values
            values = [row[0] for row in session.query(subquery.c.value).all()]

            # Add the new value to the list
            values.append(new_value)
            return getattr(np, aggregation_method)(values)

    elif not aggregation_method:
        return new_value
