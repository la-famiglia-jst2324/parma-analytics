"""Database ORM model for user table."""


import sqlalchemy as sa

from parma_analytics.db.prod.engine import Base


class User(Base):
    """Model for the user table in the database."""

    __tablename__ = "user"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    auth_id = sa.Column(sa.String, nullable=False, unique=True)
    name = sa.Column(sa.String, nullable=False)
    profile_picture = sa.Column(sa.String, nullable=True)
    role = sa.Column(sa.String, nullable=False)
    created_at = sa.Column(sa.DateTime, nullable=False, default=sa.func.now())
    modified_at = sa.Column(
        sa.DateTime, nullable=False, default=sa.func.now(), onupdate=sa.func.now()
    )
