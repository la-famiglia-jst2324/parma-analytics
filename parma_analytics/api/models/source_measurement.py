from pydantic import BaseModel

# ------------------------------------------------------------------------------------ #
#                                       Internal                                       #
# ------------------------------------------------------------------------------------ #


class _ApiSourceMeasurementBase(BaseModel):
    """Internal base model for the SourceMeasurement endpoints."""


class _ApiSourceMeasurementIdMixin:
    """Mixin for the SourceMeasurement ID."""

    source_measurement_id: int


class _ApiSourceMeasurementOutBase(
    _ApiSourceMeasurementIdMixin, _ApiSourceMeasurementBase
):
    """Output base model for the SourceMeasurement endpoint."""

    source_module_id: int
    company_id: int
    type: str
    measurement_name: str


# ------------------------------------------------------------------------------------ #
#                                     Create Models                                    #
# ------------------------------------------------------------------------------------ #


class ApiSourceMeasurementCreateIn(_ApiSourceMeasurementBase):
    """Input model for the SourceMeasurement creation endpoint."""

    pass


class ApiSourceMeasurementCreateOut(_ApiSourceMeasurementOutBase):
    """Output model for the SourceMeasurement creation endpoint."""

    pass


# ------------------------------------------------------------------------------------ #
#                                      Read Models                                     #
# ------------------------------------------------------------------------------------ #


class ApiSourceMeasurementReadIn(
    _ApiSourceMeasurementIdMixin, _ApiSourceMeasurementBase
):
    """Input model for the SourceMeasurement retrieval endpoint."""

    source_measurement_id: int
    pass


class ApiSourceMeasurementOut(_ApiSourceMeasurementOutBase):
    """Output model for the SourceMeasurement retrieval endpoint."""

    pass


# ------------------------------------------------------------------------------------ #
#                                     Update Models                                    #
# ------------------------------------------------------------------------------------ #


class ApiSourceMeasurementUpdateIn(_ApiSourceMeasurementOutBase):
    """Input model for the SourceMeasurement update endpoint."""

    pass


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


class ApiSourceMeasurementDeleteOut(_ApiSourceMeasurementOutBase):
    """Output model for the SourceMeasurement update endpoint."""

    notification_message: str
    pass
