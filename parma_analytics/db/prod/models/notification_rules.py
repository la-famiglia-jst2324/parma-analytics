"""Database ORM model for notification table."""


from sqlalchemy import Column, DateTime, Float, Integer, String, func

from parma_analytics.db.prod.engine import Base


class NotificationRules(Base):
    """Model for the notification_rules table in the database."""

    __tablename__ = "notification_rules"

    rule_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    rule_name = Column(String, nullable=False)
    source_measurement_id = Column(Integer, nullable=False)
    threshold = Column(Float, nullable=False)
    aggregation_method = Column(String, nullable=True)
    num_aggregation_entries = Column(Integer, nullable=True)
    notification_message = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    modified_at = Column(
        DateTime, nullable=False, default=func.now(), onupdate=func.now()
    )
