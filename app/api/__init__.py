from flask import Flask


def init_blueprint(app: Flask) -> None:
    from app.api.auth import auth_bp
    app.register_blueprint(auth_bp)
    from app.api.user import user_bp
    app.register_blueprint(user_bp)
