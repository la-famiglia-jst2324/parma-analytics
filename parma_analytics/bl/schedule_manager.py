"""Scheduler for providing scheduling functionality interfacing with the database."""
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Any

from sqlalchemy import Engine, or_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from parma_analytics.bl.mining_module_manager import MiningModuleManager
from parma_analytics.db.prod.models.types import (
    DataSource,
    ScheduledTasks,
)

logger = logging.getLogger(__name__)


SCHEDULING_RETRIES = 3


class ScheduleManager:
    """Context managing class for scheduling tasks."""

    # --------------------------- Context manager functions -------------------------- #

    def __init__(self, engine: Engine):
        self.session = Session(engine, autocommit=False, autoflush=False)
        self.mining_module_manager = MiningModuleManager()

    def __enter__(self):
        """Enter the context manager."""
        return self

    def __exit__(self, *args: tuple[Any, ...], **kwargs: dict[str, Any]):
        """Exit the context manager.

        Close the session.
        """
        self.session.close()

    # ------------------------------- Public functions ------------------------------- #

    def schedule_tasks(self) -> None:
        """Main function to maintain task scheduling."""
        logger.info("Starting task scheduling...")

        # Determine if there are any failed tasks and update their status accordingly
        try:
            self._update_failed_tasks()
        except SQLAlchemyError as e:
            logger.error(f"SQLAlchemyError in updating failed tasks: {e}")
        except Exception as e:
            logger.error(f"Error in updating failed tasks: {e}")

        # Process on-demand scheduled tasks
        try:
            self._process_ondemand_scheduled_tasks()
        except SQLAlchemyError as e:
            logger.error(f"SQLAlchemyError in processing scheduled tasks: {e}")
        except Exception as e:
            logger.error(f"Error in processing scheduled tasks: {e}")

        # Go through all active data sources and create new scheduled tasks if needed
        try:
            self._process_data_sources()
        except SQLAlchemyError as e:
            logger.error(f"SQLAlchemyError in processing data sources: {e}")
        except Exception as e:
            logger.error(f"Error in processing data sources: {e}")

        logger.info("Task scheduling completed.")

    async def trigger_mining_module(self, task_ids_to_trigger: list[int]) -> None:
        """Dispatching function to trigger the mining module."""
        logger.info(f"Triggering mining module for task ids {task_ids_to_trigger}")
        await self.mining_module_manager.trigger_datasources(task_ids_to_trigger)

    def is_time_to_run(
        self, start_date_time: datetime, second_param: int | str
    ) -> bool:
        """Check if it is time to run the task."""
        if isinstance(second_param, str):
            # Handle the case where second_param is Frequency
            if second_param == "DAILY":
                time_delta = timedelta(days=1)
            elif second_param == "WEEKLY":
                time_delta = timedelta(days=7)
            else:
                raise NotImplementedError("Cron frequency not implemented")
        elif isinstance(second_param, int):
            # Handle the case where second_param is maximum_expected_runtime (minutes)
            time_delta = timedelta(minutes=second_param)
        else:
            raise ValueError("Invalid second parameter type")

        return datetime.now() >= start_date_time + time_delta

    # ------------------------------ Internal functions ------------------------------ #

    def _update_failed_tasks(self) -> None:
        logger.info("Updating status of failed tasks...")
        tasks: list[ScheduledTasks] = (
            self.session.query(ScheduledTasks)
            .filter(
                ScheduledTasks.attempts >= SCHEDULING_RETRIES,
                or_(
                    ScheduledTasks.status == "PENDING",
                    ScheduledTasks.status == "PROCESSING",
                ),
            )
            .with_for_update()
            .all()
        )

        logger.info(f"Found {len(tasks)} failed tasks.")

        for task in tasks:
            self.session.begin_nested()
            try:
                self.session.refresh(task)
                logger.debug(f"-- Processing task {task.task_id}...")
                if task.status == "PENDING":
                    task.status = "FAILED"
                    logger.debug(
                        f"Task {task.task_id} status set from PENDING to FAILED."
                    )
                elif task.status == "PROCESSING":
                    data_source = task.data_source
                    if self.is_time_to_run(
                        task.locked_at, data_source.maximum_expected_run_time
                    ):
                        task.status = "FAILED"
                        logger.debug(
                            f"Task {task.task_id} status set from PROCESSING to FAILED."
                        )

            except SQLAlchemyError as e:
                logger.error(f"SQLAlchemyError in updating failed tasks: {e}")
                self.session.rollback()

        # To release the lock for all the rows that were locked in the previous query
        self.session.commit()

    def _process_ondemand_scheduled_tasks(self) -> None:
        logger.info("Processing scheduled tasks...")
        tasks: list[ScheduledTasks] = (
            self.session.query(ScheduledTasks)
            .filter(
                ScheduledTasks.schedule_type == "ON_DEMAND",
                or_(
                    ScheduledTasks.status == "PENDING",
                    ScheduledTasks.status == "PROCESSING",
                ),
            )
            .with_for_update()
            .all()
        )

        logger.info(f"Found {len(tasks)} on-demand scheduled tasks.")

        task_ids_to_trigger = []
        for task in tasks:
            logger.debug(f"Processing on-deman scheduled task {task.task_id}.")
            self.session.begin_nested()
            try:
                task_id = self._handle_ondemand_task(task)
                if task_id is not None:
                    task_ids_to_trigger.append(task_id)
            except SQLAlchemyError as e:
                logger.error(f"SQLAlchemyError in processing scheduled tasks: {e}")
                self.session.rollback()

        # To release the lock for all the rows that were locked in the previous query
        self.session.commit()
        # Trigger the mining module
        if len(task_ids_to_trigger) > 0:
            asyncio.run(self.trigger_mining_module(task_ids_to_trigger))
        else:
            logger.debug("No on-demand scheduled tasks to trigger.")

    def _process_data_sources(self) -> None:
        logger.info("Processing active data sources...")
        sources: list[DataSource] = (
            self.session.query(DataSource).filter(DataSource.is_active is True).all()
        )

        logger.info(f"Found {len(sources)} active data sources.")

        task_ids_to_trigger = []
        for source in sources:
            logger.debug(f"Processing active data source {source.id}.")
            self.session.begin_nested()
            task_id = self._handle_data_source(source)
            if task_id is not None:
                task_ids_to_trigger.append(task_id)

        # To release the lock for all the rows that were locked in the previous query
        self.session.commit()
        # Trigger the mining module
        if len(task_ids_to_trigger) > 0:
            asyncio.run(self.trigger_mining_module(task_ids_to_trigger))
        else:
            logger.debug("No active data sources to trigger.")

    def _handle_ondemand_task(self, task: ScheduledTasks) -> int | None:
        self.session.refresh(task)
        if task.status == "PENDING":
            logger.debug(f"Scheduled Task {task.task_id} status equals to PENDING.")
            return self._reschedule_task(task)
        elif task.status == "PROCESSING":
            # Check if task has exceeded the maximum expected run time using locked_at
            if self.is_time_to_run(
                task.started_at, task.data_source.maximum_expected_run_time
            ):
                logger.debug(
                    f"Scheduled Task {task.task_id} status equals to PROCESSING "
                    "and has exceeded the maximum run time."
                )
                return self._reschedule_task(task)

        return None

    def _handle_data_source(self, source: DataSource) -> int | None:
        logger.debug(f"Processing data source {source.id}...")
        latest_task: ScheduledTasks | None = (
            self.session.query(ScheduledTasks)
            .filter(
                ScheduledTasks.data_source_id == source.id,
                ScheduledTasks.schedule_type == "REGULAR",
            )
            .order_by(ScheduledTasks.started_at.desc())
            .with_for_update()
            .first()
        )
        logger.debug(f"Latest scheduled task found for data source {source.id}.")

        try:
            self.session.refresh(source)
            if not latest_task:
                logger.debug(f"No scheduled task found for data source {source.id}")
                return self._create_new_task(source)

            self.session.refresh(latest_task)
            if latest_task.status == "PENDING":
                logger.debug(
                    f"Latest scheduled task {latest_task.task_id} found for data "
                    f"source {source.id}, and it's status equals to PENDING."
                )
                return self._reschedule_task(latest_task)
            elif latest_task.status in [
                "SUCCESS",
                "FAILED",
            ] and self.is_time_to_run(latest_task.started_at, source.default_frequency):
                logger.debug(
                    f"Latest scheduled task {latest_task.task_id} found for data "
                    f"source {source.id}, and it's status equals to "
                    f"{latest_task.status} and has exceeded the default frequency."
                )
                return self._create_new_task(source)
            elif latest_task.status == "PROCESSING":
                if self.is_time_to_run(
                    latest_task.locked_at, source.maximum_expected_run_time
                ):
                    logger.debug(
                        f"Latest scheduled task {latest_task.task_id} found for data "
                        f"source {source.id}, and it's status "
                        f"equals to PROCESSING and has exceeded the maximum run time."
                    )
                    return self._reschedule_task(latest_task)
        except SQLAlchemyError as e:
            logger.error(f"SQLAlchemyError in processing data sources: {e}")
            self.session.rollback()

        return None

    def _create_new_task(self, source: DataSource) -> int:
        new_task = ScheduledTasks(
            data_source_id=source.id,
            started_at=datetime.now(),
            status="PENDING",
            attempts=0,
            schedule_type="REGULAR",
        )
        self.session.add(new_task)
        self.session.commit()
        logger.info(f"Created a new task {new_task.task_id}, data source {source.id}")
        return new_task.task_id

    def _reschedule_task(self, task: ScheduledTasks) -> int:
        # Release the lock
        task.status = "PENDING"
        task.locked_at = None
        self.session.commit()
        logger.info(
            f"Rescheduled task {task.task_id}, data source {task.data_source.id}"
        )
        return task.task_id
