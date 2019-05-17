from cmdb.models.Job import Job
from rest_framework import serializers

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ('id','name','desc','create_time','update_time','content')

    def create(self, validated_data):
        job = Job.objects.create(
            name=validated_data.get('name'),
            desc=validated_data.get('desc'),
            content=validated_data.get('content')
        )
        return job
    def update(self,instance,validated_data):
        instance.name = validated_data.get('name',instance.name)
        instance.desc = validated_data.get('desc',instance.desc)
        instance.content = validated_data.get('content',instance.content)
        instance.save()
        return instance