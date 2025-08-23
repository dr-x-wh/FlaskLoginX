import random
import re
import string

from flask import Blueprint, request

from app.extensions import cache_client
from app.utils.result import Result
from app.utils.sms_tools import send_sms

code_bp = Blueprint("code", __name__, url_prefix="/code")


@code_bp.route("", methods=["POST"])
def get_info():
    data = request.json
    if "phone" not in data or not re.fullmatch(r"^1[3-9]\d{9}$", data.get("phone", "")):
        return Result.error()
    for i in range(3):
        code = ''.join(random.choices(string.digits, k=6))
        if send_sms(data["phone"], code):
            cache_client.set(f"phone_code_{data["phone"]}", code, timeout=60)
            return Result.success()
    return Result.error()
