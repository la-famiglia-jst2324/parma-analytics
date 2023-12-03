from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, status, BackgroundTasks, Response
from sqlalchemy import Engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker, Session

from parma_analytics.db.prod.engine import get_engine
from parma_analytics.db.prod.models.data_source import DataSource
from parma_analytics.db.prod.models.enums.task_status import TaskStatus
from parma_analytics.db.prod.models.scheduled_tasks import ScheduledTasks

router = APIRouter()


@router.get(
    "/schedule",
    status_code=status.HTTP_200_OK,
    description="Endpoint to schedule the data mining modules.",
)
async def schedule(background_tasks: BackgroundTasks) -> Response:
    background_tasks.add_task(schedule_tasks)
    # Return an empty response with HTTP 200 OK
    return Response(status_code=status.HTTP_200_OK)


# Scheduling logic
def schedule_tasks() -> None:
    engine: Engine = get_engine()
    session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    session: Session = session_local()
    try:
        # Get all active data sources
        data_sources: list[DataSource] = (
            session.query(DataSource).filter(DataSource.is_active == True).all()
        )

        for data_source in data_sources:
            # Find the latest scheduled task for this data source
            latest_task: Optional[ScheduledTasks] = (
                session.query(ScheduledTasks)
                .filter(ScheduledTasks.data_source_id == data_source.id)
                .order_by(ScheduledTasks.startedAt.desc())
                .first()
            )

            task_id = None
            # If there is no scheduled task (first time) for this data source, create a new one
            if not latest_task:
                task_id = create_new_task(session, data_source)
            # If the latest task is SUCCESS
            elif latest_task.status == TaskStatus.SUCCESS:
                # And the current time is greater than the latest task's endedAt + default frequency
                if datetime.now() >= latest_task.endedAt + timedelta(
                    minutes=data_source.default_frequency
                ):
                    task_id = create_new_task(session, data_source)
            # If the latest task is PROCESSING or PENDING
            elif (
                latest_task.status == TaskStatus.PROCESSING
                or latest_task.status == TaskStatus.PENDING
            ):
                # And the current time is greater than the latest task's startedAt + maximum expected run time
                if datetime.now() >= latest_task.startedAt + timedelta(
                    minutes=data_source.maximum_expected_run_time
                ):
                    task_id = reschedule_task(session, latest_task)
            # If the latest task is FAILED
            elif latest_task.status == TaskStatus.FAILED:
                # And attempts is less than 3, reschedule the task
                if latest_task.attempts < 3:
                    task_id = reschedule_task(session, latest_task)

            if task_id is not None:
                session.commit()
                trigger_mining_module(task_id)

    except SQLAlchemyError as e:
        print(f"Database error occurred: {e}")
        session.rollback()
    finally:
        session.close()


def create_new_task(session: Session, data_source: DataSource) -> int:
    new_task = ScheduledTasks(
        dataSourceId=data_source.id,
        startedAt=datetime.now(),
        status=TaskStatus.PENDING,
        attempts=0,
    )
    session.add(new_task)
    session.flush()
    return new_task.task_id


def reschedule_task(session: Session, task: ScheduledTasks) -> int:
    task.status = TaskStatus.PENDING
    task.locked_at = None
    session.add(task)
    session.flush()
    return task.task_id


def trigger_mining_module(task_id: int) -> None:
    pass
