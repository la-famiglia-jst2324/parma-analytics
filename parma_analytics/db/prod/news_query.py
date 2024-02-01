"""Operation related to News."""

from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from parma_analytics.db.prod.models.news import News


def get_news_of_company(db: Session, company_id) -> list:
    """Get the news from db."""
    one_week_ago = datetime.now() - timedelta(weeks=1)
    return (
        db.query(News.message, News.source_measurement_id)
        .filter(News.company_id == company_id, News.timestamp >= one_week_ago)
        .all()
    )
