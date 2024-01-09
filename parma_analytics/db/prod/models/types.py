"""Types and models for our core postgres database."""

from typing import Literal, get_args

from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from parma_analytics.db.prod.models.base import Base

"""
Production PostgreSQL Table Types
This file contains all the types used in the production PostgreSQL database.
"""


# -------------------------------------- ENUMS ----------------------------------------

Frequency = Literal["HOURLY", "DAILY", "WEEKLY", "MONTHLY"]
HealthStatus = Literal["UP", "DOWN"]
ScheduleType = Literal["ON_DEMAND", "REGULAR"]
TaskStatus = Literal["PENDING", "PROCESSING", "SUCCESS", "FAILED"]
"""Success and failed are terminal states."""


def literal_to_enum(literal) -> Enum:  # noqa
    return Enum(
        *get_args(literal),
        name=literal.__name__,
        validate_strings=True,
    )


# -------------------------------------- MODELS ----------------------------------------


class DataSource(Base):
    """ORM model for the data_source table."""

    __tablename__ = "data_source"

    id = Column(Integer, primary_key=True)
    source_name = Column(String)
    is_active = Column(Boolean)
    frequency = Column(literal_to_enum(Frequency))
    health_status = Column(literal_to_enum(HealthStatus))
    description = Column(String, nullable=True)
    created_at = Column(DateTime)
    modified_at = Column(DateTime)
    max_run_seconds = Column(Integer, default=5 * 60)
    version = Column(String, default="1.0")
    invocation_endpoint = Column(String, default="")
    additional_params = Column(JSON, nullable=True)

    # Relationships
    scheduled_tasks = relationship("ScheduledTask", back_populates="data_source")
    company_data_sources = relationship(
        "CompanyDataSource", back_populates="data_source"
    )


class ScheduledTask(Base):
    """ORM model for the scheduled_task table."""

    __tablename__ = "scheduled_task"

    task_id = Column(Integer, primary_key=True)
    data_source_id = Column(Integer, ForeignKey("data_source.id"))
    schedule_type = Column(literal_to_enum(ScheduleType))
    scheduled_at = Column(DateTime)
    started_at = Column(DateTime, nullable=True)
    ended_at = Column(DateTime, nullable=True)
    max_run_seconds = Column(Integer, default=60 * 5)
    result_summary = Column(String, nullable=True)
    status = Column(literal_to_enum(TaskStatus))
    attempts = Column(Integer, default=0)

    # Relationships
    data_source = relationship("DataSource", back_populates="scheduled_tasks")


class Company(Base):
    """ORM model for the company table."""

    __tablename__ = "company"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String, nullable=True)
    added_by = Column(Integer)

    # Relationships
    company_data_sources = relationship("CompanyDataSource", back_populates="company")


class CompanyDataSource(Base):
    """ORM model for the company_data_source table."""

    __tablename__ = "company_data_source"

    data_source_id = Column(Integer, ForeignKey("data_source.id"), primary_key=True)
    company_id = Column(Integer, ForeignKey("company.id"), primary_key=True)
    is_data_source_active = Column(Boolean)
    health_status = Column(literal_to_enum(HealthStatus))

    # Relationships
    data_source = relationship("DataSource", back_populates="company_data_sources")
    company = relationship("Company", back_populates="company_data_sources")
