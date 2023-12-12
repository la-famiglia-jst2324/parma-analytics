import asyncio
import json
import logging
from datetime import datetime

import httpx
from sqlalchemy.orm import Session

from parma_analytics.db.prod.engine import get_engine
from parma_analytics.db.prod.models.types import (
    ScheduledTasks,
    TaskStatus,
    CompanyDataSource,
    DataSource,
)

logger = logging.getLogger(__name__)


class MiningModuleManager:
    def __init__(self):
        self.session = Session(get_engine(), autocommit=False, autoflush=False)

    async def trigger_datasources(self, task_ids: list[int]) -> None:
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
                payload = self.construct_payload(data_source)
                json_payload = json.dumps(payload)

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

        self.session.close()
        await asyncio.gather(*trigger_tasks)

    def schedule_task(self, task: ScheduledTasks) -> ScheduledTasks | None:
        try:
            task.status = TaskStatus.PROCESSING
            task.locked_at = datetime.now()
            task.attempts += 1
            self.session.commit()
            logger.info(
                f"Task {task.task_id} successfully scheduled (data source {task.data_source.id})"
            )
            self.session.refresh(task)
            return task
        except Exception as e:
            logger.error(f"Error scheduling task {task.task_id}: {e}")
            self.session.rollback()

        return None

    def construct_payload(self, data_source: DataSource) -> dict:
        company_data_sources = (
            self.session.query(CompanyDataSource)
            .filter(CompanyDataSource.data_source_id == data_source.id)
            .all()
        )

        payload = {}
        if data_source.source_name == "Github":
            payload = {
                "companies": {
                    cds.company.name: ["sample_repo"] for cds in company_data_sources
                }
            }
        # TODO: add other data sources here

        return payload

    async def trigger(self, invocation_endpoint: str, json_payload: str) -> None:
        try:
            logger.debug(f"Sending request to {invocation_endpoint}")
            async with httpx.AsyncClient() as client:
                headers = {"Content-Type": "application/json"}
                response = await client.post(
                    invocation_endpoint, headers=headers, content=json_payload
                )
                response.raise_for_status()
        except httpx.RequestError as exc:
            logger.error(f"An error occurred while requesting {exc.request.url!r}.")
        except httpx.HTTPStatusError as exc:
            logger.error(
                f"Error response {exc.response.status_code} while requesting {exc.request.url!r}."
            )
        except Exception as exc:
            logger.error(f"An unexpected error occurred while sending request: {exc}")
