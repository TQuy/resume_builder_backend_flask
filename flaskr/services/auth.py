from typing import Optional, Union, Any, Tuple
from werkzeug.security import check_password_hash
from flaskr.models import *
import jwt
from flask import current_app

from flaskr.repositories.user import insert_user, query_with_username


def register_user(username: Union[str, None], password: Union[str,
                  None], confirm_password: Union[str, None]) -> Union[str, None]:
    '''
    handle register logic
    '''
    error = validate_username_password(
        username=username,
        password=password,
        confirm_password=confirm_password,
    )
    if not error:

        error = insert_user(username, password)

    return error


def authenticate_user(username: str, password: str) -> Tuple[Any, str]:
    error = validate_username_password(
        username=username,
        password=password,
    )
    user = None
    if not error:
        user = query_with_username(username)
        if user is None:
            error = "Incorrect username."
        elif not check_password_hash(user.password, password):
            error = "Incorrect password."

    return user, error


def generate_jwt_token(user) -> str:
    token = jwt.encode(
        {
            "username": user.username,
            "user_id": user.id,
        },
        current_app.config['SECRET_KEY'],
        algorithm="HS256"
    )
    return token


def validate_username_password(
    username: Union[str, None],
    password: Union[str, None],
    confirm_password: Optional[str] = None,
) -> str:
    error = check_required(username, password)

    if error:
        return error
    if isinstance(confirm_password, str):
        error = validate_confirm_password(password, confirm_password)
    return error


def check_required(
    username: Union[str, None],
    password: Union[str, None],
) -> str:
    '''
        Check if username and password attributes exist
    '''
    if not username:
        return 'Username is required.'

    elif not password:
        return 'Password is required.'
    return ''


def validate_confirm_password(
    password: str,
    confirm_password: str,
) -> str:
    error = ''
    if password != confirm_password:
        error = "The password and confirm password are not the same."
    return error
