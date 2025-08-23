from datetime import datetime
from typing import Optional

from flask_sqlalchemy.pagination import Pagination

from app.extensions import db
from app.models.setting import Setting


class SettingService:
    @staticmethod
    def get_by_id(setting_id: int) -> Optional[Setting]:
        setting = Setting.query.get(setting_id)
        if not setting:
            return None
        return setting

    @staticmethod
    def get_value_by_key(key: str) -> Optional[str]:
        setting = Setting.query.filter_by(key=key).first()
        if not setting:
            return None
        return setting.value

    @staticmethod
    def get_pagination(query) -> Optional[Pagination]:
        page = query.get('page', 1, type=int)
        per_page = query.get('per_page', 10, type=int)
        desc = query.get('desc', 'true').lower() == 'true'
        order_by = query.get('order_by', 'key')

        qQuery = Setting.query

        if name := query.get('name'):
            qQuery = qQuery.filter(Setting.name.like(f'%{name}%'))

        if key := query.get('key'):
            qQuery = qQuery.filter(Setting.key.like(f'%{key}%'))

        order_field = getattr(Setting, order_by)
        if desc:
            order_field = order_field.desc()
        qQuery = qQuery.order_by(order_field)

        return qQuery.paginate(page=page, per_page=per_page, error_out=False)

    @staticmethod
    def update(setting_id: int, value: str, username: str) -> Optional[Setting]:
        setting = Setting.query.get(setting_id)
        if not setting:
            return None
        setting.value = value
        setting.update_by = username
        setting.update_time = datetime.now()
        db.session.commit()
        db.session.refresh(setting)
        if setting:
            return setting
        return None
