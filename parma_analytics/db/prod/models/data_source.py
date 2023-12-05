from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON, Enum
from sqlalchemy.orm import relationship

from .base import Base
from .enums.frequency import Frequency
from .enums.health_status import HealthStatus


class DataSource(Base):
    __tablename__ = "data_source"

    id = Column(Integer, primary_key=True)
    source_name = Column(String)
    is_active = Column(Boolean)
    default_frequency = Column(Enum(Frequency))
    frequency_pattern = Column(String, nullable=True)
    health_status = Column(Enum(HealthStatus))
    description = Column(String, nullable=True)
    created_at = Column(DateTime)
    modified_at = Column(DateTime)
    version = Column(String, default="1.0")
    maximum_expected_run_time = Column(Integer, default=60)
    invocation_endpoint = Column(String, default="")
    additional_params = Column(JSON, nullable=True)

    # Relationships
    scheduled_tasks = relationship("ScheduledTasks", back_populates="data_source")
