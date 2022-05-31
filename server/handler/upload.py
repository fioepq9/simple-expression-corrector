from flask import Response
from flask_restful import Resource, reqparse
from flask_restful.reqparse import FileStorage

from flask_jwt_extended import jwt_required, get_jwt_identity

from dal.db.image import Image
from .models import ErrorResponse, UploadResponse


class Upload(Resource):
    def __init__(self):
        parser = reqparse.RequestParser()
        parser.add_argument('file', type=FileStorage, location='files')
        self.parser = parser

    @jwt_required(locations=['headers'])
    def post(self) -> Response:
        uid = get_jwt_identity()
        req = self.parser.parse_args()

        # assert file is exist
        file: FileStorage = req['file']
        if file is None:
            return ErrorResponse(1, 'file is None')

        # upload
        filename = file.filename
        pid, save_url = Image.Upload(filename, uid)

        # save in static
        file.save(save_url)

        return UploadResponse(0, '文件上传成功', pid, filename, save_url)
