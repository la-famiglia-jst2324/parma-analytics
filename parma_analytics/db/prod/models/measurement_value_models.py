"""This module contains SQLAlchemy ORM models for measurement value tables."""

from sqlalchemy import Column, DateTime, Float, Integer, String, func

from parma_analytics.db.prod.engine import Base


class MeasurementValueBase(Base):
    """Base ORM model for measurement value tables."""

    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_measurement_id = Column("company_measurement_id", Integer)
    timestamp = Column(DateTime)
    created_at = Column("created_at", DateTime, default=func.now())
    modified_at = Column(
        "modified_at", DateTime, default=func.now(), onupdate=func.now()
    )


class MeasurementIntValue(MeasurementValueBase):
    """ORM model for measurement_int_value table."""

    __tablename__ = "measurement_int_value"
    value = Column(Integer)


class MeasurementFloatValue(MeasurementValueBase):
    """ORM model for measurement_float_value table."""

    __tablename__ = "measurement_float_value"
    value = Column(Float)


class MeasurementTextValue(MeasurementValueBase):
    """ORM model for measurement_text_value table."""

    __tablename__ = "measurement_text_value"
    value = Column(String)


class MeasurementParagraphValue(MeasurementValueBase):
    """ORM model for measurement_paragraph_value table."""

    __tablename__ = "measurement_paragraph_value"
    value = Column(String)


class MeasurementCommentValue(MeasurementValueBase):
    """ORM model for measurement_comment_value table."""

    __tablename__ = "measurement_comment_value"
    value = Column(String)


class MeasurementLinkValue(MeasurementValueBase):
    """ORM model for measurement_link_value table."""

    __tablename__ = "measurement_link_value"
    value = Column(String)


class MeasurementImageValue(MeasurementValueBase):
    """ORM model for measurement_image_value table."""

    __tablename__ = "measurement_image_value"
    value = Column(String)


class MeasurementDateValue(MeasurementValueBase):
    """ORM model for measurement_date_value table."""

    __tablename__ = "measurement_date_value"
    value = Column(DateTime)


class MeasurementNestedValue(MeasurementValueBase):
    """ORM model for measurement_nested_value table."""

    __tablename__ = "measurement_nested_value"
    value = Column(String)
