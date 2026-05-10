from django.db import models
from django.contrib.auth import get_user_model

from django.contrib.gis.db import models as gis_models
from djangoapi.settings import EPSG_FOR_GEOMETRIES

# Create your models here.
class Accidentes(models.Model):
    description = models.CharField(max_length=100)
    geom = gis_models.PointField(srid=int(EPSG_FOR_GEOMETRIES))
    creator = models.ForeignKey(get_user_model(), default=1, null=False,blank=True, on_delete=models.CASCADE)