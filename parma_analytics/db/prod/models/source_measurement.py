"""Database ORM models for source_measurement table."""

from datetime import datetime

from pydantic import BaseModel


class SourceMeasurement(BaseModel):
    """Model for the source_measurement table in the database."""

    __tablename__ = "source_measurement"

    id: int
    type: str
    measurement_name: str
    source_module_id: int
    parent_measurement_id: int | None
    created_at: datetime
    modified_at: datetime
