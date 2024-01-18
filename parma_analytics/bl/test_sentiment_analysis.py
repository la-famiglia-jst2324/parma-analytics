"""Test the sentiment analysis function for comment measurement values."""

from datetime import datetime

from parma_analytics.bl.register_measurement_values import register_values
from parma_analytics.sourcing.normalization.normalization_model import NormalizedData

test_data = NormalizedData(
    source_measurement_id=1,
    company_id=1,
    value="Fast technical support always brings peace of mind",
    timestamp=datetime.now(),
    type="comment",
)

created_measurement_id = register_values(test_data)
