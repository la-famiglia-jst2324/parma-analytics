from sqlalchemy import Column, DateTime, Integer, func
from sqlalchemy.orm import Session

from parma_analytics.db.prod.engine import Base


# Define the MeasurementIntValue model
class MeasurementIntValue(Base):
    __tablename__ = "measurement_int_value"

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_measurement_id = Column("company_measurement_id", Integer)
    value = Column(Integer)
    timestamp = Column(DateTime)
    created_at = Column("created_at", DateTime, default=func.now())
    modified_at = Column("modified_at", DateTime, onupdate=func.now())


# Define the CRUD operations
def create_measurement_int_value_query(db: Session, measurement_int_value_data) -> int:
    measurement_int_value = MeasurementIntValue(**measurement_int_value_data)
    db.add(measurement_int_value)
    db.commit()
    db.refresh(measurement_int_value)
    return measurement_int_value.id


def get_measurement_int_value_query(
    db: Session, measurement_int_value_id
) -> MeasurementIntValue:
    return (
        db.query(MeasurementIntValue)
        .filter(MeasurementIntValue.id == measurement_int_value_id)
        .first()
    )


def list_measurement_int_values_query(db: Session) -> list:
    measurement_int_values = db.query(MeasurementIntValue).all()
    return measurement_int_values


def update_measurement_int_value_query(
    db: Session, id: int, measurement_int_value_data
) -> MeasurementIntValue:
    measurement_int_value = (
        db.query(MeasurementIntValue).filter(MeasurementIntValue.id == id).first()
    )
    for key, value in measurement_int_value_data.items():
        setattr(measurement_int_value, key, value)
    db.commit()
    return measurement_int_value


def delete_measurement_int_value_query(db: Session, measurement_int_value_id) -> None:
    measurement_int_value = (
        db.query(MeasurementIntValue)
        .filter(MeasurementIntValue.id == measurement_int_value_id)
        .first()
    )
    db.delete(measurement_int_value)
    db.commit()
