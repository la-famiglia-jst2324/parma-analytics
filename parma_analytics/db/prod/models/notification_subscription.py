"""Database ORM models for notification_subscription table."""


import sqlalchemy as sa

from parma_analytics.db.prod.engine import Base


class NotificationSubscription(Base):
    """Model for the notification_subscription table in the database."""

    __tablename__ = "notification_subscription"

    user_id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    channel_id = sa.Column(sa.Integer, primary_key=True)
    channel_purpose = sa.Column(sa.String, nullable=False)
    created_at = sa.Column(sa.DateTime, nullable=False, default=sa.func.now())
    modified_at = sa.Column(
        sa.DateTime, nullable=False, default=sa.func.now(), onupdate=sa.func.now()
    )
