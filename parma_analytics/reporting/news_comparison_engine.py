"""This module provides the functionality for comparing notification rules.

It includes functions for checking notification rules based on measurement data,
comparing measurement values against set thresholds, creating news items, retrieving
data source IDs, and determining the appropriate measurement value table based on the
type of source measurement.
"""

from datetime import datetime
from typing import Any

from pydantic import BaseModel

from parma_analytics.api.models.news import NewsCreate
from parma_analytics.db.prod.aggregation_queries import (
    IncomingData,
    apply_aggregation_method,
    get_most_recent_measurement_values,
)
from parma_analytics.db.prod.engine import get_engine
from parma_analytics.db.prod.models.company_source_measurement import CompanyMeasurement
from parma_analytics.db.prod.models.measurement_value_models import (
    MeasurementCommentValue,
    MeasurementDateValue,
    MeasurementFloatValue,
    MeasurementImageValue,
    MeasurementIntValue,
    MeasurementLinkValue,
    MeasurementNestedValue,
    MeasurementParagraphValue,
    MeasurementTextValue,
)
from parma_analytics.db.prod.models.news import News
from parma_analytics.db.prod.news import create_news_query
from parma_analytics.db.prod.notification_rules_query import (
    get_notification_rules_by_source_measurement_id,
)
from parma_analytics.db.prod.source_measurement_query import (
    get_source_measurement_query,
)
from parma_analytics.reporting.notification_rule_helper import compare_to_threshold


# NewsComparisonEngineReturn
class NewsComparisonEngineReturn(BaseModel):
    """Represents the return object of the NewsComparisonEngine.

    Attributes:
        threshold (Optional[float]): The threshold value used for comparison.
        is_rules_satisfied (bool): Indicates whether the comparison rules are satisfied.
        is_aggregated (bool): Indicates whether the values are aggregated.
        aggregation_method (Optional[str]): The method used for aggregation.
        previous_value (Optional[float]): The aggregated value.
        num_aggregation_entries (Optional[int]): # of entries used for aggregation.
        percentage_difference (Optional[float]): % difference between values.
    """

    threshold: float | None = None
    is_rules_satisfied: bool = False
    is_aggregated: bool = False
    aggregation_method: str | None = None
    previous_value: float | None = None
    num_aggregation_entries: int | None = None
    percentage_difference: float | None = None


