from common.response import BaseResponse
from cmdbapi.views.BaseView import BaseView
from rest_framework import status
from cmdb.models.Host import Host
from cmdbapi.serializers.HostSerializer import HostSerializer
from cmdbapi.service.HostService import HostService
from cmdbapi.exception import AuthException
from cmdbapi.exception import NotFoundException
from cmdbapi.exception import SysException
from rest_framework.views import APIView
from cmdbapi.authentication import TokenBaseAuthentication
from rest_framework.permissions import IsAuthenticated

class HostDetailView(BaseView):
    def get(self,request,format=None):
        host_name = request.query_params.get('hostname')
        try:
            host = Host.objects.get(hostname=host_name)
            host_serializer = HostSerializer(host)
            response = BaseResponse.success("",host_serializer.data)
        except Host.DoesNotExist:
            raise NotFoundException("主机不存在")
        except Exception:
            raise SysException
        return response

class HostUpdateView(BaseView):
    def post(self,request,format=None):
        host_service = HostService()
        return host_service.update_host(request)

class HostTestView(APIView):

    authentication_classes = (TokenBaseAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self,request,format=None):
        return BaseResponse.success("大家好",None)

