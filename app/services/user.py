from typing import Optional

from app.extensions import db
from app.models.user import User


class UserService:
    @staticmethod
    def get_by_id(user_id: int) -> Optional[User]:
        user = User.query.get(user_id)
        if user:
            return user
        return None

    @staticmethod
    def get_by_username(username: str) -> Optional[User]:
        user = User.query.filter(User.username == username).first()
        if user:
            return user
        return None

    @staticmethod
    def create(username: str, password: str) -> Optional[User]:
        db_user = UserService.get_by_username(username)
        if db_user:
            return None
        user = User()
        user.username = username
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)
        if user:
            return user
        return None

    @staticmethod
    def delete_user(user_id: int) -> bool:
        db_user = User.query.get(user_id)
        if db_user:
            db.session.delete(db_user)
            db.session.commit()
            return True
        return False
