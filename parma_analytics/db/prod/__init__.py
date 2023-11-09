"""Database module for Parma Analytics."""


from sqlalchemy.engine import Engine

from .models import DbBase


def init_db_models(engine: Engine):
    """Initialize the database models."""
    DbBase.metadata.create_all(bind=engine)
