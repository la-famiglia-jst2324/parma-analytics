"""Engine utilities."""

import os
from urllib.parse import quote

from sqlalchemy.engine import create_engine


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
    return create_engine(db_url, client_encoding="utf8")
