from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from parma_analytics.db.prod.models.base import DbBase

Base = declarative_base()


class DbSourceMeasurement(DbBase):
    __tablename__ = "source_measurement"
    source_measurement_id = Column(Integer, primary_key=True, autoincrement=True)
    source_module_id = Column(Integer, ForeignKey("source_module.id"), nullable=False)
    company_id = Column(Integer, ForeignKey("company.id"), nullable=False)
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


class SourceModule(DbBase):
    __tablename__ = "source_module"

    id = Column(Integer, primary_key=True, autoincrement=True)
    # Add other columns as needed
    # ...

    # Define the relationship with SourceMeasurement
    source_measurements = relationship(
        "SourceMeasurement", back_populates="source_module"
    )


class Company(DbBase):
    __tablename__ = "company"

    id = Column(Integer, primary_key=True, autoincrement=True)
    # Add other columns as needed
    # ...

    # Define the relationship with SourceMeasurement
    source_measurements = relationship("SourceMeasurement", back_populates="company")
