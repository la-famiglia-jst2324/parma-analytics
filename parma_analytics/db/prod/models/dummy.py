import sqlalchemy as sa

from parma_analytics.db.prod.models.base import DbBase


class DbDummy(DbBase):
    """Dummy database model for testing and showcase purposes."""

    __tablename__ = "dummy"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, nullable=False)
    price = sa.Column(sa.Float, nullable=False)
    is_offer = sa.Column(sa.Boolean, nullable=True, default=None)

    created_at = sa.Column(sa.DateTime, nullable=False, default=sa.func.now())

    def __repr__(self):
        """Return a string representation of the object."""
        return (
            f"<DbDummy(id={self.id}, name={self.name}, value={self.price}, "
            f"created_at={self.created_at})>"
        )
