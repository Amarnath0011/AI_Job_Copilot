from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.db.models import User


def get_user_by_email(
    db: Session,
    email: str,
):
    return (
        db.query(User)
        .filter(User.email == email)
        .first()
    )


def create_user(
    db: Session,
    name: str,
    email: str,
    password: str,
):
    password_hash = hash_password(password)

    user = User(
        name=name,
        email=email,
        password_hash=password_hash,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user