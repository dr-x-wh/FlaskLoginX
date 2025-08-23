from flask import Blueprint, request

from app.services.notice import NoticeService
from app.utils.result import Result
from app.utils.security import login_required

notice_bp = Blueprint("notice", __name__, url_prefix="/notice")


@notice_bp.route("/list", methods=["GET"])
@login_required
def get_infos():
    query = request.args
    notices = NoticeService.get_pagination(query)
    if notices is not None:
        return Result.success({"total": notices.total, "data": [info.to_dict() for info in notices.items]})
    return Result.error()
