"""Database queries for the source_measurement table."""

from pathlib import Path

from sqlalchemy import Engine
from sqlalchemy.orm.session import Session

from parma_analytics.db.prod.models.source_measurement import SourceMeasurement
from parma_analytics.db.prod.utils.paginate import (
    ListPaginationResult,
    paginate,
    paginate_query,
)

QUERIES_DIR = Path(__file__).parent / "queries"


def create_source_measurement_query(
    engine: Engine,
    source_measurement: SourceMeasurement,
) -> SourceMeasurement:
    """Create a new source_measurement in the database.

    Args:
        engine: Database engine.
        source_measurement: values to be inserted in the database.

    Returns:
        The newly created source_measurement.
    """
    assert (
        source_measurement.id is None
        and source_measurement.created_at is None
        and source_measurement.modified_at is None
    )
    with Session(engine) as session:
        session.add(source_measurement)
        session.commit()
        session.refresh(source_measurement)
        return source_measurement


def get_source_measurement_query(
    engine: Engine, source_measurement_id: int
) -> SourceMeasurement:
    """Get a source_measurement from the database.

    Args:
        engine: Database engine.
        source_measurement_id: id of the source_measurement to be retrieved.

    Returns:
        The source_measurement with the given id.
    """
    with Session(engine) as session:
        return session.get_one(SourceMeasurement, source_measurement_id)


@paginate(default_page_size=100)
def list_source_measurements_query(
    engine: Engine, *, page: int, page_size: int
) -> ListPaginationResult[SourceMeasurement]:
    """List all source_measurements from the database.

    Args:
        engine: Database engine.
        page: Page number.
        page_size: Number of records per page.

    Returns:
        The paginated result list.
    """
    with Session(engine) as session:
        return paginate_query(
            session.query(SourceMeasurement), page=page, page_size=page_size
        )


def delete_source_measurement_query(engine: Engine, source_measurement_id: int) -> None:
    """Delete a source_measurement from the database.

    Args:
        engine: Database engine.
        source_measurement_id: id of the source_measurement to be deleted.
    """
    with Session(engine) as session:
        session.delete(session.get_one(SourceMeasurement, source_measurement_id))
        session.commit()
