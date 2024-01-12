"""Main entrypoint for the API routes in of parma-analytics."""

import logging

from fastapi import FastAPI

from parma_analytics.db.prod.engine import get_engine

from .routes import (
    crawling_finished_router,
    data_source_handshake_router,
    dummy_router,
    feed_raw_data_router,
    new_company_router,
    schedule_router,
    source_measurement_router,
)

logging.basicConfig(level=logging.INFO)


app = FastAPI()

# initialize database layer
app.state.engine = get_engine()


# root endpoint
@app.get("/", status_code=200)
def root():
    """Root endpoint for the API."""
    return {"welcome": "at parma-analytics"}


app.include_router(
    dummy_router,
    tags=["dummy"],
)

app.include_router(
    crawling_finished_router,
    tags=["crawling_finished"],
)

app.include_router(
    new_company_router,
    tags=["new_company"],
)

app.include_router(
    feed_raw_data_router,
    tags=["feed_raw_data"],
)

app.include_router(
    data_source_handshake_router,
    tags=["data_source_handshake"],
)

app.include_router(source_measurement_router, tags=["source_measurement"])

app.include_router(
    schedule_router,
    tags=["schedule_mining_modules"],
)
