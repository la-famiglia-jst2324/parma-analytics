"""Database queries for dummies."""

from sqlalchemy.engine import Engine
from sqlalchemy.orm.session import Session

from parma_analytics.db.prod.models.dummy import DbDummy
from parma_analytics.db.prod.utils.paginate import (
    ListPaginationResult,
    paginate,
    paginate_query,
)

# ------------------------------------------------------------------------------------ #
#                                      ORM Queries                                     #
# ------------------------------------------------------------------------------------ #


def create_dummy(engine: Engine, dummy: DbDummy) -> DbDummy:
    """Create a dummy.

    Args:
        engine: The database engine.
        dummy: The dummy to create.

    Returns:
        The created dummy.
    """
    with Session(engine) as session:
        session.add(dummy)
        session.commit()
        session.refresh(dummy)
        return dummy


def get_dummy(engine: Engine, dummy_id: int) -> DbDummy | None:
    """Get a dummy by its id.

    Args:
        engine: The database engine.
        dummy_id: The id of the dummy.

    Returns:
        The dummy if it exists, otherwise None.
    """
    with Session(engine) as session:
        return session.get(DbDummy, dummy_id)


@paginate(default_page_size=5)
def list_dummies(
    engine: Engine, *, page: int, page_size: int
) -> ListPaginationResult[DbDummy]:
    """List all dummies.

    Args:
        engine: The database engine.
        page: The page number.
        page_size: The number of items per page.

    Returns:
        A list of all dummies.
    """
    with Session(engine) as session:
        return paginate_query(session.query(DbDummy), page=page, page_size=page_size)
