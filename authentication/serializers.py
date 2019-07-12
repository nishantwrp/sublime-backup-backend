from rest_framework import serializers
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','password')
    
class MessageSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=500)

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','password')

class TokenResponseSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=500)
    token = serializers.CharField(max_length=500)
    username = serializers.CharField(max_length=500)