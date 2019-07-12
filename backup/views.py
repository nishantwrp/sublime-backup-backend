from django.shortcuts import render
from rest_framework.parsers import FileUploadParser
from rest_framework import status
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import generics
from .serializers import *
from .models import *
# Create your views here.


def give_response(message):
        response = ResponseSerializer({
            'message': message
        })
        return Response(response.data,status.HTTP_200_OK)

class SnippetsUpdateView(generics.GenericAPIView):
    parser_class = (FileUploadParser,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = (SnippetSerializer)

    def post(self,request):
        snippet_uploaded = request.data['snippet_file']
        user = request.user
        snippet.objects.create(snippet_file=snippet_uploaded,original_name = snippet_uploaded.name,owner=user)
        return give_response("snippet_uploaded")
        
class SnippetsListView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = (SnippetListSerializer)

    def get_queryset(self):
        return snippet.objects.filter(owner=self.request.user)

class SnippetsDeleteView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = (ResponseSerializer)

    def get(self,request):
        snippets = snippet.objects.filter(owner=request.user)
        for obj in snippets:
            obj.delete()
        return give_response("snippets_deleted")