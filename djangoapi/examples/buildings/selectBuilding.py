from djangoapi.buildings.models import Buildings
from django.contrib.gis.db.models.functions import Distance
from django.db.models import Q
from django.forms.models import model_to_dict

#using django lookups https://docs.djangoproject.com/en/5.1/ref/models/lookups/
#using spatila lookups
#https://docs.djangoproject.com/en/5.1/ref/contrib/gis/geoquerysets/#std-fieldlookup-contains_properly
#using geodjango lookups 
# Filtrar edificios con área menor que 100 (less than --> lt, greater than --> gt)

filterById = Buildings.objects.filter(id=1)

smallBuildings = Buildings.objects.filter(area__lt=100)

filteringBytext = Buildings.objects.filter(description__icontains='edificio')

combinningFilters = Buildings.objects.filter(area__lt=100, description__icontains='edificio')
filteringByGeometry = Buildings.objects.filter(geom__distance_lte=(GEOSGeometry('POINT(-74 38)'), 5)) 

intersection = Buildings.objects.filter(geom__intersects=GEOSGeometry('POLYGON((0 0, 0 10, 10 10, 10 0, 0 0))', srid=25830))
interiorIntersection = Buildings.objects.filter(geom__contains_properly=GEOSGeometry('POLYGON((0 0, 0 10, 10 10, 10 0, 0 0))', srid=25830))

#all the results are querysets: https://docs.djangoproject.com/en/5.1/ref/models/querysets/
#to access to the results you can convert the queryset to a list
l=list(filterById)
print(l)

p=l[0]

print(p.id)
print(p.area)
print(p.geom)

from django.contrib.gis.geos import GEOSGeometry

#create the geometry with geos to be able to calculate the area and length
g=GEOSGeometry(p.geom, srid=25830)
print(g.area)
print(g.length)

print(model_to_dict(p))


