from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import or_
from sqlalchemy.orm import Session
import logging

from parma_analytics.db.prod.models.data_source import DataSource
from parma_analytics.db.prod.models.enums.schedule_type import ScheduleType
from parma_analytics.db.prod.models.enums.task_status import TaskStatus
from parma_analytics.db.prod.models.scheduled_tasks import ScheduledTasks

logger = logging.getLogger(__name__)


class ScheduleManager:
    def __init__(self, db: Session):
        self.db = db

    def schedule_tasks(self) -> None:
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
            self._process_scheduled_tasks()
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

    def _update_failed_tasks(self) -> None:
        logger.info("Updating status of failed tasks...")
        tasks: list[ScheduledTasks] = (
            self.db.query(ScheduledTasks)
            .filter(
                ScheduledTasks.attempts >= 3,
                ScheduledTasks.status == TaskStatus.PENDING,
                ScheduledTasks.status == TaskStatus.PROCESSING,
            )
            .all()
        )

        for task in tasks:
            logger.debug(f"Processing task {task.task_id}...")
            if task.status == TaskStatus.PENDING:
                task.status = TaskStatus.FAILED
                logger.debug(f"Task {task.task_id} status set from PENDING to FAILED.")
            elif task.status == TaskStatus.PROCESSING:
                data_source = task.data_source
                if datetime.now() >= task.locked_at + timedelta(
                    minutes=data_source.maximum_expected_run_time
                ):
                    task.status = TaskStatus.FAILED
                    logger.debug(
                        f"Task {task.task_id} status set from PROCESSING to FAILED."
                    )

            self.db.commit()

    def _process_scheduled_tasks(self) -> None:
        logger.info("Processing scheduled tasks...")
        tasks: list[ScheduledTasks] = (
            self.db.query(ScheduledTasks)
            .filter(
                ScheduledTasks.schedule_type == ScheduleType.ON_DEMAND,
                or_(
                    ScheduledTasks.status == TaskStatus.PENDING,
                    ScheduledTasks.status == TaskStatus.PROCESSING,
                ),
            )
            .all()
        )

        for task in tasks:
            logger.debug(f"Processing scheduled task {task.task_id}.")
            self._handle_task(task)

    def _process_data_sources(self) -> None:
        logger.info("Processing active data sources...")
        sources: list[DataSource] = (
            self.db.query(DataSource).filter(DataSource.is_active == True).all()
        )

        for source in sources:
            logger.debug(f"Processing active data source {source.id}.")
            self._handle_data_source(source)

    def _handle_task(self, task: ScheduledTasks) -> None:
        if task.status == TaskStatus.PENDING:
            logger.debug(f"Scheduled Task {task.task_id} status equals to PENDING.")
            self._reschedule_task(task)
        elif task.status == TaskStatus.PROCESSING:
            # Check if the task has exceeded the maximum expected run time using locked_at
            if datetime.now() >= task.started_at + timedelta(
                minutes=task.data_source.maximum_expected_run_time
            ):
                logger.debug(
                    f"Scheduled Task {task.task_id} status equals to PROCESSING and has exceeded the maximum run time."
                )
                self._reschedule_task(task)

    def _handle_data_source(self, source: DataSource) -> None:
        latest_task: Optional[ScheduledTasks] = (
            self.db.query(ScheduledTasks)
            .filter(
                ScheduledTasks.data_source_id == source.id,
                ScheduledTasks.schedule_type == ScheduleType.REGULAR,
            )
            .order_by(ScheduledTasks.started_at.desc())
            .first()
        )

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
        ] and datetime.now() >= latest_task.started_at + timedelta(
            minutes=source.default_frequency
        ):
            logger.debug(
                f"Latest scheduled task {latest_task.task_id} found for data source {source.id}, and it's status "
                f"equals to {latest_task.status} and has exceeded the default frequency."
            )
            self._create_new_task(source)
        elif latest_task.status == TaskStatus.PROCESSING:
            if datetime.now() >= latest_task.locked_at + timedelta(
                minutes=latest_task.data_source.maximum_expected_run_time
            ):
                logger.debug(
                    f"Latest scheduled task {latest_task.task_id} found for data source {source.id}, and it's status "
                    f"equals to PROCESSING and has exceeded the maximum run time."
                )
                self._reschedule_task(latest_task)

    def _create_new_task(self, source: DataSource) -> None:
        new_task = ScheduledTasks(
            data_source_id=source.id,
            started_at=datetime.now(),
            status=TaskStatus.PENDING,
            attempts=0,
            schedule_type=ScheduleType.REGULAR,
        )
        self.db.add(new_task)
        self.db.commit()
        logger.info(f"Created a new task {new_task.task_id}, data source {source.id}")

        # Trigger the mining module
        self.trigger_mining_module(new_task)

    def _reschedule_task(self, task: ScheduledTasks) -> None:
        # Release the lock
        task.status = TaskStatus.PENDING
        task.locked_at = None
        self.db.commit()
        logger.info(
            f"Rescheduled task {task.task_id}, data source {task.data_source.id}"
        )

        # Trigger the mining module
        self.trigger_mining_module(task)

    def trigger_mining_module(self, task: ScheduledTasks) -> None:
        logger.info(f"Triggering mining module for task {task.task_id}")
        # TODO Trigger the Analytics Backend API
