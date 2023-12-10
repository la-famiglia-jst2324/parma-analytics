from sqlalchemy import text
from sqlalchemy.orm import Session
from dataclasses import dataclass

from pydantic import BaseModel, validator


class SourceMeasurement(BaseModel):
    id: int
    type: str
    measurement_name: str
    source_module_id: int
    parent_measurement_id: int
    created_at: str
    modified_at: str

    @validator("created_at", "modified_at", pre=True)
    def format_datetime(cls, value) -> str:
        return value.strftime("%Y-%m-%d %H:%M:%S")


@dataclass
class MeasurementPaginationResult:
    measurements_list: list[SourceMeasurement]
    num_pages: int


def create_source_measurement_query(db: Session, source_measurement_data) -> int:
    source_measurement_data = mapping_list(source_measurement_data)
    query = text(
        """INSERT INTO source_measurement (type, measurement_name, source_module_id, parent_measurement_id, created_at, modified_at)
                    VALUES (:type, :measurement_name, :source_module_id, :company_id, NOW(), NOW()) RETURNING *"""
    )
    result = db.execute(query, source_measurement_data)
    db.commit()
    new_source_measurement = result.fetchone()
    new_source_measurement_dict = new_source_measurement._asdict()
    return new_source_measurement_dict["id"]


def get_source_measurement_query(
    db: Session, source_measurement_id
) -> SourceMeasurement:
    query = text(
        """SELECT id, type, measurement_name, source_module_id, parent_measurement_id, created_at, modified_at
                 FROM source_measurement WHERE id = :id"""
    )
    result = db.execute(query, {"id": source_measurement_id})
    source_measurement = result.fetchone()
    source_measurement_dict = source_measurement._asdict()
    return SourceMeasurement(**source_measurement_dict)


def list_source_measurements_query(
    db: Session, *, page: int, page_size: int
) -> MeasurementPaginationResult:
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
    db: Session, id: int, source_measurement_data
) -> SourceMeasurement:
    source_measurement_data = mapping_list(source_measurement_data)
    # create a list of "column = :value" strings for each item in source_measurement_data
    set_clause = ", ".join(f"{key} = :{key}" for key in source_measurement_data.keys())
    query = text(
        f"""UPDATE source_measurement SET {set_clause}, modified_at = NOW() WHERE id = :id RETURNING *"""
    )
    source_measurement_data["id"] = str(id)
    result = db.execute(query, source_measurement_data)
    db.commit()
    updated_measurement = result.fetchone()
    updated_measurement_dict = updated_measurement._asdict()
    return SourceMeasurement(**updated_measurement_dict)


def delete_source_measurement_query(db: Session, source_measurement_id) -> None:
    query = text("""DELETE FROM source_measurement WHERE id = :id""")
    db.execute(query, {"id": source_measurement_id})
    db.commit()


def mapping_list(source_measurement_data):
    return {k: v for k, v in source_measurement_data if v is not None}
