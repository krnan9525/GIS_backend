from django.contrib.auth.models import User, Group
from django.contrib.gis.db import models
from django.contrib.gis.geos import MultiPoint, Point, GEOSGeometry
from django.core.serializers import serialize
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from GIS1.models import Activity_Record
from REST_FRAMEWORK.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

# class SnippetSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     title = serializers.CharField(required=False, allow_blank=True, max_length=100)
#     code = serializers.CharField(style={'base_template': 'textarea.html'})
#     linenos = serializers.BooleanField(required=False)
#     language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
#     style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')
#
#     def create(self, validated_data):
#         """
#         Create and return a new `Snippet` instance, given the validated data.
#         """
#         return Snippet.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         """
#         Update and return an existing `Snippet` instance, given the validated data.
#         """
#         instance.title = validated_data.get('title', instance.title)
#         instance.code = validated_data.get('code', instance.code)
#         instance.linenos = validated_data.get('linenos', instance.linenos)
#         instance.language = validated_data.get('language', instance.language)
#         instance.style = validated_data.get('style', instance.style)
#         instance.save()
#         return instance
#
class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = ('id', 'title', 'code', 'linenos', 'language', 'style')

class OutputRecordSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()

    class Mata:
        model = Activity_Record
        fields = ('location', 'user_id')

    def create(self, validated_data):
        try:
            temp_points = Activity_Record.objects.get(user_id_id=validated_data.get('user_id'))
            print(temp_points)
            g = temp_points
            buffer = GEOSGeometry.buffer(g.location,1)
            return serialize('geojson', [buffer],
                      geometry_field='location', fields=('user_id','location'))
        except Activity_Record.DoesNotExist:
            return 0


class RecordSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=True)
    location_1 = serializers.FloatField(required=True)
    location_2 = serializers.FloatField(required=True)

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        print(validated_data.get('location_1'))
        print(validated_data.get('location_2'))
        temp_obj = dict()
        temp_obj['user_id'] = User.objects.get(pk=validated_data.get('user_id'))
        try:
            temp_points = Activity_Record.objects.get(user_id_id=validated_data.get('user_id')).location
            print(temp_points)
            g = temp_points
            g.append(Point((float)(validated_data.get('location_1')), (float)(validated_data.get('location_2'))))
            temp_obj['location'] = g
            return Activity_Record.objects.update(**temp_obj)
        except Activity_Record.DoesNotExist:
            g = MultiPoint()
            g.append(Point( (float) (validated_data.get('location_1') ),(float) (validated_data.get('location_2') )))
            temp_obj['location'] = g
            return Activity_Record.objects.create(**temp_obj)
