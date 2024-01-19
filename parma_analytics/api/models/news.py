"""Pydantic REST models for the notifications endpoint."""

from typing import Optional
from pydantic import BaseModel
from datetime import datetime

# ------------------------------------------------------------------------------------ #
#                                       Internal                                       #
# ------------------------------------------------------------------------------------ #


class _ApiNewsIn(BaseModel):
    """Internal base model for the new company endpoints."""

    id: int
    message: str
    company_id: int
    data_source_id: int
    trigger_factor: Optional[str] = None
    title: Optional[str] = None
    timestamp: datetime
    source_measurement_id: int
    
    
# ------------------------------------------------------------------------------------ #
#                                     Create Models                                    #
# ------------------------------------------------------------------------------------ #

class ApiNewsIn(_ApiNewsIn):
    """Input model for the NewCompany creation endpoint."""

    pass