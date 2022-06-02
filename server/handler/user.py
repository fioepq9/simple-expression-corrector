import datetime
from flask import Response
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token

from dal.db.user import User
from .models import ErrorResponse, RegisterResponse, LoginResponse


class UserRegister(Resource):
    def __init__(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, location='json')
        parser.add_argument('password', type=str, location='json')
        self.parser = parser

    def post(self) -> Response:
        req = self.parser.parse_args()

        # assert the [username] and [password] in the JSON body
        username = req['username']
        password = req['password']
        if username is None or password is None:
            return ErrorResponse(1, 'Missing required parameter in the JSON body')

        # assert the [username] and [password] type: str
        if not isinstance(username, type('str')) or not isinstance(password, type('str')):
            return ErrorResponse(4, 'Bad Request for error param value')

        # check if user already exist
        if User.FindByUsername(username):
            return ErrorResponse(2, '用户名 {} 已存在'.format(username))

        # create user
        user, ok = User.Create(username, password)
        if not ok:
            return ErrorResponse(3, '用户注册失败')

        # use JWT to generate token
        token = create_access_token(
            identity=user.Id,
            expires_delta=datetime.timedelta(hours=1),
        )

        return RegisterResponse(0, '注册成功', user.Id, token)


class UserLogin(Resource):
    def __init__(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, location='json')
        parser.add_argument('password', type=str, location='json')
        self.parser = parser

    def post(self) -> Response:
        req = self.parser.parse_args()

        # assert the [username] and [password] in the JSON body
        username = req['username']
        password = req['password']
        if username is None or password is None:
            return ErrorResponse(1, 'Missing required parameter in the JSON body')

        # assert the [username] and [password] type: str
        if not isinstance(username, type('str')) or not isinstance(password, type('str')):
            return ErrorResponse(4, 'Bad Request for error param value')

        # check if user exist and password is correct
        user = User.FindByUsername(username)
        if not user or user.Password != password:
            return ErrorResponse(2, '用户名或密码错误')

        # use JWT to generate token
        token = create_access_token(
            identity=user.Id,
            expires_delta=datetime.timedelta(hours=1),
        )

        return LoginResponse(0, '登录成功', user.Id, token)
