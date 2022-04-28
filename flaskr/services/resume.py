from flaskr.models import *
from sqlalchemy import select
from typing import Union
from sqlalchemy.exc import NoResultFound
import json
from flask import jsonify


def list_resume(current_user) -> list:
    res = db.session.execute(
        select(
            Resume.id,
            Resume.name).join(User).where(
            User.id == current_user.id)).all()
    if res is None:
        return []
    resume_list = [dict(i) for i in res]
    return resume_list


def load_resume(current_user, resume_id):
    resume = db.session.scalar(
        select(Resume).where(
            Resume.id == resume_id).where(
            Resume.user_id == current_user.id)).first()
    return resume


def save_resume(current_user, name: str, content: str):
    existed = True
    try:
        resume = Resume.query.filter_by(user=current_user, name=name).one()
    except NoResultFound:
        resume = Resume(
            name=name,
            user=current_user
        )
        existed = False
    finally:
        resume.content = json.dumps(content)
        if existed:
            db.session.add(resume)
        db.session.commit()
    return resume


def validate_input_save_form(
        name: Union[str, None], content: Union[str, None]) -> Union[str, None]:
    if not name:
        return "Name of resume is required."
    elif not content:
        return "Content of resume is required."
    return None


def delete_resume(current_user, resume_id: id) -> bool:
    try:
        resume = Resume.query.filter_by(
            id=resume_id, user=current_user).one()
    except NoResultFound:
        return False

    db.session.delete(resume)
    db.session.commit()
    return True
