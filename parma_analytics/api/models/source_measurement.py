from datetime import datetime

from pydantic import BaseModel

# ------------------------------------------------------------------------------------ #
#                                       Internal                                       #
# ------------------------------------------------------------------------------------ #


class _ApiSourceMeasurementBase(BaseModel):
    """Internal base model for the SourceMeasurement endpoints."""


class _ApiSourceMeasurementIdMixin:
    """Mixin for the SourceMeasurement ID."""

    id: int


class _ApiSourceMeasurementOutBase(
    _ApiSourceMeasurementIdMixin, _ApiSourceMeasurementBase
):
    """Output base model for the SourceMeasurement endpoint."""

    type: str
    measurement_name: str
    source_module_id: int
    parent_measurement_id: int | None = None
    created_at: datetime
    modified_at: datetime


# ------------------------------------------------------------------------------------ #
#                                     Create Models                                    #
# ------------------------------------------------------------------------------------ #


class ApiSourceMeasurementCreateIn(_ApiSourceMeasurementBase):
    """Input model for the SourceMeasurement creation endpoint."""

    type: str
    measurement_name: str
    source_module_id: int
    parent_measurement_id: int | None = None


class ApiSourceMeasurementCreateOut(
    _ApiSourceMeasurementIdMixin, _ApiSourceMeasurementBase
):
    """Output model for the SourceMeasurement creation endpoint."""

    creation_msg: str
    pass


# ------------------------------------------------------------------------------------ #
#                                      Read Models                                     #
# ------------------------------------------------------------------------------------ #


class ApiSourceMeasurementReadIn(
    _ApiSourceMeasurementIdMixin, _ApiSourceMeasurementBase
):
    """Input model for the SourceMeasurement retrieval endpoint."""

    pass


class ApiSourceMeasurementOut(_ApiSourceMeasurementOutBase):
    """Output model for the SourceMeasurement retrieval endpoint."""

    pass


class ApiSourceMeasurementListOut(_ApiSourceMeasurementBase):
    """Output model for the SourceMeasurement retrieval endpoint."""

    measurements_list: list[ApiSourceMeasurementOut]
    num_pages: int


# ------------------------------------------------------------------------------------ #
#                                     Update Models                                    #
# ------------------------------------------------------------------------------------ #


class ApiSourceMeasurementUpdateIn(_ApiSourceMeasurementBase):
    """Input model for the SourceMeasurement update endpoint."""

    type: str | None = None
    measurement_name: str | None = None
    source_module_id: int | None = None
    parent_measurement_id: int | None = None


class ApiSourceMeasurementUpdateOut(_ApiSourceMeasurementOutBase):
    """Output model for the SourceMeasurement update endpoint."""

    pass


# ------------------------------------------------------------------------------------ #
#                                     Delete Models                                    #
# ------------------------------------------------------------------------------------ #


class ApiSourceMeasurementDeleteIn(
    _ApiSourceMeasurementIdMixin, _ApiSourceMeasurementBase
):
    """Input model for the SourceMeasurement update endpoint."""

    pass


class ApiSourceMeasurementDeleteOut(_ApiSourceMeasurementBase):
    """Output model for the SourceMeasurement update endpoint."""

    deletion_msg: str
    pass
