from typing import Any
from flask import Blueprint, request

upload_bp: Blueprint = Blueprint('upload', __name__)


@upload_bp.route('/', methods=['POST'])
def upload():
    file = request.files.get('file')
    print("ok")
    if file is None:
        return {
            'status_code': 1,
            'status_msg': '文件上传失败',
        }
    return {
        'status_code': 0,
        'status_msg': '文件上传成功',
        'file_name': file.filename,
    }
