from sqlalchemy import Column, DateTime, Float, Integer, func
from sqlalchemy.orm import Session

from parma_analytics.db.prod.engine import Base


# Define the MeasurementFloatValue model
class MeasurementFloatValue(Base):
    __tablename__ = "measurement_float_value"

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_measurement_id = Column("company_measurement_id", Integer)
    value = Column(Float)
    created_at = Column("created_at", DateTime, default=func.now())
    modified_at = Column("modified_at", DateTime, onupdate=func.now())


# Define the CRUD operations
def create_measurement_float_value_query(
    db: Session, measurement_float_value_data
) -> int:
    measurement_float_value = MeasurementFloatValue(**measurement_float_value_data)
    db.add(measurement_float_value)
    db.commit()
    db.refresh(measurement_float_value)
    return measurement_float_value.id


def get_measurement_float_value_query(
    db: Session, measurement_float_value_id
) -> MeasurementFloatValue:
    return (
        db.query(MeasurementFloatValue)
        .filter(MeasurementFloatValue.id == measurement_float_value_id)
        .first()
    )


def list_measurement_float_values_query(db: Session) -> list:
    measurement_float_values = db.query(MeasurementFloatValue).all()
    return measurement_float_values


def update_measurement_float_value_query(
    db: Session, id: int, measurement_float_value_data
) -> MeasurementFloatValue:
    measurement_float_value = (
        db.query(MeasurementFloatValue).filter(MeasurementFloatValue.id == id).first()
    )
    for key, value in measurement_float_value_data.items():
        setattr(measurement_float_value, key, value)
    db.commit()
    return measurement_float_value


def delete_measurement_float_value_query(
    db: Session, measurement_float_value_id
) -> None:
    measurement_float_value = (
        db.query(MeasurementFloatValue)
        .filter(MeasurementFloatValue.id == measurement_float_value_id)
        .first()
    )
    db.delete(measurement_float_value)
    db.commit()
