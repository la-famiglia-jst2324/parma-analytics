"""Database ORM models for company_source_measurement table."""
from sqlalchemy import Column, Integer

from parma_analytics.db.prod.engine import Base


class CompanyMeasurement(Base):
    """ORM model for company_source_measurement table."""

    __tablename__ = "company_source_measurement"

    company_measurement_id = Column(
        "company_measurement_id", Integer, primary_key=True, autoincrement=True
    )
    source_measurement_id = Column("source_measurement_id", Integer)
    company_id = Column("company_id", Integer)
