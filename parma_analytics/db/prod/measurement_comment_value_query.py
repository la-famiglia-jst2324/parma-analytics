from sqlalchemy import Column, Integer, DateTime, String, func
from sqlalchemy.orm import Session
from parma_analytics.db.prod.engine import Base


# Define the MeasurementCommentValue model
class MeasurementCommentValue(Base):
    __tablename__ = "measurement_comment_value"

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_measurement_id = Column("company_measurement_id", Integer)
    value = Column(String)
    created_at = Column("created_at", DateTime, default=func.now())
    modified_at = Column("modified_at", DateTime, onupdate=func.now())


# Define the CRUD operations
def create_measurement_comment_value_query(
    db: Session, measurement_comment_value_data
) -> int:
    measurement_comment_value = MeasurementCommentValue(
        **measurement_comment_value_data
    )
    db.add(measurement_comment_value)
    db.commit()
    db.refresh(measurement_comment_value)
    return measurement_comment_value.id


def get_measurement_comment_value_query(
    db: Session, measurement_comment_value_id
) -> MeasurementCommentValue:
    return (
        db.query(MeasurementCommentValue)
        .filter(MeasurementCommentValue.id == measurement_comment_value_id)
        .first()
    )


def list_measurement_comment_values_query(db: Session) -> list:
    measurement_comment_values = db.query(MeasurementCommentValue).all()
    return measurement_comment_values


def update_measurement_comment_value_query(
    db: Session, id: int, measurement_comment_value_data
) -> MeasurementCommentValue:
    measurement_comment_value = (
        db.query(MeasurementCommentValue)
        .filter(MeasurementCommentValue.id == id)
        .first()
    )
    for key, value in measurement_comment_value_data.items():
        setattr(measurement_comment_value, key, value)
    db.commit()
    return measurement_comment_value


def delete_measurement_comment_value_query(
    db: Session, measurement_comment_value_id
) -> None:
    measurement_comment_value = (
        db.query(MeasurementCommentValue)
        .filter(MeasurementCommentValue.id == measurement_comment_value_id)
        .first()
    )
    db.delete(measurement_comment_value)
    db.commit()
