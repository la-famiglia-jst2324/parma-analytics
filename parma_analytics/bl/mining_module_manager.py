"""Manage the interaction with the mining modules."""

import asyncio
import json
import logging
import urllib.parse
from contextlib import contextmanager
from datetime import datetime
from typing import Any, cast

import httpx
from sqlalchemy.orm import Session

from parma_analytics.bl.mining_trigger_payloads import GITHUB_PAYLOAD, REDDIT_PAYLOAD
from parma_analytics.db.prod.engine import get_engine
from parma_analytics.db.prod.models.types import (
    DataSource,
    ScheduledTask,
)
from parma_analytics.utils.jwt_handler import JWTHandler

logger = logging.getLogger(__name__)


class MiningModuleManager:
    """Manage the interaction with the mining modules."""

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
    @staticmethod
    def set_task_status_success_with_id(
        task_id: int, result_summary: str | None
    ) -> bool:
        """Set the status of the task with the given task_id to success."""
        with MiningModuleManager._manage_session() as session:
            try:
                session.begin_nested()
                task = (
                    session.query(ScheduledTask)
                    .filter(ScheduledTask.task_id == task_id)
                    .with_for_update()
                    .first()
                )
                if not task:
                    logger.error(f"Task with id {task_id} not found.")
                    return False

                task.status = "SUCCESS"
                task.ended_at = datetime.now()
                task.result_summary = result_summary or ""
                session.commit()
                logger.info(f"Task {task.task_id} successfully completed")
                return True
            except Exception as e:
                logger.error(f"Error setting task {task_id} status to success: {e}")
                session.rollback()

        return False

    def trigger_datasources(self, task_ids: list[int]) -> None:
        """Trigger the mining modules for the given task_ids.

        Read only db access.
        """
        logger.info(f"Triggering mining modules for task_ids {task_ids}")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        trigger_tasks = []

        for task_id in task_ids:
            try:
                self.session.begin_nested()
                logger.info(f"Triggering mining module for task_id {task_id}")
                task = (
                    self.session.query(ScheduledTask)
                    .filter(ScheduledTask.task_id == task_id)
                    .with_for_update()
                    .first()
                )
                if not task:
                    logger.error(f"Task with id {task_id} not found.")
                    continue

                task = self._schedule_task(task)
                if not task:
                    logger.error(f"Error scheduling task {task_id}")
                    continue

                data_source = cast(DataSource, task.data_source)
                json_payload = self._construct_payload(data_source)
                logger.debug(
                    f"Payload for data source {data_source.id}: {json_payload}"
                )

                invocation_endpoint: str = data_source.invocation_endpoint
                if not invocation_endpoint:
                    logger.error(
                        f"Invocation endpoint not found "
                        f"for data source {data_source.id}"
                    )
                    continue

                trigger_endpoint: str = urllib.parse.urljoin(
                    invocation_endpoint, "/companies"
                )

                data_source_id: int = data_source.id

                trigger_task = loop.create_task(
                    self._trigger(data_source_id, trigger_endpoint, json_payload)
                )
                trigger_tasks.append(trigger_task)

            except Exception as e:
                logger.error(
                    f"Error triggering mining module for task_id {task_id}: {e}"
                )
                self.session.rollback()
                continue

        if len(trigger_tasks) > 0:
            loop.run_until_complete(asyncio.gather(*trigger_tasks))

        loop.close()

    # ------------------------------ Internal functions ------------------------------ #

    @staticmethod
    @contextmanager
    def _manage_session():
        """Context manager for database session.

        This context manager is used for the static methods of this class.
        """
        session = Session(get_engine(), autocommit=False, autoflush=False)
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def _schedule_task(self, task: ScheduledTask) -> ScheduledTask | None:
        """Schedule the given task before triggering module."""
        try:
            task.started_at = datetime.now()
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

    def _construct_payload(self, data_source: DataSource) -> str | None:
        """Construct the payload for the given data source."""
        json_payload = None
        if data_source.source_name == "affinity":
            # For the Affinity module, we only have  GET /companies with no body
            pass
        elif data_source.source_name == "github":
            logger.warn("Github payload not implemented yet.")
            json_payload = json.dumps(GITHUB_PAYLOAD)
        elif data_source.source_name == "reddit":
            logger.warn("Reddit payload not implemented yet.")
            json_payload = json.dumps(REDDIT_PAYLOAD)
        else:
            logger.warn("Other payload not implemented yet.")
            pass

        return json_payload

    async def _trigger(
        self, data_source_id: int, invocation_endpoint: str, json_payload: str | None
    ) -> None:
        """Trigger the mining module for the given invocation endpoint and payload."""
        try:
            logger.debug(f"Sending request to {invocation_endpoint}")
            async with httpx.AsyncClient(verify=False) as client:
                token: str = JWTHandler.create_jwt(data_source_id)
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {token}",
                }
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
