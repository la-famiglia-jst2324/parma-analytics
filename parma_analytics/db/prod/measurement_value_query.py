"""This module contains the MeasurementValueCRUD class for CRUD operations."""

from typing import Any, TypeVar

from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import Session

# Define a TypeVar that is bound to DeclarativeMeta,
# which is the base class for SQLAlchemy models
ModelType = TypeVar("ModelType", bound=DeclarativeMeta)


class MeasurementValueCRUD:
    """Base class for CRUD operations on measurement value tables."""

    def __init__(self, model: ModelType):
        self.model = model

    def create_measurement_value(self, db: Session, data: dict[str, Any]) -> int:
        """Create a new measurement value in the database."""
        instance = self.model(**data)
        db.add(instance)
        db.commit()
        db.refresh(instance)
        return instance.id

    def get_measurement_value(self, db: Session, id: int) -> Any:
        """Get a measurement value from the database."""
        return db.query(self.model).filter(self.model.id == id).first()

    def list_measurement_value(self, db: Session) -> list:
        """List all measurement values from the database."""
        return db.query(self.model).all()

    def update_measurement_value(
        self, db: Session, id: int, data: dict[str, Any]
    ) -> Any:
        """Update a measurement value in the database."""
        instance = db.query(self.model).filter(self.model.id == id).first()
        for key, value in data.items():
            setattr(instance, key, value)
        db.commit()
        return instance

    def delete_measurement_value(self, db: Session, id: int) -> None:
        """Delete a measurement value from the database."""
        instance = db.query(self.model).filter(self.model.id == id).first()
        db.delete(instance)
        db.commit()

    def get_recent_measurement_value(self, db: Session, id: int):
        """Get most recent measurement value from the database."""
        return (
            db.query(self.model)
            .filter(self.model.company_measurement_id == id)
            .order_by(self.model.id.desc())
            .first()
        )
