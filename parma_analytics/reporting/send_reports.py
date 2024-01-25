"""Module to get send reports based on user subscription."""

import logging
from typing import Any

from parma_analytics.db.prod.company_query import get_company_name
from parma_analytics.db.prod.engine import get_engine, get_session
from parma_analytics.db.prod.news_query import get_news_of_company
from parma_analytics.db.prod.reporting import fetch_company_ids_for_user
from parma_analytics.db.prod.user_query import get_user
from parma_analytics.reporting.generate_html import generate_html_report
from parma_analytics.reporting.gmail.email_service import EmailService
from parma_analytics.reporting.slack.send_slack_messages import SlackService


def send_reports():
    """Method to send report."."""
    with get_session() as session:
        try:
            user_ids = get_user(session)
            for user_id in user_ids:
                company_ids = fetch_company_ids_for_user(session, user_id.id)
                news_by_company: dict[str, Any] = {}

                for company_id in company_ids:
                    if company_id.company_id is not None:
                        messages = get_news_of_company(session, company_id.company_id)
                        company_name = get_company_name(
                            get_engine(), company_id.company_id
                        )
                        if messages and company_name:
                            news_by_company[company_name] = []
                            news_by_company[company_name].extend(
                                [
                                    message.message
                                    for message in messages
                                    if message.message
                                ]
                            )
                if news_by_company:
                    user_id_int = user_id.id
                    html = generate_html_report(news_by_company)
                    email_service = EmailService(user_id_int)
                    email_service.send_report_email(html)

                    content = ""

                    for company_name, news_list in news_by_company.items():
                        content += f"{company_name}\n"

                        for news_message in news_list:
                            content += f"- {news_message}\n"
                    slack_service = SlackService()
                    slack_service.send_report(user_id_int, content)
        except Exception as e:
            logging.error(f"An error occurred in reporting/send_reports: {e}")
            raise e
