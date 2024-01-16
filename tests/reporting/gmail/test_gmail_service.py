import unittest
from unittest.mock import MagicMock, patch

from parma_analytics.reporting.gmail.email_service import EmailService


class TestEmailService(unittest.TestCase):
    """A test case class for testing the EmailService class."""

    @patch("parma_analytics.reporting.gmail.email_service.SendGridAPIClient")
    @patch("parma_analytics.reporting.gmail.email_service.NotificationServiceManager")
    def test_send_notification_email(self, mock_service, mock_sendgrid):
        """Test case for send_notification_email of EmailService class."""
        # Setup
        mock_sendgrid.return_value.send = MagicMock()
        mock_service.return_value.get_notification_destinations.return_value = [
            "test@example.com"
        ]

        email_service = EmailService(company_id=123)
        content = "Test Content"
        company_name = "Test Company"
        company_logo = "https://example.com/logo.png"

        # Act
        email_service.send_notification_email(content, company_name, company_logo)

        # Assert
        mock_sendgrid.return_value.send.assert_called()
        # Here, add more asserts to validate the call arguments, etc.


if __name__ == "__main__":
    unittest.main()
