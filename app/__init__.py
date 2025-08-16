from typing import Optional

from flask import Flask
from flask_cors import CORS

from app.config import Config

app: Optional[Flask] = None


def create_app(def_conf: Config = Config) -> Flask:
    global app
    if not app:
        app = Flask(__name__)
        app.config.from_object(def_conf)
        CORS(app)

        from app.extensions import init_extensions
        init_extensions(app)

        # from app.errors.handler import init_error_handler
        # init_error_handler(app)

        from app.api import init_blueprint
        init_blueprint(app)

    return app


__all__ = ["create_app"]
