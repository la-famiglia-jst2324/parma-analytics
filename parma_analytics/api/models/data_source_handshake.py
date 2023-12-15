from pydantic import BaseModel


class _ApiDataSourceHandshakeIn(BaseModel):
    """Internal base model for the new company endpoints."""

    invocation_endpoint: str
    data_source_id: int


class _ApiDataSourceHandshakeOut(BaseModel):
    """Output base model for the several endpoint."""

    frequency: str


class ApiDataSourceHandshakeIn(_ApiDataSourceHandshakeIn):
    """Internal base model for the new company endpoints."""

    pass


class ApiDataSourceHandshakeOut(_ApiDataSourceHandshakeOut):
    """Internal base model for the new company endpoints."""

    pass
