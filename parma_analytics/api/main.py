"""Main entrypoint for the API routes in of parma-analytics."""

from fastapi import FastAPI

from parma_analytics.db.prod.engine import get_engine

from ..db.prod import init_db_models
from .routes import dummy_router
from .routes import crawling_finished_router

app = FastAPI()

# initialize database layer
app.state.engine = get_engine()
init_db_models(app.state.engine)


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
