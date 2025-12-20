from enum import Enum
from rest_framework.response import Response
from http import HTTPStatus


class Codes:
    OK = 114514
    UserExists = 1001  # 注册时用户存在
    UserNotExists = 1002  # 登录时用户不存在
    NameOrPasswdIncorrect = 1003  # 登录用户名或密码错误


CodeMap = {
    Codes.OK: "成功",
    Codes.UserExists: "用户已存在",
    Codes.UserNotExists: "用户不存在",
    Codes.NameOrPasswdIncorrect: "用户名或密码错误",
}


def success(msg=None, data=None):
    return response(status=Codes.OK, msg=msg, data=data)


def response(
    status: int,
    msg: str | None = None,
    data=None,
    httpstatus: HTTPStatus = HTTPStatus.OK,
) -> Response:
    """
    支持自动生成msg
    """

    if data is None:
        data = {}

    if msg is None:
        msg = CodeMap.get(status, "")

    return Response(
        {
            "status": status,
            "msg": msg,
            "data": data,
        },
        status=httpstatus,
    )


HS = HTTPStatus
