"""Company DB queries."""


from sqlalchemy.orm import Session

from parma_analytics.db.prod.models.company import Company

# @dataclass
# class CompanyModel:
#     """Class for creating identifiers."""

#     id: int
#     name: str
#     description: str | None
#     added_by: int
#     value: str
#     created_at: datetime | None
#     modified_at: datetime | None


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
