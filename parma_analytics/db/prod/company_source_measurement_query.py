from sqlalchemy import Column, Integer
from sqlalchemy.orm import Session

from parma_analytics.db.prod.engine import Base


class CompanyMeasurement(Base):
    __tablename__ = "company_source_measurement"

    company_measurement_id = Column(
        "company_measurement_id", Integer, primary_key=True, autoincrement=True
    )
    source_measurement_id = Column("source_measurement_id", Integer)
    company_id = Column("company_id", Integer)


def create_company_measurement_query(
    db: Session, company_measurement_data
) -> CompanyMeasurement:
    company_measurement = CompanyMeasurement(**company_measurement_data)
    db.add(company_measurement)
    db.commit()
    db.refresh(company_measurement)
    return company_measurement


def get_company_measurement_query(
    db: Session, company_measurement_id
) -> CompanyMeasurement:
    return (
        db.query(CompanyMeasurement)
        .filter(CompanyMeasurement.company_measurement_id == company_measurement_id)
        .first()
    )


def get_by_company_and_measurement_ids_query(
    db: Session, company_id, measurement_id
) -> CompanyMeasurement:
    return (
        db.query(CompanyMeasurement)
        .filter(
            CompanyMeasurement.company_id == company_id
            and CompanyMeasurement.source_measurement_id == measurement_id
        )
        .first()
    )


def list_company_measurements_query(db: Session) -> list:
    company_measurements = db.query(CompanyMeasurement).all()
    return company_measurements


def update_company_measurement_query(
    db: Session, id: int, company_measurement_data
) -> CompanyMeasurement:
    company_measurement = (
        db.query(CompanyMeasurement)
        .filter(CompanyMeasurement.company_measurement_id == id)
        .first()
    )
    for key, value in company_measurement_data.items():
        setattr(company_measurement, key, value)
    db.commit()
    return company_measurement


def delete_company_measurement_query(db: Session, company_measurement_id) -> None:
    company_measurement = (
        db.query(CompanyMeasurement)
        .filter(CompanyMeasurement.company_measurement_id == company_measurement_id)
        .first()
    )
    db.delete(company_measurement)
    db.commit()
