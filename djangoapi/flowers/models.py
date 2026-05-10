from django.db import models
from django.contrib.gis.db import models as gis_models
from djangoapi.settings import EPSG_FOR_GEOMETRIES
# Create your models here.

class Flower(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    heath = models.FloatField(blank=True, null=True)
    age_days = models.FloatField(blank=True, null=True)
    geom = gis_models.PointField(srid=int(EPSG_FOR_GEOMETRIES), blank=True, null=True)



