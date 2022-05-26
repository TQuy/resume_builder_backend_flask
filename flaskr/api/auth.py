from flask import Blueprint, request
from pkg_resources import require
from flaskr.services.auth import authenticate_user, generate_jwt_token, handle_register_user
from flask_restx import Namespace, Resource, fields

# bp = Blueprint('auth', __name__, url_prefix='/auth/')
ns = Namespace('auth', description='Authentication APIs')

login_args = ns.model('login_arguments', {
    'username': fields.String(required=True, example='quynt'),
    'password': fields.String(requried=True, example='1'),
})

register_args = ns.inherit('register_argument', login_args, {
    'confirm_password': fields.String(required=True, example='1')
})

message_only_response = ns.model('register_return', {
    'message': fields.String(required=True, example='OK')
})

login_success_response = ns.inherit('login_success_response', message_only_response, {
    'token': fields.String(required=True, example='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InF1eW50IiwidXNlcl9pZCI6MX0.AP7IukMLkgx7c7oBXiETngaEuuQO7iUq_uHOdqBuYlA')
})


login_fail_response = ns.inherit('login_fail_response', message_only_response, {
    'token': fields.Boolean(required=True, example=None)
})


@ns.route('register/', endpoint='register')
class Register(Resource):
    '''
    Register user account
    '''
    # @ns.doc(params={'id': 'An ID'})
    @ns.expect(register_args)
    @ns.marshal_with(message_only_response)
    def post(self):
        username = request.json.get('username')
        password = request.json.get('password')
        confirm_password = request.json.get('confirm_password')
        error = handle_register_user(username, password, confirm_password)
        if error:
            return {
                "message": error
            }, 400

        return {
            "message": "OK"
        }, 201


@ns.route('login/', endpoint='login')
class Login(Resource):
    @ns.expect(login_args)
    @ns.response(200, 'OK', login_success_response)
    @ns.response(400, 'Failed', login_fail_response)
    def post(self):
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
