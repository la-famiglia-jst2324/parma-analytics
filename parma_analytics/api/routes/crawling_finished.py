"""FastAPI routes for receiving notifications when crawling job finishes."""

from fastapi import APIRouter
from starlette import status

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
    crawling_finished_data: ApiCrawlingFinishedCreateIn,
) -> ApiCrawlingFinishedCreateOut:
    """Endpoint to receive notifications when crawling job has completed.

    Args:
        crawling_finished_data: Contains details about the completed crawling job.

    Returns:
        A simple receival confirmation message.
    """
    return ApiCrawlingFinishedCreateOut(
        task_id=crawling_finished_data.task_id,
        errors=crawling_finished_data.errors,
        return_message="Notified about crawling finished",
    )
