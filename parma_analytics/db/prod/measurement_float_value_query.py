"""Database crud operations for measurement_float_value table."""

from typing import Any

from sqlalchemy.orm import Session

from parma_analytics.db.prod.models.measurement_float_value import MeasurementFloatValue


def create_measurement_float_value_query(
    db: Session, measurement_float_value_data: dict[str, Any]
) -> int:
    """Create a new measurement_float_value in the database.

    Args:
        db: Database session.
        measurement_float_value_data: values to be inserted in the database.

    Returns:
        The id of the newly created measurement_float_value.
    """
    measurement_float_value = MeasurementFloatValue(**measurement_float_value_data)
    db.add(measurement_float_value)
    db.commit()
    db.refresh(measurement_float_value)
    return measurement_float_value.id


def get_measurement_float_value_query(
    db: Session, measurement_float_value_id: int
) -> MeasurementFloatValue:
    """Get a measurement_float_value from the database.

    Args:
        db: Database session.
        measurement_float_value_id: id of the measurement_float_value to be retrieved.

    Returns:
        The measurement_float_value with the given id.
    """
    return (
        db.query(MeasurementFloatValue)
        .filter(MeasurementFloatValue.id == measurement_float_value_id)
        .first()
    )


def list_measurement_float_values_query(db: Session) -> list[MeasurementFloatValue]:
    """List all measurement_float_values from the database.

    Args:
        db: Database session.

    Returns:
        A list of all measurement_float_values.
    """
    measurement_float_values = db.query(MeasurementFloatValue).all()
    return measurement_float_values


def update_measurement_float_value_query(
    db: Session, id: int, measurement_float_value_data: dict[str, Any]
) -> MeasurementFloatValue:
    """Update a measurement_float_value in the database.

    Args:
        db: Database session.
        id: id of the measurement_float_value to be updated.
        measurement_float_value_data: values to be updated in the database.

    Returns:
        The updated measurement_float_value.
    """
    measurement_float_value = (
        db.query(MeasurementFloatValue).filter(MeasurementFloatValue.id == id).first()
    )
    for key, value in measurement_float_value_data.items():
        setattr(measurement_float_value, key, value)
    db.commit()
    return measurement_float_value


def delete_measurement_float_value_query(
    db: Session, measurement_float_value_id: int
) -> None:
    """Delete a measurement_float_value from the database.

    Args:
        db: Database session.
        measurement_float_value_id: id of the measurement_float_value to be deleted.
    """
    measurement_float_value = (
        db.query(MeasurementFloatValue)
        .filter(MeasurementFloatValue.id == measurement_float_value_id)
        .first()
    )
    db.delete(measurement_float_value)
    db.commit()
