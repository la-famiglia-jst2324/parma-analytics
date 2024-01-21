"""Pydantic REST models for the notifications endpoint."""

from datetime import datetime

from pydantic import BaseModel

# ------------------------------------------------------------------------------------ #
#                                       Internal                                       #
# ------------------------------------------------------------------------------------ #


class _NewsBase(BaseModel):
    """Internal base model for the new company endpoints."""

    message: str
    company_id: int
    data_source_id: int
    trigger_factor: str | None = None
    title: str | None = None
    timestamp: datetime
    source_measurement_id: int


# ------------------------------------------------------------------------------------ #
#                                     Create Models                                    #
# ------------------------------------------------------------------------------------ #


class NewsCreate(_NewsBase):
    """Input model for the NewCompany creation endpoint."""

    pass


class NewsReturn(_NewsBase):
    """Return model for the NewCompany creation endpoint."""

    ID: int
