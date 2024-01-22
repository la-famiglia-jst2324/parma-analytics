"""Manage the interaction with the mining modules."""

import asyncio
import logging
import urllib.parse
from contextlib import contextmanager
from datetime import datetime
from typing import Any, cast

import httpx
from sqlalchemy.orm import Session

from parma_analytics.bl.company_bll import get_company_id_bll
from parma_analytics.bl.company_data_source_bll import (
    get_all_by_data_source_id_bll,
)
from parma_analytics.bl.company_data_source_identifiers_bll import (
    get_company_data_source_identifiers_bll,
)
from parma_analytics.bl.data_source_helper import ensure_appropriate_scheme
from parma_analytics.bl.scraping_model import ScrapingPayloadModel
from parma_analytics.db.prod.engine import get_engine
from parma_analytics.db.prod.models.company_data_source import CompanyDataSource
from parma_analytics.db.prod.models.types import (
    DataSource,
    ScheduledTask,
)
from parma_analytics.sourcing.discovery.discovery_manager import (
    call_discover_endpoint,
    process_discovery_response,
    rediscover_identifiers,
)
from parma_analytics.sourcing.discovery.discovery_model import DiscoveryQueryData
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
    ) -> None:
        """Set the status of the task with the given task_id to success.

        Args:
            task_id: The ID of the task.
            result_summary: A summary of the result, if any.

        Raises:
            Exception: If the task can not be found
            Exception: If there's an error updating the task.
        """
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
                    raise Exception("Task not found!")

                task.status = "SUCCESS"
                task.ended_at = datetime.now()
                task.result_summary = result_summary or ""
                session.commit()
                logger.info(f"Task {task.task_id} successfully completed")
            except Exception as e:
                session.rollback()
                raise e

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

                trigger_task = loop.create_task(self._trigger(data_source, task_id))
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

    def _fetch_identifiers(
        self, company_id: int, data_source: DataSource
    ) -> dict[str, list[str]]:
        """Fetch identifiers for a given company and data source."""
        identifiers = get_company_data_source_identifiers_bll(
            company_id, data_source.id
        )
        if identifiers is None:
            return {}

        result: dict[str, list[str]] = {}
        for identifier in identifiers:
            if identifier.validity and identifier.validity < datetime.now():
                # rediscover all identifiers for the company if not valid anymore
                rediscover_identifiers(data_source, company_id)
                result = self._fetch_identifiers(company_id, data_source)
                break
            key = identifier.property
            if key not in result:
                result[key] = []
            result[key].append(identifier.value)
        return result

    def _create_payload(
        self, task_id: int, companies: list[CompanyDataSource], data_source: DataSource
    ) -> ScrapingPayloadModel:
        """Create payload for the discovery endpoint."""
        companies_dict = {}
        for company in companies:
            company_id = company.company_id
            identifiers = self._fetch_identifiers(company_id, data_source.id)
            # Do discovery if no identifier is found
            if not identifiers:
                company_entity = get_company_id_bll(company_id)
                query_data = [
                    DiscoveryQueryData(company_id=company_id, name=company_entity.name)
                ]
                process_discovery_response(
                    call_discover_endpoint(data_source, query_data), company.id
                )
                # Get identifiers after they are updated
                identifiers = self._fetch_identifiers(company_id, data_source.id)
            if identifiers:
                companies_dict[str(company_id)] = identifiers

        payload = ScrapingPayloadModel(task_id=task_id, companies=companies_dict)
        return payload

    async def _trigger(self, data_source: DataSource, task_id: int) -> None:
        """Trigger the given mining module with given task_id."""
        invocation_endpoint = ensure_appropriate_scheme(data_source.invocation_endpoint)
        if not invocation_endpoint:
            logger.error(
                f"Invalid invocation endpoint: "
                f"{data_source.invocation_endpoint} "
                f"for data source {data_source.id}"
            )
            return

        trigger_endpoint = urllib.parse.urljoin(invocation_endpoint, "/companies")

        data_source_id: int = data_source.id

        companies = get_all_by_data_source_id_bll(data_source_id)

        # Create payload
        json_payload = self._create_payload(task_id, companies, data_source).json()

        logger.debug(f"Payload for data source {data_source.id}: {json_payload}")

        try:
            logger.debug(f"Sending request to {trigger_endpoint}")
            async with httpx.AsyncClient(verify=False) as client:
                token: str = JWTHandler.create_jwt(data_source.id)
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {token}",
                }
                if json_payload is None:
                    logger.debug(
                        f"Missing payload for datasource {data_source.source_name}"
                    )
                else:
                    response = await client.post(
                        trigger_endpoint,
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
