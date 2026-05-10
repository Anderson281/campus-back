from django.contrib import admin
from django.contrib.gis import admin as gis_admin
from .models import Buildings, Owners, BuildingsOwners

class BuildingsAdmin(admin.ModelAdmin):
    list_display = ('id', 'description','area','perimeter', 'geom')

class OwnersAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','dni')

class BuildingsOnersAdmin(admin.ModelAdmin):
    def owner_dni(self, obj: BuildingsOwners):
        return obj.owner.dni
    def building_description(self, obj: BuildingsOwners):
        return obj.building.description
    list_display = ('id', 'building','owner','owner_percentage', 'building_description', 'owner_dni')

admin.site.register(Owners, OwnersAdmin)
gis_admin.site.register(Buildings, BuildingsAdmin)
admin.site.register(BuildingsOwners, BuildingsOnersAdmin)


