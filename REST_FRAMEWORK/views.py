import json

from django.contrib.auth.models import User, Group
from django.core import serializers
from django.db.migrations import serializer
from django.http import JsonResponse, HttpResponse
from psycopg2.extensions import JSON
from rest_framework import viewsets, status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from REST_FRAMEWORK.models import Snippet
from REST_FRAMEWORK.serializers import UserSerializer, GroupSerializer, SnippetSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def ExampleView(request):
    if request.method == 'GET':
        return Response(True)


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def GetToken(request):
    if request.method == 'GET':
        token, created = Token.objects.get_or_create(user=request.user)
        content =  json.dumps ( {'token': token.key} )
        return HttpResponse(content)