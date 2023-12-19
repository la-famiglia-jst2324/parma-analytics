"""Pydantic REST models for the crawling_finished endpoint."""

from pydantic import BaseModel

# ------------------------------------------------------------------------------------ #
#                                       Internal                                       #
# ------------------------------------------------------------------------------------ #


class _ApiCrawlingFinishedBase(BaseModel):
    """Internal base model for the new company endpoints."""

    incoming_message: str


class _ApiCrawlingFinishedOutBase(_ApiCrawlingFinishedBase):
    """Output base model for the several endpoint."""

    return_message: str


# ------------------------------------------------------------------------------------ #
#                                     Create Models                                    #
# ------------------------------------------------------------------------------------ #


class ApiCrawlingFinishedCreateIn(_ApiCrawlingFinishedBase):
    """Input model for the CrawlingFinished creation endpoint."""

    pass


class ApiCrawlingFinishedCreateOut(_ApiCrawlingFinishedOutBase):
    """Output model for the CrawlingFinished creation endpoint."""

    pass
