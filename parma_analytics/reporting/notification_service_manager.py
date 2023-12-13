from typing import Literal

from .db_operations import (
    fetch_channel_ids,
    fetch_company_id_from_bucket,
    fetch_notification_destinations,
    fetch_user_ids_for_company,
)

Category = Literal["company", "bucket"]
MessageType = Literal["notification", "report"]
ServiceType = Literal["email", "slack"]


class NotificationServiceManager:
    def __init__(
        self,
        company_or_bucket_id: int,
        subscription_table: str,
        entity_type: MessageType,
        service_type: ServiceType,
        category: Category,
    ):
        self.company_or_bucket_id = company_or_bucket_id
        self.subscription_table = subscription_table
        self.entity_type: MessageType = entity_type
        self.service_type: ServiceType = service_type
        self.category: Category = category

    def get_notification_destinations(self) -> list[str]:
        company_id = self.company_or_bucket_id
        # if the category is a bucket, get a company_id from the bucket. Assume that every company in the bucket is subscribed by the user.
        if self.category == "bucket":
            company_id = fetch_company_id_from_bucket(self.company_or_bucket_id)
        user_ids = fetch_user_ids_for_company(company_id)
        channel_ids = fetch_channel_ids(user_ids, self.subscription_table)
        return fetch_notification_destinations(
            channel_ids, self.entity_type, self.service_type
        )
