"""Database crud operations for measurement_int_value table.""."""
from typing import Any

from sqlalchemy.orm import Session

from parma_analytics.db.prod.models.measurement_int_value import MeasurementIntValue


def create_measurement_int_value_query(
    db: Session, measurement_int_value_data: dict[str, Any]
) -> int:
    """Create a new measurement_int_value in the database.

    Args:
        db: Database session.
        measurement_int_value_data: values to be inserted in the database.

    Returns:
        The id of the newly created measurement_int_value.
    """
    measurement_int_value = MeasurementIntValue(**measurement_int_value_data)
    db.add(measurement_int_value)
    db.commit()
    db.refresh(measurement_int_value)
    return measurement_int_value.id


def get_measurement_int_value_query(
    db: Session, measurement_int_value_id: int
) -> MeasurementIntValue:
    """Get a measurement_int_value from the database.

    Args:
        db: Database session.
        measurement_int_value_id: id of the measurement_int_value to be retrieved.

    Returns:
        The measurement_int_value with the given id.
    """
    return (
        db.query(MeasurementIntValue)
        .filter(MeasurementIntValue.id == measurement_int_value_id)
        .first()
    )


def list_measurement_int_values_query(db: Session) -> list:
    """List all measurement_int_values from the database.

    Args:
        db: Database session.

    Returns:
        A list of all measurement_int_values.
    """
    measurement_int_values = db.query(MeasurementIntValue).all()
    return measurement_int_values


def update_measurement_int_value_query(
    db: Session, id: int, measurement_int_value_data: dict[str, Any]
) -> MeasurementIntValue:
    """Update a measurement_int_value in the database.

    Args:
        db: Database session.
        id: id of the measurement_int_value to be updated.
        measurement_int_value_data: values to be updated in the database.

    Returns:
        The updated measurement_int_value.
    """
    measurement_int_value = (
        db.query(MeasurementIntValue).filter(MeasurementIntValue.id == id).first()
    )
    for key, value in measurement_int_value_data.items():
        setattr(measurement_int_value, key, value)
    db.commit()
    return measurement_int_value


def delete_measurement_int_value_query(
    db: Session, measurement_int_value_id: int
) -> None:
    """Delete a measurement_int_value from the database.

    Args:
        db: Database session.
        measurement_int_value_id: id of the measurement_int_value to be deleted.

    Returns:
        The updated measurement_int_value.
    """
    measurement_int_value = (
        db.query(MeasurementIntValue)
        .filter(MeasurementIntValue.id == measurement_int_value_id)
        .first()
    )
    db.delete(measurement_int_value)
    db.commit()
