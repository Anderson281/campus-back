from django.db import models
from django.db.models import UniqueConstraint

from rest_framework import serializers

from django.contrib.gis.db import models as gis_models
from djangoapi.settings import EPSG_FOR_GEOMETRIES
# Create your models here.
class Buildings(models.Model):
    #id = models.AutoField(primary_key=True) #Not necessary. It is created by default
    description = models.CharField(max_length=100, blank=True, null=True)
    area = models.FloatField(blank=True, null=True)
    perimeter = models.FloatField(blank=True, null=True)
    geom = gis_models.PolygonField(srid=int(EPSG_FOR_GEOMETRIES), blank=True, null=True)
#    def __str__(self):
#        return str(self.id)

class Owners(models.Model):
    #id = models.AutoField(primary_key=True) #Not necessary. It is created by default
    name = models.CharField(max_length=100, blank=True, null=True)#optional
    dni = models.CharField(max_length=100, unique=True)#mandatory and unique
    

class BuildingsOwners(models.Model):
    building = models.ForeignKey(Buildings,  related_name='buildingsowner_building_id', on_delete=models.CASCADE)
    owner = models.ForeignKey(Owners,  related_name='buildingsowner_owner_id', on_delete=models.CASCADE)
    owner_percentage = models.FloatField()

    #overwrite the save method of the models.Model class. This allows to check
    def save(self, *args, **kwargs):
        if self.owner_percentage <= 0 or self.owner_percentage > 100:
            raise serializers.ValidationError({'owner_percentage': 'From the model. The owner_percentage must be between 0 and 100'})
        super().save(*args, **kwargs)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['building', 'owner'], name='unique_building_owner')
        ]