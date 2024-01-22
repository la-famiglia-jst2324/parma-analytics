from datetime import datetime

import pytest
from sqlalchemy import Column, DateTime, Float, Integer, String, create_engine
from parma_analytics.db.prod.engine import Base
from sqlalchemy.orm import sessionmaker

from parma_analytics.db.prod.aggregation_queries import (
    get_most_recent_measurement_values,
)

EXAMPLE_COMPANY_MEASUREMENT_ID = 1
EXAMPLE_VALUE = 100


# Define a mock table that mimics your actual table
class MockMeasurementValueType(Base):  # type: ignore
    """Represents a mock measurement value type.

    Attributes:
        id (int): The primary key of the measurement value type.
        company_measurement_id (int): The ID of the company measurement.
        value (int): The value of the measurement.
        timestamp (datetime): The timestamp of the measurement.
    """

    __tablename__ = "mock_measurement_value_type"
    id = Column(Integer, primary_key=True)
    company_measurement_id = Column(Integer)
    value = Column(Integer)
    timestamp = Column(DateTime)


class MockNotificationRule(Base):  # type: ignore
    """Represents a mock measurement value type.

    Attributes:
        id (int): The primary key of the measurement value type.
        company_measurement_id (int): The ID of the company measurement.
        value (int): The value of the measurement.
        timestamp (datetime): The timestamp of the measurement.
    """

    __tablename__ = "mock_notification_rules"
    rule_id = Column(Integer, primary_key=True)
    source_measurement_id = Column(Integer)
    threshold = Column(Float)
    aggregation_method = Column(String)
    num_aggregation_entries = Column(Integer)


@pytest.fixture
def mock_engine():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    return engine


@pytest.fixture
def mock_session(mock_engine):
    session_object = sessionmaker(bind=mock_engine)
    session = session_object()
    yield session
    session.close()


def test_get_most_recent_measurement_values_no_rule(mock_engine, mock_session):
    # Insert mock data into the database
    mock_data = MockMeasurementValueType(
        company_measurement_id=EXAMPLE_COMPANY_MEASUREMENT_ID,
        value=EXAMPLE_VALUE,  # Example value
        timestamp=datetime.now(),
    )
    mock_session.add(mock_data)
    mock_session.commit()

    # Mock parameters
    timestamp = datetime.now()
    company_measurement_id = 1

    result = get_most_recent_measurement_values(
        mock_engine, MockMeasurementValueType, timestamp, company_measurement_id
    )

    # Assert the expected outcome
    # Adjust the assertion based on the expected result
    assert result is not None
    assert result == EXAMPLE_VALUE


def test_get_most_recent_values_num_aggregation_entries(mock_engine, mock_session):
    # Insert mock data into the database
    mock_data = MockMeasurementValueType(
        company_measurement_id=EXAMPLE_COMPANY_MEASUREMENT_ID,
        value=EXAMPLE_VALUE,  # Example value
        timestamp=datetime.now(),
    )
    mock_session.add(mock_data)
    mock_session.commit()

    mock_notification_rules = MockNotificationRule(
        source_measurement_id=EXAMPLE_COMPANY_MEASUREMENT_ID,
        threshold=EXAMPLE_VALUE,
        aggregation_method="sum",
        num_aggregation_entries=1,
    )
    # Mock parameters
    timestamp = datetime.now()
    company_measurement_id = 1

    result = get_most_recent_measurement_values(
        mock_engine,
        MockMeasurementValueType,
        timestamp,
        company_measurement_id,
        mock_notification_rules,
    )

    # Assert the expected outcome
    # Adjust the assertion based on the expected result
    assert result is not None
    assert result == EXAMPLE_VALUE


def test_get_most_recent_values_without_num_aggregation_entries(
    mock_engine, mock_session
):
    # Insert mock data into the database
    mock_data = MockMeasurementValueType(
        company_measurement_id=EXAMPLE_COMPANY_MEASUREMENT_ID,
        value=EXAMPLE_VALUE,  # Example value
        timestamp=datetime.now(),
    )
    mock_session.add(mock_data)
    mock_session.commit()

    mock_notification_rules = MockNotificationRule(
        source_measurement_id=EXAMPLE_COMPANY_MEASUREMENT_ID,
        threshold=EXAMPLE_VALUE,
        aggregation_method="max",
    )
    # Mock parameters
    timestamp = datetime.now()
    company_measurement_id = 1

    result = get_most_recent_measurement_values(
        mock_engine,
        MockMeasurementValueType,
        timestamp,
        company_measurement_id,
        mock_notification_rules,
    )

    # Assert the expected outcome
    # Adjust the assertion based on the expected result
    assert result is not None
    assert result == EXAMPLE_VALUE
