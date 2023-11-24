"""Main entrypoint for the API routes in of parma-analytics."""

from fastapi import FastAPI

from parma_analytics.db.prod.engine import get_engine

from .routes import crawling_finished_router, dummy_router, new_company_router

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
