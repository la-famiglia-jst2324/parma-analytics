"""DB model for data source."""
from sqlalchemy import JSON, Boolean, Column, DateTime, Integer, String
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.sql import func
from sqlalchemy.sql.schema import FetchedValue

from parma_analytics.db.prod.engine import Base


class DataSource(Base):
    """DB model of a data source."""

    __tablename__ = "data_source"

    id = Column(Integer, primary_key=True, autoincrement=True)
    source_name = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False)
    frequency = Column(
        ENUM("Daily", "Weekly", "Monthly", name="frequency"), nullable=False
    )
    health_status = Column(
        ENUM("Healthy", "Unhealthy", name="health_status"), nullable=False
    )
    description = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    modified_at = Column(DateTime, server_onupdate=func.now())
    max_run_seconds = Column(Integer, server_default=FetchedValue())
    version = Column(String, server_default="1.0")
    invocation_endpoint = Column(String, server_default="")
    additional_params = Column(JSON, nullable=True)
