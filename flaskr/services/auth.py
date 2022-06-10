from typing import Optional, Union, Any, Tuple
from werkzeug.security import check_password_hash
from flaskr.models import *
import jwt
from flask import current_app
from flaskr.repositories import user
from flaskr.models import User


def handle_register_user(
    username: Union[str, None],
    password: Union[str, None],
) -> str:
    '''
    handle registration logic
    '''
    if not username:
        return 'Username is required.'

    elif not password:
        return 'Password is required.'

    return user.insert_user(username, password)


def authenticate_user(
    username: Union[str, None],
    password: Union[str, None]
) -> Tuple[Union[None, User], str]:
    """
    Return models.User object if authenticate successfully
    else return error message
    """
    if not username:
        return None, 'Username is required.'

    elif not password:
        return None, 'Password is required.'

    message = ""
    matched_user = User.query.filter_by(username=username).first()
    if matched_user is None:
        message = "Incorrect username."
    elif check_password_hash(matched_user.password, password) is None:
        message = "Incorrect password."

    return matched_user, message


def generate_jwt_token(user: User) -> str:
    token = jwt.encode(
        {
            "username": user.username,
            "user_id": user.id,
        },
        current_app.config['SECRET_KEY'],
        algorithm="HS256"
    )
    return token
