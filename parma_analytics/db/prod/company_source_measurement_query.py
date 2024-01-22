"""Database crud operations for company_source_measurement table."""

from typing import Any

from sqlalchemy import and_
from sqlalchemy.orm import Session

from parma_analytics.db.prod.models.company_source_measurement import CompanyMeasurement


def create_company_measurement_query(
    db: Session, company_measurement_data: dict[str, Any]
) -> CompanyMeasurement:
    """Create a new company_measurement in the database.

    Args:
        db: Database session.
        company_measurement_data: values to be inserted in the database.

    Returns:
        The id of the newly created company_measurement.
    """
    company_measurement = CompanyMeasurement(**company_measurement_data)
    db.add(company_measurement)
    db.commit()
    db.refresh(company_measurement)
    return company_measurement


def get_company_measurement_query(
    db: Session, company_measurement_id: int
) -> CompanyMeasurement:
    """Get a company_measurement from the database.

    Args:
        db: Database session.
        company_measurement_id: id of the company_measurement to be retrieved.

    Returns:
        The company_measurement with the given id.
    """
    return (
        db.query(CompanyMeasurement)
        .filter(CompanyMeasurement.company_measurement_id == company_measurement_id)
        .first()
    )


def get_by_company_and_measurement_ids_query(
    db: Session, company_id, measurement_id: int
) -> CompanyMeasurement:
    """Get a company_measurement from the database.

    Args:
        db: Database session.
        company_id: id of the company to be retrieved.
        measurement_id: id of the measurement to be retrieved.

    Returns:
        The company_measurement with the given company_id and measurement_id.
    """
    return (
        db.query(CompanyMeasurement)
        .filter(
            and_(
                CompanyMeasurement.company_id == company_id,
                CompanyMeasurement.source_measurement_id == measurement_id,
            )
        )
        .first()
    )


def list_company_measurements_query(db: Session) -> list[CompanyMeasurement]:
    """List all company_measurements from the database.

    Args:
        db: Database session.

    Returns:
        A list of all company_measurements.
    """
    company_measurements = db.query(CompanyMeasurement).all()
    return company_measurements


def update_company_measurement_query(
    db: Session, id: int, company_measurement_data: dict[str, Any]
) -> CompanyMeasurement:
    """Update a company_measurement in the database.

    Args:
        db: Database session.
        id: id of the company_measurement to be updated.
        company_measurement_data: values to be updated in the database.

    Returns:
        The updated company_measurement.
    """
    company_measurement = (
        db.query(CompanyMeasurement)
        .filter(CompanyMeasurement.company_measurement_id == id)
        .first()
    )
    for key, value in company_measurement_data.items():
        setattr(company_measurement, key, value)
    db.commit()
    db.refresh(company_measurement)
    return company_measurement


def delete_company_measurement_query(db: Session, company_measurement_id) -> None:
    """Delete a company_measurement from the database.

    Args:
        db: DB session.
        company_measurement_id: id of the company_measurement to be deleted.
    """
    company_measurement = (
        db.query(CompanyMeasurement)
        .filter(CompanyMeasurement.company_measurement_id == company_measurement_id)
        .first()
    )
    db.delete(company_measurement)
    db.commit()
