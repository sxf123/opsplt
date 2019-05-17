from cmdb.models.Host import Host
from rest_framework import serializers

class HostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Host
        fields = ('id','hostname','ipaddress')

    def create(self, validated_data):
        host = Host.objects.create(
            hostname=validated_data.get('hostname'),
            ipaddress = validated_data.get('ipaddress')
        )
        return host

    def update(self, instance, validated_data):
        instance.hostname = validated_data.get('hostname',instance.hostname)
        instance.ipaddress = validated_data.get('ipaddress',instance.ipaddress)
        instance.save()
        return instance