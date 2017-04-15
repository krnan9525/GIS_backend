from django.contrib.gis import admin

# Register your models here.
from .models import Question
from .models import WorldBorder

admin.site.register(Question)
admin.site.register(WorldBorder, admin.OSMGeoAdmin)