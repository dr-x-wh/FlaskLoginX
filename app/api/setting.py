from flask import Blueprint, request

from app.services.setting import SettingService
from app.utils.result import Result
from app.utils.security import login_required, UserTools

setting_bp = Blueprint("setting", __name__, url_prefix="/setting")


@setting_bp.route("/list", methods=["GET"])
@login_required
def get_infos():
    query = request.args
    settings = SettingService.get_pagination(query)
    if settings is not None:
        return Result.success({"total": settings.total, "data": [info.to_dict() for info in settings.items]})
    return Result.error()


@setting_bp.route("", methods=["PATCH"])
@login_required
def update_info():
    setting = request.json
    if setting_id := setting.get("id"):
        setting_by_id = SettingService.get_by_id(setting_id)
        if setting_by_id:
            db_info = SettingService.update(setting_id, setting.get("value"),
                                            UserTools.get_current_user().get("username"))
            if not db_info:
                return Result.error()
            return Result.success()
    return Result.error()
