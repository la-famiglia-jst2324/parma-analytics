"""Database ORM model for news table."""

from sqlalchemy import Column, DateTime, Integer, String, func

from parma_analytics.db.prod.engine import Base


class News(Base):
    """Model for the news table in the database."""

    __tablename__ = "news"

    id = Column(Integer, primary_key=True, autoincrement=True)
    message = Column(String, nullable=False)
    company_id = Column(Integer, nullable=False)
    data_source_id = Column(Integer, nullable=False)
    trigger_factor = Column(String)
    title = Column(String)
    timestamp = Column(DateTime, nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    modified_at = Column(
        DateTime, nullable=False, default=func.now(), onupdate=func.now()
    )
    source_measurement_id = Column(Integer, nullable=False)
