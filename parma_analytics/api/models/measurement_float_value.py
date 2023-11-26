from parma_analytics.api.models.measurement_generic_value import (
    _ApiMeasurementGenericValueBase,
    _ApiMeasurementGenericValueIdMixin,
)

# ------------------------------------------------------------------------------------ #
#                                       Internal                                       #
# ------------------------------------------------------------------------------------ #


class _ApiMeasurementFloatValueBase(_ApiMeasurementGenericValueBase):
    """Internal base model for the MeasurementFloatValue endpoints."""

    value: float


class _ApiMeasurementFloatValueOutBase(
    _ApiMeasurementFloatValueBase, _ApiMeasurementGenericValueIdMixin
):
    """Output base model for the MeasurementFloatValue endpoint."""

    pass


# ------------------------------------------------------------------------------------ #
#                                     Create Models                                    #
# ------------------------------------------------------------------------------------ #


class ApiMeasurementFloatValueCreateIn(_ApiMeasurementFloatValueBase):
    """Input model for the MeasurementFloatValue creation endpoint."""

    pass


class ApiMeasurementFloatValueCreateOut(_ApiMeasurementFloatValueOutBase):
    """Output model for the MeasurementFloatValue creation endpoint."""

    pass


# ------------------------------------------------------------------------------------ #
#                                      Read Models                                     #
# ------------------------------------------------------------------------------------ #


class ApiMeasurementFloatValueOut(_ApiMeasurementFloatValueOutBase):
    """Output model for the MeasurementFloatValue retrieval endpoint."""

    pass


# ------------------------------------------------------------------------------------ #
#                                     Update Models                                    #
# ------------------------------------------------------------------------------------ #


class ApiMeasurementFloatValueUpdateIn(_ApiMeasurementFloatValueBase):
    """Input model for the MeasurementFloatValue update endpoint."""

    pass


class ApiMeasurementFloatValueUpdateOut(_ApiMeasurementFloatValueOutBase):
    """Output model for the MeasurementFloatValue update endpoint."""

    pass
