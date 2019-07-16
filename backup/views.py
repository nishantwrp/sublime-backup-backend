from django.shortcuts import render
from rest_framework.parsers import FileUploadParser
from rest_framework import status
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import generics
from .serializers import *
from .models import *
import requests
from django.http import HttpResponse,JsonResponse
from rest_framework.authtoken.models import Token
# Create your views here.

base_url = "https://sublime-backup.herokuapp.com/snippets/"


def get_auth_token(user):
    token, created = Token.objects.get_or_create(user=user)
    return token.key

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
        account_id = kloudless_keys.objects.get(name="account_id").key
        token = kloudless_keys.objects.get(name="token").key
        parent_id = kloudless_keys.objects.get(name="parent_id").key
        snippet_uploaded = request.data['snippet_file']
        user = request.user
        url = "https://api.kloudless.com/v1/accounts/" + account_id + "/storage/files/?overwrite=false"
        headers = {
            'Authorization' : "Bearer " + token,
            'X-Kloudless-Metadata' :  '{"parent_id":"' + parent_id + '","name":"' + snippet_uploaded.name + get_auth_token(request.user) + '"}'
        }
        files = {'file': snippet_uploaded}
        r = requests.post(url=url,headers=headers,files=files)
        kloudless_id = r.json()['id']
        snippet.objects.create(snippet_file=base_url+kloudless_id+"/",original_name=snippet_uploaded.name,owner=user,dropbox_id=kloudless_id)
        # snippet.objects.create(snippet_file=snippet_uploaded,original_name = snippet_uploaded.name,owner=user)
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
        account_id = kloudless_keys.objects.get(name="account_id").key
        token = kloudless_keys.objects.get(name="token").key
        snippets = snippet.objects.filter(owner=request.user)
        for obj in snippets:
            url = "https://api.kloudless.com/v1/accounts/" + account_id + "/storage/files/" + obj.dropbox_id + "/?permanent=true"
            headers = {
            'Authorization' : "Bearer " + token
            }
            r = requests.delete(url=url,headers=headers)
            obj.delete()
        return give_response("snippets_deleted")

def getSnippet(request,id):
    account_id = kloudless_keys.objects.get(name="account_id").key
    token = kloudless_keys.objects.get(name="token").key
    url = "https://api.kloudless.com/v1/accounts/" + account_id + "/storage/files/" + id + "/contents/"
    headers = {
            'Authorization' : "Bearer " + token,
            }
    r = requests.get(url=url,headers=headers)
    return HttpResponse(r.content, content_type='application/octet-stream')
