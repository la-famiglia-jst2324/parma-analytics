"""A service that handles the sending of emails."""
import logging
import os

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Mail,
)

from ..notification_service_manager import (
    NotificationServiceManager,
)

logger = logging.getLogger(__name__)


class EmailService:
    """A service that handles the sending of emails."""

    def __init__(self, user_id: int):
        self.sg: SendGridAPIClient = SendGridAPIClient(os.environ["SENDGRID_API_KEY"])
        self.notification_template_id: str | None = os.environ[
            "SENDGRID_NOTIFICATION_TEMPLATE_ID"
        ]
        self.report_template_id: str | None = os.environ["SENDGRID_REPORT_TEMPLATE_ID"]
        self.from_email: str | None = os.environ["SENDGRID_FROM_EMAIL"]
        self.user_id: int = user_id

    def _get_user_emails(self, user_id: int) -> list[str]:
        """Get all user emails for notification or report."""
        channel_manager = NotificationServiceManager(
            service_type="email", user_id=user_id
        )
        return channel_manager.get_notification_destinations()

    def _send_email(
        self,
        to_emails: list[str],
        template_id: str | None,
        dynamic_template_data: dict,
    ):
        """Generic function to send emails using SendGrid."""
        for email in to_emails:
            message = Mail(from_email=self.from_email, to_emails=email)
            message.template_id = template_id
            message.dynamic_template_data = dynamic_template_data
            try:
                self.sg.send(message)
                logging.debug(f"Email sent to {email}")
            except Exception as e:
                logging.error(f"Failed to send email to {email}: {e}")

    def send_notification_email(self, notification_message: str):
        """Sends a notification email."""
        emails = self._get_user_emails(self.user_id)
        dynamic_template_data = {
            "notification": notification_message,
        }
        self._send_email(emails, self.notification_template_id, dynamic_template_data)

    def send_report_email(self, message: str):
        """Sends a report email."""
        emails = self._get_user_emails(user_id=self.user_id)
        dynamic_template_data = {"message": message}
        self._send_email(emails, self.report_template_id, dynamic_template_data)
