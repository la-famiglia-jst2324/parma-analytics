from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class NormalizedData(BaseModel):
    source_measurement_id: int = Field(
        ..., description="Unique identifier for the source measurement"
    )
    timestamp: datetime = Field(
        ..., description="Timestamp when the data was retrieved or processed"
    )
    company_id: int = Field(..., description="Identifier for the company")
    value: Any = Field(..., description="The actual value of the data point")
    type: str = Field(..., description="Data type of the value")
