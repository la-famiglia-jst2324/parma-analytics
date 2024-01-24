"""DataSource DB queries."""

from sqlalchemy.engine import Engine
from sqlalchemy.orm.session import Session

from parma_analytics.db.prod.models.types import DataSource


def get_data_source_name(engine: Engine, source_module_id: int) -> str:
    """Get Data Source Name from source_module_id."""
    with Session(engine) as session:
        data_source = (
            session.query(DataSource).filter(DataSource.id == source_module_id).first()
        )
        return data_source.source_name
