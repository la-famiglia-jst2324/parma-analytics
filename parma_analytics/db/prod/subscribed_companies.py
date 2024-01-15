"""Database operations to get user subscribed companies."""
from sqlalchemy.exc import SQLAlchemyError

from parma_analytics.db.prod.engine import get_session
from parma_analytics.db.prod.models.subscribed_companies import CompanySubscription


def get_subscribed_companies(user_id: str) -> list[int]:
    """Gets subscribed companies for a particular user.

    Args:
        user_id: The id for a particular user

    Returns:
        list: The list of the subscribed companies for that user
    """
    try:
        with get_session() as session:
            company_ids = (
                session.query(CompanySubscription.companyId)
                .filter(CompanySubscription.userId == user_id)
                .all()
            )
            return [company_id for (company_id,) in company_ids]
    except SQLAlchemyError:
        raise ValueError(f"Invalid type: {user_id}")
