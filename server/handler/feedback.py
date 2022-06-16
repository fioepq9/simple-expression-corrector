from flask import Response
from flask_restful import Resource, reqparse

from flask_jwt_extended import jwt_required, get_jwt_identity

from .models import ErrorResponse, BugFeedBackResponse
from dal.db.feedback import Feedback


class BugFeedBack(Resource):
    def __init__(self):
        parser = reqparse.RequestParser()
        parser.add_argument('upload_id', type=str, location='json')
        parser.add_argument('judge_id', type=str, location='json')
        parser.add_argument('email', type=str, location='json')
        parser.add_argument('description', type=str, location='json')
        self.parser = parser

    @jwt_required(locations=['headers'])
    def post(self) -> Response:
        user_id = get_jwt_identity()
        req = self.parser.parse_args()

        # assert param is exist
        upload_id = req['upload_id']
        if upload_id is None:
            return ErrorResponse(1, 'upload_id is None')
        judge_id = req['judge_id']
        if judge_id is None:
            return ErrorResponse(1, 'judge_id is None')
        email = req['email']
        if email is None:
            return ErrorResponse(1, 'email is None')
        description = req['description']
        if description is None:
            return ErrorResponse(1, 'description is None')

        # save feedback
        Feedback.FeedBack(user_id, upload_id, judge_id, email, description)

        return BugFeedBackResponse(0, '成功反馈 Bug')
