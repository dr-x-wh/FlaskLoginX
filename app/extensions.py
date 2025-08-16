from flask import Flask
from flask_migrate import Migrate
from flask_caching import Cache
from flask_sqlalchemy import SQLAlchemy

db: SQLAlchemy = SQLAlchemy()
migrate: Migrate = Migrate()
cache_client: Cache = Cache()


def init_extensions(app: Flask):
    db.init_app(app)
    migrate.init_app(app, db)
    cache_client.init_app(app)
