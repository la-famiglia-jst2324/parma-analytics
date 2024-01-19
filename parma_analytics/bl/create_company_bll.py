"""Business layer logic for company."""

from parma_analytics.db.prod.company_query import create_company_if_not_exist
from parma_analytics.db.prod.engine import get_session
from parma_analytics.db.prod.models.company import Company


def create_company_if_not_exist_bll(
    name: str, description: str, added_by: int
) -> Company | None:
    """Business Logic Layer for creating Company instances based on.

    name, description and added_by.

    This function calls the ORM query function create_company_if_doesnt_exist.
    """
    return create_company_if_not_exist(get_session(), name, description, added_by)
