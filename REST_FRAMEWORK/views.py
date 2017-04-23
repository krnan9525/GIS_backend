import json

from django.contrib.auth.models import User, Group
from django.contrib.gis.geos import GEOSGeometry, Point, fromstr
from django.contrib.gis.measure import D, Distance
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

from GIS1.models import Activity_Record, Interest_Group
from REST_FRAMEWORK.models import Snippet
from REST_FRAMEWORK.serializers import UserSerializer, GroupSerializer, SnippetSerializer, RecordSerializer, \
    OutputRecordSerializer, OutputInterestLocation


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


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def Submit_Location(request):
    if request.method == 'POST' :

        user_id = request.user.id
        print(repr(request.data))
        serializer = RecordSerializer(data=request.data, context={'user_id': request.user.id})
        if(serializer.is_valid()):
            serializer.save()
            content = json.dumps({'status': "success"})
            return HttpResponse(content)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def Fetch_Location(request):
    if request.method == 'POST' :
        # serializer = OutputRecordSerializer(data=request.data)
        if(request.data.get('user_id')!=''):
            try:
                validated_data = request.data
                temp_points = Activity_Record.objects.get(user_id_id=validated_data.get('user_id'))
                print(temp_points)
                g = temp_points
                buffer = GEOSGeometry.buffer(g.location, 0.0005, 4)
                print(buffer.geojson)
                # return serialize('geojson', [buffer],
                #           geometry_field='location', fields=('user_id','location'))
                response_data = {}
                response_data['type'] = 'FeatureCollection'
                response_data['features'] = []
                geo_obj = dict()
                geo_obj['type'] = 'Feature'
                geo_obj['properties'] = {}
                geo_obj['geometry'] = json.JSONDecoder().decode( buffer.geojson )
                response_data['features'].append (geo_obj)
                # response_data['buffer'] = json.JSONDecoder().decode( buffer.geojson )
                # response_data['user_id'] = validated_data.get('user_id')
            except Activity_Record.DoesNotExist:
                response_data = {}
                response_data['status'] = "User id not found"
                response_data['user_id'] = validated_data.get('user_id')

            return HttpResponse(json.dumps(response_data) , status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def Fetch_Points(request):
    if request.method == 'POST' :
        serializer = OutputRecordSerializer(data=request.data)
        if (serializer.is_valid()):
            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def Fetch_Interest_Locations(request):
    if(request.method == "POST"):
        if(request.data.get('lat') and request.data.get('lng')):
            print(request.data.get('lng'))
            current_location = Point((float)(request.data.get('lng')), (float)(request.data.get('lat')))
            user_location = fromstr("POINT(%s %s)" % (request.data.get('lng'), request.data.get('lat')))
            desired_radius = {'m': 5000}
            nearby_spots = Interest_Group.objects.filter(location__distance_lte=(current_location, D(m=50000.0)))

            # print("asdasdasda")
            serializer = OutputInterestLocation(nearby_spots, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)