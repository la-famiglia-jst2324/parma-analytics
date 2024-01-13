"""Database ORM models for company_bucket_membership table."""


import sqlalchemy as sa

from parma_analytics.db.prod.engine import Base


class CompanyBucketMembership(Base):
    """Model for the company_bucket_membership table in the database."""

    __tablename__ = "company_bucket_membership"

    company_id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    bucket_id = sa.Column(sa.Integer, primary_key=True)
    created_at = sa.Column(sa.DateTime, nullable=False, default=sa.func.now())
    modified_at = sa.Column(
        sa.DateTime, nullable=False, default=sa.func.now(), onupdate=sa.func.now()
    )