def check_notification_rules(
    source_measurement_id: int,
    value: Any,
    timestamp: datetime,
    measurement_type: str,
    company_measurement: CompanyMeasurement,
) -> NewsComparisonEngineReturn:
    """Check the notification rules for a given measurement value.

    Args:
        source_measurement_id (int): The ID of the source measurement.
        company_id (int): The ID of the company.
        value (Any): The measurement value.
        timestamp (datetime): The timestamp of the value.
        measurement_type (str): The type of the measurement.
        company_measurement (CompanyMeasurement): The company measurement object.

    Returns:
        NewsComparisonEngineReturn: An object containing the threshold
        and whether the rules are satisfied.
    """
    measurement_type = measurement_type.lower()
    data_table = get_measurement_value_table(measurement_type)
    company_measurement_id = company_measurement.company_measurement_id

    # Contains measurement types for which we want to ignore changes
    if measurement_type not in ["int", "float", "comment", "link", "date"]:
        previous_value = get_most_recent_measurement_values(
            get_engine(),
            data_table=data_table,
            timestamp=timestamp,
            company_measurement_id=company_measurement_id,
        )
        if previous_value != value:
            return NewsComparisonEngineReturn(threshold=None, is_rules_satisfied=True)
        return NewsComparisonEngineReturn(threshold=None, is_rules_satisfied=False)
    else:
        notification_rule = get_notification_rules_by_source_measurement_id(
            get_engine(), source_measurement_id=source_measurement_id
        )
        if notification_rule:
            threshold = (
                notification_rule.threshold
            )  # threshold is measured in PERCENTAGE
            aggregation_method = notification_rule.aggregation_method
            num_aggregation_entries = notification_rule.num_aggregation_entries

            previous_value = get_most_recent_measurement_values(
                get_engine(),
                data_table=data_table,
                timestamp=timestamp,
                company_measurement_id=company_measurement_id,
                notification_rule=notification_rule,
            )
            if aggregation_method is None and num_aggregation_entries is None:
                percentage_difference = compare_to_threshold(
                    previous_value, value, threshold
                )
                if percentage_difference >= 0:
                    return NewsComparisonEngineReturn(
                        threshold=threshold,
                        is_rules_satisfied=True,
                        is_aggregated=False,
                        percentage_difference=percentage_difference,
                        previous_value=previous_value,
                    )
            elif aggregation_method is not None and num_aggregation_entries is None:
                new_aggregated_value = apply_aggregation_method(
                    engine=get_engine(),
                    data_table=data_table,
                    incoming_data=IncomingData(
                        timestamp=timestamp,
                        value=value,
                        company_measurement_id=company_measurement_id,
                    ),
                    notification_rule=notification_rule,
                )
                percentage_difference = compare_to_threshold(
                    previous_value, new_aggregated_value, threshold
                )
                if percentage_difference >= 0:
                    return NewsComparisonEngineReturn(
                        threshold=threshold,
                        is_rules_satisfied=True,
                        is_aggregated=True,
                        aggregation_method=aggregation_method,
                        previous_value=new_aggregated_value,
                        percentage_difference=percentage_difference,
                    )
            elif aggregation_method is not None and num_aggregation_entries is not None:
                new_aggregated_value = apply_aggregation_method(
                    engine=get_engine(),
                    data_table=data_table,
                    incoming_data=IncomingData(
                        timestamp=timestamp,
                        value=value,
                        company_measurement_id=company_measurement_id,
                    ),
                    notification_rule=notification_rule,
                )
                percentage_difference = compare_to_threshold(
                    previous_value, new_aggregated_value, threshold
                )
                if percentage_difference >= 0:
                    return NewsComparisonEngineReturn(
                        threshold=threshold,
                        is_rules_satisfied=True,
                        is_aggregated=True,
                        aggregation_method=aggregation_method,
                        previous_value=new_aggregated_value,
                        num_aggregation_entries=num_aggregation_entries,
                        percentage_difference=percentage_difference,
                    )

    return NewsComparisonEngineReturn(threshold=threshold, is_rules_satisfied=False)


def create_news(
    news_data: NewsCreate,
) -> News:
    """Creates a new News object with the given parameters.

    Args:
       news_data: The data for creating the news.

    Returns:
        News: The created News object.
    """
    return create_news_query(
        engine=get_engine(),
        news_data=news_data,
    )


def get_data_source_id(source_measurement_id: int) -> int:
    """Retrieves the data source ID associated with the given source measurement ID.

    Args:
        source_measurement_id (int): The ID of the source measurement.

    Returns:
        int: The data source ID associated with the source measurement.
    """
    source_measurement = get_source_measurement_query(
        get_engine(), source_measurement_id
    )
    return source_measurement.data_source_id


def get_measurement_value_table(source_measurement_type: str):
    """Returns the measurement value table based on the given source measurement type.

    Args:
        source_measurement_type (str): The type of the source measurement.

    Returns:
        MeasurementValue: The measurement value table
            corresponding to the source measurement type.
    """
    data_table = None
    match source_measurement_type.lower():
        case "paragraph":
            data_table = MeasurementParagraphValue
        case "int":
            data_table = MeasurementIntValue
        case "float":
            data_table = MeasurementFloatValue
        case "text":
            data_table = MeasurementTextValue
        case "comment":
            data_table = MeasurementCommentValue
        case "link":
            data_table = MeasurementLinkValue
        case "image":
            data_table = MeasurementImageValue
        case "date":
            data_table = MeasurementDateValue
        case "nested":
            data_table = MeasurementNestedValue

    return data_table
