"""Business layer logic for company data source."""

from parma_analytics.db.prod.company_data_source_query import (
    CompanyDataSourceData,
    CompanyDataSourceUpdateData,
    create_company_data_source,
    delete_company_data_source,
    get_all_company_data_sources,
    get_all_company_data_sources_by_data_source_id,
    get_company_data_source,
    update_company_data_source,
)
from parma_analytics.db.prod.engine import get_session
from parma_analytics.db.prod.models.company_data_source import (
    CompanyDataSource,
)


def get_company_data_source_bll(
    company_id: int, data_source_id: int
) -> CompanyDataSource | None:
    """BLL for fetching CompanyDataSource instances."""
    with get_session() as session:
        return get_company_data_source(session, company_id, data_source_id)


def get_all_company_data_sources_bll() -> list[CompanyDataSource]:
    """Business Logic Layer for fetching all CompanyDataSource instances."""
    with get_session() as session:
        return get_all_company_data_sources(session)


def get_all_by_data_source_id_bll(data_source_id: int) -> list[CompanyDataSource]:
    """Business Logic Layer for fetching based on data_source_id."""
    with get_session() as session:
        return get_all_company_data_sources_by_data_source_id(session, data_source_id)


def create_company_data_source_bll(
    data_source_data: CompanyDataSourceData,
) -> CompanyDataSource:
    """Business Logic Layer for creating a new CompanyDataSource instance."""
    with get_session() as session:
        return create_company_data_source(
            session,
            data_source_data,
        )


def update_company_data_source_bll(
    data_source_id: int,
    update_data: CompanyDataSourceUpdateData,
) -> CompanyDataSource | None:
    """Business Logic Layer for updating an existing CompanyDataSource instance."""
    with get_session() as session:
        return update_company_data_source(
            session,
            data_source_id,
            update_data,
        )


def delete_company_data_source_bll(data_source_id: int) -> bool:
    """Business Logic Layer for deleting a CompanyDataSource instance."""
    with get_session() as session:
        return delete_company_data_source(session, data_source_id)
