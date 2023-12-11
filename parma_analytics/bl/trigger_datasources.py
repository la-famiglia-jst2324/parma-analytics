import asyncio
import logging
from datetime import datetime

import httpx
from sqlalchemy.orm import Session

from parma_analytics.db.prod.engine import get_engine
from parma_analytics.db.prod.models.types import ScheduledTasks, TaskStatus

logger = logging.getLogger(__name__)


async def trigger_datasources(task_ids: list[int]) -> None:
    """Async Function to trigger mining modules."""

    logger.info(f"Triggering mining modules for task_ids {task_ids}")

    session = Session(get_engine(), autocommit=False, autoflush=False)
    trigger_tasks = []

    for task_id in task_ids:
        try:
            logger.info(f"Triggering mining module for task_id {task_id}")
            session.begin_nested()
            # Query and Try to Lock the task based on task_id
            task: ScheduledTasks | None = (
                session.query(ScheduledTasks)
                .filter(ScheduledTasks.task_id == task_id)
                .with_for_update()
                .first()
            )
            if not task:
                logger.error(f"Task with id {task_id} not found.")
                # TODO: This can not happen! Handle this case
                continue

            task = schedule_task(session, task)
            if not task:
                logger.error(f"Error scheduling task {task_id}")
                continue

            # Get the data source
            data_source = task.data_source

            invocation_endpoint: str = data_source.invocation_endpoint

            # TODO: Use the additional_params & version as well

            trigger_task = asyncio.create_task(trigger(invocation_endpoint))
            trigger_tasks.append(trigger_task)

        except Exception as e:
            logger.error(f"Error triggering mining module for task_id {task_id}: {e}")
            session.rollback()
            continue

    session.close()
    # TODO: Implement better error handling

    # Wait for all the tasks to complete
    await asyncio.gather(*trigger_tasks)


def schedule_task(session: Session, task: ScheduledTasks) -> ScheduledTasks | None:
    """Function to (re)schedule a task for processing."""
    try:
        task.status = TaskStatus.PROCESSING
        task.locked_at = datetime.now()
        task.attempts += 1
        session.commit()
        logger.info(
            f"Task {task.task_id} successfully processed (data source {task.data_source.id})"
        )
        session.refresh(task)
        return task
    except Exception as e:
        logger.error(f"Error scheduling task {task.task_id}: {e}")
        session.rollback()

    return None


async def trigger(invocation_endpoint: str) -> None:
    """Function to send request to the data source."""
    try:
        logger.debug(f"Sending request to {invocation_endpoint}")
        with httpx.Client() as client:
            # TODO: Add authentication
            # TODO: Add payload (??)
            response = client.get(invocation_endpoint)
            # Check if the response is successful (status code 200-299)
            response.raise_for_status()
            # TODO: Handle the response
    except httpx.RequestError as exc:
        # Network Issues
        logger.error(f"An error occurred while requesting {exc.request.url!r}.")
    except httpx.HTTPStatusError as exc:
        # HTTP errors (404 Not Found, 500 Server Error, etc)
        logger.error(
            f"Error response {exc.response.status_code} while requesting {exc.request.url!r}."
        )
    except Exception as exc:
        logger.error(
            f"An unexpected error occurred while sending request to data source: {exc}"
        )
