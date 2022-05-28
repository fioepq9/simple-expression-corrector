from flask import Blueprint, request, Response
from flask_restful import Resource, reqparse

from dal.db.user import User
from .models import ErrorResponse, RegisterResponse


class UserRegister(Resource):
    def __init__(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, location='json')
        parser.add_argument('password', type=str, location='json')
        self.parser = parser

    def post(self) -> Response:
        req = self.parser.parse_args()

        username = req['username']
        password = req['password']
        if username is None or password is None:
            return ErrorResponse(1, 'Missing required parameter in the JSON body')

        if User.FindByUsername(username):
            return ErrorResponse(2, '用户名 {} 已存在'.format(username))

        user, ok = User.Create(username, password)
        if not ok:
            return ErrorResponse(3, '用户注册失败')

        return RegisterResponse(0, '注册成功', user.Id, 'token')


class UserLogin(Resource):
    def __init__(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, location='json')
        parser.add_argument('password', type=str, location='json')
        self.parser = parser

    def post(self) -> Response:
        req = self.parser.parse_args()

        username = req['username']
        password = req['password']
        if username is None or password is None:
            return ErrorResponse(1, 'Missing required parameter in the JSON body')

        user = User.FindByUsername(username)
        if not user or user.Password != password:
            return ErrorResponse(2, '用户名或密码错误')

        return RegisterResponse(0, '登录成功', user.Id, 'token')
