from flask import Blueprint, request, g
from werkzeug.routing import ValidationError

from app.errors import BodyNotJsonError
from app.services.user import UserService
from app.utils.result import Result
from app.utils.security import login_required

user_bp = Blueprint("user", __name__, url_prefix="/user")


@user_bp.route("", methods=["POST"])
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


@user_bp.route("/info", methods=["GET"])
@login_required
def info():
    return Result.success(g.current_user)
