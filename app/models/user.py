from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db
from app.models import UserRole


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum(UserRole), nullable=False, default=UserRole.USER, server_default=UserRole.USER.value)
    remind_time = db.Column(db.String(255))

    def set_password(self, password: str) -> None:
        self.password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    def to_dict(self) -> dict:
        return {"id": self.id, "username": self.username, "phone": self.phone, "role": self.role.value,
                "remind_time": self.remind_time}
