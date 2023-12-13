from sqlalchemy import Column, DateTime, Integer, String, func
from sqlalchemy.orm import Session

from parma_analytics.db.prod.engine import Base


# Define the MeasurementTextValue model
class MeasurementTextValue(Base):
    __tablename__ = "measurement_text_value"

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_measurement_id = Column("company_measurement_id", Integer)
    value = Column(String)
    created_at = Column("created_at", DateTime, default=func.now())
    modified_at = Column("modified_at", DateTime, onupdate=func.now())


# Define the CRUD operations
def create_measurement_text_value_query(
    db: Session, measurement_text_value_data
) -> int:
    measurement_text_value = MeasurementTextValue(**measurement_text_value_data)
    db.add(measurement_text_value)
    db.commit()
    db.refresh(measurement_text_value)
    return measurement_text_value.id


def get_measurement_text_value_query(
    db: Session, measurement_text_value_id
) -> MeasurementTextValue:
    return (
        db.query(MeasurementTextValue)
        .filter(MeasurementTextValue.id == measurement_text_value_id)
        .first()
    )


def list_measurement_text_values_query(db: Session) -> list:
    measurement_text_values = db.query(MeasurementTextValue).all()
    return measurement_text_values


def update_measurement_text_value_query(
    db: Session, id: int, measurement_text_value_data
) -> MeasurementTextValue:
    measurement_text_value = (
        db.query(MeasurementTextValue).filter(MeasurementTextValue.id == id).first()
    )
    for key, value in measurement_text_value_data.items():
        setattr(measurement_text_value, key, value)
    db.commit()
    return measurement_text_value


def delete_measurement_text_value_query(db: Session, measurement_text_value_id) -> None:
    measurement_text_value = (
        db.query(MeasurementTextValue)
        .filter(MeasurementTextValue.id == measurement_text_value_id)
        .first()
    )
    db.delete(measurement_text_value)
    db.commit()
