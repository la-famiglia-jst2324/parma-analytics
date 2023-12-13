"""Engine utilities."""

import os
from typing import Iterator
from urllib.parse import quote
from sqlalchemy import Engine
from sqlalchemy.orm import Session, sessionmaker
from dotenv import load_dotenv
from sqlalchemy.engine import create_engine
from contextlib import contextmanager


engine = None
load_dotenv()


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


engine = get_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@contextmanager
def get_session() -> Iterator[Session]:
    db = SessionLocal()
    try:
        yield db
    except:
        db.rollback()
        raise
    finally:
        db.close()
