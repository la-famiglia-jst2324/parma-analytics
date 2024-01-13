"""Database ORM models for company_subscription table."""


import sqlalchemy as sa

from parma_analytics.db.prod.engine import Base


class CompanySubscription(Base):
    """Model for the company_subscription table in the database."""

    __tablename__ = "company_subscription"

    user_id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    company_id = sa.Column(sa.Integer, primary_key=True)
    created_at = sa.Column(sa.DateTime, nullable=False, default=sa.func.now())
    modified_at = sa.Column(
        sa.DateTime, nullable=False, default=sa.func.now(), onupdate=sa.func.now()
    )
