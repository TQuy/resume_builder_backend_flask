from flask_restx import Api
from flaskr.api import auth

authenticate_api = Api(
    title='APIs',
    doc='/api/'
)

authenticate_api.add_namespace(auth.ns, path='/auth/')
