"""Providing discovery functionality interfacing with data source modules."""

import json
import logging

import requests

from parma_analytics.bl.company_data_source_identifiers_bll import (
    create_company_data_source_identifier_bll,
)
from parma_analytics.db.prod.company_data_source_identifiers_query import IdentifierData
from parma_analytics.db.prod.models.company_data_source_identifier import IdentifierType
from parma_analytics.sourcing.discovery.discovery_model import (
    DiscoveryQueryData,
    DiscoveryResponseModel,
)
from parma_analytics.utils.jwt_handler import JWTHandler

logger = logging.getLogger(__name__)


def call_discover_endpoint(
    invocation_endpoint: str, data_source_id: int, query_data: list[DiscoveryQueryData]
) -> DiscoveryResponseModel:
    """Call the discovery of the module to store the identifiers in the db."""
    if not invocation_endpoint.startswith(
        "http://"
    ) and not invocation_endpoint.startswith("https://"):
        invocation_endpoint = "https://" + invocation_endpoint

    token: str = JWTHandler.create_jwt(data_source_id)
    header = {"Authorization": f"Bearer {token}"}

    request_payload = json.dumps([query.dict() for query in query_data])

    try:
        response = requests.post(
            f"{invocation_endpoint}/discover", data=request_payload, headers=header
        )
        response.raise_for_status()

        response_data = response.json()
        logger.debug(f"Discovery response: {response_data}")

        return DiscoveryResponseModel(**response_data)

    except requests.RequestException as e:
        logger.error(f"Request error: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise


def process_discovery_response(discovery_response: DiscoveryResponseModel):
    """Process discovery response and store identifiers in db."""
    for company_id, data in discovery_response.identifiers.items():
        for property_key, values in data.items():
            for value in values:
                identifier_data = IdentifierData(
                    company_data_source_id=1,  # Hardcoded for now
                    identifier_key=value,
                    identifier_type=IdentifierType.AUTOMATICALLY_DISCOVERED,
                    property=property_key,
                    value=value,
                    validity=discovery_response.validity,
                )
                create_company_data_source_identifier_bll(identifier_data)
