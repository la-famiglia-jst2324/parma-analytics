"""Database operations for the reporting service."""

from pathlib import Path

from parma_analytics.db.prod.queries.loader import read_query_file

from ..db.prod.engine import get_session

QUERIES_DIR = Path(__file__).parent.parent / "db" / "prod" / "queries"


def fetch_user_ids_for_company(company_id: int) -> list[int]:
    """Fetch user ids for a given company.

    Args:
        company_id: id of the company.

    Returns:
        A list of user ids.
    """
    with get_session() as db:
        result = db.execute(
            read_query_file(QUERIES_DIR / "fetch_user_ids_for_company.sql"),
            {"company_id": company_id},
        )
        return [row[0] for row in result.fetchall()]


def fetch_channel_ids(user_ids: list[int], subscription_table: str) -> list[int]:
    """Fetch channel ids for a given list of user ids.

    Args:
        user_ids: list of user ids.
        subscription_table: name of the subscription table.

    Returns:
        A list of channel ids.
    """
    with get_session() as db:
        result = db.execute(
            read_query_file(QUERIES_DIR / "fetch_channel_ids.sql"),
            {"subscription_table": subscription_table, "user_ids": tuple(user_ids)},
        )
        return [row[0] for row in result.fetchall()]


def fetch_notification_destinations(
    channel_ids: list[int], entity_type: str, service_type: str
) -> list[str]:
    """Fetch notification destinations for a given list of channel ids.

    Args:
        channel_ids: list of channel ids.
        entity_type: type of the entity.
        service_type: type of the service.

    Returns:
        A list of notification destinations.
    """
    with get_session() as db:
        result = db.execute(
            read_query_file(QUERIES_DIR / "fetch_notification_destinations.sql"),
            {
                "channel_ids": tuple(channel_ids),
                "entity_type": entity_type.upper(),
                "channel_type": service_type.upper(),
            },
        )
        return [row[0] for row in result.fetchall()]


def fetch_company_id_from_bucket(bucket_id: int) -> int:
    """Fetch company id for a given bucket id.

    Args:
        bucket_id: id of the bucket.

    Returns:
        A company id.
    """
    with get_session() as db:
        result = db.execute(
            read_query_file(QUERIES_DIR / "fetch_company_id_from_bucket.sql"),
            {"bucket_id": bucket_id},
        )

        # first company_id, since every company in the bucket is subscribed by the user
        return [row[0] for row in result.fetchall()][0]
