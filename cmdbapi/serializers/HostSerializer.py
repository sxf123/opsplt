from rest_framework import serializers

class HostSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False,read_only=True)
    hostname = serializers.CharField(max_length=255,required=False,allow_blank=True,allow_null=True)
    ipaddress = serializers.CharField(max_length=255,required=False,allow_blank=True,allow_null=True)
    hosttype = serializers.CharField(max_length=255,required=False,allow_blank=True,allow_null=True)
    cpu_nums = serializers.IntegerField(required=False,allow_null=True)
    memory = serializers.IntegerField(required=False,allow_null=True)
    disk = serializers.IntegerField(required=False,allow_null=True)
    node = serializers.StringRelatedField(many=True)
    instance_id = serializers.CharField(max_length=255,required=False,allow_blank=True,allow_null=True)
    expired_time = serializers.CharField(max_length=255,required=False,allow_null=True,allow_blank=True)
    pay_every_month = serializers.FloatField(required=False,allow_null=True)
    cpu_usage = serializers.FloatField(required=False,allow_null=True)
    memory_usage = serializers.FloatField(required=False,allow_null=True)
    disk_usage = serializers.JSONField()
