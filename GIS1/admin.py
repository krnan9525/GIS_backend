from django.contrib.gis import admin

# Register your models here.
from .models import Question, Activity_Record
from .models import WorldBorder


admin.GeoModelAdmin.display_wkt = True
admin.GeoModelAdmin.display_srid = True
admin.site.register(Question)
admin.site.register(WorldBorder, admin.OSMGeoAdmin)
admin.site.register(Activity_Record, admin.OSMGeoAdmin)