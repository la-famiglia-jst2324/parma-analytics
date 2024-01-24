"""A test module for the SlackService class."""
import unittest
from unittest.mock import MagicMock, patch

from parma_analytics.reporting.slack.send_slack_messages import SlackService


class TestSlackService(unittest.TestCase):
    """A test case class for testing the SlackService class."""

    def test_send_report(self):
        """Test the send_report function."""
        with patch(
            "parma_analytics.reporting.slack.send_slack_messages.SlackService"
        ) as mock_slack_service, patch(
            "parma_analytics.db.prod.engine.get_engine"
        ) as mock_get_engine, patch(
            "parma_analytics.reporting.slack.send_slack_messages."
            "SlackService._send_message_to_user"
        ) as mock_send_message_to_user:
            magic_engine = MagicMock()
            mock_get_engine.return_value = magic_engine
            mock_send_message_to_user.return_value = None

            result = SlackService.send_report(
                mock_slack_service, user_id=1, content="test"
            )
            assert result is None

    def test_send_notification(self):
        """Test the send_notification function."""
        with patch(
            "parma_analytics.reporting.slack.send_slack_messages.SlackService"
        ) as mock_slack_service, patch(
            "parma_analytics.db.prod.engine.get_engine"
        ) as mock_get_engine, patch(
            "parma_analytics.reporting.slack.send_slack_messages."
            "SlackService._send_message_to_user"
        ) as mock_send_message_to_user:
            magic_engine = MagicMock()
            mock_get_engine.return_value = magic_engine
            mock_send_message_to_user.return_value = None

            result = SlackService.send_notification(
                mock_slack_service, user_id=1, content="test"
            )
            assert result is None
