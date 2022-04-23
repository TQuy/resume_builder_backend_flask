from flask import Blueprint, redirect, url_for, request, session, flash, render_template
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.models import db, User
from sqlalchemy.exc import IntegrityError
from typing import Optional, Union

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.json['username']
        password = request.json['password']
        confirm_password = request.json['confirm_password']

        error = _validate_username_password(
            username=username,
            password=password,
            confirm_password=confirm_password,
        )

        if error is None:
            try:
                user = User(
                    username = username,
                    password = generate_password_hash(password),
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
            
    else:
        return {
            "message": "Method is not supported"
        }, 405

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        error = _validate_username_password(
            username=username,
            password=password,
        )

        if error is None:
            user = User.query.filter_by(username=username).first()
            if user is None:
                error = "Incorrect username"
            elif not check_password_hash(user.password, password):
                error = "Incorrect password"

        if error:
            return {
                "message": error
            }, 400

        session.clear()
        session['user_id'] = user.id
        return {
            "message": "OK"
        }, 200

    else:
        return {
            "message": "Method is not supported"
        }, 405

def _validate_username_password(
    username: str, 
    password: str, 
    confirm_password: Optional[str] = None,
    ) -> Union[str, None]:
    error = _check_required(username, password)

    if error:
        return error

    if confirm_password:
        error = _check_confirm_password(password, confirm_password)
    return error

def _check_required(
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

def _check_confirm_password(
    password: str, 
    confirm_password: str,
    ) -> Union[str, None]:
    error = None

    if password != confirm_password:
        error = "The password and confirm password are not the same."
    return error
