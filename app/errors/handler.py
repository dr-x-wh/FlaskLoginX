from flask import Flask
from werkzeug.exceptions import HTTPException

from app.errors import BodyNotJsonError
from app.utils.result import Result


def init_error_handler(app: Flask):
    @app.errorhandler(BodyNotJsonError)
    def handle_body(e: BodyNotJsonError) -> tuple:
        return Result.error(e.message, e.code, e.status_code)

    @app.errorhandler(HTTPException)
    def handle_http(e: HTTPException) -> tuple:
        return Result.error(e.name, e.code, e.code)

    @app.errorhandler(Exception)
    def handle_all(e: Exception) -> tuple:
        return Result.error(str(e))
