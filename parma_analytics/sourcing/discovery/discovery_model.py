"""Discovery models."""
from datetime import datetime

from pydantic import BaseModel


class DiscoveryQueryData(BaseModel):
    """Model representing a query for discovering company data."""

    company_id: str
    name: str


class DiscoveryResponseModel(BaseModel):
    """Model representing discovery response data."""

    identifiers: dict[str, dict[str, list[str]]]
    validity: datetime
