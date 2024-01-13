"""Database queries for the reporting module."""


from typing import Literal

import polars as pl
import sqlalchemy as sa
from sqlalchemy import Engine
from sqlalchemy.orm.session import Session

from parma_analytics.db.prod.models.company_bucket_membership import (
    CompanyBucketMembership,
)
from parma_analytics.db.prod.models.company_subscription import CompanySubscription
from parma_analytics.db.prod.models.measurement_comment_value import (
    MeasurementCommentValue,
)
from parma_analytics.db.prod.models.measurement_float_value import MeasurementFloatValue
from parma_analytics.db.prod.models.measurement_int_value import MeasurementIntValue
from parma_analytics.db.prod.models.measurement_paragraph_value import (
    MeasurementParagraphValue,
)
from parma_analytics.db.prod.models.measurement_text_value import MeasurementTextValue
from parma_analytics.db.prod.models.notification_channel import NotificationChannel
from parma_analytics.db.prod.models.notification_subscription import (
    NotificationSubscription,
)


def fetch_user_ids_for_company(engine: Engine, company_id: int) -> list[int]:
    """Fetch user ids for a given company.

    Args:
        engine: database engine.
        company_id: id of the company.

    Returns:
        A list of user ids.
    """
    with Session(engine) as session:
        return (
            session.query(CompanySubscription.user_id)
            .where(CompanySubscription.company_id == company_id)
            .limit(50000)
            .all()
        )


def fetch_channel_ids(
    engine: Engine,
    user_ids: list[int],
    subscription_table: Literal["notification_subscription", "report_subscription"],
) -> list[int]:
    """Fetch channel ids for a given list of user ids.

    Args:
        engine: database engine.
        user_ids: list of user ids.
        subscription_table: name of the subscription table.

    Returns:
        A list of channel ids.
    """
    with Session(engine) as session:
        if subscription_table == "report_subscription":
            raise NotImplementedError
        table = NotificationSubscription
        return (
            session.query(table).where(table.user_id.in_(user_ids)).limit(50000).all()
        )


def fetch_notification_destinations(
    engine: Engine, channel_ids: list[int], service_type: str
) -> list[str]:
    """Fetch notification destinations for a given list of channel ids.

    Args:
        engine: database engine.
        channel_ids: list of channel ids.
        service_type: type of the service.

    Returns:
        A list of notification destinations.
    """
    with Session(engine) as session:
        return (
            session.query(NotificationChannel.destination)
            .where(
                NotificationChannel.id.in_(channel_ids),
                NotificationChannel.channel_type == service_type.upper(),
            )
            .all()
        )


def fetch_company_id_from_bucket(engine: Engine, bucket_id: int) -> int:
    """Fetch company id for a given bucket id.

    Args:
        engine: database engine.
        bucket_id: id of the bucket.

    Returns:
        A company id.
    """
    with Session(engine) as session:
        return session.query(CompanyBucketMembership.company_id).where(
            CompanyBucketMembership.bucket_id == bucket_id
        )


def fetch_measurement_data(
    engine: Engine, measurement_ids: list, measurement_table: str
) -> pl.DataFrame:
    """Fetch measurement data from the database.

    Args:
        engine: database engine.
        measurement_ids: list of measurement ids.
        measurement_table: name of the table containing the measurement data.

    Returns:
        A DataFrame containing the measurement data.
    """
    table = (
        MeasurementIntValue
        if measurement_table == "measurement_int_value"
        else (
            MeasurementFloatValue
            if measurement_table == "measurement_float_value"
            else (
                MeasurementTextValue
                if measurement_table == "measurement_text_value"
                else (
                    MeasurementParagraphValue
                    if measurement_table == "measurement_paragraph_value"
                    else MeasurementCommentValue
                )
            )
        )
    )

    query = (
        sa.select(table.company_measurement_id, table.value, table.created_at)  # type: ignore
        .where(table.company_measurement_id.in_(measurement_ids))  # type: ignore
        .order_by(table.created_at.desc())  # type: ignore
        .compile(engine)
    )
    return pl.read_database(query, connection=engine)
