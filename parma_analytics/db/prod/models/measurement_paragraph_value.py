"""Database ORM models for measurement_paragraph_value table."""


from sqlalchemy import Column, DateTime, Integer, String, func

from parma_analytics.db.prod.engine import Base


class MeasurementParagraphValue(Base):
    """ORM model for measurement_paragraph_value table."""

    __tablename__ = "measurement_paragraph_value"

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_measurement_id = Column("company_measurement_id", Integer)
    value = Column(String)
    timestamp = Column(DateTime)
    created_at = Column("created_at", DateTime, default=func.now())
    modified_at = Column(
        "modified_at", DateTime, default=func.now(), onupdate=func.now()
    )
