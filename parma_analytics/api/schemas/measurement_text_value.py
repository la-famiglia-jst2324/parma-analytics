from parma_analytics.api.schemas.measurement_generic_value import (
    _ApiMeasurementGenericValueBase,
    _ApiMeasurementGenericValueIdMixin,
)

# ------------------------------------------------------------------------------------ #
#                                       Internal                                       #
# ------------------------------------------------------------------------------------ #


class _ApiMeasurementTextValueBase(_ApiMeasurementGenericValueBase):
    """Internal base model for the MeasurementTextValue endpoints."""

    value: str


class _ApiMeasurementTextValueOutBase(
    _ApiMeasurementTextValueBase, _ApiMeasurementGenericValueIdMixin
):
    """Output base model for the MeasurementTextValue endpoint."""

    pass


# ------------------------------------------------------------------------------------ #
#                                     Create Models                                    #
# ------------------------------------------------------------------------------------ #


class ApiMeasurementTextValueCreateIn(_ApiMeasurementTextValueBase):
    """Input model for the MeasurementTextValue creation endpoint."""

    pass


class ApiMeasurementTextValueCreateOut(_ApiMeasurementTextValueOutBase):
    """Output model for the MeasurementTextValue creation endpoint."""

    pass


# ------------------------------------------------------------------------------------ #
#                                      Read Models                                     #
# ------------------------------------------------------------------------------------ #


class ApiMeasurementTextValueOut(_ApiMeasurementTextValueOutBase):
    """Output model for the MeasurementTextValue retrieval endpoint."""

    pass


# ------------------------------------------------------------------------------------ #
#                                     Update Models                                    #
# ------------------------------------------------------------------------------------ #


class ApiMeasurementTextValueUpdateIn(_ApiMeasurementTextValueBase):
    """Input model for the MeasurementTextValue update endpoint."""

    pass


class ApiMeasurementTextValueUpdateOut(_ApiMeasurementTextValueOutBase):
    """Output model for the MeasurementTextValue update endpoint."""

    pass
