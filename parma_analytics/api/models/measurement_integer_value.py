from parma_analytics.api.models.measurement_generic_value import (
    _ApiMeasurementGenericValueBase,
    _ApiMeasurementGenericValueIdMixin,
)

# ------------------------------------------------------------------------------------ #
#                                       Internal                                       #
# ------------------------------------------------------------------------------------ #


class _ApiMeasurementIntegerValueBase(_ApiMeasurementGenericValueBase):
    """Internal base model for the MeasurementIntegerValue endpoints."""

    value: int


class _ApiMeasurementIntegerValueOutBase(
    _ApiMeasurementIntegerValueBase, _ApiMeasurementGenericValueIdMixin
):
    """Output base model for the MeasurementIntegerValue endpoint."""

    pass


# ------------------------------------------------------------------------------------ #
#                                     Create Models                                    #
# ------------------------------------------------------------------------------------ #


class ApiMeasurementIntegerValueCreateIn(_ApiMeasurementIntegerValueBase):
    """Input model for the MeasurementIntegerValue creation endpoint."""

    pass


class ApiMeasurementIntegerValueCreateOut(_ApiMeasurementIntegerValueOutBase):
    """Output model for the MeasurementIntegerValue creation endpoint."""

    pass


# ------------------------------------------------------------------------------------ #
#                                      Read Models                                     #
# ------------------------------------------------------------------------------------ #


class ApiMeasurementIntegerValueOut(_ApiMeasurementIntegerValueOutBase):
    """Output model for the MeasurementIntegerValue retrieval endpoint."""

    pass


# ------------------------------------------------------------------------------------ #
#                                     Update Models                                    #
# ------------------------------------------------------------------------------------ #


class ApiMeasurementIntegerValueUpdateIn(_ApiMeasurementIntegerValueBase):
    """Input model for the MeasurementIntegerValue update endpoint."""

    pass


class ApiMeasurementIntegerValueUpdateOut(_ApiMeasurementIntegerValueOutBase):
    """Output model for the MeasurementIntegerValue update endpoint."""

    pass
