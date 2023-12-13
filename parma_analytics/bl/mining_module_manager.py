import asyncio
import json
import logging
from datetime import datetime
from typing import Any

import httpx
from sqlalchemy.orm import Session

from parma_analytics.db.prod.engine import get_engine
from parma_analytics.db.prod.models.types import (
    CompanyDataSource,
    DataSource,
    ScheduledTasks,
)

logger = logging.getLogger(__name__)


class MiningModuleManager:
    # --------------------------- Context manager functions -------------------------- #

    def __init__(self):
        self.session = Session(get_engine(), autocommit=False, autoflush=False)

    def __enter__(self):
        """Enter the context manager."""
        return self

    def __exit__(self, *args: tuple[Any, ...], **kwargs: dict[str, Any]):
        """Exit the context manager.

        Close the session.
        """
        self.session.close()

    # ------------------------------- Public functions ------------------------------- #

    def set_task_status_success(self, task_id: int) -> bool:
        """Set the status of the task with the given task_id to success."""
        try:
            self.session.begin_nested()
            task = (
                self.session.query(ScheduledTasks)
                .filter(ScheduledTasks.task_id == task_id)
                .with_for_update()
                .first()
            )
            if not task:
                logger.error(f"Task with id {task_id} not found.")
                return False

            task.status = "SUCCESS"
            task.completed_at = datetime.now()
            self.session.commit()
            logger.info(f"Task {task.task_id} successfully completed")
            return True
        except Exception as e:
            logger.error(f"Error setting task {task_id} status to success: {e}")
            self.session.rollback()

        return False

    async def trigger_datasources(self, task_ids: list[int]) -> None:
        """Trigger the mining modules for the given task_ids."""
        logger.info(f"Triggering mining modules for task_ids {task_ids}")

        trigger_tasks = []

        for task_id in task_ids:
            try:
                logger.info(f"Triggering mining module for task_id {task_id}")
                self.session.begin_nested()
                task = (
                    self.session.query(ScheduledTasks)
                    .filter(ScheduledTasks.task_id == task_id)
                    .with_for_update()
                    .first()
                )
                if not task:
                    logger.error(f"Task with id {task_id} not found.")
                    continue

                task = self.schedule_task(task)
                if not task:
                    logger.error(f"Error scheduling task {task_id}")
                    continue

                data_source = task.data_source
                json_payload = self.construct_payload(data_source)
                logger.debug(
                    f"Payload for data source {data_source.id}: {json_payload}"
                )

                invocation_endpoint = data_source.invocation_endpoint
                trigger_task = asyncio.create_task(
                    self.trigger(invocation_endpoint, json_payload)
                )
                trigger_tasks.append(trigger_task)

            except Exception as e:
                logger.error(
                    f"Error triggering mining module for task_id {task_id}: {e}"
                )
                self.session.rollback()
                continue

        await asyncio.gather(*trigger_tasks)

    # ------------------------------ Internal functions ------------------------------ #

    def schedule_task(self, task: ScheduledTasks) -> ScheduledTasks | None:
        """Schedule the given task before triggering module."""
        try:
            task.status = "PROCESSING"
            task.locked_at = datetime.now()
            task.attempts += 1
            self.session.commit()
            logger.info(
                f"Task {task.task_id} scheduled (data source {task.data_source.id})"
            )
            self.session.refresh(task)
            return task
        except Exception as e:
            logger.error(f"Error scheduling task {task.task_id}: {e}")
            self.session.rollback()

        return None

    def construct_payload(self, data_source: DataSource) -> str | None:
        """Construct the payload for the given data source."""
        company_data_sources = (
            self.session.query(CompanyDataSource)
            .filter(CompanyDataSource.data_source_id == data_source.id)
            .all()
        )

        json_payload = None
        if data_source.source_name == "affinity":
            # For the Affinity module, we only have  GET /companies with no body
            pass
        else:
            github_payload = {
                "companies": {
                    cds.company.name: {
                        "domain": [cds.company.name],
                        "name": [cds.company.name],
                    }
                    for cds in company_data_sources
                }
            }
            json_payload = json.dumps(github_payload)

        return json_payload

    async def trigger(self, invocation_endpoint: str, json_payload: str | None) -> None:
        """Trigger the mining module for the given invocation endpoint and payload."""
        try:
            logger.debug(f"Sending request to {invocation_endpoint}")
            async with httpx.AsyncClient(verify=False) as client:
                headers = {"Content-Type": "application/json"}
                response = None
                if json_payload is None:
                    response = await client.get(
                        invocation_endpoint, headers=headers, timeout=None
                    )
                else:
                    response = await client.post(
                        invocation_endpoint,
                        headers=headers,
                        content=json_payload,
                        timeout=None,
                    )
                response.raise_for_status()
        except httpx.RequestError as exc:
            logger.error(
                f"An error occurred while requesting {exc.request.url!r}. Err: {exc}"
            )
        except httpx.HTTPStatusError as exc:
            logger.error(
                f"Error response {exc.response.status_code} while "
                f"requesting {exc.request.url!r}."
            )
        except Exception as exc:
            logger.error(f"An unexpected error occurred while sending request: {exc}")
