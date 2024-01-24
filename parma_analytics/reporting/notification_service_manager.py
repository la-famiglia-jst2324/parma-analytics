"""Module for managing notification service."""
# ruff: noqa: PLR0913

from typing import Literal

from parma_analytics.db.prod.engine import get_engine
from parma_analytics.db.prod.reporting import (
    fetch_channel_ids,
    fetch_notification_destinations,
    fetch_slack_destinations,
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

    def get_slack_key_and_destinations(self):
        """Get the slack key and destinations for the given company or bucket ID."""
        user_ids = [self.user_id]
        channel_ids = fetch_channel_ids(get_engine(), user_ids=user_ids)
        destinations_and_secret_ids = fetch_slack_destinations(
            get_engine(), channel_ids
        )
        return destinations_and_secret_ids


notification_service_manager = NotificationServiceManager("slack", 1)
notification_service_manager.get_slack_key_and_destinations()
