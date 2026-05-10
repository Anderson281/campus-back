from django.contrib import admin
from django.contrib.gis import admin as gis_admin
from .models import Accidentes

class AccidentesAdmin(admin.ModelAdmin):
    list_display = ('id', 'description','geom')

gis_admin.site.register(Accidentes, AccidentesAdmin)
