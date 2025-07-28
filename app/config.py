import os
from typing import Optional

from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY: str = os.getenv("SECRET_KEY", "9WIzYYFUKpyC4kV23Y7lbuMFHksJUmtFVXQTGS2e")
    SQLALCHEMY_DATABASE_URI: Optional[str] = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    REDIS_URL: Optional[str] = os.getenv("REDIS_URL")
    TOKEN_EXPIRES: int = int(os.getenv("TOKEN_EXPIRES", "86400"))
