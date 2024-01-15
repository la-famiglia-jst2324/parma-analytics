"""Database operations to get user subscribed companies."""
from sqlalchemy import Column, DateTime, Integer

from parma_analytics.db.prod.engine import Base


class CompanySubscription(Base):
    """ORM model for company_subscription."""

    __tablename__ = "company_subscription"

    user_id = Column(Integer, primary_key=True, name="user_id")
    company_id = Column(Integer, primary_key=True, name="company_id")
    created_at = Column(DateTime)
    modified_at = Column(DateTime)
