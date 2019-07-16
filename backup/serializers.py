from rest_framework import serializers
from .models import *

class SnippetSerializer(serializers.Serializer):
    snippet_file = serializers.FileField()

class SnippetListSerializer(serializers.ModelSerializer):
    class Meta:
        model = snippet
        fields = ('snippet_file','original_name')


class ResponseSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=500)
