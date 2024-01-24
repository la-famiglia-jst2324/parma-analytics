"""A test module for the EmailService class."""
import unittest
from unittest.mock import MagicMock, patch

from parma_analytics.reporting.gmail.email_service import EmailService


class TestEmailService(unittest.TestCase):
    """A test case class for testing the EmailService class."""

    def test_send_report_email(self):
        """Test the send_report_email function."""
        with patch(
            "parma_analytics.reporting.gmail.email_service.EmailService"
        ) as mock_email_service, patch(
            "parma_analytics.reporting.gmail.email_service.EmailService._get_user_emails"
        ) as mock_get_user_emails, patch(
            "parma_analytics.reporting.gmail.email_service.EmailService._send_email"
        ) as mock_send_email, patch(
            "parma_analytics.db.prod.engine.get_engine"
        ) as mock_get_engine:
            magic_engine = MagicMock()
            mock_get_engine.return_value = magic_engine
            mock_get_user_emails.return_value = ["example@gmail.com"]
            mock_send_email.return_value = None

            result = EmailService.send_report_email(mock_email_service, "test")
            assert result is None

    def test_send_notification_email(self):
        """Test the send_notification_email function."""
        with patch(
            "parma_analytics.reporting.gmail.email_service.EmailService"
        ) as mock_email_service, patch(
            "parma_analytics.reporting.gmail.email_service.EmailService._get_user_emails"
        ) as mock_get_user_emails, patch(
            "parma_analytics.reporting.gmail.email_service.EmailService._send_email"
        ) as mock_send_email, patch(
            "parma_analytics.db.prod.engine.get_engine"
        ) as mock_get_engine:
            magic_engine = MagicMock()
            mock_get_engine.return_value = magic_engine
            mock_get_user_emails.return_value = ["example@gmail.com"]
            mock_send_email.return_value = None
            result = EmailService.send_notification_email(mock_email_service, "test")
            assert result is None
