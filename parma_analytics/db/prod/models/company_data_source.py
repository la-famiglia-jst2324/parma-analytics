"""Company Data Source model."""

import sqlalchemy as sa
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from parma_analytics.db.prod.engine import Base


class CompanyDataSource(Base):
    """Model for the company_data_source table in the database."""

    __tablename__ = "company_data_source"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    data_source_id = sa.Column(sa.Integer, ForeignKey("data_source.id"), nullable=False)
    company_id = sa.Column(sa.Integer, ForeignKey("company.id"), nullable=False)
    is_data_source_active = sa.Column(sa.Boolean, nullable=False)
    health_status = sa.Column(sa.String, nullable=False)
    created_at = sa.Column(sa.DateTime, nullable=False, default=sa.func.now())
    modified_at = sa.Column(
        sa.DateTime, nullable=False, default=sa.func.now(), onupdate=sa.func.now()
    )

    # Relations
    company_data_source_identifiers = relationship(
        "CompanyDataSourceIdentifier", back_populates="company_data_source"
    )

    __table_args__ = (sa.UniqueConstraint("data_source_id", "company_id"),)
