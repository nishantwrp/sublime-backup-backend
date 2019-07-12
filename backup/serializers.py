from rest_framework import serializers
from .models import *

class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = snippet
        fields = ('snippet_file',)

class SnippetListSerializer(serializers.ModelSerializer):
    class Meta:
        model = snippet
        fields = ('snippet_file','original_name')


class ResponseSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=500)
