from rest_framework.views import APIView
from cmdbapi.serializers.HostSerializer import HostSerializer
from cmdb.models.Host import Host
from rest_framework.response import Response
from rest_framework import status

class HostList(APIView):
    def get(self,requests,format=None):
        host = Host.objects.all()
        serializer = HostSerializer(host,many=True)
        return Response(serializer.data)

    def post(self,request,format=None):
        serializer = HostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)