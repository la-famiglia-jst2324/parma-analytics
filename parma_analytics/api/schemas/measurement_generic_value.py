from pydantic import BaseModel, UUID4
from datetime import datetime

# ------------------------------------------------------------------------------------ #
#                                       Internal                                       #
# ------------------------------------------------------------------------------------ #


class _ApiMeasurementGenericValueBase(BaseModel):
    """Internal base model for the MeasurementGenericValue endpoints."""

    timestamp: datetime


class _ApiMeasurementGenericValueIdMixin:
    """Mixin for the MeasurementGenericValue ID."""

    source_measurement_id: UUID4


class _ApiMeasurementGenericValueOutBase(
    _ApiMeasurementGenericValueBase, _ApiMeasurementGenericValueIdMixin
):
    """Output base model for the MeasurementGenericValue endpoint."""

    pass


# ------------------------------------------------------------------------------------ #
#                                     Create Models                                    #
# ------------------------------------------------------------------------------------ #


class ApiMeasurementGenericValueCreateIn(_ApiMeasurementGenericValueBase):
    """Input model for the MeasurementGenericValue creation endpoint."""

    pass


class ApiMeasurementGenericValueCreateOut(_ApiMeasurementGenericValueOutBase):
    """Output model for the MeasurementGenericValue creation endpoint."""

    pass


# ------------------------------------------------------------------------------------ #
#                                      Read Models                                     #
# ------------------------------------------------------------------------------------ #


class ApiMeasurementGenericValueOut(_ApiMeasurementGenericValueOutBase):
    """Output model for the MeasurementGenericValue retrieval endpoint."""

    pass


# ------------------------------------------------------------------------------------ #
#                                     Update Models                                    #
# ------------------------------------------------------------------------------------ #


class ApiMeasurementGenericValueUpdateIn(_ApiMeasurementGenericValueBase):
    """Input model for the MeasurementGenericValue update endpoint."""

    pass


class ApiMeasurementGenericValueUpdateOut(_ApiMeasurementGenericValueOutBase):
    """Output model for the MeasurementGenericValue update endpoint."""

    pass
