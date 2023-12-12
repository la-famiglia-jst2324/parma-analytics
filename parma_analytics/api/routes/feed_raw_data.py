from fastapi import APIRouter
from starlette import status
from datetime import datetime

from parma_analytics.api.models.feed_raw_data import (
    ApiFeedRawDataCreateIn,
    ApiFeedRawDataCreateOut,
)
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
def feed_raw_data(body: ApiFeedRawDataCreateIn) -> ApiFeedRawDataCreateOut:
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

    if not mapping_schemas:
        return_message += "However normalization schema cannot be found"
        latest_mapping_schema = NormalizationSchema(schema=None)
    else:
        # Get the latest mapping schema for now
        latest_mapping_schema = mapping_schemas[-1]

    normalized_data = normalize_data(
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
    # TODO: Write normalized_data to the PROD DB

    return ApiFeedRawDataCreateOut(
        return_message=return_message,
        source_name=body.source_name,
        timestamp=timestamp,
        document_id=saved_document.id,
        company_id=body.company_id,
        raw_data=body.raw_data,
    )
