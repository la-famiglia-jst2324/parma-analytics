"""CompanyDataSourceIdentifier DB queries."""

from dataclasses import dataclass
from datetime import datetime

from sqlalchemy.orm.session import Session

from parma_analytics.db.prod.models.company_data_source import CompanyDataSource
from parma_analytics.db.prod.models.company_data_source_identifier import (
    CompanyDataSourceIdentifier,
    IdentifierType,
)


@dataclass
class IdentifierData:
    """Class for creating identifiers."""

    company_data_source_id: int
    identifier_type: str
    # TODO: REMOVE identifier_key
    identifier_key: str
    property: str
    value: str
    validity: datetime


@dataclass
class IdentifierUpdateData:
    """Class for updating identifiers."""

    identifier_type: IdentifierType | None = None
    property: str | None = None
    value: str | None = None
    validity: datetime | None = None


def get_company_data_source_identifiers(
    db_session: Session, company_id: int, data_source_id: int
) -> list[CompanyDataSourceIdentifier] | None:
    """Fetch identifiers based on company_id and data_source_id."""
    with db_session as session:
        company_data_source: CompanyDataSource = (
            session.query(CompanyDataSource)
            .filter(
                CompanyDataSource.company_id == company_id,
                CompanyDataSource.data_source_id == data_source_id,
            )
            .first()
        )

        if not company_data_source:
            return None

        identifiers: list[CompanyDataSourceIdentifier] = (
            session.query(CompanyDataSourceIdentifier)
            .filter(
                CompanyDataSourceIdentifier.company_data_source_id
                == company_data_source.id
            )
            .all()
        )

        return identifiers


def create_company_data_source_identifier(
    db_session: Session, identifier_data: IdentifierData
) -> CompanyDataSourceIdentifier:
    """Create a new CompanyDataSourceIdentifier instance."""
    with db_session as session:
        new_identifier = CompanyDataSourceIdentifier(
            company_data_source_id=identifier_data.company_data_source_id,
            identifier_type=identifier_data.identifier_type,
            property=identifier_data.property,
            value=identifier_data.value,
            validity=identifier_data.validity,
            # TODO: REMOVE identifier_key
            identifier_key=identifier_data.identifier_key,
        )

        session.add(new_identifier)
        session.commit()

        return new_identifier


def update_company_data_source_identifier(
    db_session: Session, identifier_id: int, identifier_data: IdentifierUpdateData
) -> CompanyDataSourceIdentifier | None:
    """Update an existing CompanyDataSourceIdentifier instance."""
    with db_session as session:
        identifier = (
            session.query(CompanyDataSourceIdentifier)
            .filter(CompanyDataSourceIdentifier.id == identifier_id)
            .first()
        )

        if identifier:
            if identifier_data.identifier_type is not None:
                identifier.identifier_type = identifier_data.identifier_type
            if identifier_data.property is not None:
                identifier.property = identifier_data.property
            if identifier_data.value is not None:
                identifier.value = identifier_data.value
            if identifier_data.validity is not None:
                identifier.validity = identifier_data.validity

            session.commit()

            return identifier
        else:
            return None


def delete_company_data_source_identifier(
    db_session: Session, identifier_id: int
) -> bool:
    """Delete a CompanyDataSourceIdentifier instance."""
    with db_session as session:
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
