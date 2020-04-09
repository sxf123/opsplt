from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField

class NodeTreeSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False,read_only=True)
    name = serializers.CharField(max_length=255,required=False,allow_blank=True,allow_null=True)
    parent = serializers.PrimaryKeyRelatedField(read_only=True)
    children = serializers.ListField(child=RecursiveField(),source="get_children")