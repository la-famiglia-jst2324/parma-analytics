"""FastAPI routes for receiving notifications when crawling job finishes."""

import json
import logging

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic.json import pydantic_encoder

from parma_analytics.api.dependencies.sourcing_auth import authorize_sourcing_request
from parma_analytics.api.models.crawling_finished import (
    ApiCrawlingFinishedCreateIn,
    ApiCrawlingFinishedCreateOut,
)
from parma_analytics.bl.mining_module_manager import MiningModuleManager

router = APIRouter()

logger = logging.getLogger(__name__)


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
    source_id: int = Depends(authorize_sourcing_request),
) -> ApiCrawlingFinishedCreateOut:
    """Endpoint to receive notifications when crawling job has completed.

    Args:
        crawling_finished_data: Contains details about the completed crawling job.
        source_id: The id of the module sending the notification.

    Returns:
        A simple receival confirmation message.
    """
    task_id: int = crawling_finished_data.task_id
    # TODO: When we introduce company level scheduling, this section will be updated
    result_summary: str | None = None
    if crawling_finished_data.errors is not None:
        errors_dict = {
            k: v.model_dump() for k, v in crawling_finished_data.errors.items()
        }
        result_summary = json.dumps(errors_dict, default=pydantic_encoder)

    try:
        MiningModuleManager.set_task_status_success_with_id(task_id, result_summary)
    except Exception as e:
        logger.error(f"Error setting task {task_id} status to success: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error setting task {task_id} status to success: {str(e)}",
        )

    return ApiCrawlingFinishedCreateOut(
        task_id=crawling_finished_data.task_id,
        errors=crawling_finished_data.errors,
        return_message="Notified about crawling finished",
    )
