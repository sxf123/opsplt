from cmdb.models.Host import Host
from common.response import BaseResponse
from cmdbapi.serializers.HostSerializer import HostSerializer

class HostService(object):
    def __init__(self):
        self.host = Host()
    def update_host(self,request):
        serializer = HostSerializer(data=request.data)
        try:
            host = Host.objects.get(instance_id=serializer.initial_data["instance_id"])
            host.expired_time = serializer.initial_data["expired_time"]
            host.pay_every_month = serializer.initial_data["pay_every_month"]
            host.cpu_usage = serializer.initial_data["cpu_usage"]
            host.memory_usage = serializer.initial_data["memory_usage"]
            host.disk_usage = serializer.initial_data["disk_usage"]
            host.save()
            host_serializer = HostSerializer(host)
            response = BaseResponse.success("更新成功",host_serializer.data)
        except Host.DoesNotExist:
            response = BaseResponse.error("主机不存在",None)
        except KeyError:
            response = BaseResponse.error("请求不合法",None)
        return response
