from flaskr.models import *
from sqlalchemy import select


def filter_by_user(current_user):
    res = db.session.execute(
        select(
            Resume.id,
            Resume.name
        ).where(
            Resume.user_id == current_user.id
        )
    ).all()
    return res


def filter_by_user_and_id(current_user, resume_id):
    return Resume.query.filter_by(id=resume_id, user=current_user).first()
