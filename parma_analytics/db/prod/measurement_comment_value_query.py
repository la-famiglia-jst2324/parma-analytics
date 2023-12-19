"""Database crud operations for measurement_comment_value table."""

from typing import Any

from sqlalchemy.orm import Session

from parma_analytics.db.prod.models.measurement_comment_value import (
    MeasurementCommentValue,
)


def create_measurement_comment_value_query(
    db: Session, measurement_comment_value_data: dict[str, Any]
) -> int:
    """Create a new measurement_comment_value in the database.

    Args:
        db: Database session.
        measurement_comment_value_data: values to be inserted in the database.

    Returns:
        The id of the newly created measurement_comment_value.
    """
    measurement_comment_value = MeasurementCommentValue(
        **measurement_comment_value_data
    )
    db.add(measurement_comment_value)
    db.commit()
    db.refresh(measurement_comment_value)
    return measurement_comment_value.id


def get_measurement_comment_value_query(
    db: Session, measurement_comment_value_id: int
) -> MeasurementCommentValue:
    """Get a measurement_comment_value from the database.

    Args:
        db: Database session.
        measurement_comment_value_id: id of the value to be retrieved.

    Returns:
        The measurement_comment_value with the given id.
    """
    return (
        db.query(MeasurementCommentValue)
        .filter(MeasurementCommentValue.id == measurement_comment_value_id)
        .first()
    )


def list_measurement_comment_values_query(db: Session) -> list[MeasurementCommentValue]:
    """List all measurement_comment_values from the database.

    Args:
        db: Database session.

    Returns:
        A list of all measurement_comment_values.
    """
    measurement_comment_values = db.query(MeasurementCommentValue).all()
    return measurement_comment_values


def update_measurement_comment_value_query(
    db: Session, id: int, measurement_comment_value_data: dict[str, Any]
) -> MeasurementCommentValue:
    """Update a measurement_comment_value in the database.

    Args:
        db: Database session.
        id: id of the measurement_comment_value to be updated.
        measurement_comment_value_data: values to be updated in the database.

    Returns:
        The updated measurement_comment_value.
    """
    measurement_comment_value = (
        db.query(MeasurementCommentValue)
        .filter(MeasurementCommentValue.id == id)
        .first()
    )
    for key, value in measurement_comment_value_data.items():
        setattr(measurement_comment_value, key, value)
    db.commit()
    return measurement_comment_value


def delete_measurement_comment_value_query(
    db: Session, measurement_comment_value_id: int
) -> None:
    """Delete a measurement_comment_value from the database.

    Args:
        db: Database session.
        measurement_comment_value_id: id of the measurement_comment_value to be deleted.
    """
    measurement_comment_value = (
        db.query(MeasurementCommentValue)
        .filter(MeasurementCommentValue.id == measurement_comment_value_id)
        .first()
    )
    db.delete(measurement_comment_value)
    db.commit()
