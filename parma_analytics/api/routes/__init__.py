"""REST API routes for the Parma Analytics application."""

from .dummy import router as dummy_router
from .crawling_finished import router as crawling_finished_router

__all__ = ["dummy_router", "crawling_finished"]
