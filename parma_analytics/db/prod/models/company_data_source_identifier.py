"""CompanyDataSourceIdentifier model."""
import sqlalchemy as sa
from sqlalchemy import Enum

from parma_analytics.db.prod.engine import Base


class IdentifierType(sa.Enum):
    """Enum for identifier types."""

    AUTOMATICALLY_DISCOVERED = "AUTOMATICALLY_DISCOVERED"
    MANUALLY_ADDED = "MANUALLY_ADDED"


class CompanyDataSourceIdentifier(Base):
    """Model for the company_data_source_identifier table in the database."""

    __tablename__ = "company_data_source_identifier"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    company_data_source_id = sa.Column(
        sa.Integer, sa.ForeignKey("company_data_source.id"), nullable=False
    )
    identifier_key = sa.Column(sa.String, nullable=False)
    identifier_type = sa.Column(Enum(IdentifierType), nullable=False)
    property = sa.Column(sa.String, nullable=False)
    value = sa.Column(sa.String, nullable=False)
    validity = sa.Column(sa.DateTime, nullable=False)
