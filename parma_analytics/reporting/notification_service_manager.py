"""Module for managing notification service."""
# ruff: noqa: PLR0913

from typing import Literal

from parma_analytics.db.prod.engine import get_engine
from parma_analytics.db.prod.reporting import (
    fetch_channel_ids,
    fetch_notification_destinations,
    fetch_user_ids_for_company,
)

ServiceType = Literal["email", "slack"]


class NotificationServiceManager:
    """Class for managing notification."""

    def __init__(self, company_id: int, service_type: ServiceType):
        self.company_id = company_id
        self.service_type = service_type

    def get_notification_destinations(self) -> list[str]:
        """Get the notification destinations for the given company or bucket ID."""
        company_id = self.company_id
        user_ids = fetch_user_ids_for_company(get_engine(), company_id)
        channel_ids = fetch_channel_ids(get_engine(), user_ids=user_ids)
        return fetch_notification_destinations(
            get_engine(), channel_ids, self.service_type
        )
