"""DB queries for the company data source model."""
from dataclasses import dataclass

from sqlalchemy.orm.session import Session

from parma_analytics.db.prod.models.company_data_source import CompanyDataSource


@dataclass
class CompanyDataSourceData:
    """Class for creating CompanyDataSource instances."""

    data_source_id: int
    company_id: int
    is_data_source_active: bool
    health_status: str


@dataclass
class CompanyDataSourceUpdateData:
    """Class for updating CompanyDataSource instances."""

    is_data_source_active: bool | None = None
    health_status: str | None = None


def get_company_data_source(
    db_session: Session, company_id: int, data_source_id: int
) -> CompanyDataSource | None:
    """Fetch CompanyDataSource based on company_id and data_source_id."""
    with db_session as session:
        company_data_source = (
            session.query(CompanyDataSource)
            .filter(
                CompanyDataSource.company_id == company_id,
                CompanyDataSource.data_source_id == data_source_id,
            )
            .first()
        )

        return company_data_source


def get_all_company_data_sources_by_data_source_id(
    db_session: Session, data_source_id: int
) -> list[CompanyDataSource]:
    """Fetch all CompanyDataSource instances based on data_source_id."""
    with db_session as session:
        company_data_sources: list[CompanyDataSource] = (
            session.query(CompanyDataSource)
            .filter(
                CompanyDataSource.data_source_id == data_source_id,
            )
            .all()
        )

        return company_data_sources


def get_all_company_data_sources(db_session: Session) -> list[CompanyDataSource]:
    """Fetch all CompanyDataSource instances."""
    with db_session as session:
        company_data_sources = session.query(CompanyDataSource).all()

        return company_data_sources


def create_company_data_source(
    db_session: Session, data: CompanyDataSourceData
) -> CompanyDataSource:
    """Create a new CompanyDataSource instance."""
    with db_session as session:
        new_data_source = CompanyDataSource(
            data_source_id=data.data_source_id,
            company_id=data.company_id,
            is_data_source_active=data.is_data_source_active,
            health_status=data.health_status,
        )

        session.add(new_data_source)
        session.commit()

        return new_data_source


def update_company_data_source(
    db_session: Session, id: int, data: CompanyDataSourceUpdateData
) -> CompanyDataSource | None:
    """Update an existing CompanyDataSource instance."""
    with db_session as session:
        data_source = (
            session.query(CompanyDataSource).filter(CompanyDataSource.id == id).first()
        )

        if data_source:
            if data.is_data_source_active is not None:
                data_source.is_data_source_active = data.is_data_source_active
            if data.health_status is not None:
                data_source.health_status = data.health_status

            session.commit()

            return data_source
        else:
            return None


def delete_company_data_source(db_session: Session, id: int) -> bool:
    """Delete a CompanyDataSource instance."""
    with db_session as session:
        data_source = (
            session.query(CompanyDataSource).filter(CompanyDataSource.id == id).first()
        )

        if data_source:
            session.delete(data_source)
            session.commit()

            return True
        else:
            return False
