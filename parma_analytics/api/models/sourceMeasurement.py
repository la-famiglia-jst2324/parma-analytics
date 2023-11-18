from pydantic import BaseModel, UUID4

# ------------------------------------------------------------------------------------ #
#                                       Internal                                       #
# ------------------------------------------------------------------------------------ #


class _ApiSourceMeasurementBase(BaseModel):
    """Internal base model for the SourceMeasurement endpoints."""

    source_module_id: UUID4
    company_id: UUID4
    type: str
    measurement_name: str


class _ApiSourceMeasurementIdMixin:
    """Mixin for the SourceMeasurement ID."""

    source_measurement_id: UUID4


class _ApiSourceMeasurementOutBase(
    _ApiSourceMeasurementBase, _ApiSourceMeasurementIdMixin
):
    """Output base model for the SourceMeasurement endpoint."""

    pass


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


class ApiSourceMeasurementOut(_ApiSourceMeasurementOutBase):
    """Output model for the SourceMeasurement retrieval endpoint."""

    pass


# ------------------------------------------------------------------------------------ #
#                                     Update Models                                    #
# ------------------------------------------------------------------------------------ #


class ApiSourceMeasurementUpdateIn(_ApiSourceMeasurementBase):
    """Input model for the SourceMeasurement update endpoint."""

    pass


class ApiSourceMeasurementUpdateOut(_ApiSourceMeasurementOutBase):
    """Output model for the SourceMeasurement update endpoint."""

    pass
