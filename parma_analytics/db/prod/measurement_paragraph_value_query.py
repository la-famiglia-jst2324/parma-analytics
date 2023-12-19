"""Database crud operations for measurement_paragraph_value table."""

from typing import Any

from sqlalchemy.orm import Session

from parma_analytics.db.prod.models.measurement_paragraph_value import (
    MeasurementParagraphValue,
)


def create_measurement_paragraph_value_query(
    db: Session, measurement_paragraph_value_data: dict[str, Any]
) -> int:
    """Create a new measurement_paragraph_value in the database.

    Args:
        db: Database session.
        measurement_paragraph_value_data: values to be inserted in the database.

    Returns:
        The id of the newly created measurement_paragraph_value.
    """
    measurement_paragraph_value = MeasurementParagraphValue(
        **measurement_paragraph_value_data
    )
    db.add(measurement_paragraph_value)
    db.commit()
    db.refresh(measurement_paragraph_value)
    return measurement_paragraph_value.id


def get_measurement_paragraph_value_query(
    db: Session, measurement_paragraph_value_id: int
) -> MeasurementParagraphValue:
    """Get a measurement_paragraph_value from the database.

    Args:
        db: Database session.
        measurement_paragraph_value_id: id of the value to be retrieved.

    Returns:
        The measurement_paragraph_value with the given id.
    """
    return (
        db.query(MeasurementParagraphValue)
        .filter(MeasurementParagraphValue.id == measurement_paragraph_value_id)
        .first()
    )


def list_measurement_paragraph_values_query(db: Session) -> list:
    """List all measurement_paragraph_values from the database.

    Args:
        db: Database session.

    Returns:
        A list of all measurement_paragraph_values.
    """
    measurement_paragraph_values = db.query(MeasurementParagraphValue).all()
    return measurement_paragraph_values


def update_measurement_paragraph_value_query(
    db: Session, id: int, measurement_paragraph_value_data: dict[str, Any]
) -> MeasurementParagraphValue:
    """Update a measurement_paragraph_value in the database.

    Args:
        db: Database session.
        id: id of the measurement_paragraph_value to be updated.
        measurement_paragraph_value_data: values to be updated in the database.

    Returns:
        The updated measurement_paragraph_value.
    """
    measurement_paragraph_value = (
        db.query(MeasurementParagraphValue)
        .filter(MeasurementParagraphValue.id == id)
        .first()
    )
    for key, value in measurement_paragraph_value_data.items():
        setattr(measurement_paragraph_value, key, value)
    db.commit()
    return measurement_paragraph_value


def delete_measurement_paragraph_value_query(
    db: Session, measurement_paragraph_value_id: int
) -> None:
    """Delete a measurement_paragraph_value from the database.

    Args:
        db: Database session.
        measurement_paragraph_value_id: id of the value to be deleted.

    Returns:
        None
    """
    measurement_paragraph_value = (
        db.query(MeasurementParagraphValue)
        .filter(MeasurementParagraphValue.id == measurement_paragraph_value_id)
        .first()
    )
    db.delete(measurement_paragraph_value)
    db.commit()
