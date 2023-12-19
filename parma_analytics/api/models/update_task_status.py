"""Pydantic REST models for the update_task_status endpoint."""

from pydantic import BaseModel

# ------------------------------------------------------------------------------------ #
#                                       Internal                                       #
# ------------------------------------------------------------------------------------ #


class _ApiUpdateTaskStatusBase(BaseModel):
    """Internal base model for the update task's status endpoint."""

    task_id: int
    status: str
    result_summary: str | None


class _ApiUpdateTaskStatusOutBase(_ApiUpdateTaskStatusBase):
    """Output base model for the update task's status endpoint."""

    updated: bool


# ------------------------------------------------------------------------------------ #
#                                     Create Models                                    #
# ------------------------------------------------------------------------------------ #


class ApiUpdateTaskStatusCreateIn(_ApiUpdateTaskStatusBase):
    """Input model for the UpdateTaskStatus creation endpoint."""

    pass


class ApiUpdateTaskStatusCreateOut(_ApiUpdateTaskStatusOutBase):
    """Output model for the UpdateTaskStatus creation endpoint."""

    pass
