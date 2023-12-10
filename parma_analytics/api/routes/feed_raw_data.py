from fastapi import APIRouter
from starlette import status
from datetime import datetime

from parma_analytics.api.models.feed_raw_data import (
    ApiFeedRawDataCreateIn,
    ApiFeedRawDataCreateOut,
)
from parma_analytics.db.mining.models import RawDataIn
from parma_analytics.db.mining.service import (
    read_raw_data_by_id,
    read_raw_data_by_company,
    store_raw_data,
)

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

    return ApiFeedRawDataCreateOut(
        return_message="Raw data received and saved",
        source_name=body.source_name,
        timestamp=datetime.now(),
        document_id=saved_document.id,
        company_id=body.company_id,
        raw_data=body.raw_data,
    )
