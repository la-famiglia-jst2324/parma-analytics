"""Module to get send reports based on user subscription."""

from typing import Any

from parma_analytics.db.prod.company_query import get_company_name
from parma_analytics.db.prod.engine import get_engine, get_session
from parma_analytics.db.prod.news_query import get_news_of_company
from parma_analytics.db.prod.reporting import fetch_company_ids_for_user
from parma_analytics.db.prod.user_query import get_user
from parma_analytics.reporting.generate_html import generate_html_report
from parma_analytics.reporting.gmail.email_service import EmailService


def send_reports():
    """Method to send report."."""
    with get_session() as session:
        user_ids = get_user(session)
        for user_id in user_ids:
            company_ids = fetch_company_ids_for_user(session, user_id.id)
            news_by_company: dict[str, Any] = {}

            for company_id in company_ids:
                if company_id.company_id:
                    messages = get_news_of_company(session, company_id.company_id)
                    company_name = get_company_name(get_engine(), company_id.company_id)
                    if messages and company_name:
                        news_by_company[company_name] = []
                        news_by_company[company_name].extend(
                            [message.message for message in messages if message.message]
                        )

            if news_by_company:
                html = generate_html_report(news_by_company)
                email_service = EmailService(user_id)
                email_service.send_report_email(html)
