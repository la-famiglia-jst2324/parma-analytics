"""FastAPI routes for receiving notifications when crawling job finishes."""

import json

from fastapi import APIRouter, status
from pydantic.json import pydantic_encoder

from parma_analytics.api.models.crawling_finished import (
    ApiCrawlingFinishedCreateIn,
    ApiCrawlingFinishedCreateOut,
)
from parma_analytics.bl.mining_module_manager import MiningModuleManager

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
    task_id: int = crawling_finished_data.task_id
    # TODO: When we introduce company level scheduling, this section will be updated
    result_summary: str | None = None
    if crawling_finished_data.errors is not None:
        errors_dict = {
            k: v.model_dump() for k, v in crawling_finished_data.errors.items()
        }
        result_summary = json.dumps(errors_dict, default=pydantic_encoder)

    MiningModuleManager.set_task_status_success_with_id(task_id, result_summary)

    return ApiCrawlingFinishedCreateOut(
        task_id=crawling_finished_data.task_id,
        errors=crawling_finished_data.errors,
        return_message="Notified about crawling finished",
    )
