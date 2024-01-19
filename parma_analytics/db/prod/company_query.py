"""CompanyDataSourceIdentifier DB queries."""


from sqlalchemy.orm.session import Session

from parma_analytics.db.prod.models.company import Company


def create_company_if_not_exist(
    db_session: Session, name: str, description: str, added_by: int
) -> Company:
    """Add a new company to the database if it doesn't exist."""
    with db_session as session:
        record = session.query(Company).filter(Company.name == name).first()

        if record:
            # The company already exists, do nothing
            return record
        else:
            new_company = Company(name=name, description=description, added_by=added_by)
            session.add(new_company)

            session.commit()

            session.refresh(new_company)
            return new_company
