"""Business layer logic for company."""

from parma_analytics.db.prod.company_query import (
    create_company_if_not_exist,
    get_company,
)
from parma_analytics.db.prod.engine import get_session
from parma_analytics.db.prod.models.company import Company


def create_company_if_not_exist_bll(
    name: str, description: str, added_by: int
) -> Company:
    """Business Logic Layer for creating Company instances based on.

    name, description and added_by.

    This function calls the ORM query function create_company_if_doesnt_exist.
    """
    return create_company_if_not_exist(get_session(), name, description, added_by)


def get_company_id_bll(company_id: int) -> Company | None:
    """Business Logic Layer for retrieving company by id."""
    return get_company(get_session(), company_id)
