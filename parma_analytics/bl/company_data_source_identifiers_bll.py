"""Business layer logic for company data source identifiers."""
from dataclasses import dataclass
from datetime import datetime

from company_data_source_identifiers_query import (
    create_company_data_source_identifier,
    delete_company_data_source_identifier,
    get_company_data_source_identifiers,
    update_company_data_source_identifier,
)
from models.company_data_source_identifier import (
    CompanyDataSourceIdentifier,
    IdentifierType,
)

from parma_analytics.db.prod.engine import get_session


@dataclass
class IdentifierData:
    """Class for creating identifiers."""

    company_data_source_id: int
    identifier_key: str
    identifier_type: IdentifierType
    property: str
    value: str
    validity: datetime


@dataclass
class IdentifierUpdateData:
    """Class for updating identifiers."""

    identifier_key: str | None
    identifier_type: IdentifierType | None
    property: str | None
    value: str | None
    validity: datetime | None


def get_company_data_source_identifiers_bll(
    company_id: int, data_source_id: int
) -> list[CompanyDataSourceIdentifier] | None:
    """Business Logic Layer for fetching CompanyDataSourceIdentifier instances based on.

    company_id and data_source_id.

    This function calls the ORM query function get_company_data_source_identifiers.
    """
    return get_company_data_source_identifiers(
        get_session(), company_id, data_source_id
    )


def create_company_data_source_identifier_bll(
    identifier_data: IdentifierData,
) -> CompanyDataSourceIdentifier:
    """Business Logic Layer for creating a new CompanyDataSourceIdentifier instance.

    This function calls the ORM query function create_company_data_source_identifier.
    """
    return create_company_data_source_identifier(
        get_session(),
        identifier_data.company_data_source_id,
        identifier_data.identifier_key,
        identifier_data.identifier_type,
        identifier_data.property,
        identifier_data.value,
        identifier_data.validity,
    )


def update_company_data_source_identifier_bll(
    identifier_id: int,
    update_data: IdentifierUpdateData,
) -> CompanyDataSourceIdentifier | None:
    """Business Logic Layer for updating an existing CompanyDataSourceIdentifier.

    instance.

    This function calls the ORM query function update_company_data_source_identifier.
    """
    return update_company_data_source_identifier(
        get_session(),
        identifier_id,
        update_data.identifier_key,
        update_data.identifier_type,
        update_data.property,
        update_data.value,
        update_data.validity,
    )


def delete_company_data_source_identifier_bll(identifier_id: int) -> bool:
    """Business Logic Layer for deleting a CompanyDataSourceIdentifier instance.

    This function calls the ORM query function delete_company_data_source_identifier.
    """
    return delete_company_data_source_identifier(get_session(), identifier_id)
