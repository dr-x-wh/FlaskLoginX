import os
from typing import Optional

from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY: str = os.getenv("SECRET_KEY", "9WIzYYFUKpyC4kV23Y7lbuMFHksJUmtFVXQTGS2e")
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "mfzPxQxbveE5gXcsGOeH0xdvTqiSp06v97IZ7r5j")
    JWT_ACCESS_TOKEN_EXPIRES: int = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", "86400"))

    SQLALCHEMY_DATABASE_URI: Optional[str] = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    REDIS_URL: Optional[str] = os.getenv("REDIS_URL")
