from flask import Blueprint, request
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.models import db, User
from sqlalchemy.exc import IntegrityError
from flask import current_app
import jwt
from flaskr.services.validate_auth_form import validate_username_password

bp = Blueprint('auth', __name__, url_prefix='/auth/')


@bp.route('/register/', methods=('POST',))
def register():
    if request.method == 'POST':
        username = request.json['username']
        password = request.json['password']
        confirm_password = request.json['confirm_password']

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

    else:
        return {
            "message": "Method is not supported"
        }, 405


@bp.route('/login/', methods=('POST',))
def login():
    if request.method == 'POST':
        username = request.json['username']
        password = request.json['password']

        error = validate_username_password(
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

        # send user token
        token = jwt.encode(
            {
                "username": user.username,
                "user_id": user.id,
            },
            current_app.config['SECRET_KEY'],
            algorithm="HS256"
        )
        return {
            "token": token
        }, 200

    else:
        return {
            "message": "Method is not supported"
        }, 405
