"""FastAPI routes for establishing a trust relationship with a new data source."""

import json
from ast import literal_eval
from http import HTTPStatus

import requests
from fastapi import APIRouter, HTTPException, status

from parma_analytics.api.models.data_source_handshake import (
    ApiDataSourceHandshakeOut,
)
from parma_analytics.db.mining.service import (
    NormalizationSchemaIn,
    store_normalization_schema,
)

router = APIRouter()


@router.get(
    "/handshake",
    status_code=status.HTTP_200_OK,
    description="Endpoint to ensure that the data module is functioning properly.",
)
def perform_handshake(
    invocation_endpoint: str,
    data_source_id: int,
) -> ApiDataSourceHandshakeOut:
    """Establishes a trust relationship with a new data source.

    The handshake validates the liveness of the data source and verifies that
    the authenticated frontend user added the necessary information required
    for sourcing module runs.
    Furthermore, the normalization schema exchanged and stored in the database.

    Args:
        invocation_endpoint: The endpoint of the data source.
        data_source_id: The ID of the data source.

    Returns:
        The result of the handshake containing frequency information.
    """
    if not invocation_endpoint.startswith(
        "http://"
    ) and not invocation_endpoint.startswith("https://"):
        invocation_endpoint = "https://" + invocation_endpoint

    try:
        response = requests.get(
            f"{invocation_endpoint}/initialize", params={"source_id": data_source_id}
        )
        if response.status_code != HTTPStatus.OK:
            raise HTTPException(
                status_code=502, detail="Failed to initialize the data source"
            )

        response_json = response.json()

        # Check if response_json is a string and convert it to a dictionary if necessary
        if isinstance(response_json, str):
            response_json = json.loads(response_json)

        frequency = response_json.get("frequency")
        normalization_map = response_json.get("normalization_map")
        normalization_map = literal_eval(normalization_map)
        data_source = normalization_map.get("Source")
        normalization_map_in = NormalizationSchemaIn(schema=normalization_map)

        store_normalization_schema(data_source, normalization_map_in)

        return ApiDataSourceHandshakeOut(frequency=frequency)
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        # Generic exception handler for any other types of exceptions
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
