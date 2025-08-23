from flask import Flask
from sqlalchemy import inspect

from app.extensions import db


def init_data(app: Flask) -> None:
    with app.app_context():
        inspector = inspect(db.engine)
        if "setting" in inspector.get_table_names():
            from app.models.setting import Setting
            from app.services.setting import SettingService
            notice_phone = Setting.query.filter_by(key="notice_phone").first()
            if not notice_phone:
                new_notice_phone = Setting()
                new_notice_phone.name = "通知手机号"
                new_notice_phone.key = "notice_phone"
                db.session.add(new_notice_phone)

            notice_time = Setting.query.filter_by(key="notice_time").first()
            if not notice_time:
                new_notice_time = Setting()
                new_notice_time.name = "通知时间"
                new_notice_time.key = "notice_time"
                db.session.add(new_notice_time)

            db.session.commit()
