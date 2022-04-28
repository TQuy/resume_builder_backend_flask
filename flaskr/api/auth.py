from flask import Blueprint, request
from flaskr.services.auth import authenticate_user, generate_jwt_token, register_user

bp = Blueprint('auth', __name__, url_prefix='/auth/')


@bp.route('/register/', methods=('POST',))
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    confirm_password = request.json.get('confirm_password')
    error = register_user(username, password, confirm_password)

    if error:
        return {
            "message": error
        }, 400

    return {
        "message": "OK"
    }, 201


@bp.route('/login/', methods=('POST',))
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    user, error = authenticate_user(username, password)
    if error:
        return {
            "token": None,
            "message": error
        }, 400

    token = generate_jwt_token(user)
    return {
        "token": token,
        "message": "OK",
    }, 200
