import json
from typing import Dict, Any
from flask import Response
from functools import wraps


def toResponse(fn):
    @wraps(fn)
    def dcrt(*args, **kwargs):
        data = fn(*args, **kwargs)
        return Response(json.dumps(data), mimetype='application/json')

    return dcrt


@toResponse
def BaseResponse(code: int, msg: str) -> Dict[str, Any]:
    return {
        "status": {
            "code": code,
            "msg": msg,
        }
    }


@toResponse
def RespnseWithData(code: int, msg: str, data_name: "str | None", data: Dict[str, Any]) -> Dict[str, Any]:
    if data_name is None:
        resp = {
            "status": {
                "code": code,
                "msg": msg,
            }
        }
        resp.update(data)
        return resp
    return {
        "status": {
            "code": code,
            "msg": msg,
        },
        data_name: data
    }


def ErrorResponse(code: int, msg: str) -> Response:
    return BaseResponse(code, msg)


def UploadResponse(code: int, msg: str, pid: int, name: str, url: str) -> Response:
    return RespnseWithData(code, msg, 'image', {
        'id': str(pid),
        'name': name,
        'url': url,
    })


def RegisterResponse(code: int, msg: str, uid: int, token: str) -> Response:
    return RespnseWithData(code, msg, None, {
        "id": str(uid),
        "toekn": token,
    })
