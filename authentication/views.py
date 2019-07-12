from rest_framework.response import Response
from .serializers import *
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework import status
from rest_framework import permissions
from rest_framework.authtoken.models import Token

def create_auth_token(user):
    token, created = Token.objects.get_or_create(user=user)
    return token

class RegisterView(generics.GenericAPIView):
    """
    Create A New Account
    """
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)
    
    def give_response(self,message,token,name):
        response = TokenResponseSerializer({
            'message': message,
            'token': token,
            'username': name
        })
        return Response(response.data,status.HTTP_200_OK)
    
    def post(self,request):
        self.request = request
        username = request.data['username']
        try:
            User.objects.get(username=username)
            return self.give_response("username_already_exists","","")
        except:
            user =  User.objects.create_user(username, '', request.data['password'])
            token = create_auth_token(user)
            return self.give_response("user_registered",token.key,username)

class CheckView(generics.GenericAPIView):
    serializer_class = MessageSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self,request):
        response = MessageSerializer({
            'message' : "success"
        })
        return Response(response.data,status.HTTP_200_OK)

class LoginView(generics.GenericAPIView):
    """
    Check the credentials and logs in the user
    """
    serializer_class = LoginSerializer
    permission_classes = (permissions.AllowAny,)

    def give_response(self,message,token,name):
        response = TokenResponseSerializer({
            'message' : message,
            'token': token,
            'username': name
        })
        return Response(response.data,status.HTTP_200_OK)
    
    def post(self,request):
        self.request = request
        username = request.data['username']
        password = request.data['password']
        loginit = authenticate(username=username, password=password)
        if loginit is not None:
            user = User.objects.get(username=username)
            token =  create_auth_token(user)
            return self.give_response("logged_in",token.key,username)
        else:
            return self.give_response("invalid_credentials","","")



