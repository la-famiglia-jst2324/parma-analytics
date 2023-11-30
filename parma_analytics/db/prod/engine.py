"""Engine utilities."""

import os
from urllib.parse import quote
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.engine import create_engine

Base = declarative_base()

engine = None


def get_engine():
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
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
