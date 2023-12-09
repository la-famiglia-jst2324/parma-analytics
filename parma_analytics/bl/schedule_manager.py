"""Scheduler for providing scheduling functionality interfacing with the database."""

import logging
from datetime import datetime, timedelta
from typing import Any

from sqlalchemy import Engine, or_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from parma_analytics.db.prod.models.data_source import DataSource
from parma_analytics.db.prod.models.enums.frequency import Frequency
from parma_analytics.db.prod.models.enums.schedule_type import ScheduleType
from parma_analytics.db.prod.models.enums.task_status import TaskStatus
from parma_analytics.db.prod.models.scheduled_tasks import ScheduledTasks

logger = logging.getLogger(__name__)


class ScheduleManager:
    """Context managing class for scheduling tasks."""

    # --------------------------- Context manager functions -------------------------- #

    def __init__(self, engine: Engine):
        self.session = Session(engine, autocommit=False, autoflush=False)

    def __enter__(self):
        return self

    def __exit__(self, *args: tuple[Any, ...], **kwargs: dict[str, Any]):
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

    def trigger_mining_module(self, task: ScheduledTasks) -> None:
        """Dispatching function to trigger the mining module."""
        logger.info(f"Triggering mining module for task {task.task_id}")
        # TODO Trigger the Analytics Backend API

    def is_time_to_run(self, start_date_time: datetime, second_param) -> bool:
        """Check if it is time to run the task."""
        if isinstance(second_param, Frequency):
            # Handle the case where second_param is Frequency
            if second_param == Frequency.DAILY:
                time_delta = timedelta(days=1)
            elif second_param == Frequency.WEEKLY:
                time_delta = timedelta(days=7)
            # TODO: implement other frequencies (CRON)
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
                ScheduledTasks.attempts >= 3,
                ScheduledTasks.status == TaskStatus.PENDING,
                ScheduledTasks.status == TaskStatus.PROCESSING,
            )
            .with_for_update()
            .all()
        )

        for task in tasks:
            self.session.begin_nested()
            try:
                self.session.refresh(task)
                logger.debug(f"Processing task {task.task_id}...")
                if task.status == TaskStatus.PENDING:
                    task.status = TaskStatus.FAILED
                    logger.debug(
                        f"Task {task.task_id} status set from PENDING to FAILED."
                    )
                elif task.status == TaskStatus.PROCESSING:
                    data_source = task.data_source
                    if self.is_time_to_run(
                        task.locked_at, data_source.maximum_expected_run_time
                    ):
                        task.status = TaskStatus.FAILED
                        logger.debug(
                            f"Task {task.task_id} status set from PROCESSING to FAILED."
                        )

                self.session.commit()
            except SQLAlchemyError as e:
                logger.error(f"SQLAlchemyError in updating failed tasks: {e}")
                self.session.rollback()
                raise e

    def _process_ondemand_scheduled_tasks(self) -> None:
        logger.info("Processing scheduled tasks...")
        tasks: list[ScheduledTasks] = (
            self.session.query(ScheduledTasks)
            .filter(
                ScheduledTasks.schedule_type == ScheduleType.ON_DEMAND,
                or_(
                    ScheduledTasks.status == TaskStatus.PENDING,
                    ScheduledTasks.status == TaskStatus.PROCESSING,
                ),
            )
            .with_for_update()
            .all()
        )

        for task in tasks:
            logger.debug(f"Processing scheduled task {task.task_id}.")
            self.session.begin_nested()
            try:
                self.session.refresh(task)
                self._handle_ondemand_task(task)
            except SQLAlchemyError as e:
                logger.error(f"SQLAlchemyError in processing scheduled tasks: {e}")
                self.session.rollback()

    def _process_data_sources(self) -> None:
        logger.info("Processing active data sources...")
        sources: list[DataSource] = (
            self.session.query(DataSource).filter(DataSource.is_active is True).all()
        )

        for source in sources:
            logger.debug(f"Processing active data source {source.id}.")
            self._handle_data_source(source)

    def _handle_ondemand_task(self, task: ScheduledTasks) -> None:
        if task.status == TaskStatus.PENDING:
            logger.debug(f"Scheduled Task {task.task_id} status equals to PENDING.")
            self._reschedule_task(task)
        elif task.status == TaskStatus.PROCESSING:
            # Check if the task has exceeded the maximum expected run time using locked_at
            if self.is_time_to_run(
                task.started_at, task.data_source.maximum_expected_run_time
            ):
                logger.debug(
                    f"Scheduled Task {task.task_id} status equals to PROCESSING and has exceeded the maximum run time."
                )
                self._reschedule_task(task)

    def _handle_data_source(self, source: DataSource) -> None:
        latest_task: ScheduledTasks | None = (
            self.session.query(ScheduledTasks)
            .filter(
                ScheduledTasks.data_source_id == source.id,
                ScheduledTasks.schedule_type == ScheduleType.REGULAR,
            )
            .order_by(ScheduledTasks.started_at.desc())
            .with_for_update()
            .first()
        )

        try:
            self.session.refresh(source)
            if not latest_task:
                logger.debug(f"No scheduled task found for data source {source.id}")
                self._create_new_task(source)
            elif latest_task.status == TaskStatus.PENDING:
                logger.debug(
                    f"Latest scheduled task {latest_task.task_id} found for data source {source.id}, and it's status "
                    f"equals to PENDING."
                )
                self._reschedule_task(latest_task)
            elif latest_task.status in [
                TaskStatus.SUCCESS,
                TaskStatus.FAILED,
            ] and self.is_time_to_run(latest_task.started_at, source.default_frequency):
                logger.debug(
                    f"Latest scheduled task {latest_task.task_id} found for data source {source.id}, and it's status "
                    f"equals to {latest_task.status} and has exceeded the default frequency."
                )
                self._create_new_task(source)
            elif latest_task.status == TaskStatus.PROCESSING:
                if self.is_time_to_run(
                    latest_task.locked_at, source.maximum_expected_run_time
                ):
                    logger.debug(
                        f"Latest scheduled task {latest_task.task_id} found for data source {source.id}, and it's status "
                        f"equals to PROCESSING and has exceeded the maximum run time."
                    )
                    self._reschedule_task(latest_task)
        except SQLAlchemyError as e:
            logger.error(f"SQLAlchemyError in processing data sources: {e}")
            self.session.rollback()

    def _create_new_task(self, source: DataSource) -> None:
        new_task = ScheduledTasks(
            data_source_id=source.id,
            started_at=datetime.now(),
            status=TaskStatus.PENDING,
            attempts=0,
            schedule_type=ScheduleType.REGULAR,
        )
        self.session.add(new_task)
        self.session.commit()
        logger.info(f"Created a new task {new_task.task_id}, data source {source.id}")

        # Trigger the mining module
        self.trigger_mining_module(new_task)

    def _reschedule_task(self, task: ScheduledTasks) -> None:
        # Release the lock
        task.status = TaskStatus.PENDING
        task.locked_at = None
        self.session.commit()
        logger.info(
            f"Rescheduled task {task.task_id}, data source {task.data_source.id}"
        )

        # Trigger the mining module
        self.trigger_mining_module(task)
