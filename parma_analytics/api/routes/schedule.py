import logging

from fastapi import APIRouter, status, BackgroundTasks, Response
from sqlalchemy import Engine
from sqlalchemy.orm import sessionmaker, Session

from parma_analytics.bl.schedule_manager import ScheduleManager
from parma_analytics.db.prod.engine import get_engine

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get(
    "/schedule",
    status_code=status.HTTP_200_OK,
    description="Endpoint to schedule the data mining modules.",
)
async def schedule(background_tasks: BackgroundTasks) -> Response:
    logger.info("/schedule endpoint called. Scheduling will start in the background.")
    background_tasks.add_task(schedule_tasks)
    return Response(status_code=status.HTTP_200_OK)


def schedule_tasks() -> None:
    engine: Engine = get_engine()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db: Session = SessionLocal()

    schedule_manager = ScheduleManager(db)
    schedule_manager.schedule_tasks()
