"""Module for managing notification service."""
# ruff: noqa: PLR0913

from typing import Literal

from parma_analytics.db.prod.engine import get_engine
from parma_analytics.db.prod.reporting import (
    fetch_channel_ids,
    fetch_notification_destinations,
)

ServiceType = Literal["email", "slack"]


class NotificationServiceManager:
    """Class for managing notification."""

    def __init__(self, service_type: ServiceType, user_id: int):
        self.service_type = service_type
        self.user_id = user_id

    def get_notification_destinations(self) -> list[str]:
        """Get the notification destinations for the given company or bucket ID."""
        user_ids = [self.user_id]
        channel_ids = fetch_channel_ids(get_engine(), user_ids=user_ids)
        return fetch_notification_destinations(
            get_engine(), channel_ids, self.service_type
        )
