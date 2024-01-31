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


def create_notification_rule(engine: Engine, rules_param):
    """Create notification rules."""
    with Session(engine) as session:
        new_rule = NotificationRules(
            rule_name=rules_param["rule_name"],
            source_measurement_id=rules_param["source_measurement_id"],
            threshold=rules_param["threshold"],
            aggregation_method=rules_param["aggregation_method"],
            num_aggregation_entries=rules_param["num_aggregation_entries"],
            notification_message=rules_param["notification_message"],
        )
        session.add(new_rule)
        session.commit()
