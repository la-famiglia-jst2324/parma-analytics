from unittest.mock import MagicMock, patch

import pytest
from sqlalchemy.orm import Session

from parma_analytics.db.prod.models.notification_rules import NotificationRules
from parma_analytics.db.prod.notification_rules_query import (
    get_notification_rules_by_source_measurement_id,
)


@pytest.fixture
def mock_db():
    return MagicMock(spec=Session)


@pytest.fixture
def mock_notification_rules():
    return MagicMock(spec=NotificationRules)


@patch("parma_analytics.db.prod.notification_rules_query.Session", autospec=True)
def test_get_notification_rules_by_source_measurement_id(mock_session, mock_db):
    # Define mock_notification_rules for a specific scenario
    mock_notification_rules_scenario1 = MagicMock(spec=NotificationRules)
    mock_notification_rules_scenario1.threshold = 10.0

    # Customize the behavior of mock_session to return the mock_notification_rules
    query_scenario1 = (
        mock_session.return_value.__enter__.return_value.query.return_value
    )
    filter_scenario1 = query_scenario1.filter.return_value
    filter_scenario1.first.return_value = mock_notification_rules_scenario1

    # Test scenario 1 with source_measurement_id 1
    result_scenario1 = get_notification_rules_by_source_measurement_id(
        mock_db, source_measurement_id=1
    )
    threshold = 10.0
    assert result_scenario1.threshold == threshold

    # Define mock_notification_rules for another scenario
    mock_notification_rules_scenario2 = MagicMock(spec=NotificationRules)
    mock_notification_rules_scenario2.threshold = 20.0

    # Customize the behavior of mock_session to return
    # a different mock_notification_rules for scenario 2
    query_scenario2 = (
        mock_session.return_value.__enter__.return_value.query.return_value
    )
    filter_scenario2 = query_scenario2.filter.return_value
    filter_scenario2.first.return_value = mock_notification_rules_scenario2
    # Test scenario 2 with source_measurement_id 2
    result_scenario2 = get_notification_rules_by_source_measurement_id(
        mock_db, source_measurement_id=2
    )
    threshold = 20.0
    assert result_scenario2.threshold == threshold
