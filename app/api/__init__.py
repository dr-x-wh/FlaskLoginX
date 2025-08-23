from flask import Flask, request

from app.errors import BodyNotJsonError


def init_blueprint(app: Flask) -> None:
    from app.api.auth import auth_bp
    app.register_blueprint(auth_bp)
    from app.api.user import user_bp
    app.register_blueprint(user_bp)
    from app.api.info import info_bp
    app.register_blueprint(info_bp)
    from app.api.code import code_bp
    app.register_blueprint(code_bp)
    from app.api.notice import notice_bp
    app.register_blueprint(notice_bp)
    from app.api.setting import setting_bp
    app.register_blueprint(setting_bp)


def init_before(app: Flask) -> None:
    @app.before_request
    def chack_body_json():
        if request.method == 'POST' or request.method == 'PUT' or request.method == 'PATCH':
            if request.content_length > 0:
                if not request.is_json:
                    raise BodyNotJsonError()
