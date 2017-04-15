"""GIS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin

# Serializers define the API representation.
from django.contrib.auth.models import User
from rest_framework import serializers, viewsets, routers
from REST_FRAMEWORK import views

router = routers.DefaultRouter()
router.register(r'api/users', views.UserViewSet)
router.register(r'api/groups', views.GroupViewSet)
# router.register(r'api/get_new_token', views.GroupViewSet)
# router.register(r'api/example', views.ExampleView)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^gis/', include('GIS1.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/', include('REST_FRAMEWORK.urls')),
]
