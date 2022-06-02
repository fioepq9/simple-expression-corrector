from flask import Response
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

from model import judge

from .models import ErrorResponse, JudgeResponse


class Judge(Resource):
    def __init__(self):
        parser = reqparse.RequestParser()
        parser.add_argument('url', type=str, location='json')
        self.parser = parser

    @jwt_required(locations=['headers'])
    def post(self) -> Response:
        uid = get_jwt_identity()
        req = self.parser.parse_args()

        # assert the [url] in the JSON body
        url = req['url']
        if url is None:
            return ErrorResponse(1, 'Missing required parameter in the JSON body')

        # assert the [url] type=str
        if not isinstance(url, type('str')):
            return ErrorResponse(4, 'Bad Request for error param value')

        # Do judge
        output = judge(url)

        return JudgeResponse(0, 'success', output)
