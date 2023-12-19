"""Database queries for the source_measurement table."""

from dataclasses import dataclass
from typing import Any

from sqlalchemy import text
from sqlalchemy.orm import Session

from parma_analytics.db.prod.models.source_measurement import SourceMeasurement


@dataclass
class MeasurementPaginationResult:
    """Dataclass for the pagination results of a measurement query."""

    measurements_list: list[SourceMeasurement]
    num_pages: int


def create_source_measurement_query(
    db: Session, source_measurement_data: dict[str, Any]
) -> int:
    """Create a new source_measurement in the database.

    Args:
        db: Database session.
        source_measurement_data: values to be inserted in the database.

    Returns:
        The id of the newly created source_measurement.
    """
    source_measurement_data = _mapping_list(source_measurement_data)

    # Ensure parent_measurement_id is in the dictionary
    if "parent_measurement_id" not in source_measurement_data:
        source_measurement_data["parent_measurement_id"] = None

    query = text(
        """
        INSERT INTO source_measurement (
            type, measurement_name, source_module_id, parent_measurement_id,
            created_at, modified_at
        ) VALUES (
            :type, :measurement_name, :source_module_id, :parent_measurement_id,
            NOW(), NOW()
        ) RETURNING *
        """
    )
    result = db.execute(query, source_measurement_data)
    db.commit()
    new_source_measurement = result.fetchone()
    new_source_measurement_dict = new_source_measurement._asdict()
    return new_source_measurement_dict["id"]


def get_source_measurement_query(
    db: Session, source_measurement_id: int
) -> SourceMeasurement:
    """Get a source_measurement from the database.

    Args:
        db: Database session.
        source_measurement_id: id of the source_measurement to be retrieved.

    Returns:
        The source_measurement with the given id.
    """
    query = text(
        "SELECT id, type, measurement_name, source_module_id, parent_measurement_id, "
        "created_at, modified_at "
        "FROM source_measurement WHERE id = :id"
    )
    result = db.execute(query, {"id": source_measurement_id})
    source_measurement = result.fetchone()
    source_measurement_dict = source_measurement._asdict()
    return SourceMeasurement(**source_measurement_dict)


def list_source_measurements_query(
    db: Session, *, page: int, page_size: int
) -> MeasurementPaginationResult:
    """List all source_measurements from the database.

    Args:
        db: Database session.
        page: Page number.
        page_size: Number of records per page.

    Returns:
        A list of all source_measurements.
    """
    # Get the total number of records
    count_query = text("""SELECT COUNT(*) FROM source_measurement""")
    count_result = db.execute(count_query)
    total_records = count_result.scalar()

    # Calculate the total number of pages
    num_pages = (total_records + page_size - 1) // page_size
    page = max(1, min(page, num_pages))

    query = text("""SELECT * FROM source_measurement LIMIT :limit OFFSET :offset""")
    result = db.execute(query, {"limit": page_size, "offset": (page - 1) * page_size})
    source_measurements = result.fetchall()
    source_measurement_models = [
        SourceMeasurement(**source_measurement._asdict())
        for source_measurement in source_measurements
    ]
    return MeasurementPaginationResult(
        measurements_list=source_measurement_models, num_pages=num_pages
    )


def update_source_measurement_query(
    db: Session, id: int, source_measurement_data: dict[str, Any]
) -> SourceMeasurement:
    """Update a source_measurement in the database.

    Args:
        db: Database session.
        id: id of the source_measurement to be updated.
        source_measurement_data: values to be updated in the database.

    Returns:
        The updated source_measurement.
    """
    source_measurement_data = _mapping_list(source_measurement_data)
    # create list of "column = :value" strings for each item in source_measurement_data
    set_clause = ", ".join(f"{key} = :{key}" for key in source_measurement_data.keys())
    query = text(
        f"""UPDATE source_measurement SET {set_clause}, modified_at = NOW() "
        "WHERE id = :id RETURNING *"""
    )
    source_measurement_data["id"] = str(id)
    result = db.execute(query, source_measurement_data)
    db.commit()
    updated_measurement = result.fetchone()
    updated_measurement_dict = updated_measurement._asdict()
    return SourceMeasurement(**updated_measurement_dict)


def delete_source_measurement_query(db: Session, source_measurement_id: int) -> None:
    """Delete a source_measurement from the database.

    Args:
        db: Database session.
        source_measurement_id: id of the source_measurement to be deleted.
    """
    query = text("""DELETE FROM source_measurement WHERE id = :id""")
    db.execute(query, {"id": source_measurement_id})
    db.commit()


# ------------------------------------- Internal ------------------------------------- #


def _mapping_list(source_measurement_data) -> dict[str, Any]:
    return {k: v for k, v in source_measurement_data if v is not None}
