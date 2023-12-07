from fastapi import APIRouter
from starlette import status

from parma_analytics.api.models.feed_raw_data import (
    ApiFeedRawDataCreateIn,
    ApiFeedRawDataCreateOut,
)

router = APIRouter()


@router.post(
    "/feed-raw-data",
    status_code=status.HTTP_201_CREATED,
    description=""" Endpoint to receive raw data from data mining modules """,
)
def feed_raw_data(raw_data: ApiFeedRawDataCreateIn) -> ApiFeedRawDataCreateOut:
    return ApiFeedRawDataCreateOut(
        return_message="Raw data received", raw_data=raw_data.raw_data
    )
