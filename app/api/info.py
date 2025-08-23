from datetime import date

from flask import Blueprint, request

from app.services.info import InfoService
from app.utils.result import Result
from app.utils.security import login_required, UserTools

info_bp = Blueprint("info", __name__, url_prefix="/info")


@info_bp.route("/<int:info_id>", methods=["GET"])
@login_required
def get_info(info_id: int):
    info = InfoService.get_by_id(info_id)
    if info and info.user_id == UserTools.get_current_user().get("id"):
        return Result.success(info.to_dict())
    return Result.error()


@info_bp.route("/list", methods=["GET"])
@login_required
def get_infos():
    query = request.args
    user_id = UserTools.get_current_user().get("id")
    infos = InfoService.get_pagination_by_user_id(query, user_id)
    if infos is not None:
        return Result.success({"total": infos.total, "data": [info.to_dict() for info in infos.items]})
    return Result.error()


@info_bp.route("", methods=["POST"])
@login_required
def create():
    info = request.json
    if "name" not in info or "start_date" not in info or "end_date" not in info:
        return Result.error()
    try:
        start_date = date.fromisoformat(info["start_date"])
        end_date = date.fromisoformat(info["end_date"])
    except ValueError as e:
        return Result.error(str(e))
    db_info = InfoService.create(UserTools.get_current_user().get("id"), info["name"], start_date, end_date,
                                 info.get("person"), info.get("phone"))
    if not db_info:
        return Result.error()
    return Result.success()


@info_bp.route("", methods=["PATCH"])
@login_required
def update_info():
    info = request.json
    if info_id := info.get("id"):
        info_by_id = InfoService.get_by_id(info_id)
        if not info_by_id or info_by_id.user_id != UserTools.get_current_user().get("id"):
            return Result.error()
        if info_by_id.user_id != UserTools.get_current_user().get("id"):
            return Result.error()
        db_info = InfoService.update(info_id, info.get("name"), info.get("start_date"), info.get("end_date"),
                                     info.get("person"), info.get("phone"))
        if not db_info:
            return Result.error()
    return Result.success([])


@info_bp.route("/<int:info_id>", methods=["DELETE"])
@login_required
def del_info(info_id: int):
    if InfoService.delete_info(info_id, UserTools.get_current_user().get("id")):
        return Result.success()
    return Result.error()
