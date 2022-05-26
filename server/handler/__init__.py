from .user import user_bp
from .judge import judge_bp
from .upload import upload_bp
from flask import Flask


def init_app(app: Flask):
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(judge_bp, url_prefix='/judge')
    app.register_blueprint(upload_bp, url_prefix='/upload')
