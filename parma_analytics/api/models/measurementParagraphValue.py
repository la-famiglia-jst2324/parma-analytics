from parma_analytics.api.models.measurementGenericValue import (
    _ApiMeasurementGenericValueBase,
    _ApiMeasurementGenericValueIdMixin,
)

# ------------------------------------------------------------------------------------ #
#                                       Internal                                       #
# ------------------------------------------------------------------------------------ #

## TODO: check if this needs to be removed.


class _ApiMeasurementParagraphValueBase(_ApiMeasurementGenericValueBase):
    """Internal base model for the MeasurementParagraphValue endpoints."""

    value: str


class _ApiMeasurementParagraphValueOutBase(
    _ApiMeasurementParagraphValueBase, _ApiMeasurementGenericValueIdMixin
):
    """Output base model for the MeasurementParagraphValue endpoint."""

    pass


# ------------------------------------------------------------------------------------ #
#                                     Create Models                                    #
# ------------------------------------------------------------------------------------ #


class ApiMeasurementParagraphValueCreateIn(_ApiMeasurementParagraphValueBase):
    """Input model for the MeasurementParagraphValue creation endpoint."""

    pass


class ApiMeasurementParagraphValueCreateOut(_ApiMeasurementParagraphValueOutBase):
    """Output model for the MeasurementParagraphValue creation endpoint."""

    pass


# ------------------------------------------------------------------------------------ #
#                                      Read Models                                     #
# ------------------------------------------------------------------------------------ #


class ApiMeasurementParagraphValueOut(_ApiMeasurementParagraphValueOutBase):
    """Output model for the MeasurementParagraphValue retrieval endpoint."""

    pass


# ------------------------------------------------------------------------------------ #
#                                     Update Models                                    #
# ------------------------------------------------------------------------------------ #


class ApiMeasurementParagraphValueUpdateIn(_ApiMeasurementParagraphValueBase):
    """Input model for the MeasurementParagraphValue update endpoint."""

    pass


class ApiMeasurementParagraphValueUpdateOut(_ApiMeasurementParagraphValueOutBase):
    """Output model for the MeasurementParagraphValue update endpoint."""

    pass
