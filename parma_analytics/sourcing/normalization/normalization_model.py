from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class NormalizedData(BaseModel):
    source_measurement_id: str = Field(
        ..., description="Unique identifier for the source measurement"
    )
    timeStamp: datetime = Field(
        ..., description="Timestamp when the data was retrieved or processed"
    )
    company_id: str = Field(..., description="Identifier for the company")
    value: Any = Field(..., description="The actual value of the data point")
    type: str = Field(..., description="Data type of the value")
