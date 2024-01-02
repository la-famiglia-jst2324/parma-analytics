"""FastAPI routes for scheduling the invocation of mining modules."""

import logging

from fastapi import APIRouter, BackgroundTasks, Response, status

from parma_analytics.bl.schedule_manager import ScheduleManager
from parma_analytics.db.prod.engine import get_engine

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get(
    "/schedule",
    status_code=status.HTTP_200_OK,
    description="Endpoint to schedule the data mining modules.",
)
async def schedule(background_tasks: BackgroundTasks) -> Response:
    """Trigger a background task to schedule the data mining modules.

    Args:
        background_tasks: The background tasks to schedule set up by fastapi.

    Returns:
        HTTP acknowledgement.
    """
    logger.info("/schedule endpoint called. Scheduling will start in the background.")
    background_tasks.add_task(_schedule_tasks)
    return Response(status_code=status.HTTP_200_OK)


# ------------------------------------------------------------------------------------ #
#                                       Internal                                       #
# ------------------------------------------------------------------------------------ #


def _schedule_tasks() -> None:
    """Wrapper function to schedule the data mining modules."""
    with ScheduleManager(get_engine()) as schedule_manager:
        schedule_manager.schedule_tasks()
