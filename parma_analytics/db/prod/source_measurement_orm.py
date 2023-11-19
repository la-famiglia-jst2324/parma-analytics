from typing import Optional
from sqlalchemy.engine import Engine
from sqlalchemy.orm.session import Session

from parma_analytics.db.prod.models.source_measurement_db import DbSourceMeasurement
from parma_analytics.db.prod.utils.paginate import (
    ListPaginationResult,
    paginate,
    paginate_query,
)

# ------------------------------------------------------------------------------------ #
#                                      ORM Queries                                     #
# ------------------------------------------------------------------------------------ #


def create_source_measurement_orm(
    engine: Engine, source_measurement_data
) -> DbSourceMeasurement:
    """Create a source measurement.

    Args:
        engine: The database engine.
        source_measurement_data: Data for creating the source measurement.

    Returns:
        The created source measurement.
    """
    with Session(engine) as session:
        db_source_measurement = DbSourceMeasurement(**source_measurement_data)
        session.add(db_source_measurement)
        session.commit()
        session.refresh(db_source_measurement)
        return db_source_measurement


def get_source_measurement_orm(
    engine: Engine, source_measurement_id
) -> DbSourceMeasurement | None:
    """Get a source measurement by its ID.

    Args:
        engine: The database engine.
        source_measurement_id: The ID of the source measurement.

    Returns:
        The source measurement if it exists, otherwise None.
    """
    with Session(engine) as session:
        return session.get(DbSourceMeasurement, source_measurement_id)


@paginate(default_page_size=5)
def list_source_measurements_orm(
    engine: Engine, *, page: Optional[int], page_size: Optional[int]
) -> ListPaginationResult[DbSourceMeasurement]:
    """List all source measurements.

    Args:
        engine: The database engine.
        page: The page number.
        page_size: The number of items per page.

    Returns:
        A paginated list of source measurements.
    """
    with Session(engine) as session:
        query = session.query(DbSourceMeasurement)
        if page is not None and page_size is not None:
            return paginate_query(query, page=page, page_size=page_size)
        return paginate_query(query, page=100, page_size=100)


def update_source_measurement_orm(
    engine: Engine, source_measurement_id, source_measurement_data
) -> DbSourceMeasurement:
    """Update a source measurement.

    Args:
        engine: The database engine.
        source_measurement_id: The ID of the source measurement to update.
        source_measurement_data: Updated data for the source measurement.

    Returns:
        The updated source measurement.
    """
    with Session(engine) as session:
        db_source_measurement = session.get(DbSourceMeasurement, source_measurement_id)
        for key, value in source_measurement_data.items():
            setattr(db_source_measurement, key, value)
        session.commit()
        session.refresh(db_source_measurement)
        return db_source_measurement


def delete_source_measurement_orm(
    engine: Engine, source_measurement_id
) -> DbSourceMeasurement:
    """Delete a source measurement.

    Args:
        engine: The database engine.
        source_measurement_id: The ID of the source measurement to delete.
    Returns:
        The deleted source measurement.
    """

    with Session(engine) as session:
        db_source_measurement = session.get(DbSourceMeasurement, source_measurement_id)
        session.delete(db_source_measurement)
        session.commit()
        return db_source_measurement
