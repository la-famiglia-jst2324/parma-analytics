"""Database queries for the reporting module."""


import polars as pl
import sqlalchemy as sa
from sqlalchemy.engine import Engine
from sqlalchemy.orm.session import Session

from parma_analytics.db.prod.models.measurement_value_models import (
    MeasurementCommentValue,
    MeasurementDateValue,
    MeasurementFloatValue,
    MeasurementImageValue,
    MeasurementIntValue,
    MeasurementLinkValue,
    MeasurementNestedValue,
    MeasurementParagraphValue,
    MeasurementTextValue,
    MeasurementValueModels,
)
from parma_analytics.db.prod.models.notification_channel import NotificationChannel
from parma_analytics.db.prod.models.notification_subscription import (
    NotificationSubscription,
)


def fetch_channel_ids(engine: Engine, user_ids: list[int]) -> list[int]:
    """Fetch channel ids for a given list of user ids.

    Args:
        engine: database engine.
        user_ids: list of user ids.

    Returns:
        A list of channel ids.
    """
    with Session(engine) as session:
        results = (
            session.query(NotificationSubscription.channel_id)
            .where(NotificationSubscription.user_id.in_(user_ids))
            .limit(50000)
            .all()
        )
        return [channel_id for (channel_id,) in results]


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
        results = (
            session.query(NotificationChannel.destination)
            .where(
                NotificationChannel.id.in_(channel_ids),
                NotificationChannel.channel_type == service_type.upper(),
            )
            .all()
        )
        return [destination for (destination,) in results]


def fetch_slack_destinations(engine: Engine, channel_ids: list[int]):
    """Fetch slack destinations for a given list of channel ids.

    Args:
        engine: database engine.
        channel_ids: list of channel ids.
        service_type: type of the service.

    Returns:
        A list of slack destinations.
    """
    with Session(engine) as session:
        results = (
            session.query(
                NotificationChannel.destination, NotificationChannel.secret_id
            )
            .where(
                NotificationChannel.id.in_(channel_ids),
                NotificationChannel.channel_type == "SLACK",
            )
            .all()
        )
        return results


__TableModels: dict[str, type[MeasurementValueModels]] = {
    "measurement_int_value": MeasurementIntValue,
    "measurement_float_value": MeasurementFloatValue,
    "measurement_text_value": MeasurementTextValue,
    "measurement_paragraph_value": MeasurementParagraphValue,
    "measurement_comment_value": MeasurementCommentValue,
    "measurement_link_value": MeasurementLinkValue,
    "measurement_image_value": MeasurementImageValue,
    "measurement_date_value": MeasurementDateValue,
    "measurement_nested_value": MeasurementNestedValue,
}


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
    table = __TableModels[measurement_table]

    query = (
        sa.select(table.company_measurement_id, table.value, table.created_at)
        .where(table.company_measurement_id.in_(measurement_ids))
        .order_by(table.created_at.desc())
        .compile(engine)
    )
    return pl.read_database(query, connection=engine)


def fetch_recent_value(
    engine: Engine, company_measurement_id: int, measurement_table: str
):
    """Fetch the most recent value from measurement_tables.

    Args:
        engine: database engine.
        company_measurement_id: value of company measurement ids.
        measurement_table: name of the table containing the measurement data.

    Returns:
        dict: A dictionary containing the most recent value and timestamp.
    """
    table = __TableModels[measurement_table]
    with Session(engine) as session:
        most_recent_entry = (
            session.query(table)
            .filter(table.company_measurement_id == company_measurement_id)
            .order_by(sa.desc(table.timestamp))
            .first()
        )

        return {
            "value": most_recent_entry.value,
            "timestamp": most_recent_entry.timestamp,
        }
