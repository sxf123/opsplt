from rest_framework.exceptions import APIException
from common.response import BaseResponse
from rest_framework import status

class BaseException(APIException):

    status_code = status.HTTP_200_OK

    def __init__(self,detail=None,code=None):
        if detail is None:
            detail = self.default_detail
        if code is None:
            code = self.default_code
        self.detail = {"code": code,"msg":detail}

class AuthException(BaseException):
    default_code = 403
    default_detail = "认证失败"

class NotFoundException(BaseException):
    default_code = 404
    default_detail = "对象不存在"

class SysException(BaseException):
    default_code = 500
    default_detail = "系统错误"