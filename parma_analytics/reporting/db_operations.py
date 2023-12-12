from typing import List
from sqlalchemy.sql import text
from sqlalchemy.orm import Session
from parma_analytics.db.prod.engine import get_session


def fetch_user_ids_for_company(company_id: int) -> List[int]:
    db: Session = next(get_session())
    query = text(
        "SELECT DISTINCT user_id FROM company_subscription WHERE company_id = :company_id"
    )
    result = db.execute(query, {"company_id": company_id})
    return [row[0] for row in result.fetchall()]


def fetch_channel_ids(user_ids: List[int], subscription_table: str) -> List[int]:
    db: Session = next(get_session())
    query = text(
        f"SELECT channel_id FROM {subscription_table} WHERE user_id IN :user_ids"
    )
    result = db.execute(query, {"user_ids": tuple(user_ids)})
    return [row[0] for row in result.fetchall()]


def fetch_notification_destinations(
    channel_ids: List[int], entity_type: str, service_type: str
) -> List[str]:
    db: Session = next(get_session())
    query = text(
        f"SELECT destination FROM notification_channel WHERE id IN :channel_ids AND entity_type = :entity_type AND channel_type = :channel_type"
    )
    result = db.execute(
        query,
        {
            "channel_ids": tuple(channel_ids),
            "entity_type": entity_type,
            "channel_type": service_type,
        },
    )
    return [row[0] for row in result.fetchall()]


def fetch_company_id_from_bucket(bucket_id: int) -> int:
    db: Session = next(get_session())
    query = text(
        "SELECT company_id FROM company_bucket_membership WHERE id = :bucket_id"
    )
    result = db.execute(query, {"bucket_id": bucket_id})
    return result.fetchone()[0]
