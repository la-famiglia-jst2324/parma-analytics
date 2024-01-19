"""Database ORM model for news table."""

import sqlalchemy as Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from parma_analytics.db.prod.engine import Base

class News(Base):
    """Model for the news table in the database."""

    __tablename__ = 'news'

    id = Column(Integer, primary_key=True)
    message = Column(String, nullable=False)
    company_id = Column(Integer, ForeignKey('company.id', ondelete="CASCADE"), nullable=False)
    data_source_id = Column(Integer, ForeignKey('data_source.id'), nullable=False)
    trigger_factor = Column(String)
    title = Column(String)
    timestamp = Column(DateTime, nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    modified_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
    source_measurement_id = Column(Integer, ForeignKey('sourcemeasurement.id'), nullable=False)

    # Relationships
    company = relationship("Company", back_populates="news")
    data_source = relationship("DataSource", back_populates="news")
    source_measurement = relationship("SourceMeasurement", back_populates="news")
