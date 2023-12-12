"""Models for firebase service."""

import datetime
from typing import Any, Literal

from pydantic import BaseModel


class _FirestoreBase(BaseModel):
    """Raw data."""

    id: str
    create_time: datetime.datetime
    update_time: datetime.datetime | None
    read_time: datetime.datetime | None


class TriggerIn(BaseModel):
    """Trigger input."""

    datasource: str
    started_at: datetime.datetime
    finished_at: datetime.datetime
    scheduled_task_id: int
    status: Literal["success", "error"]
    note: str


class Trigger(_FirestoreBase, TriggerIn):
    """Trigger read from firestore."""

    pass


class RawDataIn(BaseModel):
    """Raw data input."""

    mining_trigger: str
    status: Literal["success", "error"]
    company_id: str
    data: dict[str, Any]


class RawData(_FirestoreBase, RawDataIn):
    """Raw data read from firestore."""

    pass


class NormalizationSchemaIn(BaseModel):
    """Raw data input."""

    schema: dict[str, Any]


class NormalizationSchema(_FirestoreBase, NormalizationSchemaIn):
    """Raw data read from firestore."""

    pass
