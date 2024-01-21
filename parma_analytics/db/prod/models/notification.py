"""Database ORM model for notification table."""


from sqlalchemy import Column, DateTime, Integer, String, func

from parma_analytics.db.prod.engine import Base


class Notification(Base):
    """Model for the notification table in the database."""

    __tablename__ = "notification"

    id = Column(Integer, primary_key=True, autoincrement=True)
    message = Column(String, nullable=False)
    company_id = Column(Integer, nullable=False)
    data_source_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    modified_at = Column(
        DateTime, nullable=False, default=func.now(), onupdate=func.now()
    )
