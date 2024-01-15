"""Module for managing notification service."""
# ruff: noqa: PLR0913

from typing import Literal

from .db_operations import (
    fetch_channel_ids,
    fetch_notification_destinations,
    fetch_user_ids_for_company,
)

Category = Literal["company", "bucket"]
ServiceType = Literal["email", "slack"]


class NotificationServiceManager:
    """Class for managing notification."""

    def __init__(
        self,
        company_id: int,
        subscription_table: str,
        service_type: ServiceType,
        category: Category,
    ):
        self.company_id = company_id
        self.subscription_table = subscription_table
        self.service_type = service_type
        self.category = category

    def get_notification_destinations(self) -> list[str]:
        """Get the notification destinations for the given company or bucket ID."""
        company_id = self.company_id
        user_ids = fetch_user_ids_for_company(company_id)
        channel_ids = fetch_channel_ids(user_ids=user_ids)
        return fetch_notification_destinations(channel_ids, self.service_type)
