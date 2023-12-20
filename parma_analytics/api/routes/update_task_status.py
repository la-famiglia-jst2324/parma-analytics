"""FastAPI routes for updating the task's status."""

from fastapi import APIRouter, Depends, status

from parma_analytics.api.dependencies.sourcing_auth import authorize_sourcing_request
from parma_analytics.api.models.update_task_status import (
    ApiUpdateTaskStatusCreateIn,
    ApiUpdateTaskStatusCreateOut,
)
from parma_analytics.bl.mining_module_manager import MiningModuleManager

router = APIRouter()


@router.put(
    "/update-task-status",
    status_code=status.HTTP_200_OK,
    description=("Endpoint to update task's status."),
)
def update_task_status(
    task_information: ApiUpdateTaskStatusCreateIn,
    source_id: int = Depends(authorize_sourcing_request),
) -> ApiUpdateTaskStatusCreateOut:
    """Update task's status and result summary (if any).

    Args:
        task_information: The task information to update.
        source_id: The id of the data source.

    Returns:
        A simple confirmation message.
    """
    task_id: int = task_information.task_id
    status: str = task_information.status
    result_summary: str | None = task_information.result_summary

    updated: bool = False

    if status.lower() == "success":
        updated = MiningModuleManager.set_task_status_success_with_id(
            task_id, result_summary
        )

    return ApiUpdateTaskStatusCreateOut(updated=updated)
