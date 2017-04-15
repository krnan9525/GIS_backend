from django.conf.urls import url

from REST_FRAMEWORK import views
from . import views as nv

from rest_framework import serializers, viewsets, routers


urlpatterns = [
    url(r'^$', nv.BasicAuthentication),
    url(r'^example/', views.ExampleView),
    url(r'^token/', views.GetToken),

]