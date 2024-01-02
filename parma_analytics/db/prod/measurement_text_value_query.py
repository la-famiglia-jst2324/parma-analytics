"""Database crud operations for measurement_text_value table."""

from sqlalchemy.orm import Session

from parma_analytics.db.prod.models.measurement_text_value import MeasurementTextValue


def create_measurement_text_value_query(
    db: Session, measurement_text_value_data
) -> int:
    """Create a new measurement_text_value in the database.

    Args:
        db: Database session.
        measurement_text_value_data: values to be inserted in the database.

    Returns:
        The id of the newly created measurement_text_value.
    """
    measurement_text_value = MeasurementTextValue(**measurement_text_value_data)
    db.add(measurement_text_value)
    db.commit()
    db.refresh(measurement_text_value)
    return measurement_text_value.id


def get_measurement_text_value_query(
    db: Session, measurement_text_value_id: int
) -> MeasurementTextValue:
    """Get a measurement_text_value from the database.

    Args:
        db: Database session.
        measurement_text_value_id: id of the measurement_text_value to be retrieved.

    Returns:
        The measurement_text_value with the given id.
    """
    return (
        db.query(MeasurementTextValue)
        .filter(MeasurementTextValue.id == measurement_text_value_id)
        .first()
    )


def list_measurement_text_values_query(db: Session) -> list:
    """List all measurement_text_values from the database.

    Args:
        db: Database session.

    Returns:
        A list of all measurement_text_values.
    """
    measurement_text_values = db.query(MeasurementTextValue).all()
    return measurement_text_values


def update_measurement_text_value_query(
    db: Session, id: int, measurement_text_value_data
) -> MeasurementTextValue:
    """Update a measurement_text_value in the database.

    Args:
        db: Database session.
        id: id of the measurement_text_value to be updated.
        measurement_text_value_data: values to be updated in the database.

    Returns:
        The updated measurement_text_value.
    """
    measurement_text_value = (
        db.query(MeasurementTextValue).filter(MeasurementTextValue.id == id).first()
    )
    for key, value in measurement_text_value_data.items():
        setattr(measurement_text_value, key, value)
    db.commit()
    return measurement_text_value


def delete_measurement_text_value_query(db: Session, measurement_text_value_id) -> None:
    """Delete a measurement_text_value from the database.

    Args:
        db: Database session.
        measurement_text_value_id: id of the measurement_text_value to be deleted.
    """
    measurement_text_value = (
        db.query(MeasurementTextValue)
        .filter(MeasurementTextValue.id == measurement_text_value_id)
        .first()
    )
    db.delete(measurement_text_value)
    db.commit()
