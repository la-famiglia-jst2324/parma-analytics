"""This module is for notification rules database operations.

It provides functions for fetching the rules.
"""
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from parma_analytics.db.prod.models.notification_rules import NotificationRules


def get_notification_rules_by_source_measurement_id(
    engine: Engine, source_measurement_id: int
) -> NotificationRules:
    """Fetch all notification rules for a given source measurement ID.

    Args:
        engine (Engine): The database engine.
        source_measurement_id (int): The ID of the source measurement to filter by

    Returns:
        NotificationRules: A NotificationRules that matches source measurement ID.
    """
    with Session(engine) as session:
        return (
            session.query(NotificationRules)
            .filter(NotificationRules.source_measurement_id == source_measurement_id)
            .first()
        )
