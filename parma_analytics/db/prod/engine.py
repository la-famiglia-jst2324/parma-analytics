"""Engine utilities."""

import os
from collections.abc import Iterator
from contextlib import contextmanager
from urllib.parse import quote

from sqlalchemy.engine import Engine, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

Base = declarative_base()


_engine = None


def get_engine() -> Engine:
    """Get the database engine."""
    global _engine  # noqa: PLW0603
    if _engine is None:
        db_host = quote(os.environ.get("POSTGRES_HOST", "localhost"))
        db_port = os.environ.get("POSTGRES_PORT", 5432)
        db_user = quote(os.environ["POSTGRES_USER"])
        db_password = quote(os.environ["POSTGRES_PASSWORD"])
        db_name = quote(os.environ.get("POSTGRES_DB", "parma_analytics"))

        db_url = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

        _engine = create_engine(db_url, client_encoding="utf8", pool_timeout=10)
    return _engine


@contextmanager
def get_session() -> Iterator[Session]:
    """Get a database session.

    Yields:
        A database session.
    """
    db = sessionmaker(bind=get_engine(), autocommit=False, autoflush=False)()
    try:
        yield db
    except:
        db.rollback()
        raise
    finally:
        db.close()
