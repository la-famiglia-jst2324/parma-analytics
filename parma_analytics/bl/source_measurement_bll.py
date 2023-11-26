# source_measurement_bll.py
from parma_analytics.api.models.source_measurement import (
    ApiSourceMeasurementCreateIn,
    ApiSourceMeasurementCreateOut,
    ApiSourceMeasurementUpdateIn,
)

from parma_analytics.db.prod.source_measurement_orm import (
    create_source_measurement_orm,
    get_source_measurement_orm,
    list_source_measurements_orm,
    update_source_measurement_orm,
    delete_source_measurement_orm,
)

from sqlalchemy.orm import Session


def create_source_measurement_bll(
    db: Session,
    source_measurement: ApiSourceMeasurementCreateIn,
) -> ApiSourceMeasurementCreateOut:
    """Business logic function for creating a SourceMeasurement.

    Args:
        engine: The database engine.
        source_measurement: The SourceMeasurement object to create.

    Returns:
        the created source measurement.
    """
    return create_source_measurement_orm(db, source_measurement)


def read_source_measurement_bll(db: Session, source_measurement_id: int):
    """Business logic function for reading a SourceMeasurement.

    Args:
        engine: The database engine.
        source_measurement_id: The ID of the SourceMeasurement to read.

    Returns:
        The requested SourceMeasurement.
    """
    return get_source_measurement_orm(db, source_measurement_id)


def update_source_measurement_bll(
    db: Session,
    source_measurement: ApiSourceMeasurementUpdateIn,
):
    """Business logic function for updating a SourceMeasurement.

    Args:
        engine: The database engine.
        source_measurement_id: The ID of the SourceMeasurement to update.
        source_measurement: The new SourceMeasurement data.

    Returns:
        The updated SourceMeasurement.
    """
    return update_source_measurement_orm(db, source_measurement)


def delete_source_measurement_bll(db: Session, source_measurement_id: int):
    """Business logic function for deleting a SourceMeasurement.

    Args:
        engine: The database engine.
        source_measurement_id: The ID of the SourceMeasurement to delete.
    """
    delete_source_measurement_orm(db, source_measurement_id)


def list_source_measurements_bll(db: Session, page: int, page_size: int):
    """Business logic function for listing all SourceMeasurements.

    Args:
        engine: The database engine.
        page: The page number.
        page_size: The number of items per page.

    Returns:
        A paginated list of source measurements.
    """
    # Perform any necessary business logic operations here
    # Then, call the function from your data access layer to fetch the list of SourceMeasurements from the database
    return list_source_measurements_orm(db, page=page, page_size=page_size)
