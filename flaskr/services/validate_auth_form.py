from typing import Optional, Union


def validate_username_password(
    username: str,
    password: str,
    confirm_password: Optional[str] = None,
) -> Union[str, None]:
    error = check_required(username, password)

    if error:
        return error

    if confirm_password:
        error = check_confirm_password(password, confirm_password)
    return error


def check_required(
    username: str,
    password: str,
) -> Union[str, None]:
    '''
        Check if username and password attributes exist
    '''
    error = None

    if not username:
        error = 'Username is required.'

    elif not password:
        error = 'Password is required.'
    return error


def check_confirm_password(
    password: str,
    confirm_password: str,
) -> Union[str, None]:
    error = None

    if password != confirm_password:
        error = "The password and confirm password are not the same."
    return error
