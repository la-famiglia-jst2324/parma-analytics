from typing import Any, Type
from sqlalchemy.orm import Session

class MeasurementValueCRUD:
    """Base class for CRUD operations on measurement value tables."""

    def __init__(self, model: Type):
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

    def update_measurement_value(self, db: Session, id: int, data: dict[str, Any]) -> Any:
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
