from rest_framework.response import Response
from rest_framework.serializers import Serializer
from django.utils import six

class BaseResponse(Response):
    def __init__(self, data=None, status=None, code=None, msg=None,
                 template_name=None, headers=None,
                 exception=False, content_type=None):
        super(BaseResponse, self).__init__(None, status=status)

        if isinstance(data, Serializer):
            msg = (
                'You passed a Serializer instance as data, but '
                'probably meant to pass serialized `.data` or '
                '`.error`. representation.'
            )
            raise AssertionError(msg)

        self.data = {"code":code,"msg":msg,"data":data} if data is not None else {"code":code,"msg":msg}
        self.template_name = template_name
        self.exception = exception
        self.content_type = content_type

        if headers:
            for name, value in six.iteritems(headers):
                self[name] = value
    @classmethod
    def success(self,msg,data):
        return BaseResponse(code=1,msg=msg,data=data)
    @classmethod
    def error(self,msg,data):
        return BaseResponse(code=0,msg=msg,data=data)