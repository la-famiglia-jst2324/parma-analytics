import enum
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    JSON,
    Enum,
)
from sqlalchemy.orm import relationship

from parma_analytics.db.prod.models.base import Base

"""
Production PostgreSQL Table Types
This file contains all the types used in the production PostgreSQL database.
"""


# -------------------------------------- ENUMS ----------------------------------------


class Frequency(enum.Enum):
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    CRON = "CRON"


class HealthStatus(enum.Enum):
    UP = "UP"
    DOWN = "DOWN"


class ScheduleType(enum.Enum):
    ON_DEMAND = "ON_DEMAND"
    REGULAR = "REGULAR"


class TaskStatus(enum.Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"


# -------------------------------------- MODELS ----------------------------------------


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


class ScheduledTasks(Base):
    __tablename__ = "scheduled_tasks"

    task_id = Column(Integer, primary_key=True)
    data_source_id = Column(Integer, ForeignKey("data_source.id"))
    schedule_type = Column(Enum(ScheduleType))
    started_at = Column(DateTime)
    locked_at = Column(DateTime, nullable=True)
    ended_at = Column(DateTime, nullable=True)
    result_summary = Column(String, nullable=True)
    status = Column(Enum(TaskStatus))
    attempts = Column(Integer, default=0)

    # Relationships
    data_source = relationship("DataSource", back_populates="scheduled_tasks")
