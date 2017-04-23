from django.conf.urls import url

from REST_FRAMEWORK import views
from . import views as nv

from rest_framework import serializers, viewsets, routers


urlpatterns = [
    url(r'^$', nv.BasicAuthentication),
    url(r'^example/', views.ExampleView),
    url(r'^token/', views.GetToken),
    url(r'^submit_location/', views.Submit_Location),
    url(r'^fetch_location/', views.Fetch_Location),
    url(r'^fetch_points/', views.Fetch_Points),
    url(r'^fetch_interest_locations/', views.Fetch_Interest_Locations),
]