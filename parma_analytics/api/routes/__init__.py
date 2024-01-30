"""REST API routes for the Parma Analytics application."""

from .crawling_finished import router as crawling_finished_router
from .data_source_handshake import router as data_source_handshake_router
from .dummy import router as dummy_router
from .feed_raw_data import router as feed_raw_data_router
from .new_company import router as new_company_router
from .schedule import router as schedule_router
from .send_reports import router as send_reports_router
from .source_measurement import router as source_measurement_router

__all__ = [
    "crawling_finished_router",
    "dummy_router",
    "feed_raw_data_router",
    "new_company_router",
    "schedule_router",
    "source_measurement_router",
    "data_source_handshake_router",
    "send_reports_router",
]
