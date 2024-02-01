"""Script to populate notiification rule."""
import json

from parma_analytics.db.prod.data_source_query import get_all_data_source
from parma_analytics.db.prod.engine import get_engine
from parma_analytics.db.prod.notification_rules_query import create_notification_rule
from parma_analytics.db.prod.source_measurement_query import (
    get_source_measurement_from_source_module,
)


class NotificationRule:
    """Notification Rules parameters."""

    rule_name: str
    source_measurement_id: int
    threshold: float
    aggregation_method: str
    num_aggregation_entries: int
    notification_message: str


def populate_notification_rules():
    """Function to update notification Rules."""
    with open("parma_analytics/db/source_measurement_rules.json") as file:
        source_measurement_rules = json.load(file)

    source_modules = get_all_data_source(get_engine())
    for source_module in source_modules:
        source_name = source_module.source_name.lower()
        if source_name in source_measurement_rules:
            rules = source_measurement_rules[source_name]
            source_measurements = get_source_measurement_from_source_module(
                get_engine(), source_module.id
            )
            for source_measurement in source_measurements:
                for rule in rules:
                    if (
                        source_measurement.measurement_name.lower()
                        == rule["measurement_name"].lower()
                    ):
                        rules_param = {
                            "rule_name": rule["rule_name"],
                            "threshold": rule["threshold"],
                            "source_measurement_id": source_measurement.id,
                            "aggregation_method": rule["aggregation_method"],
                            "num_aggregation_entries": rule["num_aggregation_entries"],
                            "notification_message": rule["notification_message"],
                        }
                        create_notification_rule(get_engine(), rules_param)
                        break
