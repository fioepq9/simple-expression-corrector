from flask import Flask
from flask_restful import Api

from .upload import Upload
from .judge import Judge
from .user import UserRegister, UserLogin


def init_app(app: Flask):
    api = Api(app)
    # upload
    api.add_resource(Upload, '/upload')
    # judge
    api.add_resource(Judge, '/judge')
    # user
    api.add_resource(UserRegister, '/user/register')
    api.add_resource(UserLogin, '/user/login')
