from parma_analytics.db.prod.engine import get_session
from parma_analytics.db.prod.models.user import User


def test_user_crud():
    with get_session() as session:
        count = session.query(User).count()

        # Create
        user = User(
            auth_id="auth_id",
            name="name",
            profile_picture="profile_picture",
            role="USER",
        )
        session.add(user)
        session.commit()

        assert session.query(User).count() == count + 1

        # Read
        user = session.query(User).filter(User.auth_id == "auth_id").one()
        assert user.auth_id == "auth_id"
        assert user.name == "name"
        assert user.profile_picture == "profile_picture"
        assert user.role == "USER"

        # Update
        user.name = "new_name"
        session.commit()
        user = session.query(User).filter(User.auth_id == "auth_id").one()
        assert user.name == "new_name"

        # Delete
        session.delete(user)
        session.commit()
        user = session.query(User).filter(User.auth_id == "auth_id").one_or_none()
        assert user is None

        assert session.query(User).count() == count
