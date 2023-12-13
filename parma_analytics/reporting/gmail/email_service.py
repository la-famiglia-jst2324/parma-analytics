import os
import base64
import requests
from typing import List
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Mail,
    Attachment,
    FileContent,
    FileName,
    FileType,
    Disposition,
)
from ..notification_service_manager import (
    NotificationServiceManager,
    Category,
    MessageType,
)


class EmailService:
    """A service that handles the sending of emails."""

    def __init__(self, bucket_or_company: Category, company_or_bucket_id: int):
        self.sg: SendGridAPIClient = SendGridAPIClient(os.environ["SENDGRID_API_KEY"])
        self.notification_template_id: str | None = os.environ[
            "SENDGRID_NOTIFICATION_TEMPLATE_ID"
        ]
        self.report_template_id: str | None = os.environ["SENDGRID_REPORT_TEMPLATE_ID"]

        self.from_email: str | None = os.environ["SENDGRID_FROM_EMAIL"]
        self.category: Category = bucket_or_company
        self.company_or_bucket_id: int = company_or_bucket_id

    def _get_users_emails(self, message_type: MessageType) -> List[str]:
        """Get all user emails for notification or report."""
        subscription_table = (
            "notification_subscription"
            if message_type == "notification"
            else "report_subscription"
        )

        channel_manager = NotificationServiceManager(
            self.company_or_bucket_id,
            subscription_table,
            message_type,
            "email",
            self.category,
        )
        return channel_manager.get_notification_destinations()

    def _send_email(
        self,
        to_emails: List[str],
        template_id: str | None,
        dynamic_template_data: dict,
        attachments=None,
    ):
        """Generic function to send emails using SendGrid."""
        for email in to_emails:
            message = Mail(from_email=self.from_email, to_emails=email)
            message.template_id = template_id
            message.dynamic_template_data = dynamic_template_data

            if attachments:
                for file_url in attachments:
                    response = requests.get(file_url)
                    response.raise_for_status()
                    file_data = response.content
                    file_title = file_url.split("/")[-1]
                    encoded_file = base64.b64encode(file_data).decode()
                    attached_file = Attachment(
                        FileContent(encoded_file),
                        FileName(file_title),
                        FileType("application/pdf"),
                        Disposition("attachment"),
                    )
                    message.add_attachment(attached_file)

            try:
                self.sg.send(message)
                print(f"Email sent to {email}")
            except Exception as e:
                print(f"Failed to send email to {email}: {e}")

    def send_notification_email(
        self, content: str, company_name=None, company_logo=None
    ):
        """Sends a notification email."""
        emails = self._get_users_emails(message_type="notification")
        dynamic_template_data = {
            "company_name": company_name,
            "company_logo": company_logo,
            "notification": content,
        }
        self._send_email(emails, self.notification_template_id, dynamic_template_data)

    def send_report_email(self, company_bucket_name: str, attachments=None):
        """Sends a report email."""
        emails = self._get_users_emails(message_type="report")
        dynamic_template_data = {"company_bucket": company_bucket_name}
        self._send_email(
            emails, self.report_template_id, dynamic_template_data, attachments
        )


email_service = EmailService("bucket", 1)
email_service.send_notification_email(
    content="Microsoft to join OpenAI’s board after Sam Altman rehired as CEO.",
    company_name="OpenAI",
    company_logo="https://upload.wikimedia.org/wikipedia/commons/4/4d/OpenAI_Logo.svg",
)
email_service.send_report_email(
    company_bucket_name="My Bucket",
    attachments=[
        "https://www.imi.europa.eu/sites/default/files/uploads/documents/apply-for-funding/call-documents/imi1/Annex2_FinalReportTemplate.pdf",
    ],
)
