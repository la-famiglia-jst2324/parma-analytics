"""REST API routes for the Parma Analytics application."""

from .dummy import router as dummy_router
from .source_measurement import router as source_measurement_router

__all__ = ["dummy_router", "source_measurement_router"]
