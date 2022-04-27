from typing import Union
from .validate_auth_form import validate_username_password
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.models import *


def register_user(username: Union[str, None], password: Union[str,
                  None], confirm_password: Union[str, None]):
    '''
    handle register logic
    '''
    error = validate_username_password(
        username=username,
        password=password,
        confirm_password=confirm_password,
    )

    if error is None:

        try:
            user = User(
                username=username,
                password=generate_password_hash(password),
            )
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            error = f"User {username} is already registered."

    if error:
        return {
            "message": error
        }, 400

    return {
        "message": "OK"
    }, 201
