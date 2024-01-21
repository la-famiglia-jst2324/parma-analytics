"""Company DB queries."""


from sqlalchemy.engine import Engine
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


def create_company(db: Session, name: str, added_by: int, description: str | None):
    """Creates a company."""
    new_company = Company(name=name, added_by=added_by, description=description)
    db.add(new_company)
    db.commit()
    db.refresh(new_company)
    return new_company


def get_company(db: Session, company_id: int):
    """Returns a company by id."""
    return db.query(Company).filter(Company.id == company_id).first()


def get_companies(db: Session):
    """Return all companies."""
    return db.query(Company).all()


def update_company(
    db: Session,
    company_id: int,
    name: str,
    added_by: int,
    description: str,
):
    """Updates company data."""
    company = get_company(db, company_id)
    if company is None:
        return None
    if name is not None:
        company.name = name
    if added_by is not None:
        company.added_by = added_by
    if description is not None:
        company.description = description
    db.commit()
    db.refresh(company)
    return company


def delete_company(db: Session, company_id: int):
    """Deletes a company."""
    company = get_company(db, company_id)
    if company is None:
        return None
    db.delete(company)
    db.commit()
    return company


def company_exists_by_name(db: Session, name: str) -> bool:
    """Checks if a company with the given name exists."""
    return bool(db.query(Company).filter(Company.name.ilike(name)).first())


def get_company_name(engine: Engine, company_id: int) -> str:
    """Get Company Name from the company_id."""
    with Session(engine) as session:
        company = session.query(Company).filter(Company.id == company_id).first()
        return company.name
