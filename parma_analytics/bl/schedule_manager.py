"""Scheduler for providing scheduling functionality interfacing with the database."""
import logging
from datetime import timedelta
from operator import and_
from pathlib import Path
from typing import Any

import sqlalchemy as sa
from sqlalchemy import Engine, func, or_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from parma_analytics.bl.mining_module_manager import MiningModuleManager
from parma_analytics.db.prod.models.types import (
    ScheduledTask,
)

logger = logging.getLogger(__name__)

QUERIES_DIR = Path(__file__).parent.parent / "db" / "prod" / "queries"

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
        """Main function to maintain task scheduling.

        This function is multiprocessing safe and can be called as often as needed.
        """
        logger.info("Starting task scheduling...")

        # Go through all active data sources and create new scheduled tasks if needed
        try:
            # idempotent creation of tasks for next 24 hours
            with open(QUERIES_DIR / "create_pending_scheduled_tasks.sql") as f:
                statement = f.read()
                self.session.execute(sa.text(statement))
                self.session.commit()
        except Exception as e:
            logger.error(f"Error in updating data source schedules: {e}")

        # handle PENDING and PROCESSING states by checking for maximum expected run time
        try:
            self._update_overdue_tasks()
        except SQLAlchemyError as e:
            logger.error(f"SQLAlchemyError in updating failed tasks: {e}")
        except Exception as e:
            logger.error(f"Error in updating overdue tasks: {e}")
            logger.error(f"Error in processing data sources: {e}")

        logger.info("Task scheduling completed.")

    def trigger_mining_module(self, task_ids_to_trigger: list[int]) -> None:
        """Dispatching function to trigger the mining module."""
        logger.info(f"Triggering mining module for task ids {task_ids_to_trigger}")
        self.mining_module_manager.trigger_datasources(task_ids_to_trigger)

    # ------------------------------ Internal functions ------------------------------ #

    def _update_overdue_tasks(self) -> None:
        logger.info("Updating status of failed tasks...")
        tasks: list[ScheduledTask] = (
            self.session.query(ScheduledTask)
            .with_for_update()
            .filter(
                or_(
                    ScheduledTask.status == "PENDING",
                    and_(
                        ScheduledTask.status == "PROCESSING",
                        (
                            # timeout exceeded
                            ScheduledTask.started_at
                            + ScheduledTask.max_run_seconds * timedelta(seconds=1)
                            <= func.now()
                        ),
                    ),
                    ScheduledTask.status == "PROCESSING",
                ),
                (ScheduledTask.scheduled_at <= func.now()),
            )
            .all()
        )

        up_for_scheduling: list[int] = []

        logger.info(f"Found {len(tasks)} failed tasks.")

        for task in tasks:
            self.session.begin_nested()
            try:
                self.session.refresh(task)
                logger.debug(f"-- Processing task {task.task_id}...")
                if task.status == "PENDING":
                    task.status = "PROCESSING"
                    task.attempts += 1
                    up_for_scheduling.append(task.task_id)
                    logger.debug(
                        f"Task {task.task_id} status set from PENDING to PROCESSING."
                    )
                elif task.status == "PROCESSING":
                    # check if task has exceeded maximum expected run time
                    if task.attempts < SCHEDULING_RETRIES:
                        task.attempts += 1
                        logger.debug(
                            f"Task {task.task_id} moved from PROCESSING to PENDING."
                        )
                        up_for_scheduling.append(task.task_id)
                        logger.debug(
                            f"Task {task.task_id} is being rescheduled. "
                            f"Attempt {task.attempts}."
                        )

                    else:
                        task.status = "FAILED"
                        logger.debug(
                            f"Task {task.task_id} status set from PROCESSING to FAILED."
                        )

            except SQLAlchemyError as e:
                logger.error(f"SQLAlchemyError in updating failed tasks: {e}")
                self.session.rollback()

        # To release the lock for all the rows that were locked in the previous query
        self.session.commit()

        self.trigger_mining_module(up_for_scheduling)
