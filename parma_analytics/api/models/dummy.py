"""Example of a model for the API."""

from pydantic import BaseModel

# ------------------------------------------------------------------------------------ #
#                                       Internal                                       #
# ------------------------------------------------------------------------------------ #


class _ApiDummyBase(BaseModel):
    """Internal base model for the dummy endpoints."""

    name: str
    price: float
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
