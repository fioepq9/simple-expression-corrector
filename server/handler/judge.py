from flask import Response
from flask_restful import Resource, reqparse

from flask_jwt_extended import jwt_required, get_jwt_identity

from .models import ErrorResponse, JudgeResponse
from dal.db.image import Image as dbImage
from dal.db.judge import JudgeImage


import cv2
import os
from models.de import detect, get_model
from PIL import Image


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

        # save judge path to Mysql
        image = Image.open(p_url)
        filename = image.filename.split('_')[-1]
        judge_id, save_url = JudgeImage.Upload(filename, pid)

        print(f'{p_url}')

        # yolomodels
        img = cv2.imread(image.filename)
        yolov5_model = get_model()
        img = detect(yolov5_model, img)
        image = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        image.save(save_url)

        return JudgeResponse(0, '算式批改完成', judge_id, filename, save_url)
