from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest

from parma_analytics.db.prod.models.types import DataSource
from parma_analytics.sourcing.discovery.discovery_manager import (
    call_discover_endpoint,
    process_discovery_response,
)
from parma_analytics.sourcing.discovery.discovery_model import (
    DiscoveryQueryData,
    DiscoveryResponseModel,
)

# Mock data
mock_discovery_query_data = [DiscoveryQueryData(company_id="1", name="test")]
mock_discovery_response = {
    "identifiers": {"1": {"domain": ["example.com"], "name": ["example"]}},
    "validity": "2024-01-01T00:00:00",
}
mock_data_source = DataSource(
    id=1,
    source_name="Test Source",
    invocation_endpoint="https://testapi.com/discover",
    # Add other required fields
)


@pytest.fixture
def mock_requests_post():
    with patch("requests.post") as mock_post:
        yield mock_post


def test_call_discover_endpoint_success(mock_requests_post):
    mock_requests_post.return_value = MagicMock(
        status_code=200, json=MagicMock(return_value=mock_discovery_response)
    )

    result = call_discover_endpoint(mock_data_source, mock_discovery_query_data)

    expected_validity = datetime.strptime(
        str(mock_discovery_response["validity"]), "%Y-%m-%dT%H:%M:%S"
    )

    assert isinstance(result, DiscoveryResponseModel)
    assert result.identifiers == mock_discovery_response["identifiers"]
    assert result.validity == expected_validity


@patch(
    "parma_analytics.sourcing.discovery.discovery_manager.create_company_data_source_identifier_bll"
)
def test_process_discovery_response(mock_create_identifier):
    discovery_response = DiscoveryResponseModel(**mock_discovery_response)

    company_data_source_id = 1

    process_discovery_response(discovery_response, company_data_source_id)

    assert mock_create_identifier.call_count == len(
        discovery_response.identifiers["1"]["domain"]
    ) + len(discovery_response.identifiers["1"]["name"])
