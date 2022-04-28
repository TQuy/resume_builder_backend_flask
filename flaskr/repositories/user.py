from flaskr.models import *
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.exc import IntegrityError


def insert_user(username: str, password: str) -> str:
    '''
        Insert row into table user
    '''
    message = ''
    try:
        user = User(
            username=username,
            password=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()
        return message
    except IntegrityError:
        message = f"Username already registered."
    except BaseException:
        message = "Unexpected error happened."
    return message


def filter_by_username(username: str):
    '''
        query row using username and password
    '''
    return User.query.filter_by(username=username).first()
