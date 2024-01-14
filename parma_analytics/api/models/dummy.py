"""Example of a model for the API."""

from pydantic import BaseModel, Field

# ------------------------------------------------------------------------------------ #
#                                       Internal                                       #
# ------------------------------------------------------------------------------------ #


class _ApiDummyBase(BaseModel):
    """Internal base model for the dummy endpoints."""

    name: str = Field(..., min_length=1, max_length=255)
    price: float = Field(..., ge=0)
    is_offer: bool | None = None


class _ApiDummyIdMixin:
    """Mixin for the dummy ID."""

    id: int


class _ApiDummyOutBase(_ApiDummyBase, _ApiDummyIdMixin):
    """Output base model for the several endpoint."""

    pass


# ------------------------------------------------------------------------------------ #
#                                     Create Models                                    #
# ------------------------------------------------------------------------------------ #


class ApiDummyCreateIn(_ApiDummyBase):
    """Input model for the dummy creation endpoint."""

    pass


class ApiDummyCreateOut(_ApiDummyOutBase):
    """Output model for the dummy creation endpoint."""

    pass


# ------------------------------------------------------------------------------------ #
#                                      Read Models                                     #
# ------------------------------------------------------------------------------------ #


class ApiDummyOut(_ApiDummyOutBase):
    """Output model for the dummy retrieval endpoint."""

    pass


# ------------------------------------------------------------------------------------ #
#                                     Update Models                                    #
# ------------------------------------------------------------------------------------ #


class ApiDummyUpdateIn(_ApiDummyBase):
    """Input model for the dummy update endpoint."""

    pass


class ApiDummyUpdateOut(_ApiDummyOutBase):
    """Output model for the dummy update endpoint."""

    pass
