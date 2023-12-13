from typing import List
from .db_operations import (
    fetch_user_ids_for_company,
    fetch_channel_ids,
    fetch_notification_destinations,
    fetch_company_id_from_bucket,
)
from enum import Enum


class Category(Enum):
    COMPANY = "COMPANY"
    BUCKET = "BUCKET"


class MessageType(Enum):
    NOTIFICATION = "NOTIFICATION"
    REPORT = "REPORT"


class ServiceType(Enum):
    EMAIL = "EMAIL"
    SLACK = "SLACK"


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

    def get_notification_destinations(self) -> List[str]:
        company_id = self.company_or_bucket_id
        # if the category is a bucket, get a company_id from the bucket. Assume that every company in the bucket is subscribed by the user.
        if self.category == Category.BUCKET:
            company_id = fetch_company_id_from_bucket(self.company_or_bucket_id)
        user_ids = fetch_user_ids_for_company(company_id)
        channel_ids = fetch_channel_ids(user_ids, self.subscription_table)
        return fetch_notification_destinations(
            channel_ids, self.entity_type.value, self.service_type.value
        )
