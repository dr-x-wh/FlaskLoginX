import re

from flask import Blueprint, request
from werkzeug.routing import ValidationError

from app.extensions import cache_client
from app.services.user import UserService
from app.utils.result import Result
from app.utils.security import login_required, UserTools

user_bp = Blueprint("user", __name__, url_prefix="/user")


@user_bp.route("", methods=["POST"])
def register():
    user = request.json
    if "username" not in user or "password" not in user or "phone" not in user or "code" not in user:
        raise ValidationError()
    if not re.fullmatch(r"^1[3-9]\d{9}$", user["phone"]) or len(user["password"]) < 6:
        return Result.error("手机号格式错误")
    cache_code = cache_client.get(f"phone_code_{user["phone"]}")
    if cache_code is None or user["code"] != cache_code:
        return Result.error("验证码错误")
    db_user = UserService.get_by_username(user["username"])
    if db_user:
        return Result.error("用户名已存在")
    db_user = UserService.create(user["username"], user["password"], user["phone"], user.get("remind_time"))
    if not db_user:
        return Result.error("注册失败")
    return Result.success()


@user_bp.route("", methods=["DELETE"])
@login_required
def sign_out():
    return Result.success(UserService.delete_user(UserTools.get_current_user().get("id")))


@user_bp.route("/info", methods=["GET"])
@login_required
def info():
    return Result.success(UserTools.get_current_user())


@user_bp.route("/setting", methods=["PUT"])
@login_required
def setting_update():
    data = request.json
    db_user = UserService.setting_update(data.get("phone"), data.get("remind_time"))
    if db_user:
        return Result.success()
    return Result.error()
