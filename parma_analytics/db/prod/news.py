"""This module contains the code related to the news database operations.

It provides functions for creating news in the database using SQLAlchemy.
"""

from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from parma_analytics.api.models.news import NewsCreate
from parma_analytics.db.prod.models.news import News


def create_news_query(engine: Engine, news_data: NewsCreate) -> News:
    """Create a new news in the database.

    Args:
        engine: The SQLAlchemy engine used to connect to the database.
        news_data: The data for creating the news.

    Returns:
        News: The newly created news object.
    """
    with Session(engine) as session:
        session.add(News(**news_data))
        session.commit()
        session.refresh(news_data)
        return news_data
