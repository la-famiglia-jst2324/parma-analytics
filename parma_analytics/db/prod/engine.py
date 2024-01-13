"""Engine utilities."""

import os
from collections.abc import Iterator
from contextlib import contextmanager
from urllib.parse import quote

from sqlalchemy import Engine
from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

Base = declarative_base()


def get_engine() -> Engine:
    """Get the database engine."""
    db_host = quote(os.environ.get("POSTGRES_HOST", "localhost"))
    db_port = os.environ.get("POSTGRES_PORT", 5432)
    db_user = quote(os.environ["POSTGRES_USER"])
    db_password = quote(os.environ["POSTGRES_PASSWORD"])
    db_name = quote(os.environ.get("POSTGRES_DB", "parma_analytics"))

    db_url = (
        f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    )
    engine = create_engine(db_url, client_encoding="utf8")
    return engine


@contextmanager
def get_session() -> Iterator[Session]:
    """Get a database session.

    Yields:
        A database session.
    """
    db = sessionmaker(autocommit=False, autoflush=False, engine=True)()
    try:
        yield db
    except:
        db.rollback()
        raise
    finally:
        db.close()
