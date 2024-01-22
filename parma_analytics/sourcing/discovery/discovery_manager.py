"""Providing discovery functionality interfacing with data source modules."""

import json
import logging

import requests

from parma_analytics.bl.company_bll import get_company_id_bll
from parma_analytics.bl.company_data_source_bll import (
    get_company_data_source_bll,
)
from parma_analytics.bl.company_data_source_identifiers_bll import (
    create_company_data_source_identifier_bll,
    delete_company_data_source_identifier_bll,
    get_company_data_source_identifiers_bll,
)
from parma_analytics.bl.data_source_helper import ensure_appropriate_scheme
from parma_analytics.db.prod.company_data_source_identifiers_query import IdentifierData
from parma_analytics.db.prod.models.company_data_source_identifier import IdentifierType
from parma_analytics.db.prod.models.types import DataSource
from parma_analytics.sourcing.discovery.discovery_model import (
    DiscoveryQueryData,
    DiscoveryResponseModel,
)
from parma_analytics.utils.jwt_handler import JWTHandler

logger = logging.getLogger(__name__)


def call_discover_endpoint(
    data_source: DataSource, query_data: list[DiscoveryQueryData]
) -> DiscoveryResponseModel:
    """Call the discovery of the module to store the identifiers in the db."""
    invocation_endpoint = ensure_appropriate_scheme(data_source.invocation_endpoint)
    if not invocation_endpoint:
        logger.error(
            f"Invalid invocation endpoint: "
            f"{data_source.invocation_endpoint} "
            f"for data source {data_source.id}"
        )

    token: str = JWTHandler.create_jwt(data_source.id)
    header = {"Authorization": f"Bearer {token}"}

    request_payload = json.dumps([query.model_dump() for query in query_data])

    try:
        response = requests.post(
            f"{invocation_endpoint}/discover", data=request_payload, headers=header
        )
        response.raise_for_status()

        response_data = response.json()
        logger.debug(f"Discovery response: {response_data}")

        return DiscoveryResponseModel(**response_data)

    except requests.RequestException as e:
        logger.error(
            f"Request error happened for "
            f"data source {data_source.id} "
            f"while calling discovery endpoint: {e}"
        )
        raise e
    except Exception as e:
        logger.error(
            f"Unexpected error happened for "
            f"data source {data_source.id} "
            f"while calling discovery endpoint: {e}"
        )
        raise e


def process_discovery_response(
    discovery_response: DiscoveryResponseModel, company_data_source_id: int
):
    """Process discovery response and store identifiers in db."""
    for company_id, data in discovery_response.identifiers.items():
        for property_key, values in data.items():
            for value in values:
                identifier_data = IdentifierData(
                    company_data_source_id=company_data_source_id,
                    identifier_type=IdentifierType.AUTOMATICALLY_DISCOVERED,
                    property=property_key,
                    value=value,
                    validity=discovery_response.validity,
                )
                create_company_data_source_identifier_bll(identifier_data)


def rediscover_identifiers(data_source: DataSource, company_id: int):
    """Rediscover identifiers for a company and update them in the database."""
    company_entity = get_company_id_bll(company_id)

    # Prepare discovery query data
    query_data = [DiscoveryQueryData(company_id=company_id, name=company_entity.name)]

    discovery_response = call_discover_endpoint(data_source, query_data)
    company_data_source = get_company_data_source_bll(company_id, data_source.id)

    existing_identifiers = get_company_data_source_identifiers_bll(
        company_id, data_source.id
    )

    # Delete old identifiers that are not manually added
    if existing_identifiers:
        for identifier in existing_identifiers:
            if identifier.identifier_type != IdentifierType.MANUALLY_ADDED:
                delete_company_data_source_identifier_bll(identifier.id)

    if company_data_source:
        process_discovery_response(discovery_response, company_data_source.id)
