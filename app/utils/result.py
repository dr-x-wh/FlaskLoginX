from typing import Any

from flask import jsonify


class Result:
    @staticmethod
    def success(data: Any = None, message: str = "success") -> tuple:
        return jsonify({"code": 2000, "message": message, "data": data}), 200

    @staticmethod
    def error(message: str = "unknown error", code: int = 5000, status_code: int = 500, data: Any = None) -> tuple:
        return jsonify({"code": code, "message": message, "data": data}), status_code
