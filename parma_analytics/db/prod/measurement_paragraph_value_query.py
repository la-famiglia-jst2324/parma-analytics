from sqlalchemy import Column, DateTime, Integer, String, func
from sqlalchemy.orm import Session

from parma_analytics.db.prod.engine import Base


# Define the MeasurementParagraphValue model
class MeasurementParagraphValue(Base):
    __tablename__ = "measurement_paragraph_value"

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_measurement_id = Column("company_measurement_id", Integer)
    value = Column(String)
    timestamp = Column(DateTime)
    created_at = Column("created_at", DateTime, default=func.now())
    modified_at = Column(
        "modified_at", DateTime, default=func.now(), onupdate=func.now()
    )


# Define the CRUD operations
def create_measurement_paragraph_value_query(
    db: Session, measurement_paragraph_value_data
) -> int:
    measurement_paragraph_value = MeasurementParagraphValue(
        **measurement_paragraph_value_data
    )
    db.add(measurement_paragraph_value)
    db.commit()
    db.refresh(measurement_paragraph_value)
    return measurement_paragraph_value.id


def get_measurement_paragraph_value_query(
    db: Session, measurement_paragraph_value_id
) -> MeasurementParagraphValue:
    return (
        db.query(MeasurementParagraphValue)
        .filter(MeasurementParagraphValue.id == measurement_paragraph_value_id)
        .first()
    )


def list_measurement_paragraph_values_query(db: Session) -> list:
    measurement_paragraph_values = db.query(MeasurementParagraphValue).all()
    return measurement_paragraph_values


def update_measurement_paragraph_value_query(
    db: Session, id: int, measurement_paragraph_value_data
) -> MeasurementParagraphValue:
    measurement_paragraph_value = (
        db.query(MeasurementParagraphValue)
        .filter(MeasurementParagraphValue.id == id)
        .first()
    )
    for key, value in measurement_paragraph_value_data.items():
        setattr(measurement_paragraph_value, key, value)
    db.commit()
    return measurement_paragraph_value


def delete_measurement_paragraph_value_query(
    db: Session, measurement_paragraph_value_id
) -> None:
    measurement_paragraph_value = (
        db.query(MeasurementParagraphValue)
        .filter(MeasurementParagraphValue.id == measurement_paragraph_value_id)
        .first()
    )
    db.delete(measurement_paragraph_value)
    db.commit()
