"""Operation related to News."""

from sqlalchemy.orm import Session

from parma_analytics.db.prod.models.news import News


def get_news_of_company(db: Session, company_id) -> list:
    """Get the news from db."""
    return db.query(News.message).filter(News.company_id == company_id).all()
