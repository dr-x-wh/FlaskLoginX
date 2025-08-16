import uuid
from datetime import datetime, timedelta
from functools import wraps

import jwt
from flask import current_app, request, g

from app.extensions import cache_client
from app.services.user import UserService
from app.utils.result import Result


class UserTools:
    @staticmethod
    def login(user_id: int) -> str:
        jwt_exp = datetime.now() + timedelta(seconds=current_app.config.get("JWT_ACCESS_TOKEN_EXPIRES"))
        token = str(uuid.uuid4().hex)
        cache_client.set(f"USER_SESSION_{user_id}", token, current_app.config.get("JWT_ACCESS_TOKEN_EXPIRES"))
        payload = {"exp": jwt_exp.timestamp(), "iat": datetime.now().timestamp(), "sub": f"{user_id}",
                   "session_id": token, }
        return jwt.encode(payload=payload, key=current_app.config.get("JWT_SECRET_KEY"), algorithm="HS256")

    @staticmethod
    def logout() -> bool:
        if user_id := g.current_user.get("id"):
            cache_client.delete(f"USER_SESSION_{user_id}")
            return True
        return False

    @staticmethod
    def get_current_user() -> dict:
        return g.current_user


def login_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return Result.error("请登陆后再试", 4011, 401)

        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            return Result.error("请登陆后再试", 4012, 401)

        token = parts[1]

        try:
            payload = jwt.decode(token, key=current_app.config.get("JWT_SECRET_KEY"), algorithms="HS256",
                                 options={"verify_exp": True})
        except jwt.ExpiredSignatureError:
            return Result.error("登录已过期，请重新登陆", 4013, 401)
        except jwt.InvalidSignatureError:
            return Result.error("登陆失效", 4014, 401)
        except Exception as e:
            return Result.error(f"登录状态异常：{str(e)}", 4015, 401)

        user_id = int(payload.get('sub'))
        db_user = UserService.get_by_id(user_id)
        if not db_user:
            return Result.error("登陆失效", 4016, 401)

        session_id = payload.get('session_id')
        redis_session_id = redis_client.get(f"USER_SESSION_{db_user.id}")
        if not redis_session_id:
            return Result.error("登陆失效", 4017, 401)
        if redis_session_id.decode() != session_id:
            return Result.error("您的账号已在其他地方登录", 4018, 401)

        g.current_user = {"id": db_user.id, "username": db_user.username}
        return view_func(*args, **kwargs)

    return wrapper
