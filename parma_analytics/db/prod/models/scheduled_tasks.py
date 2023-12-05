from sqlalchemy import Column, Integer, DateTime, String, ForeignKey, Enum
from sqlalchemy.orm import relationship

from .base import Base
from .enums.task_status import TaskStatus
from .enums.schedule_type import ScheduleType


class ScheduledTasks(Base):
    __tablename__ = "scheduled_tasks"

    task_id = Column(Integer, primary_key=True)
    data_source_id = Column(Integer, ForeignKey("data_source.id"))
    schedule_type = Column(Enum(ScheduleType))
    started_at = Column(DateTime)
    locked_at = Column(DateTime, nullable=True)
    ended_at = Column(DateTime, nullable=True)
    result_summary = Column(String, nullable=True)
    status = Column(Enum(TaskStatus))
    attempts = Column(Integer, default=0)

    # Relationships
    data_source = relationship("DataSource", back_populates="scheduled_tasks")
