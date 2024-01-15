"""Database ORM models for notification_channel table."""


import sqlalchemy as sa

from parma_analytics.db.prod.engine import Base


class NotificationChannel(Base):
    """Model for the notification_channel table in the database."""

    __tablename__ = "notification_channel"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    channel_type = sa.Column(sa.String, nullable=False)
    destination = sa.Column(sa.String, nullable=False)
    secret_id = sa.Column(sa.String, nullable=True)
    created_at = sa.Column(sa.DateTime, nullable=False, default=sa.func.now())
    modified_at = sa.Column(
        sa.DateTime, nullable=False, default=sa.func.now(), onupdate=sa.func.now()
    )
