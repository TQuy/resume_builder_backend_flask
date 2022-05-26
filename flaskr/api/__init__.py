from sys import prefix
from flask_restx import Api
from .auth import ns

authenticate_api = Api(
    title='APIs',
    doc='/api/'
)

authenticate_api.add_namespace(ns, path='/api/auth/')
