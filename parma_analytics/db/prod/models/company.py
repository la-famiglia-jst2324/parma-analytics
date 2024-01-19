"""Company model."""
import sqlalchemy as sa

from parma_analytics.db.prod.engine import Base


class Company(Base):
    """Model for the company table in the database."""

    __tablename__ = "company"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, nullable=False)
    description = sa.Column(sa.String, nullable=True)
    added_by = sa.Column(sa.Integer, nullable=False)
    created_at = sa.Column(sa.DateTime, nullable=False, default=sa.func.now())
    modified_at = sa.Column(
        sa.DateTime, nullable=False, default=sa.func.now(), onupdate=sa.func.now()
    )

    def __repr__(self):
        """Return a string representation of the Company object."""
        return f"<Company(id={self.id}, name={self.name})>"
