from flask import Response
from flask_restful import Resource, reqparse

from flask_jwt_extended import jwt_required, get_jwt_identity

from .models import ErrorResponse, JudgeResponse
from dal.db.image import Image as dbImage


class Judge(Resource):
    def __init__(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=str, location='json')
        self.parser = parser

    @jwt_required(locations=['headers'])
    def post(self) -> Response:
        uid = get_jwt_identity()
        req = self.parser.parse_args()

        # assert id is exist
        pid = req['id']
        if pid is None:
            return ErrorResponse(1, 'id is None')

        p_url = dbImage.QueryUrl(pid=pid)
        if p_url is None:
            return ErrorResponse(2, 'original picture not found')

        # TODO: judge
        judge_id = 412433529662617601
        filename = '412433529662617601_github.png'
        save_url = 'static/judge/412433529662617601_github.png'

        return JudgeResponse(0, '算式批改完成', judge_id, filename, save_url)
