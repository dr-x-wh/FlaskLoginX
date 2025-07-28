from flask import request, Blueprint
from werkzeug.routing import ValidationError

from app.errors import BodyNotJsonError
from app.services.user import UserService
from app.utils.result import Result
from app.utils.security import SecurityUtils, login_required

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

    jwt = SecurityUtils.login(db_user.id)

    return Result.success(jwt)


@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    SecurityUtils.logout()
    return Result.success()
