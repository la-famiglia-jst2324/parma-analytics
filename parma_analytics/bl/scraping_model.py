"""Model for Scraping Payload."""
from pydantic import BaseModel


class ScrapingPayloadModel(BaseModel):
    """Model for Scraping Payload."""

    task_id: int
    companies: dict[str, dict[str, list[str]]] | None
