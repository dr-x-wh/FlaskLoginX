from datetime import date
from typing import Optional, List

from flask_sqlalchemy.pagination import Pagination
from sqlalchemy import or_, and_

from app.extensions import db, logger
from app.models.info import Info


class InfoService:
    @staticmethod
    def get_by_id(info_id: int) -> Optional[Info]:
        info = Info.query.get(info_id)
        if not info:
            return None
        return info

    @staticmethod
    def get_job() -> List[Info]:
        infos = Info.query.filter(
            and_(or_(Info.state.is_(None), Info.state != "1"), Info.end_date <= date.today())).all()
        if not infos:
            return []
        return infos

    @staticmethod
    def get_pagination_by_user_id(query, user_id: int) -> Optional[Pagination]:
        page = query.get('page', 1, type=int)
        per_page = query.get('per_page', 10, type=int)
        desc = query.get('desc', 'true').lower() == 'true'
        order_by = query.get('order_by', 'id')

        qQuery = Info.query

        qQuery = qQuery.filter(Info.user_id == user_id)

        if name := query.get('name'):
            qQuery = qQuery.filter(Info.name.like(f'%{name}%'))

        if person := query.get('person'):
            qQuery = qQuery.filter(Info.person.like(f'%{person}%'))

        if phone := query.get('phone'):
            qQuery = qQuery.filter(Info.phone.like(f'%{phone}%'))

        if (start_date_0 := query.get("start_date_0")) and (start_date_1 := query.get("start_date_1")):
            start_date_0 = date.fromisoformat(start_date_0)
            start_date_1 = date.fromisoformat(start_date_1)
            qQuery = qQuery.filter(Info.start_date.between(start_date_0, start_date_1))

        if (end_date_0 := query.get("end_date_0")) and (end_date_1 := query.get("end_date_1")):
            end_date_0 = date.fromisoformat(end_date_0)
            end_date_1 = date.fromisoformat(end_date_1)
            qQuery = qQuery.filter(Info.end_date.between(end_date_0, end_date_1))

        order_field = getattr(Info, order_by)
        if desc:
            order_field = order_field.desc()
        qQuery = qQuery.order_by(order_field)

        return qQuery.paginate(page=page, per_page=per_page, error_out=False)

    @staticmethod
    def create(user_id: int, name: str, start_date: date, end_date: date, person: Optional[int],
               phone: Optional[int]) -> Optional[Info]:
        info = Info()
        info.user_id = user_id
        info.name = name
        info.start_date = start_date
        info.end_date = end_date
        if person:
            info.person = person
        if phone:
            info.phone = phone
        db.session.add(info)
        db.session.commit()
        db.session.refresh(info)
        if info:
            return info
        return None

    @staticmethod
    def update(info_id: int, name: Optional[str], start_date: Optional[str], end_date: Optional[str],
               person: Optional[int], phone: Optional[int]) -> Optional[Info]:
        info = Info.query.get(info_id)
        if not info:
            return None
        if name:
            info.name = name
        try:
            if start_date:
                info.start_date = date.fromisoformat(start_date)
            if end_date:
                info.end_date = date.fromisoformat(end_date)
        except ValueError as e:
            logger.warning(str(e))
        if person:
            info.person = person
        if phone:
            info.phone = phone
        db.session.commit()
        db.session.refresh(info)
        if info:
            return info
        return None

    @staticmethod
    def delete_info(info_id: int, user_id: int) -> bool:
        db_info = Info.query.filter_by(id=info_id, user_id=user_id).first()
        if db_info:
            db.session.delete(db_info)
            db.session.commit()
            return True
        return False

    @staticmethod
    def state_finish(info_id: int) -> bool:
        db_info = Info.query.get(info_id)
        if db_info:
            db_info.state = "1"
            db.session.commit()
            return True
        return False
