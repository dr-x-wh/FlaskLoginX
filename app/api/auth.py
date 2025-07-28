from flask import request, Blueprint
from werkzeug.routing import ValidationError

from app.errors import BodyNotJsonError
from app.services.user import UserService
from app.utils.result import Result

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["POST"])
def login():
    if not request.is_json:
        raise BodyNotJsonError()
    user = request.json
    if "username" not in user or "password" not in user:
        raise ValidationError()
    db_user = UserService.get_by_username(user["username"])
    if not db_user:
        return Result.error("账号密码错误")
    if not db_user.check_password(user["password"]):
        return Result.error("账号密码错误")

    # 登录

    return Result.success()


@auth_bp.route("/logout", methods=["POST"])
def logout():
    # 退出登录

    return Result.success()


@auth_bp.route("/register", methods=["POST"])
def register():
    if not request.is_json:
        raise BodyNotJsonError()
    user = request.json
    if "username" not in user or "password" not in user:
        raise ValidationError()
    db_user = UserService.get_by_username(user["username"])
    if db_user:
        raise Exception("用户名已存在")
    db_user = UserService.create(user["username"], user["password"])
    if not db_user:
        return Result.error("注册失败")
    return Result.success()


@auth_bp.route("/info", methods=["GET"])
def info():
    return Result.success()
