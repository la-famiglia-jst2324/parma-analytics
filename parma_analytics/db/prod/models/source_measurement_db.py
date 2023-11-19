import uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from parma_analytics.db.prod.models.base import DbBase

Base = declarative_base()


class DbSourceMeasurement(DbBase):
    __tablename__ = "source_measurement"
    source_measurement_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    source_module_id = Column(
        UUID(as_uuid=True), ForeignKey("source_module.id"), nullable=False
    )
    company_id = Column(UUID(as_uuid=True), ForeignKey("company.id"), nullable=False)
    type = Column(String, nullable=False)
    measurement_name = Column(String, nullable=False)

    # Define relationships if needed
    source_module = relationship("SourceModule", back_populates="source_measurements")
    company = relationship("Company", back_populates="source_measurements")

    def __repr__(self):
        return (
            f"<SourceMeasurement(id={self.source_measurement_id}, "
            f"source_module_id={self.source_module_id}, company_id={self.company_id}, "
            f"type={self.type}, measurement_name={self.measurement_name} "
        )


# TODO: check with these models when the DB is setup.
class SourceModule(DbBase):
    __tablename__ = "source_module"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    # Add other columns as needed
    # ...

    # Define the relationship with SourceMeasurement
    source_measurements = relationship(
        "SourceMeasurement", back_populates="source_module"
    )


class Company(DbBase):
    __tablename__ = "company"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    # Add other columns as needed
    # ...

    # Define the relationship with SourceMeasurement
    source_measurements = relationship("SourceMeasurement", back_populates="company")
