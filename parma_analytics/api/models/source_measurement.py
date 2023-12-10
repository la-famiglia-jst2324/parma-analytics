from pydantic import BaseModel
from typing import Optional

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
    parent_measurement_id: int
    created_at: str
    modified_at: str


# ------------------------------------------------------------------------------------ #
#                                     Create Models                                    #
# ------------------------------------------------------------------------------------ #


class ApiSourceMeasurementCreateIn(_ApiSourceMeasurementBase):
    """Input model for the SourceMeasurement creation endpoint."""

    type: str
    measurement_name: str
    source_module_id: int
    parent_measurement_id: int


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

    type: Optional[str] = None
    measurement_name: Optional[str] = None
    source_module_id: Optional[int] = None
    parent_measurement_id: Optional[int] = None


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
