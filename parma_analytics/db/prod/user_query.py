"""Operation related to User."""

from sqlalchemy.orm.session import Session

from parma_analytics.db.prod.models.user import User


def get_user(db: Session):
    """Returns a user list."""
    return db.query(User.id).all()
