from flask import Response
from flask_restful import Resource, reqparse
from flask_restful.reqparse import FileStorage

from dal.db.image import ImageCli
from .models import UploadResponse


class Upload(Resource):
    def __init__(self):
        parser = reqparse.RequestParser()
        parser.add_argument('file', type=FileStorage, location='files')
        self.parser = parser

    def post(self) -> Response:
        req = self.parser.parse_args()

        file: FileStorage = req['file']
        filename = file.filename
        pid, save_url = ImageCli.Upload(filename, 0)

        file.save(save_url)
        return UploadResponse(0, '文件上传成功', pid, filename, save_url)
