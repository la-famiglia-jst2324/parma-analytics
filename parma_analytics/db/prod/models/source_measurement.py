"""Database ORM models for source_measurement table."""


import sqlalchemy as sa

from parma_analytics.db.prod.engine import Base


class SourceMeasurement(Base):
    """Model for the source_measurement table in the database."""

    __tablename__ = "source_measurement"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    type = sa.Column(sa.String, nullable=False)
    measurement_name = sa.Column(sa.String, nullable=False)
    source_module_id = sa.Column(sa.Integer, nullable=False)
    parent_measurement_id = sa.Column(sa.Integer, nullable=True)
    created_at = sa.Column(sa.DateTime, nullable=False, default=sa.func.now())
    modified_at = sa.Column(
        sa.DateTime, nullable=False, default=sa.func.now(), onupdate=sa.func.now()
    )
