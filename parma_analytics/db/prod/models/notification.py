"""Database ORM model for notification table."""


import sqlalchemy as Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from parma_analytics.db.prod.engine import Base

class Notification(Base):
    """Model for the notification table in the database."""

    __tablename__ = "notification"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    message = Column(String, nullable=False)
    company_id = Column(Integer, ForeignKey('company.id'), nullable=False)
    data_source_id = Column(Integer, ForeignKey('data_source.id'), nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    modified_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())

    # Relationships
    company = relationship("Company", back_populates="notifications")
    data_source = relationship("DataSource", back_populates="notifications")
