from flaskr.models import *
from sqlalchemy import select
from typing import Union
from sqlalchemy.exc import NoResultFound
import json

from flaskr.repositories import resume


def list_resume(current_user) -> list:
    res = resume.filter_by_user(current_user)
    if res is None:
        return []
    resume_list = [dict(i) for i in res]
    return resume_list


def load_resume(current_user, resume_id):
    res = resume.filter_by_user_and_resume_id(current_user, resume_id)
    return res


def save_resume(current_user, name: str, content: str):
    existed = True
    updated_resume = Resume.query.filter_by(
        name=name, user=current_user).first()
    if not updated_resume:
        updated_resume = Resume(
            name=name,
            user=current_user
        )
        existed = False

    updated_resume.content = json.dumps(content)
    if existed:
        db.session.add(updated_resume)
    db.session.commit()
    return updated_resume


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
