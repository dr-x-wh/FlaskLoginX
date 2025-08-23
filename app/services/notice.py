from datetime import date
from typing import Optional, List

from flask_sqlalchemy.pagination import Pagination
from sqlalchemy import or_, and_

from app.extensions import db, logger
from app.models.notice import Notice


class NoticeService:
    @staticmethod
    def get_by_id(notice_id: int) -> Optional[Notice]:
        info = Notice.query.get(notice_id)
        if not info:
            return None
        return info

    @staticmethod
    def get_job() -> List[Notice]:
        notices = Notice.query.filter(
            and_(or_(Notice.state.is_(None), Notice.state != "1"))).all()
        if not notices:
            return []
        return notices

    @staticmethod
    def get_pagination(query) -> Optional[Pagination]:
        page = query.get('page', 1, type=int)
        per_page = query.get('per_page', 10, type=int)
        desc = query.get('desc', 'true').lower() == 'true'
        order_by = query.get('order_by', 'id')

        qQuery = Notice.query

        if title := query.get('title'):
            qQuery = qQuery.filter(Notice.title.like(f'%{title}%'))

        if (release_date_0 := query.get("release_date_0")) and (release_date_1 := query.get("release_date_1")):
            release_date_0 = date.fromisoformat(release_date_0)
            release_date_1 = date.fromisoformat(release_date_1)
            qQuery = qQuery.filter(Notice.release_date.between(release_date_0, release_date_1))

        order_field = getattr(Notice, order_by)
        if desc:
            order_field = order_field.desc()
        qQuery = qQuery.order_by(order_field)

        return qQuery.paginate(page=page, per_page=per_page, error_out=False)

    @staticmethod
    def create(title: str, release_date: str) -> Optional[Notice]:
        try:
            release_date = date.fromisoformat(release_date)
        except ValueError:
            return None
        db_notice = Notice.query.filter_by(title=title, release_date=release_date).first()
        if db_notice:
            return None
        notice = Notice()
        notice.title = title
        notice.release_date = release_date
        db.session.add(notice)
        db.session.commit()
        db.session.refresh(notice)
        if notice:
            return notice
        return None

    @staticmethod
    def state_finish(notice_id: int) -> bool:
        db_notice = Notice.query.get(notice_id)
        if db_notice:
            db_notice.state = "1"
            db.session.commit()
            return True
        return False
