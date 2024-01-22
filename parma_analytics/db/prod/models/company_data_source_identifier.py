"""CompanyDataSourceIdentifier model."""
from typing import Literal

import sqlalchemy as sa

from parma_analytics.db.prod.engine import Base
from parma_analytics.db.prod.models.types import literal_to_enum

IdentifierType = Literal["AUTOMATICALLY_DISCOVERED", "MANUALLY_ADDED"]


class CompanyDataSourceIdentifier(Base):
    """Model for the company_data_source_identifier table in the database."""

    __tablename__ = "company_data_source_identifier"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    company_data_source_id = sa.Column(
        sa.Integer, sa.ForeignKey("company_data_source.id"), nullable=False
    )
    identifier_type = sa.Column(literal_to_enum(IdentifierType), nullable=False)
    # TODO: REMOVE identifier_key
    identifier_key = sa.Column(sa.String, nullable=False)
    property = sa.Column(sa.String, nullable=False)
    value = sa.Column(sa.String, nullable=False)
    validity = sa.Column(sa.DateTime, nullable=False)
