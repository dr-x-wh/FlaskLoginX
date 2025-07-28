from flask import Flask
from flask_migrate import Migrate
from flask_redis import FlaskRedis
from flask_sqlalchemy import SQLAlchemy

db: SQLAlchemy = SQLAlchemy()
migrate: Migrate = Migrate()
redis_client: FlaskRedis = FlaskRedis()


def init_extensions(app: Flask) -> None:
    db.init_app(app)
    migrate.init_app(app, db)
    redis_client.init_app(app)
