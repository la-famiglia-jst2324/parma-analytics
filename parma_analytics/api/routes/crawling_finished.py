"""FastAPI routes for receiving notifications when crawling job finishes."""

from fastapi import APIRouter, Depends
from starlette import status

from parma_analytics.api.dependencies.sourcing_auth import authorize_sourcing_request
from parma_analytics.api.models.crawling_finished import (
    ApiCrawlingFinishedCreateIn,
    ApiCrawlingFinishedCreateOut,
)

router = APIRouter()


@router.post(
    "/crawling-finished",
    status_code=status.HTTP_201_CREATED,
    description=(
        "Endpoint to receive notifications when all crawling jobs have completed. "
        "This allows the system to proceed with data processing once all data has "
        "been gathered."
    ),
)
def crawling_finished(
    done_message: ApiCrawlingFinishedCreateIn,
    source_id: int = Depends(authorize_sourcing_request),
) -> ApiCrawlingFinishedCreateOut:
    """Endpoint to receive notifications when crawling job has completed.

    Args:
        done_message: The status indicating the terminal state of the crawling job.
        source_id: The id of the module sending the notification.

    Returns:
        A simple receival confirmation message.
    """
    return ApiCrawlingFinishedCreateOut(
        incoming_message=done_message.incoming_message,
        return_message="Notified about crawling finished",
    )
