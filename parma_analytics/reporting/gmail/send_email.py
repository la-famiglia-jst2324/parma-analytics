import os
import base64
from sendgrid import SendGridAPIClient
import requests
from dotenv import load_dotenv
from sendgrid.helpers.mail import (
    Mail,
    Attachment,
    FileContent,
    FileName,
    FileType,
    Disposition,
)

load_dotenv()


def send_notification_email(
    to_email: str, content: str, company_name=None, company_logo=None
):
    """Sends an email using SendGrid.

    Parameters:
    - to_email (str): The recipient's email address.
    - subject (str): The subject of the email.
    - content (str): The HTML content of the email.
    - attachments (optional): Attachment files.

    Returns:
    - str: A message indicating the result of the email sending process.
    """

    message = Mail(from_email=os.environ.get("FROM_EMAIL"), to_emails=to_email)

    message.template_id = os.environ.get("SENDGRID_TEMPLATE_ID")
    message.dynamic_template_data = {
        "company_name": company_name,
        "company_logo": company_logo,
        "notification": content,
    }
    try:
        sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
        response = sg.send(message)

        print(f"email sent")
    except Exception as e:
        print(e)


def send_report_email(
    to_email: str, content: str, company_name=None, company_logo=None, attachments=None
):
    """Sends an email using SendGrid.

    Parameters:
    - to_email (str): The recipient's email address.
    - subject (str): The subject of the email.
    - content (str): The HTML content of the email.
    - attachments (optional): Attachment files.

    Returns:
    - str: A message indicating the result of the email sending process.
    """

    message = Mail(from_email=os.environ.get("FROM_EMAIL"), to_emails=to_email)

    message.template_id = os.environ.get("SENDGRID_TEMPLATE_ID")
    message.dynamic_template_data = {
        "company_name": company_name,
        "company_logo": company_logo,
        "notification": content,
    }

    if attachments:
        for file_url in attachments:
            # Download the file from the URL
            response = requests.get(file_url)
            response.raise_for_status()  # Ensure the download was successful
            file_data = response.content
            encoded_file = base64.b64encode(file_data).decode()

            attachedFile = Attachment(
                FileContent(encoded_file),
                FileName("Report.pdf"),
                FileType(
                    "application/pdf"
                ),  # You can change the file type based on your file
                Disposition("attachment"),
            )
            message.add_attachment(attachedFile)

    try:
        sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
        response = sg.send(message)

        print(f"email sent")
    except Exception as e:
        print(e)


attachments = [
    "https://www.imi.europa.eu/sites/default/files/uploads/documents/apply-for-funding/call-documents/imi1/Annex2_FinalReportTemplate.pdf",
    "https://firebasestorage.googleapis.com/v0/b/la-famiglia-parma-ai-staging.appspot.com/o/Company%2F3%2FDescription-1701897010652.pdf?alt=media&token=ce9567b9-0a8f-455e-b411-c4cd82e20876",
]
send_report_email(
    "basedonur@gmail.com",
    "Employee count has been by %30, from 100 to 130.",
    "Google",
    "https://img.freepik.com/vektoren-kostenlos/vogel-bunter-logo-gradientenvektor_343694-1365.jpg?w=1060&t=st=1701986058~exp=1701986658~hmac=db80b8f0fcc1a37d21a560543f15315e613b3278e89ac4dacac07ed35206f5b9",
    attachments,
)
"""
company_name
company_logo
subject
template_id: d-0589c71e88724b2a905ec7237f31c020
"""

"""
ingrid anders3
Free Trial Promo
retail free product trial
event email template
flexible welcome email
"""

"""
SendGrid requirements:
- Sender email/reply to email - sender identity verification
- API Email Send permission
- Dynamic Template ID
- La-Famiglia Logo should be uploaded to SendGrid/Firebase
"""
