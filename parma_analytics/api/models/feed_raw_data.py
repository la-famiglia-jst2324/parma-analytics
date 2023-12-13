"""Example of a model for the API."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel

# ------------------------------------------------------------------------------------ #
#                                       Internal                                       #
# ------------------------------------------------------------------------------------ #


class _ApiFeedRawDataBase(BaseModel):
    """Internal base model for the raw data endpoints."""

    source_name: str
    company_id: str
    raw_data: dict[str, Any]


class _ApiFeedRawDataOutBase(_ApiFeedRawDataBase):
    """Output base model for the several endpoint."""

    timestamp: datetime
    return_message: str


# ------------------------------------------------------------------------------------ #
#                                     Create Models                                    #
# ------------------------------------------------------------------------------------ #


class ApiFeedRawDataCreateIn(_ApiFeedRawDataBase):
    """Input model for the raw data creation endpoint."""

    pass


class ApiFeedRawDataCreateOut(_ApiFeedRawDataOutBase):
    """Output model for the raw data creation endpoint."""

    document_id: str
