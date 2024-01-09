"""Pydantic REST models for the crawling_finished endpoint."""

from pydantic import BaseModel

# ------------------------------------------------------------------------------------ #
#                                       Internal                                       #
# ------------------------------------------------------------------------------------ #


class CrawlingErrorInfo(BaseModel):
    """Error info for the crawling_finished endpoint."""

    error_type: str
    error_description: str


class _ApiCrawlingFinishedBase(BaseModel):
    """Internal base model for the crawling_finished endpoints."""

    task_id: int
    errors: dict[str, CrawlingErrorInfo] | None = None


class _ApiCrawlingFinishedOutBase(_ApiCrawlingFinishedBase):
    """Output base model for the several endpoint."""

    pass


# ------------------------------------------------------------------------------------ #
#                                     Create Models                                    #
# ------------------------------------------------------------------------------------ #


class ApiCrawlingFinishedCreateIn(_ApiCrawlingFinishedBase):
    """Input model for the CrawlingFinished creation endpoint."""

    pass


class ApiCrawlingFinishedCreateOut(_ApiCrawlingFinishedOutBase):
    """Output model for the CrawlingFinished creation endpoint."""

    pass
