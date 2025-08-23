from typing import Optional

from app.extensions import db
from app.models import UserRole
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
    def create(username: str, password: str, phone: str, remind_time: Optional[str]) -> Optional[User]:
        db_user = User.query.filter(User.username == username).first()
        if db_user:
            return None
        user = User()
        user.username = username
        user.set_password(password)
        user.phone = phone
        if remind_time:
            user.remind_time = remind_time
        count = User.query.count()
        if count == 0:
            user.role = UserRole.ADMIN
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)
        if user:
            return user
        return None

    @staticmethod
    def setting_update(phone: Optional[str], remind_time: Optional[str]) -> Optional[User]:
        from app.utils.security import UserTools
        user_id = UserTools.get_current_user().get("id")
        db_user = User.query.get(user_id)
        if not db_user:
            return None
        db_user.phone = phone
        db_user.remind_time = remind_time
        db.session.commit()
        db.session.refresh(db_user)
        if db_user:
            return db_user
        return None

    @staticmethod
    def delete_user(user_id: int) -> bool:
        db_user = User.query.get(user_id)
        if db_user:
            db.session.delete(db_user)
            db.session.commit()
            return True
        return False
