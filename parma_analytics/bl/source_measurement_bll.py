"""Business logic layer for SourceMeasurement CRUD operations."""

from sqlalchemy.engine import Engine

from parma_analytics.api.models.source_measurement import (
    ApiSourceMeasurementCreateIn,
)
from parma_analytics.db.prod.source_measurement_query import (
    SourceMeasurement,
    create_source_measurement_query,
    delete_source_measurement_query,
    get_source_measurement_query,
    list_source_measurements_query,
)
from parma_analytics.db.prod.utils.paginate import ListPaginationResult


def create_source_measurement_bll(
    engine: Engine,
    source_measurement: ApiSourceMeasurementCreateIn,
) -> SourceMeasurement:
    """Business logic function for creating a SourceMeasurement.

    Args:
        engine: The database engine.
        source_measurement: The SourceMeasurement object to create.

    Returns:
        The created source measurement.
    """
    source_measurement_instance = SourceMeasurement(
        type=source_measurement.type,
        measurement_name=source_measurement.measurement_name,
        source_module_id=source_measurement.source_module_id,
        parent_measurement_id=source_measurement.parent_measurement_id,
    )
    return create_source_measurement_query(engine, source_measurement_instance)


def read_source_measurement_bll(
    engine: Engine, source_measurement_id: int
) -> SourceMeasurement:
    """Business logic function for reading a SourceMeasurement.

    Args:
        engine: The database engine.
        source_measurement_id: The ID of the SourceMeasurement to read.

    Returns:
        The requested SourceMeasurement.
    """
    return get_source_measurement_query(engine, source_measurement_id)


def delete_source_measurement_bll(engine: Engine, source_measurement_id: int) -> None:
    """Business logic function for deleting a SourceMeasurement.

    Args:
        engine: The database engine.
        source_measurement_id: The ID of the SourceMeasurement to delete.
    """
    delete_source_measurement_query(engine, source_measurement_id)


def list_source_measurements_bll(
    engine: Engine, page: int, page_size: int
) -> ListPaginationResult[SourceMeasurement]:
    """Business logic function for listing all SourceMeasurements.

    Args:
        engine: The database engine.
        page: The page number.
        page_size: The number of items per page.

    Returns:
        A paginated list of source measurements.
    """
    # Perform any necessary business logic operations here
    # Then, call the function from your data access layer to fetch the list of
    # SourceMeasurements from the database
    return list_source_measurements_query(engine, page=page, page_size=page_size)
