from .user import UserRegister, UserLogin
from .upload import Upload
from .judge import Judge
from .feedback import BugFeedBack
from flask import Flask
from flask_restful import Api


def init_app(app: Flask):
    # app.register_blueprint(user_bp, url_prefix='/user')
    # app.register_blueprint(judge_bp, url_prefix='/judge')
    # app.register_blueprint(upload_bp, url_prefix='/upload')
    api = Api(app)
    # upload
    api.add_resource(Upload, '/upload')
    # judge
    api.add_resource(Judge, '/judge')
    # user
    api.add_resource(UserRegister, '/user/register')
    api.add_resource(UserLogin, '/user/login')
    # feedback
    api.add_resource(BugFeedBack, '/feedback/bug')
