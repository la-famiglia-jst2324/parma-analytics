"""REST API routes for the Parma Analytics application."""

from .dummy import router as dummy_router
from .crawling_finished import router as crawling_finished_router
from .new_company import router as new_company_router
from .trigger_datasources import router as trigger_datasources_router
from .feed_raw_data import router as feed_raw_data_router

__all__ = [
    "dummy_router",
    "crawling_finished_router",
    "new_company_router",
    "trigger_datasources_router",
    "feed_raw_data_router",
]
