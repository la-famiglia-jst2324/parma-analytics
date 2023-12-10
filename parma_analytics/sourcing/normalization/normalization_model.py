from pydantic import BaseModel, Field
from typing import Any
from datetime import datetime


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

    class Config:
        schema_extra = {
            "example": {
                "source_measurement_id": "GH001",
                "timeStamp": "2023-01-01T00:00:00Z",
                "company_id": "123",
                "value": "Langfuse",
                "type": "text",
            }
        }
