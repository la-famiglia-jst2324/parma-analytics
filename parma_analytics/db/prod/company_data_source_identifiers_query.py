"""CompanyDataSourceIdentifier DB queries."""

from models.company_data_source import CompanyDataSource
from models.company_data_source_identifier import (
    CompanyDataSourceIdentifier,
)
from sqlalchemy import Engine
from sqlalchemy.orm.session import Session

from parma_analytics.bl.company_data_source_identifiers_bll import (
    IdentifierData,
    IdentifierUpdateData,
)


def get_company_data_source_identifiers(
    engine: Engine, company_id: int, data_source_id: int
) -> list[CompanyDataSourceIdentifier] | None:
    """Fetch identifiers based on company_id and data_source_id."""
    with Session(engine) as session:
        company_data_source = (
            session.query(CompanyDataSource)
            .filter(
                CompanyDataSource.company_id == company_id,
                CompanyDataSource.data_source_id == data_source_id,
            )
            .first()
        )

        if company_data_source:
            return company_data_source.company_data_source_identifiers
        else:
            return None


def create_company_data_source_identifier(
    engine: Engine, identifier_data: IdentifierData
) -> CompanyDataSourceIdentifier:
    """Create a new CompanyDataSourceIdentifier instance."""
    with Session(engine) as session:
        new_identifier = CompanyDataSourceIdentifier(
            company_data_source_id=identifier_data.company_data_source_id,
            identifier_key=identifier_data.identifier_key,
            identifier_type=identifier_data.identifier_type,
            property=property,
            value=identifier_data.value,
            validity=identifier_data.validity,
        )

        session.add(new_identifier)
        session.commit()

        return new_identifier


def update_company_data_source_identifier(
    engine: Engine, identifier_id: int, identifier_data: IdentifierUpdateData
) -> CompanyDataSourceIdentifier | None:
    """Update an existing CompanyDataSourceIdentifier instance."""
    with Session(engine) as session:
        identifier = (
            session.query(CompanyDataSourceIdentifier)
            .filter(CompanyDataSourceIdentifier.id == identifier_id)
            .first()
        )

        if identifier:
            if identifier_data.identifier_key is not None:
                identifier.identifier_key = identifier_data.identifier_key
            if identifier_data.identifier_type is not None:
                identifier.identifier_type = identifier_data.identifier_type
            if property is not None:
                identifier.property = property
            if identifier_data.value is not None:
                identifier.value = identifier_data.value
            if identifier_data.validity is not None:
                identifier.validity = identifier_data.validity

            session.commit()

            return identifier
        else:
            return None


def delete_company_data_source_identifier(engine: Engine, identifier_id: int) -> bool:
    """Delete a CompanyDataSourceIdentifier instance."""
    with Session(engine) as session:
        identifier = (
            session.query(CompanyDataSourceIdentifier)
            .filter(CompanyDataSourceIdentifier.id == identifier_id)
            .first()
        )

        if identifier:
            session.delete(identifier)
            session.commit()

            return True
        else:
            return False
