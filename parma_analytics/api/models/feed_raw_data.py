"""Example of a model for the API."""

from pydantic import BaseModel
from datetime import datetime

# ------------------------------------------------------------------------------------ #
#                                       Internal                                       #
# ------------------------------------------------------------------------------------ #


class _ApiFeedRawDataBase(BaseModel):
    """Internal base model for the raw data endpoints."""

    source_name: str
    raw_data: dict


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

    pass
