"""Database ORM model for notification table."""


import sqlalchemy as Column, Integer, String, DateTime, ForeignKey, func, Float
from sqlalchemy.orm import relationship

from parma_analytics.db.prod.engine import Base

class NotificationRules(Base):
    """Model for the notification_rules table in the database."""

    __tablename__ = 'notification_rules'

    rule_id = Column(Integer, primary_key=True)
    rule_name = Column(String)
    source_measurement_id = Column(Integer, ForeignKey('source_measurement.id', ondelete="CASCADE"))
    threshold = Column(Float, name="threshold")
    aggregation_method = Column(String, nullable=True)
    num_aggregation_entries = Column(Integer, nullable=True)
    notification_message = Column(String, nullable=True)
    createdAt = Column(DateTime, nullable=False, default=func.now())
    modifiedAt = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())

    # Relationships
    sourceMeasurement = relationship("SourceMeasurement", back_populates="notification_rules")
