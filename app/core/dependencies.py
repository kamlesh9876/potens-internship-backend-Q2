from sqlalchemy.orm import Session
from fastapi import Depends

from app.db.session import get_db
from app.repositories.user_repository import UserRepository
from app.models.user import User


async def get_current_user(
    db: Session = Depends(get_db),
) -> User:
    """
    Temporary dependency without authentication.
    Returns the first user in the database.
    """
    user_repository = UserRepository(db)
    user = user_repository.get_by_id(1)

    if user is None:
        raise Exception("No user found in database")

    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    return current_user


async def get_current_admin_user(
    current_user: User = Depends(get_current_user),
) -> User:
    return current_user