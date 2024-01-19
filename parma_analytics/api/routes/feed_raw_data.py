"""FastAPI routes for establishing a trust relationship with a new data source."""

from datetime import datetime

from fastapi import APIRouter, Depends
from starlette import status

from parma_analytics.api.dependencies.sourcing_auth import authorize_sourcing_request
from parma_analytics.api.models.feed_raw_data import (
    ApiFeedRawDataCreateIn,
    ApiFeedRawDataCreateOut,
)
from parma_analytics.bl.create_company_bll import create_company_if_not_exist_bll
from parma_analytics.db.mining.models import NormalizationSchema, RawData, RawDataIn
from parma_analytics.db.mining.service import (
    read_normalization_schema_by_datasource,
    store_raw_data,
)
from parma_analytics.sourcing.normalization.normalization_engine import normalize_data

router = APIRouter()


@router.post(
    "/feed-raw-data",
    status_code=status.HTTP_201_CREATED,
    description=""" Endpoint to receive raw data from data mining modules """,
)
def feed_raw_data(
    body: ApiFeedRawDataCreateIn,
    source_id: int = Depends(authorize_sourcing_request),
) -> ApiFeedRawDataCreateOut:
    """Feed raw data from data mining modules to data normalization modules.

    Args:
        body: The raw data to be normalized.
        source_id: The id of the data source.

    Returns:
        Acknowledgement message containing the raw data and the timestamp.
    """
    saved_document = store_raw_data(
        datasource=body.source_name,
        raw_data=RawDataIn(
            mining_trigger="",
            status="success",
            company_id=body.company_id,
            data=body.raw_data,
        ),
    )
    timestamp = datetime.now()
    return_message = "Raw data received and saved. "

    mapping_schemas = read_normalization_schema_by_datasource(body.source_name)

    if not mapping_schemas or len(mapping_schemas) == 0:
        return_message += "However normalization schema cannot be found"
        latest_mapping_schema = NormalizationSchema(
            schema=None, id="", create_time=timestamp, update_time=None, read_time=None
        )
    else:
        # Get the latest mapping schema for now
        latest_mapping_schema = mapping_schemas[-1]

    _ = normalize_data(
        raw_data=RawData(
            mining_trigger="",
            status="success",
            company_id=body.company_id,
            data=body.raw_data,
            create_time=timestamp,
            id="",
            update_time=None,
            read_time=None,
        ),
        mapping_schema=latest_mapping_schema,
    )

    # Check if the module is affinity and if so,
    # save the company name to the company table if it does not exist
    if body.source_name == "affinity":
        create_company_if_not_exist_bll(
            body.raw_data["name"], body.raw_data["domain"], 1
        )

    return ApiFeedRawDataCreateOut(
        return_message=return_message,
        source_name=body.source_name,
        timestamp=timestamp,
        document_id=saved_document.id,
        company_id=body.company_id,
        raw_data=body.raw_data,
    )
